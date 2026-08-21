# Installation av enhet från dator

Nyinstallation av telefon eller platta. Ska en avrustad telefon startas
igen, se [Avrustning och uppstart](avrustning.md#uppstart-efter-återställd-atak)
i stället.

![Översikt](assets/installation/sida01-01.png)

## Appar som måste installeras från Google Play

Verktyget sidladdar bara Ramsor, HVreports, TAK ICU och ATAK-Sync.
Följande installeras av användaren på telefonen:

| App | När |
|---|---|
| **ATAK** | **Alltid, och först av allt.** ATAK-Sync är ett plugin och konfigurationen förutsätter att ATAK finns på plats. |
| **OpenVPN** | Om ni använder VPN — se [steg 3](#3-openvpn) |
| **Reolink** | Om ni använder övervakningskameror — se [Video och kameror](video-och-kameror.md#reolink-kameror) |

## 1. Grundinställning av telefonen

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

## 2. Provisionering från datorn

1. Koppla in telefonen eller telefonerna mot datorn med USB.
2. Ska USB-felsökning godkännas — godkänn. Om rutan inte kommer, aktivera
   filöverföring genom att dra nedåt i fönstret och välja
   *USB… → Överför filer*.
3. Kör provisioneringen från datorn:

   ```
   Windows:      provision.bat install
   Linux/macOS:  ./provision.sh install
   ```

   Se [repots README](../README.md#använda-verktyget) för kommandon och
   flaggor.
4. Verktyget känner av antalet anslutna enheter och avvaktar tills alla
   godkänt USB-felsökning.

Räkna med cirka 1,5 minut per telefon — 20 telefoner tar ungefär
30 minuter.

## 3. OpenVPN

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

## 4. Avsluta på telefonen

1. Flytta ut ATAK-ikonen till första sidan på telefonen.
2. Backa till första sidan.

## 5. Starta ATAK första gången

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

## 6. Callsign och teamfärg

Görs vid nästa uppstart. Proceduren är densamma som efter en avrustning —
se [Callsign och teamfärg](avrustning.md#callsign-och-teamfärg), och
[Färgsättning](handbok.md#färgsättning) för färgschemat.

Sätt även **Remarks** till rätt hashtag, se
[Uppstart och systemkonfiguration](handbok.md#uppstart-och-systemkonfiguration).

## Stänga av telefonen

Beror på modell:

* Av-knapp + volym upp
* Av-knapp + volym ner
* På en del modeller kan knappen programmeras — sök på *sidoknapp* i
  telefonens inställningar.
