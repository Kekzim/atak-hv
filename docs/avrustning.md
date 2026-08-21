# Avrustning och uppstart

Två procedurer som hör ihop: att lämna tillbaka en telefon, och att ta
emot en som någon annan lämnat tillbaka.

Datordelen — att avinstallera appar och rensa filer via `adb` — görs med
`provision.bat restore` respektive `./provision.sh restore`, se
[repots README](../README.md#avrustning-och-återlämning).

## Återställ ATAK

Genomförs efter övning eller på order.

1. Klicka ”Hamburgaren”, skrolla till **Clear Content**.
2. Bocka i **Clear maps & imagery**, klicka båda AV till LOCKED.
3. Klicka **CLEAR NOW**. ATAK avslutas.
4. Öppna filhanteraren (”Mina filer”, ”Files”, ”FileManager” eller
   motsvarande).
5. Välj **Intern lagring**, leta upp mappen `atak` och radera den.
6. Öppna mappen `ATAK-installation` och kopiera mappen `atak` till internt
   minne (rotkatalogen). Tar cirka 10 sekunder.
   Det är den rena reservkopian som lades ut vid installationen — därför
   behövs ingen dator för att återställa ATAK.
7. Backa tillbaka till telefonens hemskärm.
8. Stäng av telefonen.

Enheten är nu klar för nästa användare.

## Fabriksåterställning

Görs på order, och när telefonen ska lämnas in för förvaring eller
överlämnas till en ny enhet.

1. Ladda telefonen.
2. Nolla telefonen enligt ”Grundställ telefonen”.
3. Packa väskan enligt listan nedan.

### Innehåll TAK-väska

| Antal | Föremål |
|---:|---|
| 1 | TAK-telefon |
| 1 | Laddare med laddkabel, eller 220 V till USB-C |
| 1 | USB-C till USB-C |
| 1 | USB-A till USB-C (saknas på vissa) |
| 1 | Powerbank 10 000 eller 20 000 mAh |

## Uppstart efter återställd ATAK

När du fått en avrustad telefon.

1. Starta ATAK.
2. Godkänn alla fönster.
3. ATAK laddar — **TAK Device Setup** — *Done*.
4. Avvakta tills listen överst utökats med tre ikoner.
5. ”Hamburgaren” — skrolla till **QUIT** — *YES*.
6. Starta ATAK igen.
7. Klicka ”Hamburgaren”, välj **Import**.
8. **Local SD** — klicka ikonen till vänster under *S* i *Select Files to
   Import* — skrolla till **Download**.
9. Välj `xxxxxxx.zip` (bocka i rutan till höger) — *OK*.
10. **Copy**.
11. Logga in — användarnamn och lösenord enligt lista.
12. *OK* — ”Tak server registration completed” — *OK*.

### Callsign och teamfärg

1. ”Hamburgaren” → **Settings**.
2. **Callsign and Device Preferences**.
3. **Callsign Preferences** → **My Callsign** → ange ditt callsign enligt
   FAL-A → *OK*.
4. **My Team** → välj färg enligt
   [färgsättningen i handboken](handbok.md#färgsättning).
5. Ange **Remarks**: `#xxxxxxx` vid behov.
6. Backa med pil bakåt tills du har ren kartbild.
7. Klicka på kartikonen i överkant och välj din karta.
8. Backa tillbaka till ren kartbild.
