import base64
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
import random
load_dotenv()


def generate(debug=False):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-pro-preview-03-25"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""In the first step, generate the markdown for thema, structure of the meeting note.

In the second step, generate markdown brain storm about with should be the good part from meeting note to make question. 

In the third step generate markdown for 5 idea for question, options and design the tricky distractor options

In the fifth step, generate the json format for the final mocktest. Fowllow exactly the same structure as the example in the system instruction 

*Mocktest have to be in json format starting with ```json and ending with ```*"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1.5,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""#Prompt: Generating B2 Beruf Reading Part 4 Mock Tests (Text & Questions)

## I. Overall Goal

To generate a complete mock test item for the "Deutsch-Test für den Beruf B2 - Lesen Teil 4". This involves creating:
1.  A realistic, detailed **meeting protocol (Protokoll)** from a fictional German company.
2.  A corresponding set of **5 multiple-choice questions (Aufgaben)**, each with one correct answer and two plausible distractors, testing detailed comprehension of the protocol.
3.  Output the result in a specified **JSON format**.

---

## II. Part 1: Generating the Meeting Protocol (`meeting_note`)

### A. Header (Kopfzeile)
    *   **Title:** "Protokoll"
    *   **Date:** Specific date (e.g., `TT. Monat JJXX`). Use `XX` for the year.
    *   **Time:** Start and end time (e.g., `HH:MM – HH:MM Uhr`). Duration typically 60-90 minutes.
    *   **Location:** Specific place (e.g., `Raum X, Straße + Nr, PLZ Ort`).

### B. Participants (Teilnehmer)
    *   **Attendees (`Anwesende`):** List 6-8 attendees with `Full Name (Initials, Role/Department)`. Include diverse roles (Management, Dept. Heads - Einkauf, Verkauf, Produktion, IT, Personal, Marketing, Finanzen, Qualität, etc., Assistenz, Sekretariat).
    *   **Optional:** `Entschuldigt` (1-2 names), `Gast` (1 name with role).
    *   **Leadership:** Assign `Sitzungsleitung` (Chair) and `Protokollant/in` (Minute Taker) to specific attendees.
    *   **Abbreviations:** Define clear initials (e.g., ML, GS) for consistent use in the TOP sections.

### C. Agenda (`Tagesordnungspunkte`)
    *   **Number:** List 5-6 numbered agenda items (TOPs).
    *   **Standard Items:** Usually include TOP 1 (`Begrüßung und Genehmigung des letzten Protokolls`) and the last TOP (`Sonstiges`).
    *   **Titles:** Brief, clear titles for each TOP covering various potential themes (see below).

### D. Potential Themes for Content
    *   Sales/Market (`Verkaufszahlen`, `Marktentwicklung`)
    *   Production/Logistics (`Produktion`, `Kapazitäten`, `Lieferketten`, `Lagerbestände`)
    *   Projects (New product, IT system, renovation, construction) (`Projekte`, `Stand X`)
    *   Marketing/Sales (`Marketing`, `Homepage`, `Logo`, `Werbung`, `Kunden`)
    *   HR (`Personelles`, `Mitarbeiter`, `Ausbildung`, `Arbeitszeiten`)
    *   IT (`Software`, `Hardware`, `Datenbank`)
    *   Finance (`Kosten`, `Preise`, `Budget`)
    *   Events (`Veranstaltungen`, `Messen`, `Workshops`, `Feier`)
    *   Customer Service (`Kundenservice`)

### E. Detailed Sections (TOP 1, TOP 2, etc.)
    *   **Structure:** Section for each TOP with heading "TOP [Number] [Title]".
    *   **Length per TOP:** 3-8 sentences (1-3 short paragraphs). `Sonstiges` can vary.
    *   **Content:**
        *   **Initiator:** Clearly state who is reporting/proposing (using initials).
        *   **Information:** Present specific updates, results, problems, proposals.
        *   **Decisions/Actions:** State decisions (`wird beschlossen`, `genehmigt`) and assigned actions (`XY soll...`, `AB kümmert sich um...`).
        *   **Reasons/Causes:** Include explanations (`wegen`, `da`, `aufgrund`).
        *   **Conditions/Contingencies:** Use conditional statements (`Sollte...`, `Wenn...`).
        *   **Problems/Challenges:** Mention issues, delays, disagreements (`Probleme`, `bemängeln`, `Einwände`).
        *   **Future Steps:** Indicate follow-ups, next meetings, deadlines (`nächste Sitzung`, `bis Datum X`).
        *   **Crucial for Questions:** **While writing these sections, consciously embed specific, potentially confusing details:**
            *   Exact vs. approximate dates/times/numbers.
            *   Names of people, products, places.
            *   Clear assignments of responsibility.
            *   Conditional clauses vs. definite statements.
            *   Reasons vs. consequences.
            *   Completed actions vs. ongoing vs. planned actions.
            *   Statements applying to all vs. some/specific cases.
            *   Comparisons (more/less, better/worse).
            *   Exceptions (`außer`, `nur`).
            *   **Think ahead: How could a reader misinterpret this detail? This is the basis for your distractors.**

### F. Language and Style
    *   **Formality:** Objective, formal business German.
    *   **Tense:** Primarily Präsens for reporting/decisions; Perfekt/Präteritum for past results; Future/Modals for plans.
    *   **Vocabulary:** Appropriate B2 business vocabulary; fixed meeting phrases.
    *   **Sentences:** Mix of simple and complex structures (subordinate clauses).

---

## III. Part 2: Designing the Questions & Options (`aufgaben_list`)

### A. Question Stem (`frage`)
    *   **Format:** Short phrase/noun phrase (2-5 words).
    *   **Content:** Identifies the specific topic/person/item from the text the question is about (e.g., "Das Protokoll", "Die neue Software", "Frau Meier").

### B. Options (`optionen`)
    *   **Format:** 3 options (a, b, c), each a short, complete clause/sentence (5-15 words).
    *   **Content:**
        *   **1 Correct Option (`Lösung`):** Accurately reflects information *directly stated* or logically derived from the text.
        *   **2 Distractor Options (`Distraktoren`):** Plausible but incorrect statements targeting potential reading errors.

### C. Designing Effective Distractors (Targeting Common B2 Reading Challenges)
    *   **Base distractors on the specific, potentially confusing details embedded in the text.**
    *   **Techniques:**
        1.  **Detail Manipulation:** Slightly alter dates, names, numbers, locations, percentages found in the text.
        2.  **Agent/Recipient Confusion:** Attribute actions/statements to the wrong person.
        3.  **Status/Timing Errors:** Confuse planned/ongoing/completed; use wrong tense; shift timelines.
        4.  **Scope Errors:** Generalize specifics or specify generalities incorrectly; misuse words like "alle", "einige", "nur".
        5.  **Misleading Keywords:** Use correct words from the text but in a statement with twisted meaning.
        6.  **Opposite/Negation:** Contradict a fact (approved vs. rejected; solved vs. unsolved).
        7.  **Ignoring Conditions/Exceptions:** Present a conditional statement as absolute; ignore stated exceptions.
        8.  **Plausible but Unstated:** Create logical-sounding options not actually mentioned in *this* text.
        9.  **Partial Truth:** Combine true and false elements within one option.

### D. Important Considerations for Questions
    *   **Text Dependency:** Answers *must* come solely from the provided protocol.
    *   **Clarity:** Questions/options must be unambiguous in their *wording*. The difficulty lies in choosing the correct information from the text.
    *   **Coverage:** Distribute the 5 questions across different TOPs/aspects of the protocol.
    *   **B2 Level:** Target appropriate complexity, vocabulary, and comprehension skills (understanding detail, purpose, consequence, responsibility).

---

## IV. Final Output Format (JSON)

The final output must be a single JSON object structured as follows:

```json
{
  "meeting_note": "## Protokoll\n\n**[Date], [Time]**\n**Ort:** [Location]\n\n**Anwesende:**\n*   [Attendee 1 (Initials, Role)]\n*   [...]\n\n**Sitzungsleitung:** [Name]\n**Protokollant:** [Name]\n\n**Tagesordnungspunkte**\n\n1.  [TOP 1 Title]\n2.  [...]\n6.  [Last TOP Title]\n\n**TOP 1 [Title]**\n\n[Paragraph 1 text for TOP 1]...\n\n**TOP 2 [Title]**\n\n[Paragraph 1 text for TOP 2]...\n\n[...]\n\n**TOP 6 [Title]**\n\n[Paragraph 1 text for TOP 6]...",
  "aufgaben_list": [
    {
      "frage": "[Question 1 Stem]",
      "optionen": [
        {
          "key": "a",
          "text": "[Option a text for Question 1]"
        },
        {
          "key": "b",
          "text": "[Option b text for Question 1]"
        },
        {
          "key": "c",
          "text": "[Option c text for Question 1]"
        }
      ],
      "loesung": "[Correct key: 'a', 'b', or 'c']"
    },
    {
      "frage": "[Question 2 Stem]",
      "optionen": [
        {
          "key": "a",
          "text": "[Option a text for Question 2]"
        },
        {
          "key": "b",
          "text": "[Option b text for Question 2]"
        },
        {
          "key": "c",
          "text": "[Option c text for Question 2]"
        }
      ],
      "loesung": "[Correct key: 'a', 'b', or 'c']"
    },
    // ... (objects for questions 3, 4, 5)
  ]
}
---

Example 1:

{
    "meeting_note": "## Protokoll\n\n**19. Februar 20XX, 10.00–11.45 Uhr**\n**Konferenzraum 7, Ort: Neuburger Allee 28, 87341 Ballhausen**\n\n**Anwesende:**\n*   Maria Loppinet (ML, Geschäftsführung)\n*   Lukas Meier (LM, Leitung Einkauf)\n*   Magda Nauner (MN, Leitung Personal)\n*   Gert Schrader (GS, Leitung Produktion)\n*   Peter Schuldt (PS, Leitung Verkauf)\n*   Katja Stevens (KS, Leitung Qualitätskontrolle)\n*   Volha Schäfer (VS, Leitung Finanzen)\n*   Gast: Wanda Lubic (WL, IT-Beauftragte)\n\n**Sitzungsleitung:** Magda Nauner\n**Protokollantin:** Volha Schäfer\n\n**Tagesordnungspunkte**\n\n1.  Begrüßung und Genehmigung des letzten Protokolls\n2.  Stand des Projekts "Fertigungsanlage"\n3.  Berichte\n4.  Neue Mitarbeiterinnen und Mitarbeitern\n5.  Update der Software\n6.  Sonstiges\n\n**TOP 1 Begrüßung und Genehmigung des letzten Protokolls**\n\nMN begrüßt Frau Loppinet und alle Leiterinnen und Leiter zur heutigen Sitzung. Sie bittet um Genehmigung des Protokolls der letzten Sitzung. Nach Handzeichen wird das Protokoll der Sitzung vom 15.01. ohne weitere Änderungen und Ergänzungen einstimmig genehmigt.\n\n**TOP 2 Stand des Projekts "Fertigungsanlage"**\n\nLM gibt einen Überblick zum Projekt "Fertigungsanlage". Er berichtet über den Auftrag an eine Firma aus Italien, die bereits ähnliche Anlagen hergestellt und aufgebaut hat. Die italienische Firma kommt nächsten Monat, um sich vor Ort ein Bild von unseren Werkshallen II und IV zu machen, wo die Anlage stehen soll. Der genaue Termin steht noch nicht fest. Wenn Werkshalle II oder IV als geeignet erscheint, wird unmittelbar mit der Herstellung der Fertigungsanlage in Italien begonnen. Die Montage der Anlage ist dann einige Monate später. Wie geplant soll die neue Fertigungsanlage im folgenden Frühjahr betriebsbereit sein. Sollte keine der beiden Werkshallen für den Aufbau der Fertigungsanlage groß genug sein, müssten wir zuerst eine komplett neue Werkshalle auf dem südlichen Werksgelände errichten lassen. Dadurch könnte sich die Inbetriebnahme einer neuen Fertigungsanlage um mindestens 8 bis 9 Monate verschieben.\n\n**TOP 3 Berichte**\n\nGS berichtet über die ohne große Probleme laufende Produktion der Metallkästen und Metallgehäuse, die sehr nachgefragt sind. Bei noch größerer Nachfrage nach Metallgehäusen könnte jedoch die derzeitige Fertigungsanlage nicht ausreichen. GS freut sich daher über die Planung einer neuen Fertigungsanlage.\n\nPS legt neue Verkaufszahlen vor, die im letzten Quartal 20 Prozent über dem vergleichbaren Quartal des Vorjahrs liegen. Besonders die Metallgehäuse für den Hochbau zeigen sehr gute Verkaufszahlen. PS erwähnt hier einen großen Auftrag aus Kasachstan, der für das hohe Auftragsvolumen ausschlaggebend ist.\n\n**TOP 4 Neue Mitarbeiterinnen und Mitarbeitern**\n\nMN nennt die Namen von fünf neuen Mitarbeiterinnen und Mitarbeitern, drei Frauen und zwei Männern, die ab dem 1. des Monats im Betrieb in Vollzeit tätig sind.\n\n**TOP 5 Update der Software**\n\nWL spielt am kommenden Freitag ab 19 Uhr ein Software-Update auf unser Computersystem. Daher darf am Freitag ab 19 Uhr niemand am Computer arbeiten.\nDie leicht überarbeitete Software hat einige Neuerungen. Allen Mitarbeiterinnen und Mitarbeitern werden diese Neuerungen in einem halbtägigen Info-Workshop demonstriert. Es wird zeitversetzte Workshops geben. Die Termine dafür werden noch bekannt gegeben.\n\n**TOP 6 Sonstiges**\n\nML berichtet über den Stand der Planung eines Sommerfests, das etwas größer als in den vergangenen Jahren sein soll. Alle wichtigen Kunden und großen Lieferanten werden eingeladen. ML bittet alle Leiterinnen und Leiter, sich den 31. Juli freizuhalten. Der Ort steht auch schon fest. ML möchte ihn aber noch nicht nennen. Es soll eine Überraschung für alle sein, da der 31. Juli auch ihr 60. Geburtstag ist, den sie mit allen feiern möchte.",
    "aufgaben_list": [
      {
        "frage": "Das Protokoll",
        "optionen": [
          {
            "key": "a",
            "text": "der letzten Sitzung ist nach Überarbeitung genehmigt."
          },
          {
            "key": "b",
            "text": "nennt die Teilnehmer der Januar-Sitzung."
          },
          {
            "key": "c",
            "text": "wird heute von Frau Schäfer geschrieben."
          }
        ],
        "loesung": "c"
      },
      {
        "frage": "Die neue Fertigungsanlage",
        "optionen": [
          {
            "key": "a",
            "text": "kommt in die Werkshalle IV."
          },
          {
            "key": "b",
            "text": "steht in einem Neubau."
          },
          {
            "key": "c",
            "text": "wird in Italien gebaut."
          }
        ],
        "loesung": "c"
      },
      {
        "frage": "Metallkästen und Metallgehäuse",
        "optionen": [
          {
            "key": "a",
            "text": "lassen sich nur in Deutschland verkaufen."
          },
          {
            "key": "b",
            "text": "sind eine Belastung für die Produktion."
          },
          {
            "key": "c",
            "text": "zeigen steigende Verkaufszahlen."
          }
        ],
        "loesung": "c"
      },
      {
        "frage": "Das Update der Software",
        "optionen": [
          {
            "key": "a",
            "text": "erfordert ein neues Computersystem."
          },
          {
            "key": "b",
            "text": "schließt einen eintägigen Workshop mit ein."
          },
          {
            "key": "c",
            "text": "wird am Freitag installiert."
          }
        ],
        "loesung": "c"
      },
      {
        "frage": "Die Geschäftsführerin",
        "optionen": [
          {
            "key": "a",
            "text": "berichtet über Ort und Termin eines Sommerfests."
          },
          {
            "key": "b",
            "text": "erwartet eine genaue Planung des Sommerfests."
          },
          {
            "key": "c",
            "text": "möchte zum Sommerfest Kunden und Lieferanten einladen."
          }
        ],
        "loesung": "c"
      }
    ]
}

Example 2:

{
    "meeting_note": "## PROTOKOLL\n\n**Monatsmeeting: 08.06.20XX, Besprechungsraum I**\n\n**Teilnehmer*innen:** Torsten Koslik (TK, Geschäftsleitung), Manuela Batista (MB, Kundenservice), Joseph Chuma (JC, Herstellung), Christine Gündel (CG, Marketing), Andreas Radosch (AR, IT)\n**Entschuldigt:** Sumaiya Reza (SR, Verkauf)\n**Protokoll:** MB\n\n**TAGESORDNUNG**\n\n**TOP 1:** Materialkosten & Preise\n**TOP 2:** Kundenservice: Stand der Dinge\n**TOP 3:** Zusatzauftrag\n**TOP 4:** Neues Logo\n**TOP 5:** Veranstaltungen\n\n**TOP 1: Materialkosten & Preise**\n\nSeit Jahresbeginn sind die Preise für Holz stetig gestiegen und das wird voraussichtlich auch im zweiten Halbjahr so bleiben. Einen wesentlichen Grund für den Preisanstieg sieht TK darin, dass Bauen mit Holz zurzeit stark im Trend liegt und Holz deshalb sowohl von Baufirmen als auch von Privatleuten stärker nachgefragt wird. TK berichtet, dass die meisten anderen Möbelhersteller ihre Verkaufspreise bereits erhöht haben. Bei Möbel Koslik sind bis zum Jahresende jedoch keine Preisanpassungen vorgesehen und das soll auch so auf der Webseite kommuniziert werden. CG verfasst diese Woche noch einen entsprechenden Text. Im Januar wird die Situation neu bewertet.\n\n**TOP 2: Kundenservice: Stand der Dinge**\n\nMB berichtet, dass die Kundenzufriedenheit nach wie vor sehr hoch ist. Besonders geschätzt wird die individuelle Betreuung der Kunden, die allerdings sehr zeitaufwändig ist. Um sich wiederholende Kundenanfragen zu reduzieren, schlägt MB vor, den Fragen-und-Antworten-Bereich auf der Webseite zu erweitern. AR glaubt nicht, dass dies zu einer spürbaren Entlastung im Kundenservice führt. Er schlägt zusätzlich vor, kurze Erklärfilme zu produzieren, die die Produkte und Leistungen des Unternehmens unterhaltsam und leicht verständlich darstellen. Die praktische Umsetzbarkeit dieses Vorschlags und die damit verbundenen Kosten sollen in den kommenden Wochen geprüft werden: AR recherchiert Dienstleister und Preise, CG und MB skizzieren mögliche Inhalte der Erklärfilme.\n\n**TOP 3: Zusatzauftrag**\n\nVor acht Jahren wurde die Einrichtung für das Restaurant "Landhaus" von Möbel Koslik angefertigt. Nach einem Brand muss die Einrichtung komplett erneuert werden und der Inhaber des Restaurants hat angefragt, ob Möbel Koslik diesen zusätzlichen Auftrag übernehmen kann. Die Anfertigung der Einrichtung soll größtenteils parallel zu der Gebäudesanierung laufen und rechtzeitig zur Neueröffnung (voraussichtlich Ende September) fertig sein. TK möchte den Auftrag annehmen. JC hat bereits zu bedenken gegeben, dass die Produktion zurzeit keine Kapazitäten für ein zusätzliches Projekt hat. Um den Auftrag trotzdem ausführen zu können, schlägt er vor, vorübergehend Leiharbeiter einzustellen. TK stimmt zu und wird den Personaldienstleister kontaktieren.\n\n**TOP 4: Neues Logo**\n\nIm Rahmen der Modernisierungsmaßnahmen von Möbel Koslik soll auch ein neues Logo für das Unternehmen entwickelt werden. CG hat im Vorfeld Angebote von verschiedenen Agenturen eingeholt und stellt die drei besten vor. Nach sorgfältigem Vergleich wurde entschieden, dass die Agentur Kellermann den Zuschlag erhält. Das Angebot liegt preislich zwar über dem der anderen, aber die Agentur ist deutschlandweit für ihre ausgezeichneten Logodesigns bekannt, die TK sehr überzeugt haben. CG kontaktiert die Agentur heute im Laufe des Tages, um den Auftrag zu erteilen.\n\n**TOP 5: Veranstaltungen**\n\nAm 25.07. findet wieder der Teambuilding-Tag statt, der alle zwei Jahre für die Angestellten organisiert wird. Zur Vorbereitung sammelt eine Arbeitsgruppe zurzeit neue Ideen für einen geeigneten Ort und Aktivitäten. Die zuständige Ansprechpartnerin ist CG. Wer Vorschläge oder Wünsche für den Teambuilding-Tag hat, kann sich an sie wenden.\n\nDer Seniorchef Manfred Koslik wird sich ab September aus Altersgründen komplett aus dem Unternehmen zurückziehen. Aus diesem Anlass wird sein Nachfolger Paul Koslik eine Feier im Parkhotel organisieren, zu der alle Mitarbeiter*innen eingeladen werden. Ob die Feier wie von Manfred Koslik gewünscht am 26.08. stattfinden kann oder doch erst am 30., wird derzeit noch geklärt.",
    "aufgaben_list": [
      {
        "frage": "In der zweiten Jahreshälfte",
        "optionen": [
          {
            "key": "a",
            "text": "müssen die Kunden bei Möbel Koslik mehr bezahlen."
          },
          {
            "key": "b",
            "text": "sollen die Preise bei Möbel Koslik stabil bleiben."
          },
          {
            "key": "c",
            "text": "werden die Holzpreise voraussichtlich wieder sinken."
          }
        ],
        "loesung": "b"
      },
      {
        "frage": "Manuela Batista schlägt eine Maßnahme vor, um",
        "optionen": [
          {
            "key": "a",
            "text": "die Kosten für die Produktion der Erklärfilme zu senken."
          },
          {
            "key": "b",
            "text": "die Zufriedenheit der Kunden zu verbessern."
          },
          {
            "key": "c",
            "text": "Zeit bei der Kundenbetreuung einzusparen."
          }
        ],
        "loesung": "c"
      },
      {
        "frage": "Möbel Koslik",
        "optionen": [
          {
            "key": "a",
            "text": "benötigt mehr Personal, um den Auftrag durchzuführen."
          },
          {
            "key": "b",
            "text": "hat noch keinen Auftrag für das Restaurant ausgeführt."
          },
          {
            "key": "c",
            "text": "soll nach Abschluss der Sanierung mit der Arbeit beginnen."
          }
        ],
        "loesung": "a"
      },
      {
        "frage": "Die Agentur Kellermann",
        "optionen": [
          {
            "key": "a",
            "text": "bekommt den Auftrag, obwohl sie am teuersten ist."
          },
          {
            "key": "b",
            "text": "organisiert die Modernisierungsmaßnahmen."
          },
          {
            "key": "c",
            "text": "wurde von Frau Gündel bereits beauftragt."
          }
        ],
        "loesung": "a"
      },
      {
        "frage": "Es gibt zurzeit noch",
        "optionen": [
          {
            "key": "a",
            "text": "keine Neubesetzung für Manfred Kosliks Position im Unternehmen."
          },
          {
            "key": "b",
            "text": "keinen festen Termin für die Abschiedsfeier im Parkhotel."
          },
          {
            "key": "c",
            "text": "niemanden, der sich um die Vorbereitung des Teambuilding-Tags kümmert."
          }
        ],
        "loesung": "b"
      }
    ]
}
  

Example 3:

{
    "meeting_note": "## Protokoll\n\n**30. Januar 20XX, 14:00–15:30 Uhr**\n**Ort:** Besprechungsraum, Baseler Landstraße 158-162, 79342 Herbolzen\n\n**Anwesende:**\n*   Franz Schwacker (FS, Geschäftsführung)\n*   Metin Basel (MB, Assistenz Geschäftsführung)\n*   Samson Abdulkarim (SA, Leitung Vertrieb)\n*   Lothar Charrier (LC, Leitung Personal)\n*   Christian Celin (CC, Leitung Online-Vertrieb)\n*   Bertha Willmann (BW, Leitung Einkauf)\n\n**Sitzungsleitung:** Franz Schwacker\n**Protokollant:** Metin Basel\n\n**Tagesordnungspunkte**\n\n1.  Begrüßung und Genehmigung des letzten Protokolls\n2.  Verkaufszahlen\n3.  Webshop\n4.  Einführung Mitarbeiterkleidung\n5.  Personelles\n6.  Sonstiges\n\n**TOP 1 Begrüßung und Genehmigung des letzten Protokolls**\n\nFS begrüßt die Anwesenden und bittet um Genehmigung des Protokolls der letzten Sitzung. BW erhebt Einwände gegen TOP 3: Es wurden nicht wie angegeben zwei, sondern drei Vergleichsangebote zum Bau des neuen Gewächshauses eingeholt. Nach dieser Korrektur wird das Protokoll einstimmig genehmigt.\n\n**TOP 2 Verkaufszahlen**\n\nSA gibt einen Überblick über die Verkäufe im vergangenen Geschäftsjahr: Wie bisher standen mehrjährig blühende Pflanzen oben in der Rangliste der Verkäufe. Weiterhin ungeschlagen ganz vorne liegen die Schnittblumen, während sich die Zimmerpflanzen etwas geringer verkauft haben. Stärker eingebrochen dagegen sind die Verkaufszahlen bei den Orchideen. Die Überraschung des Jahres ist die Flamingoblume, die erst im Februar ins Sortiment aufgenommen wurde, und bereits auf Platz fünf der Verkäufe geklettert ist. SA berichtet insgesamt von einem positiven Ergebnis, obwohl die Absätze im vierten Quartal gegenüber dem ersten bis dritten Quartal gesunken sind.\n\n**TOP 3 Webshop**\n\nCC schlägt vor, auch für weitere Pflanzen zu prüfen, ob der Onlinehandel möglich ist. Nach seiner Einschätzung kämen dafür luftreinigende Pflanzen fürs Büro sowie Kakteen in Frage. SA wendet ein, dass sich der Verkauf von Pflanzen über das Internet durch den Aufwand für Verpackung und Versand bisher nicht gelohnt hat. Er empfiehlt, höchstens künstliche Blumen oder Trockenblumen ins Sortiment aufzunehmen. Nach kurzer Diskussion wird die Entscheidung über den Ausbau des Webshops auf das Frühjahr vertagt.\n\n**TOP 4 Einführung Mitarbeiterkleidung**\n\nLC berichtet vom Stimmungsbild unter den Mitarbeitenden zum Thema Einheitliche Mitarbeiterkleidung. Nahezu alle Befragten haben sich ablehnend geäußert. Es wird beschlossen, dass es außer im Verkauf bei der alten Regelung bleibt.\n\n**TOP 5 Personelles**\n\nLC informiert darüber, dass Zaccarias Özil am 1. August diesen Jahres bei uns seine Ausbildung zum Einzelhandelskaufmann beginnen wird. Herr Özil kennt unsere Firma schon von einem Schüler- und einem zweimonatigen betrieblichen Praktikum nach seinem Schulabschluss. LC betont, dass man im Betrieb einen sehr guten Eindruck von Herrn Özil gewonnen habe und besonders seine Fremdsprachenkenntnisse hilfreiche eingebunden werden können.\n\n**TOP 6 Sonstiges**\n\nFS informiert über Probleme bei der Planung der Tage der Offenen Gärtnerei. Diese könnten in diesem Jahr nicht wie immer am ersten Mai-Wochenende stattfinden, da durch den Bau des neuen Gewächshauses noch nicht genug Schaufläche für die Fachbesucher zur Verfügung steht. Er schlägt für die Tage der Offenen Gärtnerei das zweite Wochenende im Juli vor. Nach Abstimmung wird das so beschlossen. Keine sonstigen Punkte durch die Teilnehmenden. Die nächste Sitzung findet am 28.02. statt.",
    "aufgaben_list": [
      {
        "frage": "Das Protokoll der letzten Sitzung",
        "optionen": [
          {
            "key": "a",
            "text": "hat Frau Willmann geschrieben."
          },
          {
            "key": "b",
            "text": "musste korrigiert werden."
          },
          {
            "key": "c",
            "text": "wird in mehreren Punkten ergänzt."
          }
        ],
        "loesung": "b"
      },
      {
        "frage": "Die Verkäufe",
        "optionen": [
          {
            "key": "a",
            "text": "einer neuen Pflanze waren unerwartet gut."
          },
          {
            "key": "b",
            "text": "für Schnittblumen haben sich positiv verändert."
          },
          {
            "key": "c",
            "text": "sind im vergangenen Jahr stark gefallen."
          }
        ],
        "loesung": "a"
      },
      {
        "frage": "Der Handel über das Internet",
        "optionen": [
          {
            "key": "a",
            "text": "fängt jetzt erst an."
          },
          {
            "key": "b",
            "text": "macht noch keinen Gewinn."
          },
          {
            "key": "c",
            "text": "wird bald ausgebaut."
          }
        ],
        "loesung": "b"
      },
      {
        "frage": "Der neue Auszubildende",
        "optionen": [
          {
            "key": "a",
            "text": "beendet demnächst die Schule."
          },
          {
            "key": "b",
            "text": "ist das erste Mal im Betrieb."
          },
          {
            "key": "c",
            "text": "wird in sechs Monaten anfangen."
          }
        ],
        "loesung": "c"
      },
      {
        "frage": "Der Geschäftsführer",
        "optionen": [
          {
            "key": "a",
            "text": "berichtet von Problemen im Gewächshaus."
          },
          {
            "key": "b",
            "text": "plant im Sommer einen Geschäftsbesuch."
          },
          {
            "key": "c",
            "text": "verschiebt den Termin einer Veranstaltung."
          }
        ],
        "loesung": "c"
      }
    ]
}
  

Example 4:

{
    "meeting_note": "## Protokoll\n\n**15. März 20XX, 9:00 – 10:30 Uhr**\n**Ort: Konferenzraum 2, Karlingerstraße 15, 75347 Holzhausen**\n\n**Anwesende:**\n*   Christine Belarz (CB, Klinikleiterin)\n*   Michael Ahlers (MA, Personalleiter)\n*   Ramona Hartmann (RH, Leiterin der Station 3)\n*   Tanja Schmied (TS, Verwaltungsleiterin)\n*   Andrey Petruk (AP, Pflegeleitung)\n*   Thomas Bringhaus (TB, Technik)\n*   Dr. Fatma Schüler (FS, Innere Medizin)\n*   Aigul Kohrmann (AK, Sekretariat)\n\n**Sitzungsleitung:** Michael Ahlers\n**Protokollantin:** Aigul Kohrmann\n\n**Tagesordnungspunkte**\n\n1.  Begrüßung und Genehmigung des letzten Protokolls\n2.  Personelles\n3.  Renovierung der Station 4\n4.  Probleme auf der Station 3\n5.  Erfahrungsbericht mit der neuen Software\n6.  Sonstiges\n\n**TOP 1 Begrüßung und Genehmigung des letzten Protokolls**\n\nMA begrüßt Frau Belarz und alle anwesenden Mitarbeitenden zur heutigen Sitzung und entschuldigt sich für die Verspätung durch einen anderen Termin. Das Protokoll vom 2. Februar wird durch Handzeichen ohne Einwände einstimmig angenommen.\n\n**TOP 2 Personelles**\n\nMA weist darauf hin, dass in der Unfallstation zwei Kolleginnen zum 30. April in Rente gehen und noch kein Ersatz eingestellt wurde. Der generelle Personalmangel in der Pflege wurde laut MA schon oft diskutiert, familienfreundlichere Arbeitszeiten machen die Klinik als Arbeitgeber aber attraktiv. Im Verlauf des nächsten halben Jahres werden vier weitere Mitarbeitende im Pflegedienstbereich eingestellt.\n\n**TOP 3 Renovierung der Station 4**\n\nFS berichtet vom Stand der Dinge: Mehr als die Hälfte der Zimmer, in denen die Bäder durch den häufigen Gebrauch von Desinfektionsmitteln unansehnlich geworden waren, und die teilweise auch beschädigte Waschbecken und Fliesen hatten, wurden bereits renoviert. Bis Mitte April sollen alle Arbeiten dort abgeschlossen werden. Danach wird der Flur der Station in freundlichen Farben gestrichen. Dafür liegen bereits Angebote von zwei Malerbetrieben vor.\n\n**TOP 4 Probleme auf der Station 3**\n\nAP und RH bemängeln, dass es auf der Geburtenstation immer wieder Probleme mit jungen Vätern gibt, die manchmal spät abends angetrunken auf die Station kommen, um Mutter und Kind zu besuchen. Das ist natürlich verboten und stört andere Mütter und das Personal. Manche übertreiben es auch mit Blumensträußen, sodass es in einigen Krankenzimmern wie in einer Gärtnerei aussehe. Die Krankenhausregeln müssen klarer kommuniziert werden.\n\n**TOP 5 Erfahrungsbericht mit der neuen Software**\n\nAK berichtet über ihre Erfahrungen mit der neuen Software für die Aufnahme neuer Patientinnen und Patienten. Sie ist insgesamt zufrieden damit. Nur die Verbindung zur Medikamentendatenbank mache manchmal Probleme. Die Software-Firma ist schon verständigt.\n\n**TOP 6 Sonstiges**\n\nCB lobt den gelungenen Umbau der Cafeteria im Erdgeschoss von Haus 5. Die große Glasfront zur Terrasse lässt viel Licht herein und der Übergang zur Terrasse ist jetzt barrierefrei. Die freundliche Atmosphäre lädt auch das Personal ein, hier die Pausen zu verbringen. CB weist dringend darauf hin, sich hier nicht über vertrauliche Patienteninformationen zu unterhalten.\nKommenden Freitagnachmittag lädt der Personalleiter dort die Auszubildenden anlässlich ihrer bestandenen Prüfung zu Kaffee und Kuchen ein. Die Stationsleitungen sollen das in der Arbeitszeitplanung berücksichtigen.",
    "aufgaben_list": [
      {
        "frage": "Die heutige Sitzung",
        "optionen": [
          {
            "key": "a",
            "text": "dauert zwei Stunden."
          },
          {
            "key": "b",
            "text": "muss pünktlich enden."
          },
          {
            "key": "c",
            "text": "wurde zweimal verschoben."
          }
        ],
        "loesung": "b"
      },
      {
        "frage": "Die Praktikantin",
        "optionen": [
          {
            "key": "a",
            "text": "hat noch keine Berufserfahrung."
          },
          {
            "key": "b",
            "text": "spricht im Anschluss Termine ab."
          },
          {
            "key": "c",
            "text": "wird in der Personalabteilung arbeiten."
          }
        ],
        "loesung": "b"
      },
      {
        "frage": "Die Produktion der Saisonartikel",
        "optionen": [
          {
            "key": "a",
            "text": "erfolgt mit zusätzlichem Personal."
          },
          {
            "key": "b",
            "text": "hat bereits pünktlich begonnen."
          },
          {
            "key": "c",
            "text": "verzögert sich wegen fehlender Zutaten."
          }
        ],
        "loesung": "a"
      },
      {
        "frage": "Die neue Produktionsstätte",
        "optionen": [
          {
            "key": "a",
            "text": "geht in 6 Monaten in Betrieb."
          },
          {
            "key": "b",
            "text": "kann bis zu 30 km entfernt liegen."
          },
          {
            "key": "c",
            "text": "wird voraussichtlich in Thüringen gebaut."
          }
        ],
        "loesung": "b"
      },
      {
        "frage": "Der Geschäftsführer",
        "optionen": [
          {
            "key": "a",
            "text": "erläutert den Dienstplan zwischen Weihnachten und Neujahr."
          },
          {
            "key": "b",
            "text": "informiert über die Weihnachtsaktion."
          },
          {
            "key": "c",
            "text": "will anstelle der Feier Geld spenden."
          }
        ],
        "loesung": "b"
      }
    ]
}
  

Example 5:

{
    "meeting_note": "## Protokoll\n\n**15. Juli 20XX, 10:00–11:00 Uhr**\n**Ort: Raum 471, Rostocker Chaussee 10, 17628 Grabenow**\n\n**Anwesende:**\n*   Heide Wessely (HW, Geschäftsführung)\n*   Roman Lauf (RL, Assistenz Geschäftsführung)\n*   Ottmar Peters (OP, Abteilungsleiter Marketing)\n*   Andrea Olms (AO, Abteilungsleiterin IT)\n*   Frank Traube (FT, Abteilungsleiter Einkauf)\n*   Ingmar Kves (IK, Abteilungsleiter Logistik)\n\n**Sitzungsleitung:** Heide Wessely\n**Protokollant:** Roman Lauf\n\n**Tagesordnungspunkte**\n\n1.  Begrüßung, Genehmigung des letzten Protokolls\n2.  Berichte aus den Abteilungen\n3.  Baumaßnahmen Rostocker Chaussee\n4.  Stand Homepage\n5.  Termine\n6.  Verschiedenes\n\n**TOP 1 Begrüßung, Genehmigung des letzten Protokolls**\n\nNach der Begrüßung durch HW wird die Tagesordnung einstimmig beschlossen. OP meldet sich zum Protokoll der letzten Sitzung zu Wort und weist darauf hin, dass unter TOP 5 ein falscher Termin für die Schiffbauermesse steht. Nach Korrektur des Termins erfolgt einstimmig die Abnahme des Protokolls.\n\n**TOP 2 Berichte aus den Abteilungen**\n\nHW weist auf die Berichte hin, die vorab an alle Teilnehmenden verschickt wurden, und bittet um Fragen oder Anmerkungen. FT greift den Bericht der IT-Abteilung auf. Die Datenbank zur Erfassung der Lagerbestände habe sich seit ihrer Einführung vor einem Jahr bewährt. FT weist auf Probleme beim Log-in hin, die er kürzlich hatte. Diese Probleme seien jetzt zwar gelöst, er bittet aber darum, dies der Vollständigkeit halber in dem Bericht zu ergänzen. AO sagt zu, den Bericht entsprechend zu ändern.\n\n**TOP 3 Baumaßnahmen Rostocker Chaussee**\n\nIK informiert über die kurzfristig geplante Fahrbahnerneuerung auf der Rostocker Chaussee, die laut Bauamt bereits im August erfolgen soll. Dafür wird es notwendig sein, die Rostocker Chaussee für eine Fahrbahn zu sperren und eine Ampel für Wechselverkehr einzurichten. Wie lange die Sperrung dauert, ist noch nicht bekannt. Das bedeute logistische Herausforderungen, so IK. Es werde aufgrund der Sperrung zu längeren Fahrzeiten bei An- und Auslieferungen kommen und es stelle sich die Frage, ob die Zufahrt während der Baumaßnahmen auch für große Fahrzeuge möglich sein wird. IK soll sich umgehend mit dem Bauamt in Verbindung setzen, um diese Punkte zu klären. Ein Bericht darüber soll zur Information für alle ins Intranet gestellt werden.\n\n**TOP 4 Stand Homepage**\n\nWie auf der letzten Sitzung beschlossen, hat AO Angebote eingeholt und im Vorfeld dieser Sitzung drei Angebote präsentiert, die in die engere Auswahl kommen. Alle Firmen haben Erfahrung darin, einen Webshop für Großkunden auf einer Homepage zu integrieren, was die zentrale Neuerung bei uns sein wird. AO hält die zuverlässige Abwicklung der Arbeiten dabei für wichtiger, als nur auf die Kosten zu achten. OP stimmt zu und weist darauf hin, dass bereits zahlreiche Kunden angefragt haben, wann es bei uns die Möglichkeit des Online-Einkaufs geben wird. Das Thema sei für die Kunden entscheidend, so OP, und wir sollten dies schnell und qualitativ hochwertig umsetzen lassen. Unter Berücksichtigung dieser Aspekte wird einstimmig beschlossen, der Firma Sasaki Systems den Zuschlag zu erteilen.\n\n**TOP 5 Termine**\n\nIm kommenden Januar unternehmen FT und OP eine Geschäftsreise nach Busan (Südkorea), um dort eine Schiffswerft zu besichtigen, die an einer Zusammenarbeit interessiert ist.\n\n**TOP 6 Verschiedenes**\n\nHW berichtet von einer Anfrage, im kommenden Jahr einen Tag der Berufsorientierung für Schülerinnen und Schüler durchzuführen. Sie halte dies für interessant und werde auf der nächsten Sitzung genauer darüber informieren.",
    "aufgaben_list": [
      {
        "frage": "Das Protokoll",
        "optionen": [
          {
            "key": "a",
            "text": "führt heute ein Abteilungsleiter."
          },
          {
            "key": "b",
            "text": "wird nach Änderung genehmigt."
          },
          {
            "key": "c",
            "text": "wird um einen TOP erweitert."
          }
        ],
        "loesung": "b"
      },
      {
        "frage": "Der Bericht der IT-Abteilung",
        "optionen": [
          {
            "key": "a",
            "text": "beschreibt Schwierigkeiten."
          },
          {
            "key": "b",
            "text": "soll korrigiert werden."
          },
          {
            "key": "c",
            "text": "wird in der Sitzung verteilt."
          }
        ],
        "loesung": "b"
      },
      {
        "frage": "Die Fahrbahnerneuerung vor dem Firmengelände",
        "optionen": [
          {
            "key": "a",
            "text": "bereitet der Logistik Probleme."
          },
          {
            "key": "b",
            "text": "betrifft die Firma kaum."
          },
          {
            "key": "c",
            "text": "dauert nicht mehr lange."
          }
        ],
        "loesung": "a"
      },
      {
        "frage": "Die Homepage der Firma",
        "optionen": [
          {
            "key": "a",
            "text": "ist von vielen Kunden kritisiert worden."
          },
          {
            "key": "b",
            "text": "kostet der Marketingleitung zu viel."
          },
          {
            "key": "c",
            "text": "wird um einen wichtigen Bereich erweitert."
          }
        ],
        "loesung": "c"
      },
      {
        "frage": "Im nächsten Jahr",
        "optionen": [
          {
            "key": "a",
            "text": "besuchen Mitarbeiter eine andere Firma."
          },
          {
            "key": "b",
            "text": "kommen Gäste zu Besuch."
          },
          {
            "key": "c",
            "text": "kooperiert der Betrieb mit einer Schule."
          }
        ],
        "loesung": "a"
      }
    ]
}
  

Example 6:

{
    "meeting_note": "## Protokoll\n\n**7. Mai 20.., 8:30–9:30 Uhr**\n**Ort: Besprechungszimmer 2, Max-Reiter-Weg 4, 95139 Süßheim**\n\n**Anwesende:**\n*   Max Quirin (MQ, Geschäftsführung)\n*   Sara Nakamura (SN, Leitung Produktion)\n*   Günter Lorenz (GL, Leitung Qualitätskontrolle)\n*   Paula Raabe (PR, Leitung Einkauf)\n*   Tassilo Wüst (TW, Leitung Verkauf)\n*   Marie Steinberg (MS, Leitung Finanzen)\n*   Dirk Pätsch (DP, Leitung Personal)\n*   Klaus Schranz (KS, Leitung Marketing)\n*   Gast: Nieva Escarda (NE, Praktikantin)\n\n**Protokollant:** Günter Lorenz\n\n**Tagesordnungspunkte**\n\n1.  Begrüßung, Termine und Genehmigung des letzten Protokolls\n2.  Personelles\n3.  Aktuelle Lage in der Produktion\n4.  Stand Produktionsstätte II\n5.  Berichte\n6.  Sonstiges\n\n**TOP 1 Begrüßung, Termine und Genehmigung des letzten Protokolls**\n\nMQ begrüßt alle Anwesenden, lobt das pünktliche und vollständige Erscheinen und kündigt an, dass die Sitzung wegen eines wichtigen Außentermins heute auf keinen Fall länger als bis 09:30 Uhr dauern kann. Nach Diskussion zweier Termine wird die nächste Sitzung auf den 21. Mai, 8:30 Uhr bis 10:30 Uhr gelegt. Das Protokoll der letzten Sitzung wird nach einer kurzen Diskussion genehmigt.\n\n**TOP 2 Personelles**\n\nDP stellt Frau Escarda vor, die neue Halbjahrespraktikantin. NE studiert Betriebswirtschaft und stammt ursprünglich von den Philippinen, wo sie mehrere Jahre in einem Hotel als Rezeptionistin tätig war. In den nächsten Wochen soll sie alle Abteilungen kennenlernen und macht dafür anschließend an die Sitzung mit der jeweiligen Leitung Zeiten aus.\n\n**TOP 3 Aktuelle Lage in der Produktion**\n\nSN stellt fest, dass wegen des im Vergleich zum letzten Jahr erfreulich hohen Auftragsvolumens dieses Jahr schon ab KW 25 mit der Produktion der Lebkuchen und sonstigen saisonalen Waren begonnen werden muss. PR ergänzt, dass die Zulieferer alle erforderlichen Zutaten in ausreichender Menge zugesagt haben und die entsprechenden Bestellungen schon getätigt worden sind, sodass die Ware rechtzeitig angeliefert werden kann. DP berichtet, dass er für diese Produktionsphase bei der Zeitarbeitsfirma flexibelhelp, mit der wir seit Jahren gut zusammenarbeiten, fünf Aushilfskräfte angefordert hat.\n\n**TOP 4 Stand Produktionsstätte II**\n\nMQ berichtet über die Erweiterungspläne der Firma. Die zweite Produktionsstätte wird nun doch nicht in Süßheim angemietet werden, da hier die Gewerbemieten zu hoch sind. Damit kann auch der ursprünglich geplante Eröffnungstermin in einem halben Jahr nicht gehalten werden. MQ hat einen Immobilienmakler beauftragt, die Lage im benachbarten Thüringen zu prüfen, da dort die Mieten deutlich niedriger liegen. Es wird aber auf jeden Fall ein Standort in weniger als 30 km Entfernung gesucht.\n\n**TOP 5 Berichte**\n\nKS zeigt das Werbevideo, das produziert wurde, um wieder vermehrt auch jüngere Zielgruppen für unsere Produkte zu interessieren. Es bekam großen Beifall und wird ab nächste Woche online über verschiedene Kanäle ausgestrahlt werden. Außerdem ist KS auf der Suche nach einem Influencer, der Werbung für unseren Adventskalender macht. Details dazu dann in der nächsten Sitzung.\n\n**TOP 6 Sonstiges**\n\nAbschließend gibt MQ bekannt, dass unsere externen freien Mitarbeiter*innen dieses Jahr anstelle eines Lebkuchenpakets aus unserer Produktion elektronische Grußkarten bekommen werden. Diese enthalten die Mitteilung, dass das Geld für Projekte in den Kakaoanbaugebieten unserer Zulieferer gespendet wird. Diese Projekte fördern insbesondere die Ausbildung von Mädchen. Er kündigt im Sinne einer langfristigen Terminplanung außerdem vorab schon einmal an, dass die Weihnachtsfeier wie üblich am letzten Freitag vor Heiligabend stattfindet und die Firma auch dieses Jahr zwischen dem 24.12. und dem 1.1. geschlossen bleiben wird.",
    "aufgaben_list": [
      {
        "frage": "Die Sitzung heute",
        "optionen": [
          {
            "key": "a",
            "text": "dauert zwei Stunden."
          },
          {
            "key": "b",
            "text": "muss pünktlich enden."
          },
          {
            "key": "c",
            "text": "wurde zweimal verschoben."
          }
        ],
        "loesung": "b"
      },
      {
        "frage": "Die Praktikantin",
        "optionen": [
          {
            "key": "a",
            "text": "hat noch keine Berufserfahrung."
          },
          {
            "key": "b",
            "text": "spricht im Anschluss Termine ab."
          },
          {
            "key": "c",
            "text": "wird in der Personalabteilung arbeiten."
          }
        ],
        "loesung": "b"
      },
      {
        "frage": "Die Produktion der Saisonartikel",
        "optionen": [
          {
            "key": "a",
            "text": "erfolgt mit zusätzlichem Personal."
          },
          {
            "key": "b",
            "text": "hat bereits pünktlich begonnen."
          },
          {
            "key": "c",
            "text": "verzögert sich wegen fehlender Zutaten."
          }
        ],
        "loesung": "a"
      },
      {
        "frage": "Die neue Produktionsstätte",
        "optionen": [
          {
            "key": "a",
            "text": "geht in 6 Monaten in Betrieb."
          },
          {
            "key": "b",
            "text": "kann bis zu 30 km entfernt liegen."
          },
          {
            "key": "c",
            "text": "wird voraussichtlich in Thüringen gebaut."
          }
        ],
        "loesung": "b"
      },
      {
        "frage": "Der Geschäftsführer",
        "optionen": [
          {
            "key": "a",
            "text": "erläutert den Dienstplan zwischen Weihnachten und Neujahr."
          },
          {
            "key": "b",
            "text": "informiert über die Weihnachtsaktion."
          },
          {
            "key": "c",
            "text": "will anstelle der Feier Geld spenden."
          }
        ],
        "loesung": "b"
      }
    ]
}"""),
        ],
    )
    output = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if chunk.text is not None:
            output += chunk.text
            if debug:
                print(chunk.text, end="")
        else:
            # print(f"Chunk is None: {chunk}")
            break
    return output

def format_json(json_str):
    # find the json part in the string
    json_start = json_str.find("```json")
    if json_start == -1:  # If "```json" is not found, try just "```"
        json_start = json_str.find("```")
        if json_start == -1:  # If no markdown code blocks at all
            return json.loads(json_str)  # Try parsing the entire string
        json_start += 3  # Skip past the "```"
    else:
        json_start += 7  # Skip past the "```json"
    
    json_end = json_str.find("```", json_start)
    if json_end == -1:  # If no closing code block
        extracted_json = json_str[json_start:]  # Take everything after the opening marker
    else:
        extracted_json = json_str[json_start:json_end]  # Extract only the JSON content
    
    # Clean up the extracted JSON to handle potential issues
    extracted_json = extracted_json.strip()
    
    try:
        return json.loads(extracted_json)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"JSON content: {extracted_json[:100]}...")  # Print part of the content for debugging
        raise


def verify_json_structure(json_data):
    """
    Verifies that the JSON data follows the expected structure for a meeting note mocktest.
    
    Returns:
        tuple: (is_valid, message) where is_valid is a boolean and message is an error message or None
    """
    # Check if json_data is a dictionary
    if not isinstance(json_data, dict):
        return False, "JSON data is not a dictionary"
    
    # Check if meeting_note exists and is a string
    if "meeting_note" not in json_data:
        return False, "Missing 'meeting_note' field"
    if not isinstance(json_data["meeting_note"], str):
        return False, "'meeting_note' must be a string"
    if not json_data["meeting_note"].strip():
        return False, "'meeting_note' cannot be empty"
    
    # Check if aufgaben_list exists and is a list
    if "aufgaben_list" not in json_data:
        return False, "Missing 'aufgaben_list' field"
    if not isinstance(json_data["aufgaben_list"], list):
        return False, "'aufgaben_list' must be a list"
    
    # Check if aufgaben_list has exactly 5 items
    if len(json_data["aufgaben_list"]) != 5:
        return False, f"'aufgaben_list' must contain exactly 5 items, found {len(json_data['aufgaben_list'])}"
    
    # Check each item in aufgaben_list
    for i, aufgabe in enumerate(json_data["aufgaben_list"]):
        # Check if aufgabe is a dictionary
        if not isinstance(aufgabe, dict):
            return False, f"Item {i+1} in 'aufgaben_list' is not a dictionary"
        
        # Check if frage exists and is a string
        if "frage" not in aufgabe:
            return False, f"Missing 'frage' field in item {i+1}"
        if not isinstance(aufgabe["frage"], str):
            return False, f"'frage' in item {i+1} must be a string"
        if not aufgabe["frage"].strip():
            return False, f"'frage' in item {i+1} cannot be empty"
        
        # Check if optionen exists and is a list
        if "optionen" not in aufgabe:
            return False, f"Missing 'optionen' field in item {i+1}"
        if not isinstance(aufgabe["optionen"], list):
            return False, f"'optionen' in item {i+1} must be a list"
        
        # Check if optionen has exactly 3 items
        if len(aufgabe["optionen"]) != 3:
            return False, f"'optionen' in item {i+1} must contain exactly 3 items, found {len(aufgabe['optionen'])}"
        
        # Check each option
        expected_keys = ['a', 'b', 'c']
        option_keys = []
        
        for j, option in enumerate(aufgabe["optionen"]):
            # Check if option is a dictionary
            if not isinstance(option, dict):
                return False, f"Option {j+1} in item {i+1} is not a dictionary"
            
            # Check if key exists and is a string
            if "key" not in option:
                return False, f"Missing 'key' field in option {j+1} of item {i+1}"
            if not isinstance(option["key"], str):
                return False, f"'key' in option {j+1} of item {i+1} must be a string"
            if option["key"] not in expected_keys:
                return False, f"'key' in option {j+1} of item {i+1} must be one of {expected_keys}, found '{option['key']}'"
            
            option_keys.append(option["key"])
            
            # Check if text exists and is a string
            if "text" not in option:
                return False, f"Missing 'text' field in option {j+1} of item {i+1}"
            if not isinstance(option["text"], str):
                return False, f"'text' in option {j+1} of item {i+1} must be a string"
            if not option["text"].strip():
                return False, f"'text' in option {j+1} of item {i+1} cannot be empty"
        
        # Check if all option keys are unique and contain all expected keys
        if set(option_keys) != set(expected_keys):
            return False, f"Option keys in item {i+1} must include exactly 'a', 'b', and 'c'"
        
        # Check if loesung exists and is a string
        if "loesung" not in aufgabe:
            return False, f"Missing 'loesung' field in item {i+1}"
        if not isinstance(aufgabe["loesung"], str):
            return False, f"'loesung' in item {i+1} must be a string"
        if aufgabe["loesung"] not in expected_keys:
            return False, f"'loesung' in item {i+1} must be one of {expected_keys}, found '{aufgabe['loesung']}'"
    
    return True, None

def generate_mocktest():
    json_str = generate(debug=True)
    json_data = format_json(json_str)
    is_valid, message = verify_json_structure(json_data)
    if not is_valid:
        print(f"Invalid JSON structure: {message}")
        raise Exception(f"Invalid JSON structure: {message}")
    return json_data

if __name__ == "__main__":
    # Generate 100 more mocktests. 
    idx = 0
    while idx < 100:
        try:
            mocktest = generate_mocktest()
            with open(f"/Users/binhnguyen/Workspaces/TELC_B2_test/data_mocktest/lesen/teil_4/mocktest_generated_{idx + 7}.json", "w", encoding="utf-8") as f:
                json.dump(mocktest, f, indent=4, ensure_ascii=False)
            idx += 1
        except Exception as e:
            print(f"Error generating mocktest {idx}: {e}")