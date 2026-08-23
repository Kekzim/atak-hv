# ATAK-handbok

Praktisk handhavandebeskrivning för ATAK, med tips och felsökning.
Bilderna kommer från TAK-utbildningen; kursupplägg, metodikavsnitt och
övningsuppgifter är bortplockade.

Visas som bildspel via [viewer.html](viewer.html?deck=handbok).

## ATAK-specifika styrningar

ATAKs uppbyggnad sätter vissa gränser. En av dem är färgsättning av team:
standardfärgerna GUL, GRÖN, LJUSBLÅ och RÖD är reserverade eftersom de
finns som standard i TAK för markörer.

Funktionen `#` ger bredd i hanteringen — till exempel `#Sjukvårdare`,
`#Ordonnans`.

### Färgsättning

Färgerna nedan syns mot olika kartunderlag. Hemvärnets förslag:

| Nivå | Färg |
|---|---|
| **Bataljon** | OMR = SVART, TEAM = BRUN |
| **Kompani** (OMR/teamfärg) | 1:A VIT · 2:A ORANGE · 3:E ROSA (Magenta) · 4:E GRÅBLÅ/TEAL |
| **Pluton** (OMR/teamfärg) | 1:A LILA · 2:A BLÅ · 3:E MÖRKRÖD/MAROON · 4:E MÖRK GRÖN |
| **Grupp/team** | GRP 1–4, samma som plutonfärgen |

Övrig färgmarkering, TAK-standard för markörer:

| Färg | Betydelse |
|---|---|
| LJUSBLÅ | Vänlig / friendly |
| LJUSGRÖN | Neutral |
| GUL | Okänd / unknown |
| RÖD | Fientlig / hostile |

Reservfärgmarkering: **MÖRKBLÅ**.

---

## Grundlayout

Kartvyn har fyra funktionsytor:

* **Navigering**
* **Egen positionering**
* **Snabbmeny**
* **Menyträd**

Kartan fungerar som en GPS — du kan rotera, vinkla och låsa på din
position. Manövrering sker med tryck, tryck-och-håll och två fingrar.

![Grundlayout](assets/handbok/slide19-17.jpg)
![Grundlayout](assets/handbok/slide19-18.png)
![Grundlayout](assets/handbok/slide19-19.png)

---

## Snabbmeny
![Bildobjekt 3](assets/handbok/slide20-20.png)
![Bildobjekt 42](assets/handbok/slide20-21.png)
- Funktioner användaren ofta använder och vill ha åtkomst till snabbt.
- Användaren kan själv välja vad användaren vill ha tillgängligt, genom att klicka på pennan och editera menyn eller dra en ny funktion till snabbmenyn
- Därefter spara med disketten

---

## Menyträd/tools (”Hamburgerikonen” uppe till höger)
![Bildobjekt 6](assets/handbok/slide21-22.jpg)
![Bildobjekt 10](assets/handbok/slide21-23.png)
- Navigera menyn genom att scrolla.
- Samlingsplats för samtliga verktyg (Tools).
- Alla Tools kommer inte vara användbara för dig och din enhet.

---

## Lägg in ditt Callsign (ENLIGT FAL-A)och teamfärg:(”Hamburgerikonen” uppe till höger)
![Bildobjekt 6](assets/handbok/slide23-25.jpg)
- Klicka på  ”Hamburgaren”
- scrolla till Settings
Ange enligt FAL-A
![Bildobjekt 16](assets/handbok/slide23-26.jpg)
Välj: Callsign and Device Preferences
- Välj: My Team
- Välj: Färg enligt färgsättning
![Bildobjekt 9](assets/handbok/slide23-27.jpg)
![Bildobjekt 17](assets/handbok/slide23-28.jpg)
- Välj: Remarks
- Ange en Hashtag (tex #Sjukvård)
- Backa 3ggr till ren kartbild
Välj: Callsign Preferences
![Bildobjekt 18](assets/handbok/slide23-29.jpg)
![Bildobjekt 11](assets/handbok/slide23-30.jpg)
Välj: My Callsign
![Bildobjekt 13](assets/handbok/slide23-31.jpg)
![Bildobjekt 39](assets/handbok/slide23-32.png)

---

## Tools: Maps
![Bildobjekt 8](assets/handbok/slide24-33.jpg)
![Bildobjekt 1](assets/handbok/slide24-34.png)
MAPS där samlas alla tillgängliga kartor, här kan man välja olika kartunderlag
![A3FE3D63-218E-4DBC-9C34-96991C3FA5F3](assets/handbok/slide24-35.jpg)
Se till att det står ONLINE nere till höger i rutan.

---

## Tools: Maps
![Bildobjekt 1](assets/handbok/slide25-36.png)
- Dags att lägga in karta: (bör vara samma på alla enheter)
- Rekommenderad:
- Google Hybrid
- Google Sattelite Only
- Open TOPO
- Kartor av olika slag kan läggas till i systemet tex sjökort, mm filformatet är .xml
- Det är på gång kartor i andra format.
- Även en online kardataserver mot geodata

---

## Navigation
Klartext: ”Enklare inställningar för hur användaren ser, och använder sin egen position på kartan”
![Bildobjekt 4](assets/handbok/slide26-37.jpg)
-  Kompassriktning
-  Egen position.
-  Zoom in/ut.
![Bildobjekt 15](assets/handbok/slide26-38.jpg)
![Bildobjekt 3](assets/handbok/slide26-39.jpg)
Tryck och håll in kompassriktning för att ändra.
Rotation: Vit = AV, Gul = På, Hänglås = Låst
3D: Vit = AV, Gul = På, Hänglås = Låst
![Bildobjekt 11](assets/handbok/slide26-40.jpg)
Ändringar av kartans positionering görs med tvåfingersmanöver.
![Bildobjekt 7](assets/handbok/slide26-41.jpg)
![Bildobjekt 12](assets/handbok/slide26-42.jpg)
- Egen position.
- Vit = Fri rörelse.
- Gul = Fast på egen pos.
För att ändra från Gul=låset till Vit håll in ikonen ca 1 sek
![Bildobjekt 13](assets/handbok/slide26-43.jpg)

---

## Egen position
- Återgå till egen position
- (Om gul med hänglås i studsar man alltid tillbaka till sin position)
![Bildobjekt 7](assets/handbok/slide29-45.jpg)
Klartext: ”Vart jag är, koordinater”.
![Bildobjekt 6](assets/handbok/slide29-46.jpg)
- Callsign: Ditt namn
- MGRS koordinat
- Höjd
- Hastighet
- Genom att klicka på denna ruta kan man ändra vilken information som man vill visa om egen position

---

## HUR KOMMUNICERAR MAN I TAK OCH VAD
- Vilka kommunikationssätt  finns?
  - CHAT (ej uppdaterad info, ), textmeddelanden med bifogad fil
    - CHATROOMS
    - GRUPPER
    - TEAMS
    - DIREKT TILL ANNAN TAK ENHET
  - FEED (typ av chat)(uppdaterad info,) med bifogad fil
    - Synkroniserad kommunikation mellan olika takenheter
    - Tänk social media tråd
    - All information ses av all och uppdateras när man skickar via ”lasso”,  det du ser är det aktuella läget
    - För att FEED skall fungera måste enheterna ha ATAK-SYNK installerad
  - VAD: Pointdroppers, Vägar, OLEAT, DATAPAKET mm
  - SERVER SYNC: allt man lägger på kartan autosynkas till alla
  - Minskad radiokommunikation.
  - Vid AKUT kommunikation använd radio!

---

## Tools: Contacts
![Bildobjekt 8](assets/handbok/slide32-49.jpg)
![34C697DB-2BD4-4B3A-99FF-AC107DFA0973](assets/handbok/slide32-50.jpg)
- CONTACTS låter användaren kontakta andra användare på olika sätt.
- Chatt funktionen är likt vanliga sms. Du kan välja att friskriva eller nyttja de kortkommandon som finns inlagda för snabb kommunikation.
![Bildobjekt 4](assets/handbok/slide32-51.png)
![CD16DDBF-D4C0-4339-AAA7-7BAF2F7D85BA](assets/handbok/slide32-52.jpg)
Skapa en gruppchatt för att enkelt kommunicera inom enheten.

---

## Skicka information/ändringar på kartan: (utgå från standard rutiner, hur rapporterar jag via radio)
- Kommunikation med andra (Chatt) av information/ändringar på kartan:
  - Rita/lägg ut pointdropper/det du vill förmedla
  - Klicka på kontakter/Contacts – hitta din mottagare
  - Klicka på ikonen längst ut till höger med 2 rutor (du kommer till Chatfönstret)
  - Vill du bifoga något klicka sedan på Gemet (angiven text på textrad försvinner)
  - Välj det alternativ som passar bäst
  - Klicka done uppe till höger och meddelandet skickas
- Kommunicera lägesförändring eller specifika ikoner på kartan via Feed:
  - Rita/lägg ut pointdropper/det du vill förmedla – skicka till FEED
  - Rita – Ringa in med Lasso – skicka till specifik FEED

---

## Tools: point dropper
![Bildobjekt 1](assets/handbok/slide36-54.png)
- POINT DROPPER är ett verktyget där användaren kan placera ut  olika markörer på kartan.
- ATAK har flertalet olika markör-typer inlagda.
- Alla ikoner finns inte så namngivning är viktigt
![AFB1B6E5-B7C9-433D-A761-58EE1CFDF083](assets/handbok/slide36-55.jpg)
![Bildobjekt 3](assets/handbok/slide36-56.jpg)
- Om man klickar på Markers så kommer det fler alternativ, tex Rapporter med 8S
- Man kan även välja Hemvärnets ikoner
- Kommentar: Att placera ut markörer på kartan med lämplig titel är ett mycket bra sätt att kommunicera.
- Stridsställningar, FI, andra viktiga punkter.

---

## Tools: Point dropper
![Bildobjekt 1](assets/handbok/slide37-57.png)
- NAMN = CALLSIGN-TNR-HÄNDELSE
- EX: QA-241215-GRUPPERING 1
- EX: QA-241231-GRUPPERING 2
- EX: QA-241500-REKADE VÄGAR
![Bildobjekt 3](assets/handbok/slide37-58.png)

---

## Radial meny
RADIAL MENY är en funktion vissa markörer innehar för att komma åt den tryck på din egen positionsmarkör eller andra markörer.
I RADIAL MENYN går det att fin justera eller få tillgång till ytterligare information.
![7CDF78D4-50B3-49D2-8E2A-975E6EE7665D](assets/handbok/slide38-59.jpg)
Kommentar: Olika markörer har olika funktioner inom RADIAL MENY, experimentera själv och se vad för funktioner just denna markören har.

---

## Radial meny för egen position och markör

Radial meny är en funktion vissa markörer har. Tryck på din egen
positionsmarkör eller på en annan markör för att öppna den. När en
funktion aktiverats blir den markerad.

Funktioner med **gul ytterkant** har ytterligare alternativ — håll inne
för att se dem.

### För egen position

1. Markör Info
2. Kompass
3. Polär markör
4. Fin justering
5. GPS AV/PÅ
6. R&B Line
7. Threat Rings
8. Lås Pos
9. Spårbildning

![Radial meny för egen position](assets/handbok/slide39-60.jpg)

### För markör

1. Radera
2. Polär markör
3. Fin justering
4. R&B Line
5. Lås Pos
6. Skapare
7. Threat Rings
8. Spårbildning
9. Markör Info

![Radial meny för markör](assets/handbok/slide39-61.jpg)

---

## Tools: point dropper
![Bildobjekt 1](assets/handbok/slide40-62.png)
![Bildobjekt 15](assets/handbok/slide40-63.jpg)
- Radial menyn öppnas klicka på
- för att redigera information
![AFB1B6E5-B7C9-433D-A761-58EE1CFDF083](assets/handbok/slide40-64.jpg)
Välj PointDropper
![Bildobjekt 7](assets/handbok/slide40-65.png)
Markerad blir gulmarkerad, Klicka i kartan för att lägga ut den
![Bildobjekt 17](assets/handbok/slide40-66.jpg)
Namnge Ikonen genom att klicka brevid ikonen
![Bildobjekt 8](assets/handbok/slide40-67.jpg)
![Bildobjekt 19](assets/handbok/slide40-68.jpg)
![Bildobjekt 10](assets/handbok/slide40-69.jpg)
Bocka i: Show Modifiers
Avmarkera PointDropper eller backa ur med pil bakåt
Under STAFF COMMENT: lägg till information som visas bredvid ikonen
![Bildobjekt 12](assets/handbok/slide40-70.jpg)
![Bildobjekt 4](assets/handbok/slide40-71.jpg)
Du kan nu klicka på ikonen du lagt ut

---

## Tools: Drawing tools
![F35BCC30-A237-4C1F-933A-6C68049BE48C](assets/handbok/slide42-74.jpg)
DRAWING TOOLS låter användaren markera ut olika geometriska former i ATAK.
![0A34B33C-A4D5-4B04-8C5E-56D43984CA92](assets/handbok/slide42-75.jpg)
Kan användas för tex grupperingsområden, vägar, stridsställningar, mineringsområden mm

---

## Tools: LASSO
![Bildobjekt 13](assets/handbok/slide44-77.jpg)
![Bildobjekt 12](assets/handbok/slide44-78.png)
- LASSO funktionen ger dig möjlighet att ringa in flera objekt och på ett enkelt sätt skicka detta vidare, radera eller spara det som tex ett DATAPAKET
- Genom att välja lasso och sedan ringa in objekt, får man valen att skicka, spara mm
![Bildobjekt 14](assets/handbok/slide44-79.jpg)
![Bildobjekt 15](assets/handbok/slide44-80.jpg)
![Bildobjekt 16](assets/handbok/slide44-81.jpg)

---

## Tools: Data packages
DATA PACKAGES nyttjas för att komprimera data, och skicka till det utvald mottagare.
![Bildobjekt 15](assets/handbok/slide46-84.jpg)
- Se data packet som folder/dokument/filer på en dator
- Utgångsgrupperingar, ordrar, färdvägar mm
- Kan med fördel skickas som FEED så att all info alltid är uppdaterad
![57EDA6B0-6978-45E1-80ED-751F8296E4ED](assets/handbok/slide46-85.jpg)
![57EDA6B0-6978-45E1-80ED-751F8296E4ED](assets/handbok/slide46-86.jpg)
Kommentar: Enkelt och smidigt för chefer att sprida tex kommande grupperingsområden , kommande fasta uppgifter mm

---

## Tools: Data packages
![Bildobjekt 11](assets/handbok/slide47-87.jpg)
![Bildobjekt 12](assets/handbok/slide47-88.jpg)
![57EDA6B0-6978-45E1-80ED-751F8296E4ED](assets/handbok/slide47-89.jpg)
Ikonerna i DATA PACKAGES-vyn:

| Ikon | Funktion |
|---|---|
| **Plus** | Skapa ett nytt data package |
| **Download** | Ladda ner tidigare data package från TAK-servern |
| **Transfer Log** | Visa tidigare skickade och mottagna data package |
| **Multi Select Action** | Öppnar ”Overlay Manager” — extrahera eller radera flera data package |
| **Sök** | Hitta ett efterfrågat data package |

---

## Tools: Digital pointer
![Bildobjekt 7](assets/handbok/slide48-90.png)
![Bildobjekt 5](assets/handbok/slide48-91.jpg)
Med Digital pointer kan man snabbt påkalla andras uppmärksamhet till ett speciellt objekt (man ser inte själv linjen)
![Bildobjekt 6](assets/handbok/slide48-92.jpg)
- DigitDigital Pointer: uppgift
- Sätt ut en digital pointer
- Ta bort pointer
- Obs! Den som skapat Digital pointer
- Är den som måste ta bort den

---

## Tools: 8S (A-I, Fordon, METHANE)
![Bildobjekt 5](assets/handbok/slide49-93.jpg)
- Ligger under Pointdropper och Rapporter:
- Nulägesrapport via ATAK
- CS och TNR sätts automatiskt
Du klickar på kartan där du vill att ikonen skall placeras.
![Bildobjekt 6](assets/handbok/slide49-94.jpg)
- Fyll i informationen, klicka done och en 8S (samma gäller alla rapporter) kommer att synas på kartan. Den kan nu skickas till berörd enhet/person
- Hamnar under HV rapporter för historik
![Bildobjekt 7](assets/handbok/slide49-95.jpg)

---

## PEDARS & FORS
- Är knuten till den Blåa pointdropper ikonen
- Markera ikonen och välj dess funktioner
- Fyll i PEDARS & FORS, skicka till berörd enhet/person
- Under HV - Rapporter kan man se vad som kommit in
![Bildobjekt 2](assets/handbok/slide51-99.jpg)
![Bildobjekt 6](assets/handbok/slide51-100.jpg)
![Bildobjekt 1](assets/handbok/slide51-101.jpg)
![Bildobjekt 3](assets/handbok/slide51-102.jpg)

---

## RAMSOR:
- Under ”Hamburgaren” TOOLS, finns ikonen MNEMONICS (Ramsor)
- Det är en lathund för att komma ihåg alla funktioner en ramsa har:
![Bildobjekt 10](assets/handbok/slide53-107.png)
![Bildobjekt 9](assets/handbok/slide53-108.png)
MNEMONICS

---

## FEED
FEED (SYNKRONISERAT INFORMATIONSFLÖDE)
- Med en FEED upprätthåller man läget på alla enheter som man skickar informationen till eller från
- För att kunna skap en FEED måste ATAK-SYNC vara installerad på enheten/enheterna
- FEED bygger man genom att använda anropssignalerna och sätt ihop dessa till gemensamma grupper, (den sparas på server och bara den  som skapar FEED är den som kan ta bort den från servern)
- Tex: AS - Eget läge
- Tex: QL - Fiende läge
- Tex : VJ – Gröna vägar
- Feeds kan tändas och släckas med ”ögat” vilket
- möjliggör enkel översikt över kartbilden.
![Bildobjekt 1](assets/handbok/slide56-109.png)
HELA BATALJONEN
Genom att sätta läs/skriv rättigheter och pinkod på FEED kan man styra hur man vill att informationen skall uppdateras

---

## FEED
- Feed är ett sätt att kommunicerar information med synkning.
- Alla ändringar i en befintlig feed autouppdateras till alla i feeden
- FEEDs på en bataljon skulle kunna vara följande tex:
BAT
8S  QV
Mineringar RV
KOMP
KOMP
8S AQ
TMM AR
Minering BQ
Gruppering BR
PLUT
PLUT
PLUT
PLUT
- VJ – Gröna vägar
- Alla ser samma information i nutid
G
G
G
G
8S EA
Gruppfeed
- AS – Eget läge
- Alla ser samma information i nutid

---

## HUR SKAPAR VI EN FEED I ATAK?
- Öppna: overlay manager
- Klicka:  Feeds
- Klicka: plus i ring
- Create new feed
- Välj default role: Read Only, då kan du senare ändra de användare som behöver skriva i feeden tillstånd
- Namnge feed tex: batled-kompaniledning eller bara bataljonen
- Klicka;  bakåtpil och done
- Klicka: TAK server
- Klicka på er skapade Feed
- Klicka: kugghjul med 2 vita pilar i cirkel uppe till höger
- Bredvid default role till höger klicka på: 3 personer bilden
- Invite others
- ANGE DE ENHETER SOM SKALL INGÅ I KOMMUNIKATIONSFLÖDET (alla enheter som är startade och finns i er ”Bataljon” är synliga)
- Klicka: Invite
- Sedan ok - Alla valda anropssignaler kommer att få en inbjudan till Feed ”namn” och från vem
![Bildobjekt 1](assets/handbok/slide59-110.jpg)
![Bildobjekt 2](assets/handbok/slide59-111.png)
![Bildobjekt 3](assets/handbok/slide59-112.png)
![Bildobjekt 4](assets/handbok/slide59-113.png)

---

## Tools: Skapa Data packages
![Bildobjekt 15](assets/handbok/slide63-114.jpg)
![Bildobjekt 17](assets/handbok/slide63-115.jpg)
![57EDA6B0-6978-45E1-80ED-751F8296E4ED](assets/handbok/slide63-116.jpg)
![CDF081C6-870C-4F14-8A5C-B835EF5D012D](assets/handbok/slide63-117.jpg)
**Skapa nytt data package**

- Ikoner eller ritad information samt dokument kan inkluderas i DATA PACKAGE
- Välj filer från EUD (End User Device) lagringsminne
- Välj mellan specifik kategori eller enskild ikoner att inkl. i DATA PACKAGE
- Dra en cirkel runt de ikoner du vill inkl. i DATA PACKAGE (rekommenderas) eller välj Map select och klicka på det som skall ingå
- Välj select
- Välj new och döp till lämpligt namn enl CS-TNR-”Information”
- Klicka build
- Du kan nu skicka ditt datapaket genom att klicka send till höger
- Välj en användare eller till Server för att alla skall kunna hämta det via datapackage och download, eller via feed.

---

## OM TELEFONEN TAPPAR KONTAKTEN MED SERVERN (serverconnect.pdf)

> [!NOTE]
> Händer det efter en omstart räcker det inte alltid att ta bort
> anslutningen i ATAK med soptunneikonen. Ett gammalt `atak-box.zip` kan
> ligga kvar under `atak/tools/datapackage/` på telefonen och blockera
> registreringen. Radera då den filen från telefonens lagring också, innan
> du importerar `atak-box.zip` från Download igen.
- Denna information finns även på Telefonen under Download eller ATAK-Installation mappen
- Klicka på den röda pricken nere i högra hörnet av bilden på TAK skölden
- Klicka på Soptunnan
- Klicka yes
- Backa med pilen 1 ggr
- Klicka på ”Hamburgaren” uppe till höger
- Scrolla till import files
- Klicka: import files
- Klicka:  Local sd
- Bläddra till download
- Hitta: atak-box.zip
- Den kan ligga under Atak mappen under Download
- Klicka på: atak-box.zip
- Klicka :ok
- Klicka: COPY
- Klicka: ok
- Tak server registration successful
- Klicka: done
- OBS!!!   Kontroller ditt Call Sign och TEAM färg
- Inloggning
- Username
  - Password

---

## Uppstart och systemkonfiguration

**Anropssignaler (callsign).** Skilj strikt på personliga enheter
(individuell anropssignal, t.ex. RU1) och funktionsenheter (stabsdator
eller nod, t.ex. RU).

**Teamfärger.** Bat = svart, 1. komp = vit, 2. komp = orange. Pluton 1–4
ställs in internt. Grupp och soldat följer plutonens färgkodning. Se
[Färgsättning](#färgsättning) för hela schemat.

**Nivåmarkering (filtreringstagg).** Använd `#Bat`, `#Komp`, `#Plut`,
`#Grp` i fältet *Remarks*, så att högre staber snabbt kan filtrera fram
rätt beslutsnivå.

**Kritiska enhetsinställningar.** MGRS, MSL (meters), km/h, Numeric
Heading, Mils, Grid North.
Avvikelser skapar kritiska fel vid eldledning.

På en telefon som provisionerats med verktyget är de här redan satta —
se `[prefs.entries]` i `provision.toml`. Kontrollera ändå, och rätta för
hand om något avviker. Observera att självmarkörens ruta alltid visar
grader och `M` även när streck och gitternord är satta; den visningen
säger ingenting om de två inställningarna.

![Anropssignaler](assets/handbok/hv-slide06-13.png)
![Teamfärger](assets/handbok/hv-slide06-14.png)
![Nivåmarkering](assets/handbok/hv-slide06-15.png)
![Enhetsinställningar](assets/handbok/hv-slide06-16.png)

---

## Uppdateringsintervall mot server

Genom att justera rapporteringsintervallen får du antingen snabbare
uppdateringar eller bättre batteritid. Alla värden anges i sekunder.

1. ”Hamburgaren” → **Settings**.
2. **My Preferences**.
3. **Callsign and Device Preferences**.
4. **Reporting Preferences** — skrolla till fälten som slutar på
   *(Server)*.

| Inställning | Värde | Gäller |
|---|---:|---|
| Dynamic Reporting Rate Stationary (Server) | 180 | Stillastående |
| Dynamic Reporting Rate Minimum (Server) | 120 | Långsam rörelse |
| Dynamic Reporting Rate Maximum (Server) | 120 | Snabb rörelse |

Värdena ovan är utprovade. Motsvarande *(Mesh)*-fält gäller mesh-nätet
och lämnas orörda när enheten rapporterar mot TAK-server.

![Hamburgarmenyn med Settings](assets/handbok/intervall-slide01-01.jpg)
![Settings / My Preferences](assets/handbok/intervall-slide01-04.jpg)
![Callsign and Device Preferences](assets/handbok/intervall-slide01-02.jpg)
![Reporting Preferences](assets/handbok/intervall-slide01-03.jpg)
