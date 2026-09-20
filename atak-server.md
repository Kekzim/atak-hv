# TAK Server — operations notes

Working notes from testing a local TAK Server against the kit, 2026-09-20.
Written to give a running start on a real server, not as a manual.

**Rig:** TAK Server 5.7-RELEASE-43 in Docker, against ATAK-CIV 5.8.0.5 on a
OnePlus Nord N100. Everything below was run, not read.

Two things this file deliberately leaves out: server addresses and
credentials. Fill them in locally.

---

## 1. The one thing to understand first

**ATAK's own state can come from the server. Android's cannot.**

ATAK is an ordinary sandboxed app. There is no `Settings.Global.put` anywhere
in its source, no `pm disable-user`, no `appops`. So the split is fixed:

| Layer | Delivered by | Changes |
|---|---|---|
| Preferences, overlays, maps, loadouts, terrain | **Server**, any time | Often |
| Android lockdown, debloat, permissions, Doze | **`provision.py` over USB** | Once, at issue |
| Identity, trust, `deviceProfileEnableOnConnect` | **USB or enrollment** | Once, bootstraps the rest |

The last row is a chicken-and-egg: the server cannot bootstrap itself. A
device has to be told where the server is and to trust it before the server
can manage anything.

`deviceProfileEnableOnConnect` defaults to **false** (`CotMapServerListener`).
Nothing arrives until it is true. `atak-box.zip` sets it.

---

## 2. Device profiles

The mechanism. Admin UI → Device Profiles, or the API below. A profile is a
set of files plus a type and a group scope.

| Type | Fires |
|---|---|
| `Enrollment` | once, when a device enrolls for a certificate |
| `Connection` | every connect, for every device |

Mutually exclusive — the API derives the booleans from `type`, so setting one
clears the other.

### API

All under `/Marti/api/device/profile`, client-cert authenticated.

```bash
CURL="curl -sk --cert admin-cert.pem --key admin-key.pem"

$CURL -X POST "$S/device/profile/NAME"                      # create
$CURL -X PUT  --data-binary @file "$S/device/profile/NAME/file?filename=X"
$CURL         "$S/device/profile/NAME/files"                # list
$CURL -X DELETE "$S/device/profile/NAME/file/ID"
$CURL -X PUT -H 'Content-Type: application/json' \
      -d '{"id":1,"name":"NAME","active":true,"type":"Connection",
           "groups":["APPLY_TO_ALL_GROUPS"]}' "$S/device/profile/NAME"
```

`type` is required on update — omit it and you get a 500 from a
`NullPointerException` on `getType()`.

Fetch as a client would, which is how to test without a phone:

```bash
$CURL "$S/device/profile/connection?syncSecago=-1&clientUid=ANDROID-test"
```

### What it can deliver — all verified on hardware

| Content | Where ATAK puts it | Prompts |
|---|---|---|
| `.pref` | applied to preferences | none |
| `.kml` | `atak/overlays/` | none |
| imagery `.xml` | `atak/imagery/` | none |
| loadout `.zip` | unpacked, `.pref` imported | none |
| DTED `.zip` (containing `DTED/`) | `atak/DTED/` | none |
| **`.apk`** | `atak/tmp/` → Android installer | **two taps** |

Nothing is configured client-side. ATAK's importer routes by file type. A
data package nested inside a profile is unpacked and imported.

**Plugin APKs need two taps per app per device** — Android's installer, then
ATAK's "load plugin". Not unattended. That's the one thing that stays a
physical exercise.

### Loadouts need no zip

`provision.py` reads the `<preference>` blocks out of `Grund.zip` /
`Planering.zip` and stages them. Feed the same generator and upload one
`.pref`: it both defines the loadouts and selects one via
`selected_loadout_key`. The zips are only a source format.

Selection is confirmed in Tools → pencil, which names the current loadout.
Do **not** judge by the toolbar: `Grund` sets only `hidden=`, so it leaves the
nav bar at default, and `Planering`'s `buttons=` renders almost identically.

---

## 3. Measurements

Loopback clients, clean heap, API service at `-Xmx5201m`.

| Package | Concurrent clients | Result |
|---|---|---|
| 170 kB | 100 | 100/100, 0.4 s |
| 6.5 MB | 100 | 100/100, 1.8 s |
| 45 MB | 10 | 10/10 |
| 45 MB | 15 | **13/15** |
| 45 MB | 20 | 20/20 |
| 45 MB | 30 | **23/30**, then 19/30 |
| 317 MB | 3 | **2/3** |

Failure is always the same:

```
java.lang.OutOfMemoryError: Java heap space
  at java.util.zip.ZipOutputStream.write
  at com.bbn.marti.util.missionpackage.MissionPackage.addEntry
```

**The server builds every package into a `ByteArrayOutputStream`** — the whole
zip in RAM, per request. Cost is per fetching client, not once.

Note the non-monotonic 15/20/30 rows: this is garbage-collection timing, not
a clean threshold. Around 45 MB it becomes unreliable somewhere above ten
clients and you cannot predict where. Don't design near it.

### Steady state is free

Those numbers are **first connect only**. The client sends `syncSecago` =
seconds since its own last sync, and the server returns only profiles whose
`updated` timestamp falls inside that window:

```
syncSecago=60     → HTTP 204, 0 bytes     (nothing changed)
syncSecago=86400  → HTTP 200, 45 MB       (only because a profile was edited 9 min earlier)
```

So terrain transfers **once per device**, and again only when you edit that
profile. Load recurs in exactly two cases: initial rollout, and after an edit.

### The filter is per profile, not per file

`getProfileFiles` selects whole profiles by timestamp, then returns all their
files. Touch one file in a profile and every client re-pulls the whole thing.

**Split content by how often it changes:**

| Profile | Contents | Churn |
|---|---|---|
| policy | units, reporting rates, loadouts | often, kB |
| content | overlays, imagery | occasional, MB |
| terrain | DTED, one per grupp | rare, 5–12 MB |

---

## 4. DTED

Cells are 1°×1°, named by their south-west corner: `e015/n56` covers
15–16°E, 56–57°N.

### MR S coverage — 24 cells, 44.8 MB zipped (298 MB raw)

Box `e012`–`e017` × `n55`–`n58`. Zipped MB per cell:

```
        n55    n56    n57    n58
e012    0.1    1.0    3.9    2.6
e013    1.8    3.2    3.3    1.9
e014    0.5    2.7    3.0    2.3
e015      0    2.7    3.6    3.5
e016      0    0.7    2.3    3.4
e017      0      0      0    0.9
```

Five cells are open Baltic and cost nothing — keep them.

**Never ship all of MR S to every device.** One profile per
militärregiongrupp, its own cells only, lands at 5–12 MB — comfortably in the
regime that took 100 clients. A shared all-of-MR-S profile would fail when a
unit reconnects after an exercise.

Blekinge is the worked example: `e014/n55`, `e014/n56`, `e015/n55`,
`e015/n56` — **6.1 MB**, four cells. Slightly more than the obvious two
because the coast dips below 56°N (Utklippan ≈ 55.95°N). The two `n55` cells
are 0.6 MB combined.

### Delivery

Zip a directory named `DTED/` containing the `e0xx/` folders. ATAK recognises
it as `[Zipped DTED directories]` and unpacks to `/sdcard/atak/DTED/`.
Case doesn't matter — the phone's filesystem is case-insensitive, verified.

Budget **2.5–3× the compressed size** in free space during transfer: the zip
and its extraction coexist before cleanup. 317 MB peaked at ~640 MB.

Drop the GDAL `.aux.xml` sidecars; ATAK never reads them.

### ATAK streams DTED0 by itself — check this

`ElevationDownloader implements AtakMapView.OnMapMovedListener`. As the map
moves it fetches missing tiles:

```
https://<server>/elevation/DTED/<path>.zip
```

| Preference | Default |
|---|---|
| `prefs_dted_stream` | **true** |
| `prefs_dted_stream_server` | **tak.gov** |

**Every device is doing this out of the box**, including locked-down ones —
outbound HTTPS to tak.gov as soldiers pan the map. This explained a phone's
DTED0 count rising 84 → 119 mid-session.

The level is hardcoded to `0`, so it only ever streams DTED0 (~900 m). It
will not deliver the DTED2 needed for siktlinjer. Decide deliberately: turn
it off, or point it at your own host. Both are preferences, so both ship in
the policy profile.

---

## 5. Certificate self-enrollment

Removes per-device certificate files. Verified end to end.

### Setup

1. **Intermediate CA** — the root alone will not do; the signing keystore
   must hold the CA key plus its chain.

   ```bash
   docker exec <container> bash -c "cd /opt/tak/certs && ./makeCert.sh ca MY-INT-CA"
   ```

   Answer **no** when it offers to re-sign existing certs, so server and admin
   certs keep chaining to the root.

2. **CoreConfig**, after `</security>`:

   ```xml
   <certificateSigning CA="TAKServer">
       <certificateConfig>
           <nameEntries>
               <nameEntry name="O" value="..."/>
               <nameEntry name="OU" value="..."/>
           </nameEntries>
       </certificateConfig>
       <TAKServerCAConfig keystore="JKS"
           keystoreFile="/opt/tak/certs/files/MY-INT-CA-signing.jks"
           keystorePass="..." validityDays="365" signatureAlg="SHA256WithRSA"/>
   </certificateSigning>
   ```

3. **Accounts** — enrollment uses HTTP Basic, so identities must exist:

   ```bash
   java -jar /opt/tak/utils/UserManager.jar usermod -p '<pw>' -g <group> <user>
   ```

   Password rules: ≥15 chars, upper, lower, digit, special.

4. Restart.

### The flow

```
POST https://<host>:8446/Marti/api/tls/signClient/v2?clientUid=X&version=5.8
     Basic auth, body = PEM CSR
  → 200 {"signedCert": "...", "ca0": "...", "ca1": "..."}
```

Then that cert authenticates to 8443 and pulls its group's profile. Both
verified.

### At battalion scale

```
POST /user-management/api/new-users
     {"usernameExpression":"hv36-", "startN":1, "endN":200, "groupList":["Blekingegruppen"]}
```

One call creates the identities; **one identical `atak-box.zip`** (CA cert
plus `enrollForCertificateWithTrust`) serves the whole battalion; each phone
enrols itself on first connect and receives its grupp's profile.

`DELETE /Marti/api/certadmin/cert/revoke/{ids}` cuts off a lost device
centrally.

---

## 6. Traps

Things that cost time, in the order they bite.

**Docker build fails as documented.** `postgres:15.1` is unbuildable — 77
packages 404 from the bullseye-security pool. `postgres:15` (trixie) has no
`openjdk-17`, which the guide requires. Use **`postgres:15-bookworm`**. Keep
the vendor Dockerfile and build from a patched copy.

**Use the tak.gov docker zip, not Iron Bank.** The deck shows only
`registry1.dso.mil`, which needs a Platform One account. Guide §6.2 documents
building from `takserver-docker-<version>.zip`, and its Dockerfiles use plain
public bases.

**`certmod` must run after the API is up.** Too early and it dies with an
`InvocationTargetException` from `OnlineFileAuthModule.getUsers`. Same command
works unchanged once the server has started.

**No CoreConfig `sed` needed** for a root-only CA. The deck's
`truststore-root` rewrite applies to the intermediate-CA workflow.

**TAK's p12 files use RC2-40-CBC.** OpenSSL 3 refuses without `-legacy`:

```bash
openssl pkcs12 -legacy -in cert.p12 -nocerts -nodes -out key.pem
```

**CoreConfig is root-owned** by the container, and the container has **no
`python3`**. Edit from inside with `sed`.

**`cot_streams` is not merged per index.** ATAK parses every index
`0..count-1` from the file being imported. A file with `count=2` but only
index-1 keys throws `NullPointerException` on `String.split()` and applies
nothing. A `count=1` file with index 0 *is* merged into the existing list —
importing a server package does not wipe the others.

**Re-importing a connection package drops cached credentials.** The user has
to re-enter them.

**No delivery confirmation for profiles.** Nothing records which device
received which profile; the only evidence is the API log line `Returning
connection profile for <uid>`. Certificates *are* tracked —
`/Marti/api/certadmin/cert/active`.

---

## 7. Reference

**OpenAPI spec**, machine-readable, no login:

```
https://docs.tak.gov/api/takserver/<version>/openapispec.json
https://docs.tak.gov/api/takserver/tags.json     # version list
```

301 endpoints in 5.6-RELEASE-14. Versions jump 5.6 → 5.8; no 5.7 published.
The Redoc page needs JavaScript; the JSON does not.

Server source: `~/repos/atak-server` — `com.bbn.marti.device.profile` is the
profile machinery. Client source: `~/repos/atak-civ`.

---

## 8. Open

- **Mobile network untested.** Everything measured over LAN or loopback.
  Decides whether terrain distribution works in the field or only in garrison.
- **Concurrency measured with simulated clients.** Real phones hold
  connections longer, so the true limit is likely lower than the table.
- **Data Sync feeds untouched.** Metodanvisning §1.4 makes Feeds the core of
  how SLO, UPK and UND move, with per-role rights. Not explored at all.
- **One device model tested.**
