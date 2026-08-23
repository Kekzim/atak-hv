# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A provisioning kit, not an application. `provision.py` drives `adb` to set up
Android phones for ATAK use in the Swedish Home Guard (Hemvärnet), alongside
the payload that lands on the devices and the Swedish instruction material in
`docs/`.

Python 3.11+, standard library only (`tomllib`). No dependencies, no build
step, no package metadata. The kit must run from any directory — a USB stick,
`C:\`, a home directory — so every path is resolved relative to
`provision.toml`.

## Commands

```bash
./provision.sh devices                    # list attached devices and exit
./provision.sh install --dry-run          # print the plan, change nothing
./provision.sh install --no-optimize      # skip the lockdown steps
./provision.sh restore --wipe-media       # also delete user media (types WIPE)
```

`provision.bat` is the Windows entry point; both are thin launchers around
`python3 provision.py`. Common flags work before or after the subcommand.
`--serial` targets one device, `-j N` provisions N in parallel, `-y` skips
every confirmation including the `WIPE` word-prompt.

## Testing

**There is no test suite, no linter and no CI.** Verification means running
the tool against a real phone over `adb`. Useful properties when doing that:

- `--dry-run` still needs a device connected — `wait_for_devices` runs before
  any task, and read-only adb calls execute for real.
- The plan is printed as labelled steps, but the actual adb commands only
  reach `logs/<serial>.log`, never stdout.
- Simulate destructive matching without running it: read
  `adb shell pm list packages` and apply `uninstall_match` /
  `protected_prefixes` in a scratch script before trusting `restore`.
- Package ids can be read straight out of an APK's binary `AndroidManifest.xml`
  string pool when `aapt` is unavailable.
- **Device state settles asynchronously — poll, do not check once.** A
  single check right after an adb command can read a stale value and turn
  into a wrong conclusion in a commit message. The Doze allowlist, for one,
  keeps an uninstalled app listed for under a second.

## Architecture

`provision.py` is one file in four layers:

- **`Adb`** wraps `subprocess`. Every call is tagged `mutating=True/False`;
  read-only calls run even under `--dry-run`, mutating ones return a stubbed
  `CompletedProcess`. This is why a dry run reports the device's *current*
  state and can warn about things a real run would have fixed.
- **`Task`/`Result`/`Runner`** — a `Task` is a label plus a closure
  `(adb, device, log) -> (ok, note)`. `Runner` executes the list per device,
  writing every command to the device log. It continues past failures unless
  `task.fatal` — `task_requirements` and any `[[push]]` marked
  `required = true` are fatal. A fatal failure does not stop the device
  outright: it skips ahead to the remaining tasks marked `always`, which are
  the steps that hand the device back rather than change it further. A note
  starting with `WARNING` surfaces in the summary without failing the run.
- **`task_*` builders** turn config into `Task` objects.
- **`build_install_tasks` / `build_restore_tasks`** compose the plan from
  `provision.toml`.

**Behaviour lives in `provision.toml`, not in `provision.py`.** Adding a
manufacturer, an app, a permission, a debloat target or a setting is a config
change. Prefer extending the config over adding code.

### Invariants worth knowing before editing

- **Task closures are shared across devices.** `build_*_tasks` runs once and
  `-j > 1` hands the same `Task` objects to a `ThreadPoolExecutor`. Any state
  a closure keeps between its steps must be keyed by serial — see
  `tasks_stay_awake`.
- **Ordering is load-bearing.** Installs must precede `task_permissions`:
  `pm grant`, `appops` and the Doze allowlist all skip packages missing from
  `pm list packages`. The stay-awake revert must stay last, and is marked
  `always=True` so a failed `atak-box.zip` push cannot leave the screen
  pinned on.
- **A package id the device does not have is reported, not skipped.**
  `task_permissions` collects the names and prefixes its note with
  `WARNING` so they reach the summary; the run still succeeds, since an
  app may legitimately be absent. Under `--dry-run` this also fires for a
  package the same run would have sideloaded. Package ids can be read out
  of an APK's manifest when in doubt — that is how `com.atakmap.takcam`
  was confirmed.
- **Leave no trace.** `install` must hand the device back as it found it.
  Anything it changes for the duration of the run — the package verifier,
  the stay-awake setting — gets saved and restored, and `restore` must undo
  what `install` did.
- **An unset Android setting reads back as the string `"null"`.** Restoring
  it means `settings delete global <key>`, never `settings put ... null`.
- **ATAK preferences can be staged, not just typed in.** ATAK reads
  `/sdcard/atak/config/prefs/defaults` at startup (`ingestDefaults()` in
  `PreferenceControl`, called early from `ATAKActivity`), applies every
  entry and deletes the file. `task_prefs` writes it.
  `[prefs.entries]` carries the settings that are identical on every device
  (MGRS, MSL, mils, grid north). Same XML shape as the `config.pref` inside
  `atak-box.zip`. Values that look numeric are **strings** — ATAK reads them
  with `getString()` then `Integer.parseInt()`, so an Integer entry throws
  `ClassCastException` inside the app. The importer
  applies any key — the blacklist naming `locationCallsign` is on the JSON
  path, not this one — and ATAK only invents a callsign when the pref is
  empty, so a staged value wins.
- `restore` matches package ids by **substring**, so a broad term like
  `"atak"` is deliberate and `protected_prefixes` is the guard that keeps it
  from taking out system components.

## Payload and secrets

`payload/apks/` holds only sideloaded apps. **ATAK-CIV (Civil Use)** and its
two plugins — **ATAK Plugin: Data Sync** and **ATAK Plugin: GeoCam** — come
from Google Play and are *checked for*, not installed; see `[requirements]`,
where the labels are the Play Store names so the tool's warning is the string
an operator can search for. ATAK-CIV must already be present or `install`
aborts.

`payload/ATAK-installation/atak-box.zip` carries the TAK server address and
certificates. It is förbandsspecifik, gitignored, and required: preflight
aborts `install` without it. `.gitignore` also blocks certificates and the
Play Store APK filenames — check before adding anything under `payload/`.

## Conventions

- **Commit messages: Swedish, ASCII only** — no `å`, `ä`, `ö`. 27 of 28
  commits follow this. Subject line in the imperative, body explaining why.
- **Docs (`README.md`, `docs/*.md`): Swedish with full diacritics.**
- **Code comments, docstrings and task labels: English.** Comments explain
  *why* a step exists, usually naming the failure it prevents.
- `provision.toml` comments mix both: English for structure, Swedish
  (ASCII) for domain notes.
- `.gitattributes` pins line endings: `*.bat` CRLF, `*.py`/`*.sh`/`*.toml` LF.
