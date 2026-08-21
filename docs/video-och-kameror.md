# Video och kameror

Att få rörlig bild in i ATAK: strömmande video via RTSP, och fasta
övervakningskameror.

## Streaming

Till TAK kan flera källor kopplas för att strömma information:

* Drönare (UAS)
* Externa kameror

Viktigast är **metoden** — vem bestämmer var, när och hur.

Streamingprotokoll: **RTSP** (används just nu), http/https med flera.

### Setup i ATAK

1. Öppna ATAK.
2. Under ”Hamburgaren” → **Video**.
3. Klicka **+**.
4. **Type** — RTSP.
5. Adress: `xxxx.xxxx.xxxx.xxxx:8554/callsign?tcp`
6. **Alias Name** — callsign.
7. **Wowza Server Username** — tilldelas av ansvarig.
8. **Wowza Server Password** — tilldelas av ansvarig.
9. **Add**.
10. Klicka ”Hamburgaren” till höger om din tillagda videoström.
11. **Send** till dem som behöver den, via chatt eller feed.

### Från UAS till ATAK-enhet

Inställningarna i UAS-enheten görs enligt UAS-utbildningsanvisning.

På ATAK-enheten syns drönarens position automatiskt. Klicka på
drönarikonen och därefter på videoikonen för att se vad drönaren strömmar
— strömmar UAS får du bild, annars inget.

## Reolink-kameror

> [!NOTE]
> Reolink ingår inte i utrustningspaketet. Appen installeras från Google
> Play vid behov, av den som ska hantera övervakningskameror.

> **OBS!** Avdela en telefon som huvudtelefon för kamera, till exempel hos
> sensoransvarig.

### Lägga till kameror (sensoransvarig)

Kameran måste vara påslagen och ansluten till internet.

1. Öppna appen **Reolink**.
2. Starta — **Godkänn**.
3. Klicka **Lägg till enhet** och skanna QR-koden.
4. Skapa lösenord.
5. Namnge kameran enligt klisterlappen.
6. **Inspelning** — välj video och bild.
7. Klicka på kamerans bild → kugghjulet uppe till höger.
8. Skrolla till **Push-meddelande** — välj PÅ.
9. Testa med ett tryck uppe till höger — **Test**.
10. Backa till Reolinks startvy, ”My Home”.
11. Klicka plusset uppe till höger.
12. Repetera från punkt 3 tills alla kameror är inlagda.

![Reolink-appens översikt](assets/video-och-kameror/reolink-oversikt.png)

### Popup-varning vid kameradetektering

1. **Inställningar** → **Tillgänglighet** → **Avancerade inställningar**.
2. **Dags att vidta åtgärder** — välj hur länge popupen visas vid
   detektering.
   **OBS!** Detta påverkar alla popuper på telefonen.
3. Ladda ner Reolink-appen till din telefon.
4. Håll in Reolink-ikonen, klicka på **i** i bubblan som öppnas.
5. Skrolla till **Visa överst**, klicka och tillåt behörigheten.
6. Backa tillbaka två gånger.
7. Starta Reolink-appen.
8. Klicka plusset uppe till höger och skanna QR-koden från
   sensoransvarig.

### Dela ut en kamera via QR-kod

Vid behov.

1. Öppna **Reolink**.
2. Välj kameran du vill dela.
3. Klicka kugghjulet uppe till höger.
4. Skrolla till **Dela kamera**.
5. Be mottagaren skanna QR-koden från sin Reolink-app.
6. Uppge lösenordet.

### Placera kamera

Används av sensoransvarig.

1. Placera övervakningskameran på vald plats.
2. I ATAK: sätt ut ikonen **SENSOR** med rätt riktning och namn.

### Återlämning

1. Radera kameran från appen.
2. Nollställ kameran med RESET-knappen (under gummifliken under
   objektivet).
3. Stäng av kameran.
