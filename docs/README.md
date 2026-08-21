# Handhavande och instruktioner

Instruktionsmaterial för ATAK i Markdown, i
[reveal.js](https://revealjs.com)-format. Varje fil går att läsa direkt på
GitHub, eller visas som bildspel via `viewer.html`.

För installation och avrustning av enheter, se [repots README](../README.md).

| Dokument | Avsnitt | Innehåll |
|---|---:|---|
| [ATAK-handbok](atak-handbok.md) | 36 | Handhavande: layout, menyer, kartor, navigation, point dropper, ritverktyg, data packages, 8S/PEDARS/FORS, feeds, tips och felsökning |
| [Installation med VPN från dator](atak-installation-med-vpn-fran-dator.md) | 5 | Installation av enhet från dator |
| [Uppstart efter återställd ATAK](atak-uppstart-efter-aterstalld.md) | 1 | Konfiguration av en avrustad telefon, inkl. färgsättning |
| [Avrustning och grundinställning](atak-avrustning-grundinstallning.md) | 1 | Fabriksåterställning och packning av TAK-väska |
| [Streaming setup](atak-streaming-setup.md) | 5 | RTSP-streaming från TAK ICU, ATAK och UAS |
| [Kamera – Reolink setup](atak-kamera-reolink-setup.md) | 2 | Uppsättning av Reolink-kameror |
| [Ställa om uppdateringsintervallen](stall-om-uppdateringsintervallen.md) | 1 | Rapporteringsintervall |

Dessutom:

* [instruktion-atak-hemvarn-0.9.pdf](instruktion-atak-hemvarn-0.9.pdf) — Instruktion ATAK Hemvärn, 22 sidor
* [mall-vaska-a6.pdf](mall-vaska-a6.pdf) — mall för väskmärkning A6, 12 sidor

De två PDF-filerna är kvar som PDF eftersom de saknar PowerPoint-källa och
är layoutberoende.

## Visa som bildspel

`viewer.html` hämtar reveal.js från CDN och kräver internetanslutning.
Servera mappen lokalt — filerna kan inte läsas via `file://`:

```bash
python3 -m http.server -d docs 8000
```

Öppna sedan <http://localhost:8000/viewer.html> och välj dokument.

## Om innehållet

Materialet är konverterat automatiskt från PowerPoint och PDF och är därför
inte pixelperfekt. Text, punktlistor och bilder följer med; exakt layout och
animationer gör det inte.

Rent kursmaterial — agenda, mål, kursupplägg, metodikavsnitt och
övningsuppgifter — är bortplockat. Kvar är handhavande och instruktioner.
