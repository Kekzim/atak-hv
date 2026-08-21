# Läs mig — ATAK installation, avrustning och återlämning

Sammanslagen och uppdaterad version av de två tidigare `Läs mig .docx`-filerna
(en i repots rot, en i `ATAKautoinstall/`).

## Förutsättningar

* En dator med Windows
* USB C–C-kabel, USB A–C-kabel, eller en USB-hub (A eller C)
* Utvecklarläge och USB-felsökning aktiverat på telefonerna

## Appar som installeras från Google Play

Följande appar sidladdas **inte** längre av skriptet — de installeras från
Google Play innan `ATAK autoinstall.bat` körs:

| App | Anmärkning |
|---|---|
| **ATAK** | **Måste installeras först.** ATAK-Sync är ett plugin och den utpushade konfigurationen kräver att ATAK redan finns på enheten. |
| OpenVPN | Krävs om ni använder OpenVPN-klienter |
| Geocam | |
| Reolink | **Vid behov.** Installeras från Google Play om ni använder övervakningskameror — se [Kamera – Reolink setup](presentations/atak-kamera-reolink-setup.md). Ingår inte i utrustningspaketet. |
| Signal, FileManager | Ingår inte längre i utrustningspaketet. Kan installeras från Google Play vid behov. |

## Appar som sidladdas av skriptet

Dessa ligger i `ATAKautoinstall/Filer/` och installeras i tur och ordning:

1. `Ramsor.apk`
2. `HVreports.apk`
3. `Icu.apk` (TAK ICU)
4. `ATAK-Sync.apk`

## Innehåll i ATAKautoinstall

```
ATAKautoinstall/
├── ATAK autoinstall.bat        installerar appar och pushar konfiguration
├── ATAK-Restore.bat            avinstallerar appar
├── Restore + delete files.bat  avinstallerar appar och rensar filer
├── platform-tools/             adb.exe m.m. (hämtas från Google, se README)
└── Filer/
    ├── adb1.bat
    ├── *.apk                   apparna i listan ovan
    ├── atak/                   ATAK-konfiguration, pushas till /sdcard/atak
    ├── ATAK-installation/
    │   └── atak-box.zip        serverpaket — LÄGGS IN, se nedan
    └── VPN-clients/            era OpenVPN-klienter läggs här
```

## Före utskick

1. **Lägg in `atak-box.zip` för er TAK-server** i
   `Filer/ATAK-installation/`. Filen måste heta exakt `atak-box.zip`.
   Paketet innehåller serveradress och certifikat, distribueras separat och
   ingår medvetet inte i repot — du får hämta det från er
   TAK-serveransvarige. Saknas det avbryts installationen med ett
   felmeddelande.
2. **Lägg era OpenVPN-klienter i `Filer/VPN-clients/`.** Använder ni inte
   OpenVPN kan mappen lämnas tom — skriptet pushar den ändå.
3. Kopiera hela mappen `ATAKautoinstall` till `C:\` — skripten använder
   absoluta sökvägar under `C:\ATAKautoinstall\`.

## Installation

Läs presentationen [ATAK installation med VPN från dator](presentations/)
innan du kör skriptet. Kör därefter `C:\ATAKautoinstall\ATAK autoinstall.bat`
och följ checklistan som visas på skärmen.

## Avrustning

Vid avrustning, när systemet ska lämnas in: läs presentationen om ATAK
avrustning och grundinställning, och kör `ATAK-Restore.bat` eller
`Restore + delete files.bat`.

## Uppstart efter avrustning

När du fått en avrustad telefon: läs presentationen om ATAK-uppstart efter
återställd ATAK.
