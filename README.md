# atak-hv

Utrustnings- och utbildningspaket för **ATAK** (Android Team Awareness Kit)
i Hemvärnet. Repot innehåller installationsskripten som provisionerar
telefoner via `adb`, ATAK-konfigurationen som pushas till enheterna, och
utbildningsmaterialet i Markdown-form.

> [!IMPORTANT]
> **Serverpaketet `atak-box.zip` ligger medvetet inte i det här repot.**
> Det innehåller TAK-serveradress och certifikat och är förbandsspecifikt.
> Se [Före utskick](#före-utskick).

## Innehåll

```
atak-hv/
├── ATAKautoinstall/              provisioneringspaket, kan ligga var som helst
│   ├── atak_provision.py         verktyget (Windows, Linux, macOS)
│   ├── atak-provision.toml       konfiguration — appar, pushar, paket
│   ├── atak-provision.bat        startar verktyget på Windows
│   ├── atak-provision.sh         startar verktyget på Linux/macOS
│   ├── ATAK autoinstall.bat      GAMMAL, ersätts av verktyget ovan
│   ├── ATAK-Restore.bat          GAMMAL
│   ├── Restore + delete files.bat  GAMMAL
│   ├── platform-tools/           adb.exe för Windows (följer med)
│   └── Filer/
│       ├── *.apk                 apparna som sidladdas
│       ├── atak/                 ATAK-konfiguration → /sdcard/atak
│       ├── ATAK-installation/    → /sdcard/ATAK-installation
│       └── VPN-clients/          era OpenVPN-klienter läggs här
└── docs/
    ├── las-mig.md                installation, avrustning, återlämning
    ├── presentations/            handhavande och instruktioner (Markdown)
    ├── instruktion-atak-hemvarn-0.9.pdf
    └── mall-vaska-a6.pdf
```

## Kom igång

1. Läs [docs/las-mig.md](docs/las-mig.md).
2. Läs [ATAK installation med VPN från dator](docs/presentations/atak-installation-med-vpn-fran-dator.md).
   För handhavande, se [ATAK-handbok](docs/presentations/atak-handbok.md).
3. Följ [Före utskick](#före-utskick) nedan.
4. Kör provisioneringen — se [Använda verktyget](#använda-verktyget):

   ```
   Windows:      atak-provision.bat install
   Linux/macOS:  ./atak-provision.sh install
   ```

Paketet kan ligga var som helst; sökvägarna löses relativt konfigurationen.
Kräver Python 3.11+. `adb` följer med för Windows; på Linux/macOS
installeras den med pakethanteraren — se [Före utskick](#före-utskick).

## Appar

**Installeras av användaren från Google Play, före körning:**

| App | Anmärkning |
|---|---|
| **ATAK** | **Måste installeras först.** ATAK-Sync är ett plugin, och konfigurationen som pushas kräver att ATAK redan finns på enheten. Skriptet installerar inte ATAK. |
| OpenVPN | Om ni använder OpenVPN |
| Geocam | |
| Reolink | **Vid behov** — installeras från Google Play om ni använder övervakningskameror. Se [Kamera – Reolink setup](docs/presentations/atak-kamera-reolink-setup.md). Ingår inte i utrustningspaketet. |

**Sidladdas av `ATAK autoinstall.bat`** (ligger i `ATAKautoinstall/Filer/`):

`Ramsor.apk` · `HVreports.apk` · `Icu.apk` (TAK ICU) · `ATAK-Sync.apk`

## Före utskick

1. **Lägg in ert eget `atak-box.zip`** i
   `ATAKautoinstall/Filer/ATAK-installation/`. Filen måste heta exakt
   `atak-box.zip`. Den innehåller serveradress och certifikat för *er*
   TAK-server och distribueras utanför repot.
2. **Lägg era OpenVPN-klienter** i `ATAKautoinstall/Filer/VPN-clients/`.
   Använder ni inte OpenVPN kan mappen lämnas tom.
3. **Se till att `adb` finns.** På Windows följer den med i repot
   (`ATAKautoinstall/platform-tools/adb.exe`) — inget att göra. På Linux:
   `sudo apt install adb android-sdk-platform-tools-common`. macOS:
   `brew install android-platform-tools`. Verktyget skriver ut rätt
   kommando för ditt system om `adb` saknas.

## Vad som inte ligger i git

| Vad | Varför | Var man får tag på det |
|---|---|---|
| `atak-box.zip` | Serveradress + certifikat, förbandsspecifikt | Från er TAK-serveransvarige |
| `VPN-clients/*.ovpn` | Enhetsspecifika hemligheter | Från er VPN-ansvarige |
| ATAK, OpenVPN, Geocam m.fl. `.apk` | Finns på Google Play | Google Play |
| `_source/` | Original i `.pptx`/`.docx`/`.pdf`, ersatta av Markdown | Lokalt i arbetskopian |

## Använda verktyget

`atak_provision.py` sköter installation och avrustning via `adb`, på Windows,
Linux och macOS. Kör det via en av startfilerna i `ATAKautoinstall/`:

| System | Så här |
|---|---|
| Windows | Dubbelklicka `atak-provision.bat` för en installation, eller kör `atak-provision.bat <kommando>` från kommandotolken |
| Linux / macOS | `./atak-provision.sh <kommando>` |

Exemplen nedan visar Windows-varianten; på Linux byter du bara
`atak-provision.bat` mot `./atak-provision.sh`.

### Kommandon

```
atak-provision.bat devices                Visa anslutna enheter och avsluta
atak-provision.bat install                Installera appar och pusha konfiguration
atak-provision.bat restore                Avinstallera appar, ta bort ATAK-filer
atak-provision.bat restore --wipe-media   Som restore, plus radera användarens filer
```

`install` stänger av system- och appuppdateringar, installerar apparna i
`Filer/`, pushar `atak/`, `ATAK-installation/` och `VPN-clients/` till
`/sdcard/`, och lägger `atak-box.zip` i `/sdcard/Download/`.

> [!NOTE]
> `atak-box.zip` ingår inte i repot — se [Före utskick](#före-utskick). Utan
> den avbryter `install` direkt med ett felmeddelande; enheterna får annars
> ingen kontakt med TAK-servern.

`restore` gör tvärtom: avinstallerar ATAK-apparna, tar bort de utpushade
mapparna och slår på uppdateringarna igen. `--wipe-media` rensar dessutom
Download, DCIM, Pictures och Documents.

### Vanliga flaggor

| Flagga | Betydelse |
|---|---|
| `--dry-run` | Visar vad som skulle köras, ändrar ingenting |
| `--serial SERIAL` | Kör bara mot en enhet; kan upprepas |
| `-j N` | Provisionera N enheter parallellt (standard 1) |
| `--adb SÖKVÄG` | Använd en specifik `adb` |
| `-y` | Fråga inte om bekräftelse |

**Prova alltid med `--dry-run` först**, och kör en enskild telefon med
`--serial` innan du kör en hel omgång:

```
atak-provision.bat install --dry-run
atak-provision.bat install --serial R58N1234ABC
```

### Bekräftelse

Verktyget listar anslutna enheter och frågar innan det gör något.
`restore --wipe-media` raderar användarens egna bilder och dokument och
kräver därför att man skriver `WIPE` — `y` räcker inte. `-y` hoppar över
alla frågor, även den.

### Om något går fel

Varje enhet får en logg i `ATAKautoinstall/logs/<serienummer>.log` med alla
adb-anrop. Misslyckas något avslutar verktyget med felkod och
sammanfattningen visar vilket steg det gällde:

```
SUMMARY
  R58N1234ABC              FAILED: Install apps
```

Fullständig beskrivning — alla flaggor, felsökningstabell och hur man lägger
till en ny telefonmodell — finns i
[docs/provisionering.md](docs/provisionering.md).

De gamla `.bat`-skripten (`ATAK autoinstall.bat` med flera) ligger kvar tills
verktyget är utprovat på riktig hårdvara, och tas bort därefter.

## Instruktioner

Se [docs/presentations/](docs/presentations/README.md) — handhavande,
installation, avrustning, streaming och felsökning. Dokumenten kan läsas
direkt på GitHub eller visas som bildspel med `viewer.html`.

Rent kursmaterial (agenda, mål, metodik och övningsuppgifter) ingår inte;
originalen ligger kvar lokalt i `_source/`.

## Att verifiera

* `Filer/atak/` och `Filer/ATAK-installation/atak/` är två nästan identiska
  träd (~11 MB vardera) som båda pushas till enheten av
  `ATAK autoinstall.bat`. ATAK läser `/sdcard/atak`, och `Läs mig` beskriver
  bara `atak-box.zip` under `ATAK-installation`. Det nästlade trädet är
  sannolikt överflödigt, men användningen är inte verifierad — behålls tills
  vidare.

## Licens

Skripten och dokumentationen i det här repot saknar ännu licens. `.apk`-filer
under `ATAKautoinstall/Filer/` tillhör respektive upphovsman och omfattas av
sina egna villkor.

`ATAKautoinstall/platform-tools/` innehåller `adb` ur Android SDK
Platform-Tools (revision 36.0.0), © Google LLC, huvudsakligen under Apache
License 2.0. Fullständiga licensvillkor och attributionsnoteringar
(`NOTICE.txt`) följer med Googles egen distribution:
<https://developer.android.com/tools/releases/platform-tools>
