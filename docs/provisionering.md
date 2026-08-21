# Provisionering av enheter

`atak_provision.py` installerar appar och konfiguration på ATAK-telefoner via
`adb`. Verktyget ersätter de tidigare `.bat`-skripten och fungerar på Windows,
Linux och macOS.

## Krav

* **Python 3.11 eller senare.**
  Linux: `sudo apt install python3` (finns oftast redan).
  Windows: <https://www.python.org/downloads/> — kryssa i
  *"Add python.exe to PATH"* i installationsprogrammet.
* **Android SDK Platform-Tools** (`adb`). Verktyget letar först i
  `ATAKautoinstall/platform-tools/`, sedan i `PATH`. Peka annars ut den med
  `--adb`.
* Utvecklarläge och USB-felsökning aktiverat på telefonerna.

Paketet kan ligga var som helst — USB-sticka, hemkatalog, `C:\`. Alla
sökvägar löses relativt konfigurationsfilen.

## Användning

Windows — dubbelklicka `atak-provision.bat` för en installation, eller kör
från kommandotolken:

```
atak-provision.bat devices
atak-provision.bat install
atak-provision.bat restore
```

Linux och macOS:

```bash
./atak-provision.sh devices
./atak-provision.sh install
./atak-provision.sh restore
```

### Kommandon

| Kommando | Gör |
|---|---|
| `devices` | Listar anslutna enheter och avslutar |
| `install` | Stänger av uppdateringar, installerar appar, pushar konfiguration |
| `restore` | Avinstallerar appar, tar bort ATAK-filer, slår på uppdateringar igen |
| `restore --wipe-media` | Som `restore`, plus rensar Download, DCIM, Pictures och Documents |

### Flaggor

| Flagga | Betydelse |
|---|---|
| `--dry-run` | Visar vad som skulle köras utan att ändra något |
| `--serial SERIAL` | Kör bara mot en enhet; kan upprepas |
| `-j N` | Provisionerar N enheter parallellt (standard 1) |
| `--adb SÖKVÄG` | Använd en specifik `adb` |
| `--config FIL` | Använd en annan konfigurationsfil |
| `--log-dir KATALOG` | Loggar hamnar här (standard `logs/`) |
| `-y` | Fråga inte om bekräftelse |

Kör alltid `--dry-run` först om du är osäker.

## Innan du kör `install`

1. **ATAK måste vara installerat från Google Play på alla enheter.**
   ATAK-Sync är ett plugin och konfigurationen som pushas förutsätter ATAK.
   Verktyget installerar inte ATAK.
2. Installera OpenVPN och Geocam från Google Play (Reolink vid behov).
3. Lägg in rätt `atak-box.zip` för er TAK-server i
   `ATAKautoinstall/Filer/ATAK-installation/`. Saknas den avbryts körningen.
4. Lägg era OpenVPN-klienter i `ATAKautoinstall/Filer/VPN-clients/`.

## Loggar och felsökning

Varje enhet får en egen logg i `logs/<serienummer>.log` med alla adb-anrop
och deras utdata. Verktyget avslutar med felkod om någon enhet misslyckades,
och sammanfattningen visar vilket steg det gällde.

Vanliga fall:

| Symptom | Orsak |
|---|---|
| `unauthorized` | Godkänn USB-felsökning på telefonen |
| `offline` | Koppla ur och i kabeln |
| `no permissions` (Linux) | udev-regler saknas för telefonen |
| `adb not found` | Se Krav ovan, eller använd `--adb` |

## Konfiguration

Allt som kan behöva ändras ligger i `ATAKautoinstall/atak-provision.toml`:
vilka appar som installeras, vilka mappar som pushas, vilka inställningar
som sätts och vilka paket som stängs av.

### Lägga till en ny telefonmodell

Uppdateringstjänster skiljer sig mellan tillverkare. Kärntjänsterna
(Google/AOSP) gäller alla enheter och ligger under `[packages] core`.
Tillverkarspecifika paket ligger under `[packages.vendor]`, med
tillverkarnamnet i gemener som nyckel.

Verktyget läser `ro.product.manufacturer` och tillämpar bara den post som
matchar. En okänd telefon får alltså kärntjänsterna och fungerar ändå.

Så här tar du reda på vad som ska läggas till för en ny modell:

```bash
adb shell getprop ro.product.manufacturer
adb shell pm list packages | grep -i -E 'update|ota|fota'
```

Lägg sedan till en rad i konfigurationen:

```toml
[packages.vendor]
samsung = ["com.wssyncmldm", "com.sec.android.soagent"]
xiaomi  = ["com.miui.updater"]
motorola = ["com.motorola.ccc.ota"]   # ny
```

Det krävs ingen kodändring — bidra gärna med fler tillverkare.
