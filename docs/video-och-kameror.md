# Video och kameror

Att få rörlig bild in i ATAK: strömmande video via RTSP.

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
