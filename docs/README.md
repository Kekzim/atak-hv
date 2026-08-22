# Handhavande och instruktioner

Instruktionsmaterial för ATAK. Varje dokument går att läsa direkt på
GitHub, eller visas som bildspel via `viewer.html`.

Installation av en enhet — från grundinställning av telefonen till första
start av ATAK — står i [repots README](../README.md#installera-en-enhet),
tillsammans med provisioneringsverktyget.

| Dokument | Innehåll |
|---|---|
| [ATAK-handbok](handbok.md) | Handhavande: styrningar och färgsättning, layout, menyer, kartor, navigation, markörer, ritverktyg, data packages, 8S/PEDARS/FORS, feeds, uppdateringsintervall, tips och felsökning |
| [Avrustning och uppstart](avrustning.md) | Återställ ATAK, fabriksåterställning, packlista för TAK-väskan, uppstart av en avrustad telefon |
| [Video och kameror](video-och-kameror.md) | RTSP-streaming från ATAK och UAS |

Dessutom:

* [instruktion-atak-hemvarn-0.9.pdf](instruktion-atak-hemvarn-0.9.pdf) — Instruktion ATAK Hemvärn, 22 sidor
* [mall-vaska-a6.pdf](mall-vaska-a6.pdf) — mall för väskmärkning A6, 12 sidor

De två PDF-filerna är kvar som PDF eftersom de saknar redigerbar källa och
är layoutberoende.

## Visa som bildspel

`viewer.html` hämtar reveal.js från CDN och kräver internetanslutning.
Servera mappen lokalt — filerna kan inte läsas via `file://`:

```bash
python3 -m http.server -d docs 8000
```

Öppna sedan <http://localhost:8000/viewer.html> och välj dokument.

## Om innehållet

Materialet är konverterat från PowerPoint och PDF och därefter
omstrukturerat. Kursmaterial — agenda, mål, metodikavsnitt och
övningsuppgifter — ingår inte; kvar är handhavande och instruktioner.

Uppgifter som annars skulle upprepas står på ett ställe och länkas till:
färgsättningen finns i [handboken](handbok.md#färgsättning), och
callsign-inställningen i
[Avrustning och uppstart](avrustning.md#callsign-och-teamfärg).
