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

## Före utskick

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

**`install`** stänger av system- och appuppdateringar, installerar apparna i
`payload/apks/`, beviljar ATAK:s rättigheter, lägger ut `atak/` och
`ATAK-installation/` under `/sdcard/`, och placerar `atak-box.zip` i
`/sdcard/Download/`.

### Testa på en egen telefon

Standardläget låser ner och rensar enheten. På ett utlämnat system är det
meningen, men på någons privata telefon är det inte det:

* system- och appuppdateringar stängs av — telefonen slutar få
  säkerhetsuppdateringar
* paketverifieraren stängs av
* tillverkarens uppdateringstjänster inaktiveras
* 25 Google-appar och tillverkarens appar inaktiveras, inklusive
  telefoni, kontakter och SMS
* bakgrundssynk, animationer och adaptiv batterihantering stängs av

Kör därför `install --no-optimize` när du provar verktyget på en telefon
som används privat. Appar och konfiguration installeras precis som vanligt,
men telefonens uppdateringsinställningar lämnas orörda.

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
igen. `--wipe-media` rensar dessutom
Download, DCIM, Pictures och Documents.

### Flaggor

| Flagga | Betydelse |
|---|---|
| `--callsign SIGNAL` | Endast `install`: anropssignal för enheten. Frågas efter om den utelämnas |
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
| `install` avbryts direkt | `atak-box.zip` eller en `.apk` saknas — se [Före utskick](#före-utskick) |

## Installera en enhet

Hela kedjan från kartong till färdig ATAK-telefon. Ska en avrustad telefon
startas igen, se
[Uppstart efter återställd ATAK](docs/avrustning.md#uppstart-efter-återställd-atak)
i stället.

### 1. Grundinställning av telefonen

Vissa steg saknas på en del modeller.

1. Starta telefonen. Sitter simkort i måste du ange PIN. Välj språk.
2. Anslut till wifi. Nätverk krävs för Google-inloggningen i nästa steg
   och för att hämta apparna ur Play Store.
3. Kopiera appar och data — **kopiera inte**.
4. Logga in med förbandets Google-konto. Kontot behövs för att hämta
   ATAK-CIV och plugin-apparna ur Play Store, och **ska stanna kvar på
   enheten** — det är därigenom apparna kan uppdateras längre fram.
   `install` stänger ändå av de automatiska uppdateringarna, så en
   uppdatering blir ett medvetet beslut och sker när ni väljer det.
5. Google-tjänster — bocka ur ”skicka diagnostik och användardata”,
   godkänn.
6. Välj webbläsare och sökmotor — Google.
7. Tillverkarens egna konton och tjänster — hoppa över. Bocka ur
   telemetri och diagnostik, och tacka nej till operatörens erbjudanden.
   Skärmarna ser olika ut för Samsung, Xiaomi, OnePlus och andra.
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
16. Öppna **Play Store** och installera **ATAK-CIV (Civil Use)** samt
    plugin-apparna **ATAK Plugin: Data Sync** och **ATAK Plugin: GeoCam**.
    Se [Appar](#appar) för länkar och paketnamn. ATAK-CIV **måste** finnas
    på plats innan nästa steg — utan den avbryts `install` direkt.
17. **Ljud och vibration** → aktivera vibration och/eller ljud vid behov.

Aviseringar behöver inte röras. Verktyget beviljar `POST_NOTIFICATIONS`
åt ATAK i nästa steg.

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
4. Verktyget listar de enheter det hittar, **frågar efter anropssignal**
   och ber om bekräftelse innan det gör något. Svara enligt FAL-A. Tryck
   Enter för att lämna signalen orörd, eller ange den i förväg med
   `--callsign`.

> [!IMPORTANT]
> Verktyget startar så snart **minst en** telefon är godkänd — det väntar
> inte in de övriga. Godkänn *Tillåt USB-felsökning* på **alla** telefoner
> innan du svarar på frågan, och kontrollera att antalet i listan stämmer.
> En telefon som inte hunnit godkännas varnas det för en gång, och blir
> sedan stående oprovisionerad.

Kör flera telefoner parallellt med `-j`, till exempel
`provision.bat install -j 4`. Loggen skrivs per serienummer, så
sammanfattningen visar ändå vilken telefon som gjorde vad.

Räkna med cirka 1,5 minut per telefon — 20 telefoner tar ungefär
30 minuter.

### 3. Avsluta på telefonen

1. Flytta ut ATAK-ikonen till första sidan på telefonen.
2. Backa till första sidan.

### 4. Starta ATAK första gången

1. Starta ATAK och tillåt de frågor som kommer upp. Rättigheterna och
   undantaget från batterioptimering är redan satta av verktyget, så det
   bör bli få eller inga frågor. Kommer ändå en ruta om batteri eller
   bakgrundskörning — godkänn den.
2. **TAK Device Setup** — *Done*.
3. Avvakta 5–7 sekunder. *Load Iconset* blinkar förbi på displayen.
4. Menyn i överkant fylls på med tre ikoner.
5. Stäng ner ATAK — ”Hamburgaren” → **Quit** → *Yes*.
6. Starta ATAK igen.
7. ”Hamburgaren” → **Import**.
8. **Local SD** — klicka ikonen till vänster under *S* i *Select Files to
   Import* — skrolla till **Download**.
9. Välj `atak-box.zip` (bocka i rutan till höger) — *OK*.
10. **Copy**.
11. Logga in — användarnamn och lösenord enligt lista.
12. *OK* — ”Tak server registration completed” — *OK*.

### 5. Callsign, teamfärg och Remarks

**Anropssignalen är redan satt** om du angav en i steg 2. Verktyget lägger
den i den preferensfil ATAK själv läser vid start
(`/sdcard/atak/config/prefs/defaults`), så den sitter första gången ATAK
startas — ingen handpåläggning. Kontrollera i självmarkörens ruta att det
står rätt signal.

Blev det fel, eller hoppade du över frågan, sätts den för hand enligt
[Callsign och teamfärg](docs/avrustning.md#callsign-och-teamfärg).

**Teamfärgen** kommer ur er `atak-box.zip`, som sätter `locationTeam`.
Ska en enhet ha en annan färg än paketets, ändra den för hand — se
[Färgsättning](docs/handbok.md#färgsättning) för färgschemat.

**Remarks** sätts fortfarande för hand. Se
[Uppstart och systemkonfiguration](docs/handbok.md#uppstart-och-systemkonfiguration).

### Stänga av telefonen

Beror på modell:

* Av-knapp + volym upp
* Av-knapp + volym ner
* På en del modeller kan knappen programmeras — sök på *sidoknapp* i
  telefonens inställningar.

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

Skripten och dokumentationen saknar ännu licens. `.apk`-filer under
`payload/apks/` tillhör respektive upphovsman och omfattas av sina egna
villkor.

`platform-tools/` innehåller `adb` ur Android SDK Platform-Tools (revision
36.0.0), © Google LLC, huvudsakligen under Apache License 2.0. Fullständiga
licensvillkor och attributionsnoteringar följer med Googles egen
distribution:
<https://developer.android.com/tools/releases/platform-tools>
