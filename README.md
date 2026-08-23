# atak-hv

Utrustningspaket för **ATAK** (Android Team Awareness Kit) i Hemvärnet.
Repot innehåller verktyget som provisionerar telefoner via `adb`,
konfigurationen som läggs ut på enheterna, och instruktionsmaterialet.

> [!IMPORTANT]
> **Serverpaketet `atak-box.zip` ingår inte i repot.** Det innehåller
> TAK-serverns adress och certifikat och är förbandsspecifikt. Utan det
> avbryts installationen. Se [Före utskick](#före-installation-på-enhet).

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
│   └── ATAK-installation/  → /sdcard/ATAK-installation
│       └── atak/           ren reservkopia, se nedan
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

Namnen nedan är precis som de står i Play Store. Sök hellre på
paketnamnet eller följ länken — *ATAK* ensamt ger många träffar, och det
är bara `com.atakmap.app.civ` som avses.

| App i Play Store | Paketnamn | Anmärkning |
|---|---|---|
| **[ATAK-CIV (Civil Use)](https://play.google.com/store/apps/details?id=com.atakmap.app.civ)** | `com.atakmap.app.civ` | **Måste installeras först.** De andra två är plugin till den, och konfigurationen som läggs ut kräver att den redan finns på enheten. Verktyget installerar den inte. |
| **[ATAK Plugin: Data Sync](https://play.google.com/store/apps/details?id=com.atakmap.android.datasync.plugin)** | `com.atakmap.android.datasync.plugin` | Sidladdas inte längre — Play Store-versionen är signerad med en annan nyckel, så en telefon som redan har den därifrån kan inte uppdateras med paketets version. |
| [ATAK Plugin: GeoCam](https://play.google.com/store/apps/details?id=com.atakmap.android.geocam.plugin) | `com.atakmap.android.geocam.plugin` | |

**Sidladdas av verktyget** från `payload/apks/`:

`Ramsor.apk` · `HVreports.apk`

Verktyget **kontrollerar först att Play Store-apparna finns** och avbryter
om ATAK saknas — det är ingen idé att lägga ut konfiguration på en telefon
utan ATAK. Saknas någon av de övriga blir det en varning. Listan ligger
under `[requirements]` i `provision.toml`.

## Enhetsinställningar som verktyget sätter

ATAK har tre inställningar som måste stämma per telefon, och sju som måste
vara lika på alla. Verktyget lägger ut samtliga, så ingenting av det här
behöver knappas in på enheten.

Allt hamnar i den preferensfil ATAK själv läser vid start,
`/sdcard/atak/config/prefs/defaults`. ATAK tillämpar posterna och raderar
sedan filen. Listan ligger under `[prefs]` i `provision.toml`.

### Frågas efter vid installationen

Unika per telefon, så verktyget frågar efter dem när enheten listats —
före bekräftelsen, så att svaren står på skärmen som en del av det du
godkänner.

| Vad | Flagga | Innebörd |
|---|---|---|
| **Anropssignal** | `--callsign` | Enligt FAL-A. Skilj på personliga enheter (t.ex. `QS1`) och funktionsenheter (t.ex. `QS`) |
| **Remarks** | `--remarks` | Nivåtaggen högre staber filtrerar på: `#Bat`, `#Komp`, `#Plut`, `#Grp` |

Tryck Enter för att hoppa över en fråga — då lämnas telefonens nuvarande
värde orört. Med `-y` ställs inga frågor alls, och båda lämnas orörda om
du inte angett flaggorna.

**Teamfärg och roll sätts inte av verktyget.** Alternativen är många och
valet hänger på förband och befattning, så de väljs i ATAK efter första
uppstarten. Er `atak-box.zip` sätter ett utgångsvärde som sedan ändras på
enheten.

### Sätts alltid, lika på alla enheter

Handboken kallar dem *kritiska enhetsinställningar* — ”avvikelser skapar
kritiska fel vid eldledning”. De sätts vid varje `install`, även med `-y`
och även med `--no-optimize`.

| Inställning | Värde | Nyckel i `provision.toml` |
|---|---|---|
| Koordinatformat | MGRS | `coord_display_pref` |
| Höjdreferens | MSL (över havet) | `alt_display_pref` |
| Höjdenhet | meter | `alt_unit_pref` |
| Hastighet | km/h | `speed_unit_pref` |
| Kurs | numerisk | `compass_heading_display` |
| Bäring | streck (mils) | `rab_brg_units_pref` |
| Nordreferens | gitternord | `rab_north_ref_pref` |

Behöver ni andra värden ändrar ni dem under `[prefs.entries]`. Värdena
skrivs som strängar även när de ser ut som siffror — ATAK läser dem så,
och ett heltal får appen att kasta undantag.

### Kontrollera på enheten

Klicka på din egen markör och välj detaljer. Där står anropssignal,
**Remarks** och **Role**.

Koordinatrutan uppe till höger visar bäring och nordreferens, t.ex.
`551 milsG` — streck och gitternord.

> [!NOTE]
> **Självmarkörens ruta nere till höger visar alltid grader och `M`**,
> även när streck och gitternord är satta. Den widgeten skiljer bara på
> rättvisande nord och ”övrigt” och formaterar alltid i grader.
> Inställningarna är satta ändå. Använd rutan uppe till höger för att
> kontrollera just de två.

## Före installation på enhet

1. **Lägg in `atak-box.zip` för er TAK-server** i
   `payload/ATAK-installation/`. Filen måste heta exakt `atak-box.zip` och
   hämtas från er TAK-serveransvarige. Den innehåller serveradress och
   certifikat, distribueras separat och ingår inte i repot. Saknas den
   avbryts `install` direkt.
2. **Kontrollera att `adb` finns** enligt [Krav](#krav).

## Använda verktyget

Exemplen visar Windows-varianten; på Linux/macOS byter du
`provision.bat` mot `./provision.sh`.

### Kommandon

```
provision.bat devices                Visa anslutna enheter och avsluta
provision.bat install                Installera appar och lägg ut konfiguration
provision.bat install --no-optimize  Samma, men rör inte telefonens uppdateringar
provision.bat restore                Avinstallera appar, ta bort ATAK-filer
provision.bat restore --wipe-media   Som restore, plus radera användarens filer
```

**`install`** stänger av system-, appuppdateringar och bloatware, installerar apparna i
`payload/apks/`, beviljar ATAK:s rättigheter, lägger ut `atak/` och
`ATAK-installation/` under `/sdcard/`, och placerar `atak-box.zip` i
`/sdcard/Download/`.

### Testa på en egen telefon

Standardläget optimerar enheten för att vara dedikerad ATAK enhet.
På ett utlämnad enhet/privat dedikerad ATAK enhet är det meningen, 
men på någons privata primära telefon är det inte det:

* system- och appuppdateringar stängs av — telefonen slutar få
  säkerhetsuppdateringar
* paketverifieraren stängs av
* tillverkarens uppdateringstjänster inaktiveras
* 25 Google-appar och tillverkarens appar inaktiveras, inklusive
  telefoni, kontakter och SMS
* bakgrundssynk, animationer och adaptiv batterihantering stängs av

Kör därför `install --no-optimize` när du provar verktyget på en telefon
som används privat som primär telefon. Appar och konfiguration installeras
precis som vanligt, men telefonens uppdateringsinställningar lämnas orörda.

Ett undantag: paketverifieraren stängs av även då, eftersom Android annars
vägrar sidladdningen. Den sätts tillbaka som den var direkt efteråt — var
den aldrig satt från början tas nyckeln bort igen.

**Slå på utvecklarläge och USB-felsökning först.** Utan det syns telefonen
inte för `adb` över huvud taget, och verktyget står bara och väntar på en
enhet som aldrig dyker upp. Det är samma steg som för en utlämnad telefon,
och det måste göras på varje telefon en gång:

1. **Inställningar → Om telefonen**, leta upp **Version** och tryck på den
   sju gånger. På en del modeller heter den **Kompileringsnummer** och
   ligger under *Om telefonen → Programvaruinformation*. Telefonen räknar
   ner och svarar att du nu är utvecklare.
2. Backa ett steg, sök på *USB-fel* i inställningarna och slå på
   **USB-felsökning**.
3. Anslut kabeln. Välj **Filöverföring (MTP)** om telefonen frågar, och
   godkänn rutan *Tillåt USB-felsökning*. Bocka i *Tillåt alltid från den
   här datorn* så slipper du rutan nästa gång.

Kontrollera med `provision.bat devices` (`./provision.sh devices`) innan du
kör något annat. Står telefonen inte i listan är något av stegen ovan inte
gjort — se även [Loggar och felsökning](#loggar-och-felsökning).

> [!NOTE]
> Vissa tillverkare, bland andra Xiaomi, kräver dessutom att du godkänner
> en ruta **på telefonens skärm för varje app som sidladdas**. Missar du
> den avbryts steget med `INSTALL_FAILED_USER_RESTRICTED: Install canceled
> by user` — det är rutan som inte hann godkännas, inte ett fel i
> verktyget. Ha telefonen framför dig under körningen.

Verktyget skriver ut vilket läge det kör i och väntar på bekräftelse innan
det börjar, så du hinner avbryta om du valt fel.

Har du redan kört en full `install` på en privat telefon: `restore` slår på
uppdateringarna igen och avinstallerar ATAK-apparna.

**`restore`** gör tvärtom: avinstallerar ATAK-apparna, tar bort deras
undantag ur Doze, tar bort de utlagda mapparna och slår på uppdateringarna
igen. `--wipe-media` rensar dessutom Download, DCIM, Pictures och Documents.

### Flaggor

| Flagga | Betydelse |
|---|---|
| `--callsign SIGNAL` | Endast `install`: anropssignal för enheten. Frågas efter om den utelämnas |
| `--remarks TAGG` | Endast `install`: nivåtaggen i *Remarks*. Frågas efter om den utelämnas |
| `--no-optimize` | Endast `install`: hoppa över nedlåsningen, se nedan |
| `--dry-run` | Visar vad som skulle köras, ändrar ingenting. Själva adb-kommandona hamnar i loggen, inte på skärmen |
| `--serial SERIAL` | Kör bara mot en enhet; kan upprepas |
| `-j N` | Provisionera N enheter parallellt (standard 1) |
| `--adb SÖKVÄG` | Använd en specifik `adb` |
| `--config FIL` | Använd en annan konfigurationsfil |
| `--log-dir KATALOG` | Loggar hamnar här (standard `logs/`) |
| `--wait SEK` | Hur länge verktyget väntar på enheter (standard 300) |
| `-y` | Fråga inte om bekräftelse |
| `-q` | Skriv bara ut det nödvändiga |

**Prova alltid med `--dry-run` först**, och kör en enskild telefon med
`--serial` innan du kör en hel omgång:

```
provision.bat install --dry-run
provision.bat install --serial R58N1234ABC
```

Flaggorna går att kombinera. Ska ni prova på egna telefoner är det här
körningen som varken låser ner något eller ändrar något:

```
provision.bat install --dry-run --no-optimize
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
| `no authorized devices within ...` | Telefonen syns inte alls. Utvecklarläge och USB-felsökning påslagna? Se [Testa på en egen telefon](#testa-på-en-egen-telefon) |
| `unauthorized` | Godkänn USB-felsökning på telefonen |
| `offline` | Koppla ur och i kabeln |
| `INSTALL_FAILED_USER_RESTRICTED` | Rutan på telefonens skärm hann inte godkännas. Vanligt på Xiaomi — kör om med telefonen framför dig |
| `no permissions` (Linux) | `sudo apt install android-sdk-platform-tools-common`, koppla sedan ur och i telefonen |
| `adb not found` | Se [Krav](#krav), eller använd `--adb` |
| `install` avbryts direkt | `atak-box.zip` eller en `.apk` saknas — se [Före utskick](#före-installation-på-enhet) |

## Rättigheter

De sidladdade apparna får alla rättigheter direkt vid installationen
(`adb install -g`). **ATAK kommer från Google Play och får ingenting** —
därför beviljar verktyget ATAK:s rättigheter separat, i stället för att
lita på att operatören trycker rätt i varje dialogruta.

Det gäller plats, kamera, mikrofon, media, Bluetooth, wifi-upptäckt och
aviseringar, samt *All files access* (`MANAGE_EXTERNAL_STORAGE`) som krävs
för att komma åt `/sdcard/atak`. ATAK läggs också till i undantagslistan
för batterioptimering.

> [!IMPORTANT]
> Viktigast är **`ACCESS_BACKGROUND_LOCATION`**. Utan den rapporterar ATAK
> position bara när appen ligger i förgrunden — Blue Force Tracking slutar
> alltså fungera så fort skärmen släcks eller soldaten byter app. Den går
> **inte** att bevilja via de vanliga dialogrutorna; Android kräver ett
> separat besök i Inställningar. Det är precis vad verktyget gör åt dig.

Rättigheter som appen inte deklarerar, eller som inte finns i den
Android-versionen, hoppas över utan att räknas som fel. Listan ligger under
`[permissions]` i `provision.toml`.

Står det däremot ett paketnamn i `[permissions]`, `[appops]` eller
`[battery]` som inte finns på telefonen, varnar verktyget och namnger det i
sammanfattningen. Ett felstavat paketnamn ska inte kunna se ut som att allt
gick bra.

Detta steg körs **även med `--no-optimize`** — det handlar om att ATAK ska
fungera, inte om att låsa ner telefonen.

## Optimering

`install` låser ner enheten och tar bort det som inte hör hemma på ett
system vars enda uppgift är ATAK. Allt styrs från `provision.toml` och
allt återställs av `restore`.

| Vad | Varför |
|---|---|
| Uppdateringar av system och appar, paketverifierare | En oplanerad uppdatering får inte ändra beteende eller kräva omstart mitt i ett uppdrag |
| 25 Google-appar (mejl, video, assistent, plånbok, kalender, telefoni …) | Kör annars bakgrundstjänster, synk och uppdateringskontroller |
| Tillverkarens appar och telemetri | Samma sak — `[packages.vendor]`, matchas mot telefonens tillverkare |
| Bakgrundssynk (`master_sync`) | ATAK använder inte Androids synkramverk |
| Animationer | Kostar GPU och batteri för rent kosmetiska övergångar |
| Adaptiv batterihantering | Lägger CPU på att lära sig vilka appar som ska strypas — meningslöst när enheten kör en app |
| BLE-skanning för positionering | Android skannar efter beacons även med Bluetooth av |

Orörda med avsikt: `com.google.android.gms`, `com.google.android.gsf`,
Play Store och `com.android.location.fused` — de krävs för GPS, mobilnät,
wifi och framtida appinstallationer. Detsamma gäller tillverkarnas
OS-överlägg för tema, lagring och nätverk.

### Vad optimeringen inte rör

**Mobildata, wifi och Bluetooth fortsätter fungera.** Det är ett medvetet
krav:

* **Mobildata påverkas inte** av att telefoni-, kontakt- och SMS-apparna
  inaktiveras. Data bärs av telefoniramverket i systemet, inte av
  uppringningsappen. Enheten är en dataenhet — inga röstsamtal går till
  den — så de tre apparna stängs av. Ska era telefoner även användas för
  samtal, ta bort dem ur `debloat` i `provision.toml`.
* **Bluetooth-radion stängs inte av.**
  `payload/atak/tools/bluetooth/bluetooth_devices.xml` konfigurerar
  laseravståndsmätare (PLRF, MOSKITO, Vector21, TruePulse) och externa
  GNSS-mottagare (Bad Elf, Trimble R8/R10/R12). En avstängd radio slår ut
  dem. Använder ni inga sådana tillbehör kan `[commands]` i
  `provision.toml` slå av den ändå.
* **Wifi-skanning lämnas orörd**, eftersom wifi kan vara enhetens
  primära datalänk via delad uppkoppling.

Detsamma gäller `com.google.android.gms`, `com.google.android.gsf`, Play
Store, `com.android.location.fused` och tillverkarnas OS-överlägg för
tema, lagring och nätverk.

Efter installationen kontrollerar verktyget att ATAK är undantagen från
**Doze**. Är den inte det stryps positionsrapporteringen i bakgrunden, och
verktyget varnar i sammanfattningen. Inget ändras automatiskt.

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
oneplus  = ["cn.oneplus.photos", "com.oneplus.calculator", ...]
motorola = ["com.motorola.ccc.ota"]   # ny
```

Ingen kodändring krävs — bidra gärna med fler tillverkare.

## De två atak-mapparna

`payload/atak/` och `payload/ATAK-installation/atak/` innehåller samma
konfiguration, och båda läggs ut på telefonen. Det är avsiktligt:

* `/sdcard/atak/` är den **arbetskopia** ATAK läser och skriver i.
* `/sdcard/ATAK-installation/atak/` är en **ren reservkopia** som ligger
  kvar på telefonen. Vid ”Återställ ATAK” raderar soldaten arbetskopian
  och kopierar tillbaka reservkopian — utan dator, se
  [Avrustning och uppstart](docs/avrustning.md#återställ-atak).

Håll dem synkade. Läggs en ny kartdefinition till i `payload/atak/imagery/`
måste den in i reservkopian också, annars försvinner den vid nästa
återställning i fält.

## Dokumentation

Handhavande och instruktioner finns i [docs/](docs/README.md) — bland annat
[ATAK-handboken](docs/handbok.md) med menyer, kartor, navigation,
markörer, ritverktyg, rapportering, feeds och felsökning.

## Vad som inte ligger i git

| Vad | Varför | Var man får tag på det |
|---|---|---|
| `atak-box.zip` | Serveradress + certifikat, förbandsspecifikt | Från er TAK-serveransvarige |
| ATAK-CIV och de två plugin-apparna | Finns på Google Play | Google Play |
| `logs/` | Körloggar | Skapas vid körning |

## Att verifiera

Verktyget är utprovat mot riktiga telefoner: en Xiaomi 21051182G
(Android 13) och en OnePlus Nord N100 (Android 11) — med och utan
`--no-optimize`, samt en full `restore` med kontroll av att inställningar
och avstängda paket kommer tillbaka.

`restore --wipe-media` är **inte** utprovat. Det är också det enda
kommandot som raderar användarens egna filer.

Kör ändå `--dry-run` och en enskild enhet först på en modell ni inte
provisionerat förut — tillverkarnas paketlistor skiljer sig åt.

## Licens

Skripten och dokumentationen i det här repot står under **Apache License
2.0** — se [LICENSE](LICENSE). Det gäller `provision.py`, `provision.toml`,
launcherna, README och materialet under `docs/`.

Undantag, som har sina egna villkor och inte omfattas av licensen ovan:

* `.apk`-filerna under `payload/apks/` tillhör respektive upphovsman.
* ATAK-konfigurationen under `payload/atak/` och
  `payload/ATAK-installation/` innehåller kartkällor, KML-lager och
  datapaket från tredje part.
* `docs/instruktion-atak-hemvarn-0.9.pdf` är Hemvärnets eget
  instruktionsmaterial.

ATAK:s egen dokumentation (`ATAK_User_Guide.pdf`, `ATAK_Icon_Glossary.pdf`)
ingår **inte** i repot. ATAK lägger själv ut den under
`/sdcard/atak/support/docs/` när appen installeras eller uppdateras.

`platform-tools/` innehåller `adb` ur Android SDK Platform-Tools (revision
36.0.0), © Google LLC, huvudsakligen under Apache License 2.0. Fullständiga
licensvillkor och attributionsnoteringar följer med Googles egen
distribution:
<https://developer.android.com/tools/releases/platform-tools>
