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
| Reolink | Vid behov — om ni använder övervakningskameror, se [Video och kameror](docs/video-och-kameror.md) |

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

## Installera en enhet

Hela kedjan från kartong till färdig ATAK-telefon. Ska en avrustad telefon
startas igen, se
[Uppstart efter återställd ATAK](docs/avrustning.md#uppstart-efter-återställd-atak)
i stället.

### 1. Grundinställning av telefonen

Vissa steg saknas på en del modeller.

1. Starta telefonen. Sitter simkort i måste du ange PIN. Välj språk.
2. Wifi — hoppa över, fortsätt utan nätverk.
3. Kopiera appar och data — **kopiera inte**.
4. Hoppa över Google-inloggning.
5. Google-tjänster — bocka ur ”skicka diagnostik och användardata”,
   godkänn.
6. Välj webbläsare och sökmotor — Google.
7. Samsung-tjänster: glömt lösen → ange → *Nästa* → *Hoppa över* → bocka
   ur tre rutor → *Acceptera* → *Nästa* → bocka ur Telia → *Nästa*.
8. Skapa PIN: fyra siffror, framtagen av chef.
9. Granska fler appar — bocka ur om du tillfrågas.
10. Fingeravtryck — **nej tack**.
11. Ansiktsregistrering — **nej tack**.
12. Inställningar → sök *SIM* → ta bort simkortslås.
13. Inställningar → **Om telefonen** → hitta **Version** och tryck sju
    gånger för att aktivera utvecklaralternativ. På vissa modeller ligger
    det under *Om telefonen → Programvaruinformation →
    Kompileringsnummer*.
14. Backa ett steg, sök *USB-fel* och aktivera **USB-felsökning**.
15. Backa ett steg.
16. **Aviseringar** → **App-aviseringar** → tillåt ATAK.
17. Backa ett steg → **Ljud och vibration** → aktivera vibration
    och/eller ljud vid behov.

### 2. Provisionering från datorn

1. Koppla in telefonen eller telefonerna mot datorn med USB.
2. Ska USB-felsökning godkännas — godkänn. Om rutan inte kommer, aktivera
   filöverföring genom att dra nedåt i fönstret och välja
   *USB… → Överför filer*.
3. Kör provisioneringen från datorn:

   ```
   Windows:      provision.bat install
   Linux/macOS:  ./provision.sh install
   ```

   Se [Använda verktyget](#använda-verktyget) för kommandon och
   flaggor.
4. Verktyget känner av antalet anslutna enheter och avvaktar tills alla
   godkänt USB-felsökning.

Räkna med cirka 1,5 minut per telefon — 20 telefoner tar ungefär
30 minuter.

### 3. OpenVPN

Hoppa över om ni inte använder VPN.

> [!NOTE]
> **OpenVPN installeras från Google Play** — den sidladdas inte av
> verktyget. Installera den på telefonen innan du fortsätter här.

1. Starta **OpenVPN** → *Agree*.
2. Välj **Upload File**.
3. *Browse* → filhanteraren → **Main Storage** → `VPN-clients`.
4. Välj rätt `.ovpn`-fil. Administratören har den i
   `OpenVPN-server-Readme.txt`.
5. **Import** → *OK*.
6. Lösenord enligt lista från administratören.

### 4. Avsluta på telefonen

1. Flytta ut ATAK-ikonen till första sidan på telefonen.
2. Backa till första sidan.

### 5. Starta ATAK första gången

1. Starta ATAK och tillåt alla frågor som kommer upp.
2. **TAK Device Setup** — *Done*.
3. *Disable battery…* — *OK*.
4. Tillåt appen att köras i bakgrunden — *Tillåt*.
5. Avvakta 5–7 sekunder. *Load Iconset* blinkar förbi på displayen.
6. Menyn i överkant fylls på med tre ikoner.
7. Stäng ner ATAK — ”Hamburgaren” → **Quit** → *Yes*.
8. Starta ATAK igen.
9. ”Hamburgaren” → **Import**.
10. **Local SD** — klicka ikonen till vänster under *S* i *Select Files to
    Import* — skrolla till **Download**.
11. Välj `xxxxxx.zip` (bocka i rutan till höger) — *OK*.
12. **Copy**.
13. Logga in — användarnamn och lösenord enligt lista.
14. *OK* — ”Tak server registration completed” — *OK*.

### 6. Callsign och teamfärg

Görs vid nästa uppstart. Proceduren är densamma som efter en avrustning —
se [Callsign och teamfärg](docs/avrustning.md#callsign-och-teamfärg), och
[Färgsättning](docs/handbok.md#färgsättning) för färgschemat.

Sätt även **Remarks** till rätt hashtag, se
[Uppstart och systemkonfiguration](docs/handbok.md#uppstart-och-systemkonfiguration).

### Stänga av telefonen

Beror på modell:

* Av-knapp + volym upp
* Av-knapp + volym ner
* På en del modeller kan knappen programmeras — sök på *sidoknapp* i
  telefonens inställningar.

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
3. Se [Avrustning och uppstart](docs/avrustning.md) för återställning av
   ATAK, fabriksåterställning och packlista för TAK-väskan.

När du får en avrustad telefon, se
[uppstart efter återställd ATAK](docs/avrustning.md#uppstart-efter-återställd-atak).

## Dokumentation

Handhavande och instruktioner finns i [docs/](docs/README.md) — bland annat
[ATAK-handboken](docs/handbok.md) med menyer, kartor, navigation,
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
