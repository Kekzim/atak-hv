# Bloatware-genomgång: Huawei

Genomgången är gjord på en **Huawei P20 Lite (ANE-LX1)**, Android 9,
EMUI 9.1.0 — en enhet från tiden före sanktionerna, så den har Google
Play-tjänster och den gemensamma `debloat`-listan biter på den.

> [!WARNING]
> **Ingenting här är provkört.** Listan är klassad utifrån paketnamn,
> `codePath` och vad som körde på enheten. Det finns ingen `huawei`-nyckel
> i `[packages.vendor]`, och den ska inte läggas in förrän listan körts
> skarpt på en Huawei. Se [Läs det här först](#läs-det-här-först).

## Vad verktyget gör på en Huawei idag

Eftersom `[packages.vendor]` saknar `huawei` faller `task_packages`
tillbaka på de gemensamma listorna och loggar
`no vendor entry for 'huawei' - common lists only`. **Inget
Huawei-paket rörs.** På provenheten stängdes 16 paket av, samtliga
`com.google.android.*`.

`com.google.android.webview` och `com.google.android.apps.work.oobconfig`
låg redan avstängda från fabrik — inte verktygets verk. WebView levereras
av `com.android.chrome`, så ingenting saknas.

## Läs det här först

### Konto och stöldskydd — samma kategori som Knox Guard

`com.huawei.hwid` (med `.core`, `.persistent`, `.container2`,
`.container3`) är Huawei-ID och bär Find My Phone. Fyra av dess processer
kör samtidigt. Att stänga av den på en telefon som är knuten till ett
Huawei-konto är samma sorts misstag som `com.samsung.android.kgclient` var
på en Knox Guard-ansluten SM-A405FN: agenten läses som manipulerad och
enheten kan låsa sig.

Samma resonemang gäller autentisering och säkerhet:
`com.huawei.hwasm` (`/product/app/HwFidoAsm`, FIDO),
`com.huawei.behaviorauth`, `com.huawei.trustagent`,
`com.huawei.trustcircle`, `com.huawei.securitymgr`.

### Tangentbordet — enheten har inget annat

`com.touchtype.swiftkey` är **enda aktiverade** inmatningsmetod och
standardval; `com.swiftkey.swiftkeyconfigurator` hör till den. Det finns
ingen Huawei-IME som reserv. Stängs den av går det inte att skriva in
PIN-koden.

### Position — ATAK står och faller med den

`com.huawei.lbs` (kör), `com.huawei.msdp`, `com.huawei.motionservice`.
GNSS-demonerna `gnss_engine_hisi` och `gnss_supl20clientd_hisi` finns, så
A-GPS är på plats.

### Kamera, skal och systemramverk

`com.huawei.camera` (GeoCam-pluginet behöver den),
`com.huawei.android.launcher`, `com.huawei.hidisk`,
`com.huawei.systemserver`, `com.huawei.iaware` (HwIAware,
resursschemaläggning), `com.huawei.nb.service` (HwNaturalBase — flera
systemdelar läser ur den), `com.huawei.featurelayer.featureframework`,
`com.huawei.featurelayer.sharedfeature.map`,
`com.huawei.android.internal.app`, `com.hisi.mapcon`.

### Strömhantering

`com.huawei.systemmanager` och `com.huawei.powergenie` — se
[PowerGenie](#powergenie-är-det-som-faktiskt-hotar-atak).

## Steg 1 — tredjepartspreloads

```
com.facebook.appmanager
com.facebook.services
com.facebook.system
com.ebay.carrier
com.netflix.partner.activation
```

Facebook-paketen är stubbar som installerar och uppdaterar Facebook-appar
i bakgrunden även om Facebook aldrig används.

## Steg 1 — butik, media och konsumentappar

| Paket | Anmärkning |
|---|---|
| `com.huawei.appmarket` | AppGallery — körde |
| `com.huawei.himovie.overseas` | Huawei Video |
| `com.huawei.health` | körde |
| `com.huawei.gameassistant` | körde |
| `com.huawei.vassistant` | röstassistent |
| `com.huawei.android.totemweather` | väder — körde |
| `com.huawei.android.thememanager` | teman — körde |
| `com.huawei.android.tips`, `com.huawei.tips` | tips — körde |
| `com.huawei.android.FMRadio` | |
| `com.huawei.compass` | |
| `com.huawei.scanner` | HiVision |
| `com.huawei.hitouch` | |
| `com.huawei.intelligent` | HiBoard/assistentskärmen — körde |
| `com.huawei.search` | körde |
| `com.huawei.recsys` | rekommendationer och reklam — körde |
| `com.huawei.hicard` | körde |
| `com.huawei.hifolder` | mapprekommendationer |
| `com.huawei.videoeditor` | |
| `com.huawei.screenrecorder` | |
| `com.huawei.printservice` | |
| `com.huawei.numberidentity` | körde |
| `com.huawei.contactscamcard` | visitkortsläsning |
| `com.huawei.parentcontrol` | |
| `com.huawei.pcassistant` | HiSuite |
| `com.huawei.phoneservice` | supportappen — körde |
| `com.example.android.notepad` | Huaweis anteckningar, paketet heter faktiskt så |

## Steg 1 — telemetri, uppdatering och diagnostik

```
com.huawei.android.chr              # Huawei-telemetri
com.huawei.hiview                   # körde
com.huawei.hiviewtunnel             # körde
com.huawei.hwdetectrepair           # körde
com.huawei.android.hwouc            # OTA-klient
com.huawei.android.hwupgradeguide
com.huawei.autoinstallapkfrommcc    # installerar operatörsappar på egen hand
com.huawei.KoBackup
```

## Steg 2 — delning och spegling

```
com.huawei.android.instantonline
com.huawei.android.instantshare
com.huawei.android.mirrorshare
com.android.hwmirror
com.huawei.android.wfdft
com.huawei.HwMultiScreenShot
com.huawei.nearby
com.huawei.synergy
com.huawei.iconnect
com.huawei.android.FloatTasks
```

## Steg 2 — AI, språk och ljud

```
com.huawei.hiaction                 # körde
com.huawei.hiai                     # körde
com.huawei.languagedownloader
com.huawei.imedia.sws
```

## Steg 2 — fabriks- och operatörsverktyg

```
com.huawei.android.projectmenu      # ingenjörsmeny
com.huawei.mmitest                  # fabrikstest
com.huawei.omacp                    # OMA client provisioning
com.huawei.rcsserviceapplication
com.huawei.wifiprobqeservice
com.huawei.android.dsdscardmanager  # dubbelt SIM — körde
```

## Att titta närmare på — medvetet oklassat

| Paket | Varför det står här |
|---|---|
| `com.huawei.hicloud` | Huawei Cloud. Ligger nära `hwid` och Find My Phone, så den hålls utanför steg 1 med flit |
| `com.huawei.android.hsf` | Huawei Service Framework, ligger i `/data/app`. Push-infrastruktur |
| `com.huawei.android.pushagent` | körde. Aviseringar går via den |
| `com.huawei.android.hwaps` | HwAps, delar system-UID |

**Användarinstallerade appar hör inte hemma i en debloat-lista.** På
provenheten fanns `com.magicwach.rdefense` — installerad ur Play Store
(`installerPackageName=com.android.vending`), utan `INTERNET`-behörighet,
med `.TitleActivity` som ingång. Det är ett spel som någon valt själv, inte
bloatware. Kontrollera `installerPackageName` innan ett paket förs upp på
listan.

## PowerGenie är det som faktiskt hotar ATAK

Debloat är inte problemet på den här plattformen. EMUI stänger av
bakgrundsappar på egen hand, oberoende av det Doze-undantag verktyget
sätter. `com.huawei.powergenie` och `com.huawei.systemmanager` kör båda.

ATAK måste ställas in **för hand på varje telefon**:

> Telefonhanteraren → Appstart → ATAK → **Hantera manuellt**, med alla tre
> reglagen på: starta automatiskt, sekundär start och kör i bakgrunden.

Utan det slutar ATAK rapportera position när skärmen släcks, och Blue
Force Tracking dör tyst. Det går inte att sätta över `adb` på EMUI 9 och
finns därför inte i `provision.toml`.

## Om provenheten

Telefonen såg inga wifi-nät under genomgången. Drivrutinen slutförde varje
sökning och lämnade tomt resultat till `wpa_supplicant`, 32 gånger i rad,
genom omstart, radiocykel, återställning av nätverksinställningar och
manuellt tillagt nät.

**Det var inget hårdvarufel.** Enda accesspunkten inom räckhåll sände på
5805 MHz — kanal 161 i UNII-3-bandet (5725–5875 MHz), som är en
amerikansk tilldelning. Telefonen skickade landskoden `SE` till
drivrutinen, och en enhet som följer den regulatoriska domänen varken
söker eller ansluter på den kanalen. Sökningarna returnerade alltså
ingenting därför att det inte fanns något telefonen *fick* se. Samma
telefon ansluter utan problem till ett 2,4 GHz-nät.

Lärdomen är att en Samsung i samma rum inte duger som kontroll: den såg
nätet på −43 dBm, men olika kretsar hanterar UNII-3 olika, så jämförelsen
sade ingenting om Huawei-enheten. Kontrollera kanalen innan tomma
sökresultat tolkas som trasig radio.

Telefonen saknade SIM, så wifi var dess enda nätverksväg.

Listan ovan är ändå inte provkörd — den behöver köras skarpt innan den
förs in i `provision.toml`.
