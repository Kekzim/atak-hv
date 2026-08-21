#!/usr/bin/env python3
"""Provision ATAK devices over adb.

Replaces the Windows-only .bat scripts. Runs on Windows, Linux and macOS,
from any directory - nothing needs to live in C:\\.

    provision.py devices          list attached devices
    provision.py install          install apps and push configuration
    provision.py restore          uninstall apps, remove ATAK files
    provision.py restore --wipe-media   also clear Download/DCIM/Pictures/Documents

Configuration lives in provision.toml next to this file.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

if sys.version_info < (3, 11):
    sys.exit(
        "Python 3.11 or newer is required (this is %d.%d).\n"
        "Windows: https://www.python.org/downloads/\n"
        "Debian/Ubuntu: sudo apt install python3"
        % sys.version_info[:2]
    )

import tomllib

HERE = Path(__file__).resolve().parent
DEFAULT_CONFIG = HERE / "provision.toml"


# --------------------------------------------------------------------------
# output
# --------------------------------------------------------------------------

class Out:
    """Console output. ASCII only - Windows consoles are not reliably UTF-8."""

    def __init__(self, quiet: bool = False):
        self.quiet = quiet

    def rule(self, text: str = "") -> None:
        if self.quiet:
            return
        print("=" * 60)
        if text:
            print(text)
            print("=" * 60)

    def info(self, text: str) -> None:
        if not self.quiet:
            print(text)

    def step(self, n: int, total: int, text: str) -> None:
        if not self.quiet:
            print(f"  [{n}/{total}] {text} ... ", end="", flush=True)

    def ok(self, note: str = "ok") -> None:
        if not self.quiet:
            print(note)

    def fail(self, note: str) -> None:
        if not self.quiet:
            print(f"FAILED ({note})")

    def warn(self, text: str) -> None:
        print(f"WARNING: {text}", file=sys.stderr)

    def error(self, text: str) -> None:
        print(f"ERROR: {text}", file=sys.stderr)


# --------------------------------------------------------------------------
# adb
# --------------------------------------------------------------------------

@dataclass
class Device:
    serial: str
    manufacturer: str = "?"
    model: str = "?"

    def __str__(self) -> str:
        return f"{self.serial} ({self.manufacturer} {self.model})"


class Adb:
    def __init__(self, binary: Path, dry_run: bool = False):
        self.binary = binary
        self.dry_run = dry_run

    def run(self, args: list[str], serial: str | None = None, timeout: int = 300,
            mutating: bool = True) -> subprocess.CompletedProcess:
        cmd = [str(self.binary)]
        if serial:
            cmd += ["-s", serial]
        cmd += args
        # Read-only queries still run under --dry-run; otherwise the tool
        # could not even see which devices are attached.
        if self.dry_run and mutating:
            return subprocess.CompletedProcess(cmd, 0, f"[dry-run] {' '.join(cmd)}\n", "")
        try:
            # stdin=DEVNULL: adb subprocesses otherwise inherit our stdin and
            # can swallow the operator's keystrokes before a prompt is read.
            return subprocess.run(cmd, capture_output=True, text=True,
                                  timeout=timeout, errors="replace",
                                  stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            return subprocess.CompletedProcess(cmd, 124, "", f"timed out after {timeout}s")

    def shell(self, args: list[str], serial: str, timeout: int = 120,
              mutating: bool = True) -> subprocess.CompletedProcess:
        return self.run(["shell", *args], serial=serial, timeout=timeout, mutating=mutating)

    def start_server(self) -> None:
        self.run(["start-server"], timeout=60, mutating=False)

    def list_devices(self) -> tuple[list[str], list[tuple[str, str]]]:
        """Return (ready serials, [(serial, state)] for anything not ready)."""
        proc = self.run(["devices"], timeout=30, mutating=False)
        ready: list[str] = []
        pending: list[tuple[str, str]] = []
        for line in proc.stdout.splitlines()[1:]:
            line = line.strip()
            if not line or "\t" not in line:
                continue
            serial, state = line.split("\t", 1)
            state = state.strip()
            (ready if state == "device" else pending).append(
                serial if state == "device" else (serial, state)
            )
        return ready, pending

    def describe(self, serial: str) -> Device:
        def prop(name: str) -> str:
            p = self.shell(["getprop", name], serial, timeout=30, mutating=False)
            return p.stdout.strip() or "?"
        return Device(serial, prop("ro.product.manufacturer"), prop("ro.product.model"))


def find_adb(config: dict, override: str | None, out: Out) -> Path:
    if override:
        p = Path(override).expanduser()
        if not p.exists():
            raise SystemExit(f"ERROR: adb not found at {p}")
        return p.resolve()

    exe = "adb.exe" if os.name == "nt" else "adb"
    for source in config.get("adb", {}).get("lookup", ["bundled", "path"]):
        if source == "bundled":
            candidate = HERE / "platform-tools" / exe
            if candidate.exists():
                return candidate.resolve()
        elif source == "path":
            found = shutil.which("adb")
            if found:
                return Path(found).resolve()

    if sys.platform == "win32":
        howto = (
            "  Install Android SDK Platform-Tools:\n"
            "    1. Download https://developer.android.com/tools/releases/platform-tools\n"
            f"    2. Unzip it so that adb.exe sits directly in\n"
            f"       {HERE / 'platform-tools'}"
        )
    elif sys.platform == "darwin":
        howto = ("  Install it with Homebrew:\n"
                 "    brew install android-platform-tools")
    else:
        howto = (
            "  Install it with your package manager:\n"
            "    Debian/Ubuntu: sudo apt install adb android-sdk-platform-tools-common\n"
            "    Fedora:        sudo dnf install android-tools\n"
            "    Arch:          sudo pacman -S android-tools\n"
            "  (android-sdk-platform-tools-common adds the udev rules that\n"
            "   otherwise cause 'no permissions' errors.)\n"
            "  Note: the bundled platform-tools/ folder holds Windows binaries only."
        )

    raise SystemExit(
        "ERROR: adb not found - it is required, this tool only drives it.\n"
        f"  Looked in: {HERE / 'platform-tools' / exe}\n"
        "             and on PATH\n"
        f"{howto}\n"
        "  Or point at an existing adb with --adb /path/to/adb"
    )


# --------------------------------------------------------------------------
# per-device work
# --------------------------------------------------------------------------

@dataclass
class Task:
    label: str
    action: object          # callable(adb, device, log) -> (ok, note)
    fatal: bool = False


@dataclass
class Result:
    device: Device
    failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    log_path: Path | None = None

    @property
    def ok(self) -> bool:
        return not self.failures


class Runner:
    def __init__(self, adb: Adb, out: Out, log_dir: Path):
        self.adb = adb
        self.out = out
        self.log_dir = log_dir

    def run(self, device: Device, tasks: list[Task]) -> Result:
        self.log_dir.mkdir(parents=True, exist_ok=True)
        log_path = self.log_dir / f"{device.serial}.log"
        result = Result(device, log_path=log_path)

        with log_path.open("w", encoding="utf-8") as log:
            log.write(f"{datetime.now().isoformat(timespec='seconds')}  {device}\n")
            for i, task in enumerate(tasks, 1):
                self.out.step(i, len(tasks), task.label)
                log.write(f"\n--- {task.label} ---\n")
                log.flush()   # so an interrupted run still leaves a record
                try:
                    ok, note = task.action(self.adb, device, log)
                except Exception as exc:                      # noqa: BLE001
                    ok, note = False, f"{type(exc).__name__}: {exc}"
                    log.write(f"exception: {exc}\n")
                if ok:
                    self.out.ok(note or "ok")
                    if note and note.startswith("WARNING"):
                        result.warnings.append(note)
                else:
                    self.out.fail(note or "see log")
                    result.failures.append(task.label)
                    if task.fatal:
                        log.write("fatal - aborting this device\n")
                        log.flush()
                        break
                log.flush()
        return result


def _logged(log, proc: subprocess.CompletedProcess) -> None:
    log.write(f"$ {' '.join(proc.args)}\n")
    if proc.stdout:
        log.write(proc.stdout)
    if proc.stderr:
        log.write(proc.stderr)
    log.write(f"[exit {proc.returncode}]\n")


# --- task builders --------------------------------------------------------

def task_stay_awake() -> Task:
    def run(adb, dev, log):
        p = adb.shell(["svc", "power", "stayon", "true"], dev.serial)
        _logged(log, p)
        return p.returncode == 0, "ok"
    return Task("Keep screen awake", run)


def task_settings(groups: dict) -> Task:
    def run(adb, dev, log):
        bad = []
        for namespace in ("global", "secure", "system"):
            for key, value in groups.get(namespace, []):
                p = adb.shell(["settings", "put", namespace, key, str(value)], dev.serial)
                _logged(log, p)
                if p.returncode != 0:
                    bad.append(f"{namespace}/{key}")
        # Settings are best-effort: some keys do not exist on every ROM.
        return True, "ok" if not bad else f"ok ({len(bad)} not supported)"
    return Task("Apply system settings", run)


def task_packages(packages: dict, enable: bool) -> Task:
    """Disable (or re-enable) update services, unused apps and vendor bloat.

    `core` and `debloat` apply everywhere. `vendor` is keyed by
    ro.product.manufacturer, so an unknown handset simply gets the common
    lists and still works.
    """
    verb = "enable" if enable else "disable-user"
    vendor = packages.get("vendor", {})

    def run(adb, dev, log):
        targets = list(packages.get("core", [])) + list(packages.get("debloat", []))
        key = dev.manufacturer.lower()
        matched = next((v for k, v in vendor.items() if k.lower() == key), None)
        if matched:
            targets += matched
            log.write(f"vendor match: {key} -> {len(matched)} packages\n")
        else:
            log.write(f"no vendor entry for '{key}' - common lists only\n")

        touched = failed = 0
        for pkg in targets:
            args = ["pm", verb] + ([] if enable else ["--user", "0"]) + [pkg]
            p = adb.shell(args, dev.serial)
            _logged(log, p)
            combined = p.stdout + p.stderr
            if p.returncode == 0 and "Exception" not in combined:
                touched += 1
            else:
                # A package not present on this ROM, or a GMS component the
                # shell may not touch, is expected - not an error.
                failed += 1
        note = f"{touched}/{len(targets)}"
        if failed:
            note += f" ({failed} n/a)"
        if matched:
            note += f", vendor: {key}"
        return True, note
    return Task("Re-enable disabled packages" if enable else "Disable unused packages", run)


def task_shell(commands: list[list[str]], label: str) -> Task:
    """Run extra adb shell commands from the config."""
    def run(adb, dev, log):
        for cmd in commands:
            p = adb.shell([str(a) for a in cmd], dev.serial)
            _logged(log, p)
        return True, f"{len(commands)} commands"
    return Task(label, run)


def task_requirements(required: dict, optional: dict) -> Task:
    """Check that the Play Store apps are on the device before doing anything.

    Pushing configuration to a phone without ATAK accomplishes nothing,
    and the failure only becomes visible much later, in the field.
    """
    def run(adb, dev, log):
        installed = adb.shell(["pm", "list", "packages"], dev.serial, mutating=False).stdout
        miss_req = [n for p, n in required.items() if f"package:{p}" not in installed]
        miss_opt = [n for p, n in optional.items() if f"package:{p}" not in installed]
        log.write(f"missing required: {miss_req}\nmissing optional: {miss_opt}\n")

        if miss_req:
            return False, ("not installed: " + ", ".join(miss_req)
                           + " - install from Google Play first")
        if miss_opt:
            return True, f"WARNING: not installed: {', '.join(miss_opt)}"
        return True, f"{len(required) + len(optional)} present"
    return Task("Check required apps", run, fatal=True)


def task_permissions(perms: dict, appops: dict, exempt: list[str]) -> Task:
    """Grant runtime permissions to apps installed from the Play Store.

    Sideloaded APKs get everything from `adb install -g`. ATAK does not,
    so it is granted here rather than relying on the operator tapping
    through every dialog - and ACCESS_BACKGROUND_LOCATION cannot be
    granted from those dialogs at all.
    """
    def run(adb, dev, log):
        installed = adb.shell(["pm", "list", "packages"], dev.serial, mutating=False).stdout
        granted = skipped = missing = 0

        for pkg, permissions in perms.items():
            if f"package:{pkg}" not in installed:
                log.write(f"{pkg} not installed - skipping permissions\n")
                missing += 1
                continue
            for perm in permissions:
                p = adb.shell(["pm", "grant", pkg, perm], dev.serial)
                _logged(log, p)
                # pm grant is silent on success. Output means the app does
                # not declare it, or this Android version lacks it.
                if adb.dry_run or (p.returncode == 0 and not (p.stdout + p.stderr).strip()):
                    granted += 1
                else:
                    skipped += 1

        for pkg, ops in appops.items():
            if f"package:{pkg}" not in installed:
                continue
            for op, mode in ops:
                p = adb.shell(["appops", "set", pkg, op, mode], dev.serial)
                _logged(log, p)

        for pkg in exempt:
            if f"package:{pkg}" not in installed:
                continue
            p = adb.shell(["dumpsys", "deviceidle", "whitelist", f"+{pkg}"], dev.serial)
            _logged(log, p)

        note = f"{granted} granted" + (" (dry-run)" if adb.dry_run else "")
        if skipped:
            note += f", {skipped} n/a"
        if missing:
            note += f", {missing} app(s) not installed"
        return True, note
    return Task("Grant ATAK permissions", run)


def task_doze_check(packages: list[str]) -> Task:
    """Verify ATAK is exempt from Doze - checked, never changed.

    Blue-force tracking needs background GPS and network. If a future
    reset drops the exemption, this is where it becomes visible.
    """
    def run(adb, dev, log):
        p = adb.shell(["dumpsys", "deviceidle", "whitelist"], dev.serial, mutating=False)
        _logged(log, p)
        listed = p.stdout
        installed = adb.shell(["pm", "list", "packages"], dev.serial, mutating=False).stdout

        # A package that is not installed is not a problem; one that is
        # installed but not exempt is.
        present = [pkg for pkg in packages if f"package:{pkg}" in installed]
        absent = [pkg for pkg in packages if f"package:{pkg}" not in installed]
        missing = [pkg for pkg in present if pkg not in listed]
        if absent:
            log.write(f"not installed, not checked: {absent}\n")
        if missing:
            log.write(f"NOT allowlisted: {missing}\n")
            return True, f"WARNING: {', '.join(missing)} not exempt from Doze"
        note = f"{len(present)} exempt"
        if absent:
            note += f", {len(absent)} not installed"
        return True, note
    return Task("Check Doze allowlist", run)


VERIFIER_KEYS = ("package_verifier_enable", "verifier_verify_adb_installs")


def task_install(apks: list[Path], restore_verifier: bool = False) -> Task:
    """Sideload the APKs.

    Android's package verifier blocks adb installs with
    INSTALL_FAILED_VERIFICATION_FAILURE, so it is turned off for the
    duration regardless of --no-optimize - otherwise nothing installs at
    all. With --no-optimize the previous values are put back afterwards,
    since leaving the verifier off is a lockdown change the operator did
    not ask for.
    """
    def run(adb, dev, log):
        previous = {}
        for key in VERIFIER_KEYS:
            q = adb.shell(["settings", "get", "global", key], dev.serial, mutating=False)
            previous[key] = (q.stdout or "").strip()
            adb.shell(["settings", "put", "global", key, "0"], dev.serial)
        log.write(f"verifier was {previous}, disabled for install\n")

        failed, conflicts = [], []
        try:
            for apk in apks:
                p = adb.run(["install", "-r", "-g", str(apk)], serial=dev.serial, timeout=600)
                _logged(log, p)
                if adb.dry_run:
                    continue
                combined = p.stdout + p.stderr
                if p.returncode == 0 and "Success" in combined:
                    continue
                if "INSTALL_FAILED_UPDATE_INCOMPATIBLE" in combined:
                    conflicts.append(apk.name)
                else:
                    failed.append(apk.name)
        finally:
            if restore_verifier:
                for key, value in previous.items():
                    if value and value != "null":
                        adb.shell(["settings", "put", "global", key, value], dev.serial)
                log.write("verifier restored to previous values\n")

        if failed or conflicts:
            parts = []
            if failed:
                parts.append("failed: " + ", ".join(failed))
            if conflicts:
                parts.append("already installed with a different signature, "
                             "uninstall first: " + ", ".join(conflicts))
            return False, "; ".join(parts)
        return True, f"{len(apks)} apps" + (" (dry-run)" if adb.dry_run else "")
    return Task("Install apps", run)


def task_push(entry: dict, base: Path) -> Task:
    source = (base / entry["source"]).resolve()
    target = entry["target"]
    label = entry.get("label") or f"Push {entry['source']}"

    def run(adb, dev, log):
        if not source.exists():
            msg = f"missing: {source}"
            log.write(msg + "\n")
            return (False, msg) if entry.get("required") else (True, "skipped (not present)")
        p = adb.run(["push", str(source), target], serial=dev.serial, timeout=1800)
        _logged(log, p)
        return p.returncode == 0, "ok"
    return Task(label, run, fatal=bool(entry.get("required")))


def task_remove(paths: list[str], label: str) -> Task:
    def run(adb, dev, log):
        for path in paths:
            # single quotes so the device shell expands any glob, not ours
            p = adb.shell(["rm", "-rf", path], dev.serial)
            _logged(log, p)
        return True, f"{len(paths)} paths"
    return Task(label, run)


def task_uninstall(match: list[str], protected: list[str]) -> Task:
    def run(adb, dev, log):
        listing = adb.shell(["pm", "list", "packages"], dev.serial, mutating=False)
        _logged(log, listing)
        packages = [line.split(":", 1)[1].strip()
                    for line in listing.stdout.splitlines()
                    if line.startswith("package:")]

        targets = []
        for pkg in packages:
            low = pkg.lower()
            if not any(m.lower() in low for m in match):
                continue
            if any(low == p.lower() or low.startswith(p.lower()) for p in protected):
                log.write(f"protected, skipping: {pkg}\n")
                continue
            targets.append(pkg)

        removed = []
        for pkg in targets:
            p = adb.run(["uninstall", pkg], serial=dev.serial, timeout=180)
            _logged(log, p)
            if adb.dry_run or (p.returncode == 0 and "Success" in p.stdout):
                removed.append(pkg)
        if adb.dry_run:
            return True, f"{len(removed)} would be removed (dry-run)"
        return True, f"{len(removed)} removed" if removed else "nothing to remove"
    return Task("Uninstall apps", run)


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------

def build_install_tasks(cfg: dict, base: Path, optimize: bool = True) -> list[Task]:
    """Build the install sequence.

    `optimize` covers the lockdown steps - turning off system and app
    updates and disabling the manufacturers' update services. Wanted on an
    issued device, unwanted on someone's personal phone, so it can be
    skipped with --no-optimize.
    """
    apks = [(base / a).resolve() for a in cfg["kit"]["apks"]]
    req = cfg.get("requirements", {})
    tasks = []
    if req.get("required") or req.get("optional"):
        tasks.append(task_requirements(req.get("required", {}), req.get("optional", {})))
    tasks.append(task_stay_awake())
    if optimize:
        tasks += [
            task_settings(cfg["settings"]["install"]),
            task_packages(cfg["packages"], enable=False),
        ]
        extra = cfg.get("commands", {}).get("install", [])
        if extra:
            tasks.append(task_shell(extra, "Apply extra settings"))
    tasks += [task_install(apks, restore_verifier=not optimize)]
    if cfg.get("permissions") or cfg.get("appops") or cfg.get("battery", {}).get("exempt"):
        tasks.append(task_permissions(cfg.get("permissions", {}),
                                      cfg.get("appops", {}),
                                      cfg.get("battery", {}).get("exempt", [])))
    tasks += [task_push(e, base) for e in cfg["push"]]
    cleanup = cfg["kit"].get("cleanup_after_push", [])
    if cleanup:
        tasks.append(task_remove(cleanup, "Clean stale atak-box.zip"))
    doze = cfg.get("doze", {}).get("verify", [])
    if doze:
        tasks.append(task_doze_check(doze))
    return tasks


def build_restore_tasks(cfg: dict, wipe_media: bool) -> list[Task]:
    r = cfg["restore"]
    tasks = [
        task_uninstall(r["uninstall_match"], r.get("protected_prefixes", [])),
        task_remove(r["remove_paths"], "Remove ATAK files"),
    ]
    if wipe_media:
        tasks.append(task_remove(r["wipe_paths"], "Wipe user media"))
    tasks += [
        task_settings(cfg["settings"]["restore"]),
        task_packages(cfg["packages"], enable=True),
    ]
    extra = cfg.get("commands", {}).get("restore", [])
    if extra:
        tasks.append(task_shell(extra, "Revert extra settings"))
    return tasks


def preflight(cfg: dict, base: Path, out: Out) -> bool:
    problems = []
    for apk in cfg["kit"]["apks"]:
        if not (base / apk).exists():
            problems.append(f"missing app: {apk}")
    for entry in cfg["push"]:
        if entry.get("required") and not (base / entry["source"]).exists():
            problems.append(
                f"missing required file: {entry['source']}\n"
                "    This holds the TAK server address and certificate. It is\n"
                "    distributed separately - add the package for your server\n"
                "    before provisioning, or devices get no server contact."
            )
    for p in problems:
        out.error(p)
    return not problems


def wait_for_devices(adb: Adb, out: Out, timeout: int) -> list[Device]:
    out.info("Waiting for authorized devices (Ctrl-C to abort) ...")
    deadline = time.monotonic() + timeout
    warned: set[str] = set()

    while True:
        ready, pending = adb.list_devices()
        for serial, state in pending:
            if serial not in warned:
                hint = {
                    "unauthorized": "accept the USB debugging prompt on the device",
                    "offline": "reconnect the cable",
                    "no permissions": "check udev rules (Linux)",
                }.get(state, state)
                out.warn(f"{serial}: {state} - {hint}")
                warned.add(serial)
        if ready:
            return [adb.describe(s) for s in ready]
        if time.monotonic() > deadline:
            raise SystemExit("ERROR: no authorized devices within %ds" % timeout)
        time.sleep(2)


def confirm(prompt: str) -> bool:
    try:
        return input(f"{prompt} [y/N] ").strip().lower() in ("y", "yes", "j", "ja")
    except EOFError:
        return False


def confirm_word(prompt: str, word: str) -> bool:
    """Require the exact word. Used where a wrong keystroke destroys data."""
    try:
        return input(f"{prompt} (type {word} to confirm): ").strip() == word
    except EOFError:
        return False


def main(argv: list[str] | None = None) -> int:
    # Common options are accepted both before and after the subcommand, so
    # "provision install --dry-run" works as readily as
    # "provision --dry-run install". argparse.SUPPRESS keeps the subparser
    # from overwriting a value that was already given before the subcommand.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--config", type=Path, default=argparse.SUPPRESS,
                        help=f"config file (default: {DEFAULT_CONFIG})")
    common.add_argument("--adb", default=argparse.SUPPRESS,
                        help="path to adb, overriding auto-detection")
    common.add_argument("--serial", action="append", default=argparse.SUPPRESS,
                        help="only this device; repeatable")
    common.add_argument("-j", "--jobs", type=int, default=argparse.SUPPRESS,
                        help="devices to provision in parallel (default: 1)")
    common.add_argument("--log-dir", type=Path, default=argparse.SUPPRESS,
                        help="default: logs/ next to the config")
    common.add_argument("--wait", type=int, default=argparse.SUPPRESS,
                        help="seconds to wait for devices (default: 300)")
    common.add_argument("--dry-run", action="store_true", default=argparse.SUPPRESS,
                        help="print adb commands, change nothing")
    common.add_argument("-y", "--yes", action="store_true", default=argparse.SUPPRESS,
                        help="do not ask for confirmation")
    common.add_argument("-q", "--quiet", action="store_true", default=argparse.SUPPRESS)

    ap = argparse.ArgumentParser(
        prog="provision",
        parents=[common],
        description="Provision ATAK devices over adb (Windows, Linux, macOS).",
    )

    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("devices", parents=[common], help="list attached devices and exit")
    p_install = sub.add_parser("install", parents=[common],
                               help="install apps and push configuration")
    p_install.add_argument(
        "--no-optimize", action="store_true",
        help="skip the lockdown steps: leave system and app updates, the "
             "package verifier and the manufacturer's update services alone. "
             "Use this on a personal phone.")
    p_restore = sub.add_parser("restore", parents=[common],
                               help="uninstall apps and remove ATAK files")
    p_restore.add_argument("--wipe-media", action="store_true",
                           help="also delete Download, DCIM, Pictures and Documents")

    args = ap.parse_args(argv)
    for name, value in (("config", DEFAULT_CONFIG), ("adb", None), ("serial", []),
                        ("jobs", 1), ("log_dir", None), ("wait", 300),
                        ("dry_run", False), ("yes", False), ("quiet", False)):
        if not hasattr(args, name):
            setattr(args, name, value)
    out = Out(args.quiet)

    if not args.config.exists():
        out.error(f"config not found: {args.config}")
        return 2
    with args.config.open("rb") as fh:
        cfg = tomllib.load(fh)
    base = args.config.resolve().parent

    adb = Adb(find_adb(cfg, args.adb, out), dry_run=args.dry_run)
    out.info(f"adb: {adb.binary}")
    if args.dry_run:
        out.info("DRY RUN - no changes will be made")

    if args.command == "install" and not preflight(cfg, base, out):
        return 2

    adb.start_server()
    try:
        devices = wait_for_devices(adb, out, args.wait)
        if args.serial:
            wanted = set(args.serial)
            devices = [d for d in devices if d.serial in wanted]
            if not devices:
                out.error("none of the requested serials are connected")
                return 2

        out.rule("DEVICES")
        for i, d in enumerate(devices, 1):
            out.info(f"  {i}. {d}")
        out.rule()

        if args.command == "devices":
            return 0

        if args.command == "restore" and args.wipe_media and not args.yes:
            # Listed from the config, not hardcoded, so the warning cannot
            # drift away from what is actually deleted.
            print()
            print("!" * 60)
            print("  --wipe-media DELETES USER DATA on all "
                  f"{len(devices)} device(s) above:")
            for path in cfg["restore"]["wipe_paths"]:
                print(f"    {path}")
            print("  Photos, downloads and documents included. Not reversible.")
            print("!" * 60)
            if not confirm_word("Proceed?", "WIPE"):
                out.info("Aborted.")
                return 1
        elif args.command == "install" and not args.yes:
            print()
            if args.no_optimize:
                print("  Install WITHOUT lockdown: system and app updates are left")
                print("  as they are. Apps and configuration are still installed.")
            else:
                print("  Install WITH lockdown - on every device listed above:")
                print("    - system and app updates turned OFF")
                print("    - package verifier turned OFF")
                print("    - the manufacturer's update services disabled")
                print("  Not what you want on a personal phone; use --no-optimize.")
            if not confirm(f"Run install on {len(devices)} device(s)?"):
                out.info("Aborted.")
                return 1
        elif not args.yes and not confirm(f"Run '{args.command}' on {len(devices)} device(s)?"):
            out.info("Aborted.")
            return 1

        if args.command == "install":
            tasks = build_install_tasks(cfg, base, optimize=not args.no_optimize)
        else:
            tasks = build_restore_tasks(cfg, args.wipe_media)

        log_dir = args.log_dir or (base / "logs")
        runner = Runner(adb, out, log_dir)

        results: list[Result] = []
        if args.jobs > 1 and len(devices) > 1:
            out.info(f"Provisioning {len(devices)} devices, {args.jobs} at a time ...")
            quiet_runner = Runner(adb, Out(quiet=True), log_dir)
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
                futures = {pool.submit(quiet_runner.run, d, tasks): d for d in devices}
                for fut in concurrent.futures.as_completed(futures):
                    res = fut.result()
                    results.append(res)
                    out.info(f"  {res.device.serial}: "
                             + ("OK" if res.ok else "FAILED: " + ", ".join(res.failures)))
        else:
            for d in devices:
                out.rule(f"DEVICE {d}")
                results.append(runner.run(d, tasks))

        out.rule("SUMMARY")
        for res in results:
            status = "OK" if res.ok else "FAILED: " + ", ".join(res.failures)
            out.info(f"  {res.device.serial:<24} {status}")
            for w in res.warnings:
                out.info(f"  {'':<24} {w}")
        failed = [r for r in results if not r.ok]
        if failed:
            out.info(f"\n{len(failed)} of {len(results)} device(s) failed. Logs: {log_dir}")
            return 1
        out.info(f"\nAll {len(results)} device(s) completed. Logs: {log_dir}")
        return 0
    finally:
        # Deliberately not killing the adb server: it is shared, and tearing
        # it down would disrupt any other adb user - including a second copy
        # of this tool provisioning other devices at the same time.
        pass


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nAborted.", file=sys.stderr)
        sys.exit(130)
