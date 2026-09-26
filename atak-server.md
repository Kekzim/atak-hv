# TAK Server — operations notes

Working notes from testing TAK Server against the kit, 2026-09-20, 21 and
26. Written to give a running start on a real server, not as a manual.

**Rigs:** TAK Server 5.7-RELEASE-43 in Docker — first on a workstation, then
on a home NAS reachable from the internet (§8). Clients: ATAK-CIV 5.8.0.5 on
a OnePlus Nord N100 (Android 11), and on a Sony Xperia X running LineageOS
20 with no Google services at all. Measurements were run, not read. The
exceptions are flagged where they appear: the product fees and licence terms
in §6 come from Geotorget's own listings.

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

`deviceProfileEnableOnConnect` defaults to **false** (`CotMapServerListener`),
and Connection profiles are skipped until it is true. `atak-box.zip` does
**not** set it — neither does anything else in the kit.

The way in is enrollment. Right after a phone enrolls for its certificate,
`CertificateEnrollmentClient` fetches the **Enrollment** profile with
`onConnect=false`, and the gate in `DeviceProfileClient:181` only checks
on-connect requests. So the Enrollment profile must carry a `.pref` setting
`deviceProfileEnableOnConnect=true`; that one file unlocks every Connection
profile after it. **Verified on hardware**, on a freshly installed phone:
the Enrollment profile's `.pref` was applied 0.9 s before the first
on-connect profile request, which then went out instead of being skipped.

On 2026-09-26 a phone was built entirely this way. USB installed ATAK and its
Android permissions — nothing else. Enrollment, settings, loadouts, map
sources, overlays and plugins all came from the server (§2, §3).

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
$CURL -X PUT  -H 'Content-Type: application/octet-stream' \
      --data-binary @file "$S/device/profile/NAME/file?filename=X"
$CURL         "$S/device/profile/NAME/files"                # list
$CURL -X DELETE "$S/device/profile/NAME/file/ID"            # one file
$CURL -X DELETE "$S/device/profile/ID"                      # a profile: by id, not name
$CURL -X PUT -H 'Content-Type: application/json' \
      -d '{"id":1,"name":"NAME","active":true,"type":"Connection",
           "groups":["APPLY_TO_ALL_GROUPS"]}' "$S/device/profile/NAME"
```

`type` is required on update — omit it and you get a 500 from a
`NullPointerException` on `getType()`.

Without the `octet-stream` header the upload fails with `400 Invalid Request
Body`: curl's default form content type. URL-quote `filename`; non-ASCII
names such as `Sjökort-SFV-TS.xml` survive intact.

`APPLY_TO_ALL_GROUPS` is resolved when a device asks, not when the profile is
saved: a group created afterwards still received the profile.

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
| **`.apk`** | `atak/tmp/` → Android installer | **one per delivery** — see below |

Nothing is configured client-side. ATAK's importer routes by file type. A
data package nested inside a profile is unpacked and imported.

**Put one APK in a delivery, never several.** ATAK fires every install intent
within about half a second, and Android's installer keeps only the last:
with four plugins in one profile, three prompts were torn down mid-staging
and only the fourth could be installed. One APK per connect works — four
plugins in 1 min 47 s, an ATAK restart each — but plugins belong in ATAK's
update server instead (§3).

### Loadouts need no zip

`provision.py` reads the `<preference>` blocks out of `Grund.zip` /
`Planering.zip` and stages them. Feed the same generator and upload one
`.pref`: it both defines the loadouts and selects one via
`selected_loadout_key`. The zips are only a source format.

Selection is confirmed in Tools → pencil, which names the current loadout.
Do **not** judge by the toolbar: `Grund` sets only `hidden=`, so it leaves the
nav bar at default, and `Planering`'s `buttons=` renders almost identically.

### Phones pull; nothing is pushed

A profile reaches a phone at its **next connect**, not when it is saved.
ATAK stores the start time of its last successful profile request
(`deviceProfileOnConnectSyncTime<server>`) and asks for everything changed
since then. In daily use that is the next network drop, restart or morning;
on issue day, one ATAK restart.

### The kit as one profile

The kit's ATAK state fits one Connection profile, 160 kB zipped:

| File | Source |
|---|---|
| one `.pref`: the kit's 14 settings, both loadouts with Grund selected, the three update-server keys (§3) | `provision.task_prefs` |
| 27 map sources | `payload/atak/imagery/` |
| 2 overlays | `payload/atak/overlays/` |

The `.pref` comes from the kit's own code, so it cannot drift from what USB
provisioning stages: call `task_prefs({}, cfg["prefs"], base)` with a
stand-in adb whose `run(["push", src, dst])` copies `src` out and returns
success. Extra keys go into `cfg["prefs"]["entries"]` in memory. Empty
answers leave callsign and remarks out — those are per device.

On a fresh phone it arrived 24 s after an ATAK restart. Units switched at
once; the default map and the complete loadout took **one more ATAK start**,
because ATAK reads those at startup. Left out on purpose: `tools/bluetooth`
and `tools/vehicle_models` (ATAK ships its own), the maps package in
`tools/datapackage` (a duplicate of `imagery/`), licence files.

---

## 3. Plugins — ATAK's update server

The plugin channel. Verified on a Google-free phone: four plugins installed
in 48 s, one at a time, no ATAK restarts.

### How ATAK finds it

Three preferences, all deliverable in a profile:

| Key | Value |
|---|---|
| `appMgmtEnableUpdateServer` | `true` (Boolean; default false) |
| `atakUpdateServerUrl` | `https://<host>:<port>/update` (String; default empty) |
| `repoStartupSync` | `true` — re-read the index at every start |

ATAK refuses plain HTTP (`Update Server must be HTTPs`). It first requests a
version folder, `…/update/5.8.0/product.infz`, and falls back to
`…/update/product.infz` on a 404 — so per-ATAK-version plugin sets are
possible later, one folder each.

### TAK Server does not host it

TAK Server 5.7 has no repository endpoint. Any static HTTPS server does —
here, nginx in its own container on a port of its own.

**It can require client certificates, and should.** For an HTTPS URL on the
TAK host, ATAK trusts only the truststore configured for that host (system
CAs ignored) and presents the device's enrolled certificate — also on a port
that is not TAK's, confirmed in the nginx log:

```nginx
ssl_certificate        server.pem;            # TAK's own server certificate
ssl_client_certificate root-and-int-ca.pem;   # enrolled phones chain to the intermediate
ssl_verify_client      on;
ssl_verify_depth       2;
```

Without an enrolled certificate the answer is `400`. Nothing to install or
configure on the phones beyond the three preferences.

### The index

`product.infz` is a zip holding `product.inf`: one line per product, 13
comma-separated fields; `#` lines are comments.

```
#platform,type,package,name,version,versionCode,apk,icon,description,sha256,minSdk,takApi,size
Android,plugin,<package>,<name>,<versionName>,<versionCode>,<file.apk>,,<text>,<sha256>,21,com.atakmap.app@5.8.0.CIV,<bytes>
```

A comma inside a field must be written `\u002c`. The APK path is relative to
the index. ATAK checks the SHA-256 before handing the APK to Android.

**`versionCode` drives updates.** ATAK offers an update only when the repo
lists a higher one. hvreports and Ramsor both ship with `versionCode 1` —
whoever builds them must raise it with every release, or no phone is ever
offered the new version.

### On the phone

Settings → Tool Preferences → **Package Management**. (The Grund loadout
hides the Plugins tool; this path always works.) The screen shows the
update-server URL with a green check, then every product with its status.
Per plugin: tap it, confirm Android's install prompt. ATAK loaded each
plugin within a second of the install finishing — no separate "load plugin"
tap was needed.

Plugins built for ATAK 5.5.0 (hvreports, Ramsor) pass 5.8.0.5's
compatibility and signature checks.

---

## 4. Measurements

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

## 5. DTED

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

## 6. Maps

The kit ships 27 map definitions in `payload/atak/imagery/`, 119 KB total.
None of them is a map: each is a ~400-byte URL template (26 XYZ sources, one
WMS — Sjöfartsverket's chart). **Everything streams.** The only offline map
data on a device is `atak/imagecache/`, one SQLite per source holding tiles
someone already looked at — 52 MB on the test phone from casual panning,
against 1.6 GB of DTED. Terrain is offline and heavy; the map is online and
weightless.

### What ATAK accepts — verified on hardware

| Form | Where it lands | Notes |
|---|---|---|
| tile-source `.xml` | `atak/imagery/` | no prompts, ~400 bytes |
| GeoTIFF | mosaic dataset under `imagery/` | `ImageryScanner` recurses 3 deep |
| GeoPackage | ATAK **moves** it to `imagery/mobile/` | `provider=gpkg` |

`ImportGRGSort.MAX_GDAL_LENGTH` caps a single GDAL file at **256 MB**.

A GeoTIFF in `imagery/nmk50/` produced `srid 3006` in the mosaic database —
ATAK reads SWEREF99 TM directly, no reprojection step. It also stored the
sheet as a quadrilateral (`ullon` 15.86919 vs `lllon` 15.86256), so grid
convergence is modelled rather than assumed away.

On 5.8 a `.gpkg` dropped in `atak/layers/` is relocated at startup:

```
AppVersionUpgrade: Try move /storage/emulated/0/atak/layers/x.gpkg
                        -> /storage/emulated/0/atak/imagery/x.gpkg
```

ATAK then deletes `layers/`, so a second push to that path fails silently
with `remote couldn't create file: Is a directory`. Recreate it first.

### NMK50 — closed, and streaming is not the issue

Försvarsmakten's 1:50 000 field map is on Geotorget, free, no legal review.
A personal account is **not** enough: the military products need an
organizational login.

The STAC catalogue is open and needs no account —
`https://api.lantmateriet.se/stac-karta/v1` — but every data asset on
`dl1.lantmateriet.se` returns 401. Metadata public, pixels gated.

| Product | Sweden | MR S | Blekinge |
|---|---|---|---|
| NMK50 (1:50k) | 409 sheets, 7.59 GB | 97, 1.67 GB | 18, 275 MB |
| NMK250 (1:250k) | 88 sheets, 419 MB | 19, 99 MB | 6, 31 MB |

Sheets average 18.6 MB, max 29.7 MB — comfortably under the 256 MB cap.

**There is no NMK streaming product.** Geotorget lists only
`nmk50-nedladdning-api` and `nmk250-nedladdning-api`. If the requirement is
streaming, NMK is out regardless of who holds the login. MSB's own guidance
treats civil NMK as something to print.

### Lantmäteriet's topographic map

Open data, and the download route needs no account at all:

```
ftp://download-opendata.lantmateriet.se/Topografisk_webbkarta_raster/
```

Anonymous FTP. Four whole-Sweden GeoPackages, 139.3 GB (nedtonad/mercator)
to 175.3 GB (färg/sweref). Standard Web Mercator pyramid, zoom 0–17, 256 px
tiles, EPSG:3857.

The server honours byte ranges, and a GeoPackage is a SQLite tile pyramid,
so a region can be carved out without downloading the file. Walking the
B-tree over FTP, **Blekinge to zoom 12 took 369 tiles, 6.8 MB, 24 seconds,
fetching 0.019% of the source.** Measured, not estimated; the result passed
`integrity_check` and rendered on the phone. A prototype was written and
then reverted — the technique is what matters, and it is sound.

Scaling from measurement: z13 = 966 tiles/16.1 MB, z14 = 3 818/48.4 MB, so
z15 lands near 180 MB for one county. **z13 is the server-pushable tier**;
anything deeper is USB, which is why this route was set aside.

### Streaming Lantmäteriet costs money

| Product | Fee | Use |
|---|---|---|
| Visning, cache | **Avgift** | zoom 0–18, colour + nedtonad — the one to want |
| Visning | Avgift | dynamic rendering |
| Visning, översiktlig | CC0, free | **≤ 1:30 236 only, ends 2026-12-31** |
| Nedladdning, raster | free | the 139 GB GeoPackage above |

Being filed under Geotorget's **Krisberedskap och blåljus** category does not
make a product free. That category marks MSB's recommended national
background map. The free-of-charge arrangement covers *regionernas
ambulansverksamheter och kommunala räddningstjänster* — not Hemvärnet.

> `minkarta.lantmateriet.se/map/topowebbcache` serves the full map with no
> authentication and would be a drop-in tomorrow. **Do not use it.** It is
> the backend of Lantmäteriet's own web application, and the matching
> product is one of the paid ones above.

The realistic path is `https://maps.lantmateriet.se/topowebb/v1.1/wmts` under
an agreement Försvarsmakten plausibly already holds. The question for the
chain of command is which agreement covers it and who administers the token —
not whether to buy it. Once there is a token it is one XML in
`payload/atak/imagery/` and a line in `provision.toml`.

---

## 7. Certificate self-enrollment

Removes per-device certificate files. Verified end to end.

### Setup

1. **Intermediate CA** — the root alone will not do; the signing keystore
   must hold the CA key plus its chain.

   ```bash
   docker exec <container> bash -c "cd /opt/tak/certs && ./makeCert.sh ca MY-INT-CA"
   ```

   Answer **no** when it offers to re-sign existing certs, so server and admin
   certs keep chaining to the root.

   Then **import the intermediate into the server's truststore**. With the
   root alone, a phone that presents only its own certificate, without the
   chain, is rejected on 8443 and 8089:

   ```bash
   openssl x509 -in MY-INT-CA.pem -out MY-INT-CA-only.pem   # first cert only
   keytool -importcert -noprompt -trustcacerts -alias my-int-ca \
       -file MY-INT-CA-only.pem -keystore truststore-root.jks -storepass:env CAPASS
   ```

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
GET  https://<host>:8446/Marti/api/tls/config        → the O / OU a CSR must carry
POST https://<host>:8446/Marti/api/tls/signClient/v2?clientUid=X&version=5.8
     Basic auth, body = PEM CSR
  → 200 {"signedCert": "...", "ca0": "...", "ca1": "..."}
GET  https://<host>:8446/Marti/api/tls/profile/enrollment?clientUid=X   (Basic auth)
```

Verified on phones: the signed certificate carries the stream on 8089 and the
profile requests on 8443. A CSR without the `O`/`OU` from `/tls/config` is
refused — `CSR validation failed`, surfacing as a 500; ATAK always includes
them. When scripting it, note that the base64 in the response already
contains line breaks: strip whitespace before re-wrapping as PEM.

Straight after enrolling, ATAK logs `error occurred and the preference
activity has been closed prior to the enrollment completing` with `Can't
create handler inside thread`. Harmless — only its completion dialog fails.

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

Our connection package gives its truststore its own filename and password
rather than reusing `caCert.p12`: two packages shipping the same filename
risk overwriting each other's CA (not tested). Its password should not be
CAPASS either — that one also protects the CA's signing keystore (§9).
Build the `.p12` with `-legacy` (SHA-1 MAC, 2048 iterations), as
`atak-box.zip`'s is, for older Android.

---

## 8. Running it outside the lab

The rig moved to a home NAS (Unraid) and was used from the internet. What
that took, and what it taught.

### Getting traffic in

**Cloudflare Tunnel cannot carry TAK.** 8089 is raw TLS, not HTTP, and for
anything but HTTP the tunnel needs `cloudflared` on the client. Cloudflare's
edge also terminates TLS, which breaks TAK's trust in both directions: the
phone sees Cloudflare's certificate, not one in its truststore, and the
server never sees the client certificate. Spectrum would pass TLS through,
but arbitrary TCP ports are Enterprise-only.

What works: a DNS-only (grey-cloud) record, and the router forwarding TCP
**8089, 8443, 8446** — plus the plugin repository's port (§3). Nothing else:
not 8444 or 9000 (federation), not 5432. 8446 is the only port that accepts
a password; close its forward when no one is enrolling.

On a UniFi gateway hairpin NAT is on by default, so phones on the home WiFi
reach the public name too; they show up with the gateway's LAN address as
source. The gateway's own UniFi application listens on 8443 — the forward
still wins.

From a phone on a carrier network (Telenor, via a hotspot), enrollment,
stream and profiles all worked.

### The containers

Plain `docker run` from one script: Unraid ships no Compose.

- **TAK sizes its five JVMs from `/proc/meminfo`, and inside a container that
  is the host's RAM** — about 40% of the whole host as heap ceilings. Every
  `*_MAX_HEAP` is overridable; set them. At the values TAK picks for an 8 GB
  box (239 / 1331 / 1331 / 279 / 279 MB) the server used 2.6–3.2 GiB and the
  database ~270 MiB with a few phones.
- **The database script initialises `/var/lib/postgresql/15/data`, not the
  image's `PGDATA`.** Mount that path, owned by uid 999, or the data lives in
  the container and dies with it.
- **`CoreConfig.xml` must exist before the database's first start**: its
  setup reads the database password from the `<connection>` element.
- **TAK rewrites `CoreConfig.xml` on first start**, adding a federation block
  that copies the `<tls>` passwords. Correct passwords there too.
- **The container stays "Up" when a JVM inside it dies.** Five Java processes
  are backgrounded and the script idles. Count them.
- **The images are thin** — Temurin 17, and Postgres 15 with PostGIS. All of
  TAK lives in the mounted `tak/` directory, so the images move with
  `docker save | ssh … docker load`, and the licensed part is the directory,
  not the images.
- **Reusing an extracted `tak/` tree:** `unzip` keeps the vendor's file dates,
  so anything dated after extraction is state an earlier run created —
  certificates, generated configs, `work/`, logs.
- `makeCert.sh server <fqdn>` puts the name in both CN and SAN, which ATAK's
  hostname check needs.

### Phones without Google

ATAK-CIV 5.8.0.5 and all four plugins contain **zero** Google Play Services
classes, checked in every `classes*.dex`. On LineageOS 20 with no Google apps
at all, everything in this file worked: enrollment, profiles, and installs
from the update server.

An idle phone with its screen off let WiFi sleep, and ATAK could not
reconnect until it was woken. Keep test phones awake on USB.

---

## 9. Traps

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

**No CoreConfig `sed` needed** for the truststore. Keep `truststore-root.jks`
and import the intermediate into it (§7); the deck's switch to a
`truststore-<int>` file is the other road to the same place.

**Two certificate passwords, not one.** `makeRootCa.sh` protects
`truststore-root.jks`, `truststore-root.p12` and `fed-truststore.jks` with
**CAPASS**; the server keystore uses **PASS**. Left at `atakatak` both, it
never shows. Set them apart and every `truststorePass` in CoreConfig must be
CAPASS, or TAK logs `keystore password incorrect` and opens no port.

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

**Profile uploads need `Content-Type: application/octet-stream`**, and
**profiles are deleted by id**: `DELETE /device/profile/<name>` gives 400,
`Failed to convert value of type 'java.lang.String' to required type
'java.lang.Long'`.

**A single-file bind mount does not see `sed -i`.** It writes a new file and
renames it over the old; the container keeps the old inode, so a reload
reloads the old config. Recreate the container.

**Grund hides ATAK's Plugins tool.** Settings → Tool Preferences → Package
Management reaches the same screen.

**No delivery confirmation for profiles.** Nothing records which device
received which profile; the only evidence is the API log line `Returning
connection profile for <uid>`. Certificates *are* tracked —
`/Marti/api/certadmin/cert/active`.

---

## 10. Reference

**OpenAPI spec**, machine-readable, no login:

```
https://docs.tak.gov/api/takserver/<version>/openapispec.json
https://docs.tak.gov/api/takserver/tags.json     # version list
```

301 endpoints in 5.6-RELEASE-14. Versions jump 5.6 → 5.8; no 5.7 published.
The Redoc page needs JavaScript; the JSON does not.

Server source: `~/repos/atak-server` — `com.bbn.marti.device.profile` is the
profile machinery. Client source: `~/repos/atak-civ` — for the update server
`com.atakmap.android.update`: `RemoteProductProvider` (URL handling, version
folder), `ProductInformation` (the `product.inf` columns),
`http/GetRepoIndexOperation`; certificate selection for HTTPS in takkernel's
`CertificateManager.ExtendedSSLSocketFactory`.

---

## 11. Open

- **One carrier tested.** Telenor (via a hotspot) works end to end; Telia,
  Tele2 and Tre are untested. Terrain distribution over mobile data is
  unmeasured — the throughput table is LAN and loopback.
- **Concurrency measured with simulated clients.** Real phones hold
  connections longer, so the true limit is likely lower than the table.
- **Data Sync feeds untouched.** Metodanvisning §1.4 makes Feeds the core of
  how SLO, UPK and UND move, with per-role rights. Not explored at all.
- **Two device models tested**: a OnePlus Nord N100 on stock Android 11, and
  a Sony Xperia X on LineageOS 20.
- **One unexplained empty profile answer.** Once, just after a phone's WiFi
  woke, an on-connect request got nothing though a profile was waiting. Not
  the streaming-group race (`useStreamingGroup` is unset). It did not recur
  in later deliveries.
- **Multi-select install untested.** Package Management was used one plugin
  at a time.
- **Kit scope.** The kit profile is scoped to one test group. Real use needs
  all groups, or one kit per grupp.
- **No map licence read.** The FTP is open and the data free, but
  *Användningsvillkor för Topografisk webbkarta Nedladdning, raster* governs
  what may be done with an extract. Unread.
- **Who holds the Lantmäteriet agreement?** The streaming product is the
  whole map question. Nobody has been asked yet.
- **Raster performance unmeasured.** The GeoTIFF test used a 1.2 MB
  stand-in, not a real 21.9 MB sheet, so reprojection cost on a phone and
  seams between adjacent sheets are both unknown.
