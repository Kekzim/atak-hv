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
4. Kör provisioneringen — se [docs/provisionering.md](docs/provisionering.md):

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

## Provisionering

`atak_provision.py` sköter installation och avrustning via `adb` och fungerar
på Windows, Linux och macOS. Se [docs/provisionering.md](docs/provisionering.md)
för kommandon, flaggor, loggar och hur man lägger till en ny telefonmodell.

De gamla `.bat`-skripten ligger kvar tills verktyget är utprovat på riktig
hårdvara, och tas bort därefter.

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
