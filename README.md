# atak-hv

Utrustningspaket för **ATAK** (Android Team Awareness Kit) i Hemvärnet.
Repot innehåller verktyget som provisionerar telefoner via `adb`,
konfigurationen som läggs ut på enheterna, och instruktionsmaterialet.

> [!IMPORTANT]
> **Serverpaketet `atak-box.zip` ingår inte i repot.** Det innehåller
> TAK-serverns adress och certifikat och är förbandsspecifikt. Utan det
> avbryts installationen. Se [Före utskick](#före-utskick).

## Snabbstart

```bash
# Windows
provision.bat devices           # ser verktyget telefonerna?
provision.bat install --dry-run # vad skulle hända?
provision.bat install           # kör

# Linux / macOS
./provision.sh devices
./provision.sh install --dry-run
./provision.sh install
```

Paketet kan ligga var som helst — USB-sticka, hemkatalog, `C:\`. Alla
sökvägar löses relativt repots rot.

## Innehåll

```
atak-hv/
├── provision.py            verktyget
├── provision.toml          konfiguration — appar, filer, inställningar
├── provision.bat           startar verktyget på Windows
├── provision.sh            startar verktyget på Linux/macOS
├── platform-tools/         adb.exe för Windows (följer med)
├── payload/                det som hamnar på telefonen
│   ├── apks/               appar som sidladdas
│   ├── atak/               ATAK-konfiguration → /sdcard/atak
│   ├── ATAK-installation/  → /sdcard/ATAK-installation
│   └── VPN-clients/        era OpenVPN-klienter läggs här
└── docs/                   handhavande och instruktioner
```

## Krav

**På datorn:**

* **Python 3.11 eller senare.**
  Linux: `sudo apt install python3` (finns oftast redan).
  Windows: <https://www.python.org/downloads/> — kryssa i
  *"Add python.exe to PATH"*. Saknas Python skriver `provision.bat` ut var
  den hämtas; den kontrollerar även att versionen är tillräckligt ny.
* **`adb`** (Android Debug Bridge). Det är `adb` som gör själva jobbet —
  verktyget styr bara den.

  | System | Hämtas så här |
  |---|---|
  | **Windows** | **Följer med i repot**, `platform-tools/adb.exe`. Inget att installera. |
  | Linux | `sudo apt install adb android-sdk-platform-tools-common` — det andra paketet lägger in udev-reglerna som annars ger `no permissions`. Fedora: `sudo dnf install android-tools`. |
  | macOS | `brew install android-platform-tools` |

  `platform-tools/` i repot innehåller bara Windows-binärer. Kör verktyget
  utan `adb` så skrivs rätt kommando ut för ditt system.

**Utrustning:** en dator, samt USB C–C-kabel, USB A–C-kabel eller en
USB-hub. Flera telefoner kan anslutas samtidigt.

**På telefonen:** utvecklarläge och USB-felsökning aktiverat, skärmen
upplåst, och *File transfer (MTP)* vald om den frågar.

## Appar

**Installeras av användaren från Google Play, före körning:**

| App | Anmärkning |
|---|---|
| **ATAK** | **Måste installeras först.** ATAK-Sync är ett plugin, och konfigurationen som läggs ut kräver att ATAK redan finns på enheten. Verktyget installerar inte ATAK. |
| OpenVPN | Om ni använder OpenVPN |
| Geocam | |
| Reolink | Vid behov — om ni använder övervakningskameror, se [kamerainstruktionen](docs/atak-kamera-reolink-setup.md) |

**Sidladdas av verktyget** från `payload/apks/`:

`Ramsor.apk` · `HVreports.apk` · `Icu.apk` (TAK ICU) · `ATAK-Sync.apk`

## Före utskick

1. **Lägg in `atak-box.zip` för er TAK-server** i
   `payload/ATAK-installation/`. Filen måste heta exakt `atak-box.zip` och
   hämtas från er TAK-serveransvarige. Den innehåller serveradress och
   certifikat, distribueras separat och ingår inte i repot. Saknas den
   avbryts `install` direkt.
2. **Lägg era OpenVPN-klienter** i `payload/VPN-clients/`. Använder ni inte
   OpenVPN kan mappen lämnas tom — den läggs ut ändå.
3. **Kontrollera att `adb` finns** enligt [Krav](#krav).

## Använda verktyget

Exemplen visar Windows-varianten; på Linux/macOS byter du
`provision.bat` mot `./provision.sh`.

### Kommandon

```
provision.bat devices                Visa anslutna enheter och avsluta
provision.bat install                Installera appar och lägg ut konfiguration
provision.bat restore                Avinstallera appar, ta bort ATAK-filer
provision.bat restore --wipe-media   Som restore, plus radera användarens filer
```

**`install`** stänger av system- och appuppdateringar, installerar apparna i
`payload/apks/`, lägger ut `atak/`, `ATAK-installation/` och `VPN-clients/`
under `/sdcard/`, och placerar `atak-box.zip` i `/sdcard/Download/`.

**`restore`** gör tvärtom: avinstallerar ATAK-apparna, tar bort de utlagda
mapparna och slår på uppdateringarna igen. `--wipe-media` rensar dessutom
Download, DCIM, Pictures och Documents.

### Flaggor

| Flagga | Betydelse |
|---|---|
| `--dry-run` | Visar vad som skulle köras, ändrar ingenting |
| `--serial SERIAL` | Kör bara mot en enhet; kan upprepas |
| `-j N` | Provisionera N enheter parallellt (standard 1) |
| `--adb SÖKVÄG` | Använd en specifik `adb` |
| `--config FIL` | Använd en annan konfigurationsfil |
| `--log-dir KATALOG` | Loggar hamnar här (standard `logs/`) |
| `--wait SEK` | Hur länge verktyget väntar på enheter (standard 300) |
| `-y` | Fråga inte om bekräftelse |

**Prova alltid med `--dry-run` först**, och kör en enskild telefon med
`--serial` innan du kör en hel omgång:

```
provision.bat install --dry-run
provision.bat install --serial R58N1234ABC
```

### Bekräftelse

Verktyget listar anslutna enheter och frågar innan det gör något.
`restore --wipe-media` raderar användarens egna bilder och dokument och
kräver därför att man skriver `WIPE` — `y` räcker inte. Sökvägarna som
kommer att raderas listas före frågan.

`-y` hoppar över **alla** frågor, även `WIPE`. Använd den bara i skript där
du redan vet vad som kommer att hända.

### Loggar och felsökning

Varje enhet får en logg i `logs/<serienummer>.log` med alla adb-anrop och
deras utdata. Misslyckas något avslutar verktyget med felkod och
sammanfattningen visar vilket steg det gällde:

```
SUMMARY
  R58N1234ABC              FAILED: Install apps
```

| Symptom | Orsak |
|---|---|
| `unauthorized` | Godkänn USB-felsökning på telefonen |
| `offline` | Koppla ur och i kabeln |
| `no permissions` (Linux) | `sudo apt install android-sdk-platform-tools-common`, koppla sedan ur och i telefonen |
| `adb not found` | Se [Krav](#krav), eller använd `--adb` |
| `install` avbryts direkt | `atak-box.zip` eller en `.apk` saknas — se [Före utskick](#före-utskick) |

## Konfiguration

Allt som brukar behöva ändras ligger i `provision.toml`: vilka appar som
installeras, vilka mappar som läggs ut, vilka inställningar som sätts och
vilka paket som stängs av.

### Lägga till en ny telefonmodell

Uppdateringstjänster skiljer sig mellan tillverkare. Kärntjänsterna
(Google/AOSP) gäller alla enheter och ligger under `[packages] core`.
Tillverkarspecifika paket ligger under `[packages.vendor]`, med
tillverkarnamnet i gemener som nyckel.

Verktyget läser `ro.product.manufacturer` och tillämpar bara den post som
matchar. En okänd telefon får alltså kärntjänsterna och fungerar ändå.

Ta reda på vad som behövs för en ny modell:

```bash
adb shell getprop ro.product.manufacturer
adb shell pm list packages | grep -i -E 'update|ota|fota'
```

Lägg sedan till en rad:

```toml
[packages.vendor]
samsung  = ["com.wssyncmldm", "com.sec.android.soagent"]
xiaomi   = ["com.miui.updater"]
motorola = ["com.motorola.ccc.ota"]   # ny
```

Ingen kodändring krävs — bidra gärna med fler tillverkare.

## Avrustning och återlämning

Vid avrustning, när systemet ska lämnas in eller lämnas över:

1. Ladda telefonen.
2. Kör `provision.bat restore` (eller `--wipe-media` om användarens egna
   filer också ska bort).
3. Se [avrustning och grundinställning](docs/atak-avrustning-grundinstallning.md)
   för fabriksåterställning och packlista för TAK-väskan.

När du får en avrustad telefon, se
[uppstart efter återställd ATAK](docs/atak-uppstart-efter-aterstalld.md).

## Dokumentation

Handhavande och instruktioner finns i [docs/](docs/README.md) — bland annat
[ATAK-handboken](docs/atak-handbok.md) med menyer, kartor, navigation,
markörer, ritverktyg, rapportering, feeds och felsökning.

## Vad som inte ligger i git

| Vad | Varför | Var man får tag på det |
|---|---|---|
| `atak-box.zip` | Serveradress + certifikat, förbandsspecifikt | Från er TAK-serveransvarige |
| `VPN-clients/*.ovpn` | Enhetsspecifika hemligheter | Från er VPN-ansvarige |
| ATAK, OpenVPN, Geocam m.fl. `.apk` | Finns på Google Play | Google Play |
| `logs/` | Körloggar | Skapas vid körning |

## Att verifiera

* `payload/atak/` och `payload/ATAK-installation/atak/` är två nästan
  identiska träd (~11 MB vardera) som båda läggs ut på enheten. ATAK läser
  `/sdcard/atak`. Det nästlade trädet är sannolikt överflödigt, men
  användningen är inte verifierad — behålls tills vidare.
* Verktyget är utprovat mot en simulerad `adb`, inte mot riktiga telefoner.
  Kör `--dry-run` och en enskild enhet först.

## Licens

Skripten och dokumentationen saknar ännu licens. `.apk`-filer under
`payload/apks/` tillhör respektive upphovsman och omfattas av sina egna
villkor.

`platform-tools/` innehåller `adb` ur Android SDK Platform-Tools (revision
36.0.0), © Google LLC, huvudsakligen under Apache License 2.0. Fullständiga
licensvillkor och attributionsnoteringar följer med Googles egen
distribution:
<https://developer.android.com/tools/releases/platform-tools>
