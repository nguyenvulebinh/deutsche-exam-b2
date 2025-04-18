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
                types.Part.from_text(text="""In the first step, generate the markdown for thema and idea about the text content. 

In the second step generate markdown for the idea about the questions and the distractor. 
- With task 1: Richtig/Falsch, generate 1 comprehensive candidate for Richtig, one comprehensive candiate for Falsch, pick a random a canditate in the final task (prefer richtig more than falsch). 
- With task 2: Multiple Choice, generate the ideas about the question or incomplete sentence stem, then carefully generate comprehensive options.

In the third step, generate the json format for the final mocktest. Fowllow exactly the same structure as the example in the system instruction 

*Mocktest have to be in json format starting with ```json and ending with ```*"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1.5,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""**Guideline for Creating a TELC B2 Lesen Teil 2 Exercise**

**Persona:** Act as an examiner creating materials for the \"Test für den Beruf B2: Einweisungen und Unterweisungen verstehen\". Your goal is to create realistic comprehension tasks based on typical workplace information, mirroring the style, difficulty, and format of provided examples.

**Task:** Generate a complete German reading comprehension exercise.

**Core Requirements:**

1.  **Overall Theme:** The exercise must fit under the umbrella theme: **\"Willkommensmappe für neue Mitarbeiterinnen und Mitarbeiter\"** (Welcome Pack for New Employees).

2.  **Language Level & Text Difficulty (B2 CEFR):**
    *   The text and questions must be suitable for the **B2 CEFR level**.
    *   **Vocabulary:** Include specific, relevant workplace terminology (e.g., *Urlaubsvertretung, Desk-Sharing, Zeiterfassungssystem, Gemeinschaftsküche, Schutzkittel*) alongside standard B2 vocabulary.
    *   **Grammar:** Utilize typical B2 structures, such as complex sentences with various subordinate clauses (dass, wenn, damit, weil, obwohl etc.), passive voice where natural (e.g., *werden getragen, muss beachtet werden*), modal verbs, and consistent use of the formal \"Sie\" address.
    *   **Content Style:** Focus on conveying specific rules, procedures, conditions, or information pertinent to a workplace setting. The text should be **information-dense**, providing concrete details rather than general descriptions. It needs to read like an authentic excerpt from internal company communication or guidelines.

3.  **Text Generation:**
    *   **Topic Selection:** Choose **one specific, realistic workplace topic** relevant to new employees (e.g., IT Usage Policy, Meeting Room Booking, Health & Safety, Company Benefits, Sickness Reporting, Canteen Rules, Internal Communication, Data Protection, Company Events, Code of Conduct, Time Tracking).
    *   **Length:** Aim for a text length of approximately **180-280 words**, typically structured into **3-5 paragraphs**.
    *   **Content:** Write the German text explaining the chosen topic, ensuring it contains multiple distinct pieces of specific information (rules, times, locations, responsibilities, procedures, conditions, exceptions).
    *   **Clarity for Questions:** The text *must* provide enough specific, unambiguous detail so that both comprehension questions can be answered *solely and definitively* based on the information explicitly given. Avoid vagueness. Ensure there's enough distinct information to form both a R/F question and a MC question with good distractors.

4.  **Task Generation:** Based *only* on the generated text, create exactly **two** comprehension tasks:

    *   **Task 1: Richtig/Falsch**
        *   **Stem Construction:** Formulate one clear, **concise statement (typically 10-15 words)**.
        *   **Solution:** This statement must be definitively **true (richtig)** or **false (falsch)** according to the information given *only* in the text.
        *   **Making it Require Careful Thought (Tricks):** The statement should **not** be a simple copy-paste. Design it to test close reading and understanding by using one of these techniques:
            *   **Synthesis/Combination:** Combine explicitly stated information from *two or more different sentences* into a single statement, requiring the reader to connect the points.
            *   **Paraphrasing:** Rephrase a specific rule/detail using different vocabulary or sentence structure, requiring recognition of synonymous meaning.
            *   **Generalization/Summary:** Create a statement summarizing the overall implication of several specific details/examples from the text.
            *   **Absolute Claims vs. Specifics (Often leads to 'Falsch'):** Make a broad/absolute statement (using *alle, immer, nie, nur, keine*) contradicted by specific conditions, exceptions, or limitations mentioned in the text.
            *   **Implication by Omission (Often leads to 'Falsch'):** State something exists/is possible within a described system, when the text details that system but *omits* this specific thing, implying its absence.
            *   **Focus on Subtle Distinctions:** Base the statement on a fine difference or specific condition mentioned in the text that could be easily overlooked.

    *   **Task 2: Multiple Choice**
        *   **Question Stem Construction:**
            *   Formulate a clear, **short question or incomplete sentence stem (typically 5-12 words)**.
            *   Target a **specific detail, condition, reason, consequence, procedure, permission, or restriction** explicitly mentioned in the text. Use structures like \"Wer...\", \"Wenn...\", \"Sie dürfen/müssen...\", \"Die [Subject]...\", \"Der/Die [Role]...\".
            *   Ensure the question is *unambiguously answerable* using only the text.
        *   **Option Construction:**
            *   Provide **three options (a, b, c)**. Each option should be **relatively concise (typically 5-15 words)**.
            *   **Correct Option:** Exactly one option must be correct, accurately reflecting or paraphrasing the specific information targeted by the stem, as stated in the text.
            *   **Distractor Options (Incorrect):** The other two options must be **plausible but definitively incorrect** distractors *based solely on the text*. Create them using these techniques:
                *   **Use Keywords, Change Meaning:** Reuse keywords from the text but place them in a context that contradicts the text's details (wrong time/person/condition, opposite meaning).
                *   **Contradict Explicit Details:** Directly state the opposite of a specific fact mentioned.
                *   **Misattribute Information:** Apply a detail true for one context/person/item incorrectly to the subject of the question.
                *   **Introduce Incorrect Specifics:** Change numbers, durations, frequencies, locations, or sequences.
                *   **Overgeneralize/Understate:** Make a statement too broad (*alle, immer*) or too narrow/absolute when the text provides conditions/exceptions (or vice versa).
                *   **Misrepresent Modality:** Confuse obligation (müssen), recommendation (sollten), possibility (können), or entitlement (Anspruch).
                *   **Invent Plausible but Unstated Details:** Create an option logical within the context but not mentioned/supported by the specific text.
            *   **Avoid:** Options that are illogical, require outside knowledge, or are unrelated to the text. Difficulty must stem from careful text reading.

5.  **Solution Specification:** Clearly indicate the correct solution for both tasks (\"richtig\"/\"falsch\" and \"a\"/\"b\"/\"c\").

6.  **Output Format:** Structure the entire output as a **single JSON object**. Use the following precise keys and structure:

```json
{
  \"thema\": \"Willkommensmappe für neue Mitarbeiterinnen und Mitarbeiter\",
  \"text\": \"## [Generated Text Title in German]\\n\\n[Generated German text, paragraph 1]\\n\\n[Generated German text, paragraph 2]\\n\\n[Generated German text, paragraph 3-5... Use Markdown for paragraphs/structure]\",
  \"Aufgaben\": [
    {
      \"type\": \"richtig/falsch\",
      \"frage\": \"[Generated Richtig/Falsch statement in German]\",
      \"loesung\": \"[Correct solution: 'richtig' or 'falsch']\"
    },
    {
      \"type\": \"multiple-choice\",
      \"frage\": \"[Generated Multiple-Choice question stem in German]\",
      \"optionen\": [
        {
          \"key\": \"a\",
          \"text\": \"[Generated Option A text in German]\"
        },
        {
          \"key\": \"b\",
          \"text\": \"[Generated Option B text in German]\"
        },
        {
          \"key\": \"c\",
          \"text\": \"[Generated Option C text in German]\"
        }
      ],
      \"loesung\": \"[Correct solution: 'a', 'b', or 'c']\"
    }
  ]
}
```

Example 1:

{
    \"thema\": \"Willkommensmappe für neue Mitarbeiterinnen und Mitarbeiter\",
    \"text\": \"## Sicherheit im Labor beachten:\\n\\n### LABORKLEIDUNG\\n\\nBeim Arbeiten im Labor muss eine angemessene Kleidung getragen werden, um einerseits sich selbst, andererseits auch bestimmte Materialien zu schützen. Dazu gehört zunächst ein weißer Schutzkittel aus Baumwolle, der immer geschlossen und sauber sein muss.\\n\\nDa ein Kittel nicht den ganzen Körper schützt, ist darauf zu achten, dass stets geschlossenes, festes Schuhwerk (keine hohen Absätze oder offene Sandalen) sowie lange Hosen zu tragen sind. Das feste, flache Schuhwerk dient nebenbei auch dem Zweck, in Notsituationen das Labor zügig verlassen zu können.\\n\\nAus hygienischen Gründen müssen auch die Haare durch eine Haube bedeckt sein. Lange Haare müssen zusätzlich zu einem Zopf zusammengebunden werden. Häufig kommt auch noch eine Schutzbrille zum Einsatz.\\n\\nBeim Hantieren mit empfindlichen oder gefährlichen Substanzen sind Handschuhe zu tragen, um die Hände vor Kontamination zu schützen. Das heißt jedoch nicht, dass die Handschuhe bei Arbeitsbeginn im Labor angezogen und erst wieder abends ausgezogen werden. Da die Handschuhe durch die Arbeit mit chemischen Substanzen verunreinigt sein könnten, sollten diese nach durchgeführter Arbeit stets abgelegt und nicht auch noch während anderer Tätigkeiten im Labor getragen werden. Auf keinen Fall darf das Labor mit Handschuhen verlassen werden.\",
    \"Aufgaben\": [
      {
        \"type\": \"richtig/falsch\",
        \"frage\": \"Beim Arbeiten im Labor darf man weder kurze Hosen tragen noch längere Haare offen lassen.\",
        \"loesung\": \"richtig\"
      },
      {
        \"type\": \"multiple-choice\",
        \"frage\": \"Im Labor müssen Handschuhe\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"bei allen Arbeiten getragen werden.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"gleich bei Arbeitsantritt angelegt werden.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"nach Arbeiten mit Chemikalien ausgezogen werden.\"
          }
        ],
        \"loesung\": \"c\"
      }
    ]
}
  
Example 2:

{
    \"thema\": \"Willkommensmappe für neue Mitarbeiterinnen und Mitarbeiter\",
    \"text\": \"## Gemeinschaftsveranstaltungen\\n\\nNeben zahlreichen Sozialleistungen bietet unser Unternehmen alljährlich zwei Gemeinschaftsveranstaltungen an. Immer am dritten Mittwoch im Mai findet unser eintägiger Betriebsausflug statt, der sowohl einen kulturellen als auch einen sportlichen Teil enthält und mit einem Essen abschließt. Den Organisationsausschuss bilden stets zwei langjährige und zwei neue Mitarbeiterinnen oder Mitarbeiter. Die Geschäftsleitung stellt ein festgelegtes Budget zur Verfügung, die Kosten für alkoholische Getränke trägt jeder Mitarbeiter selbst.\\n\\nNach einer Umfrage unter unseren Mitarbeiterinnen und Mitarbeitern entschieden wir uns aufgrund der Arbeitsdichte zum Jahresabschluss, der religiösen Vielfalt in unseren Teams und der hohen Termindichte in der Vorweihnachtszeit dazu, ein Sommerfest statt einer Weihnachtsfeier zu veranstalten. Dieses findet immer eine Woche vor den Betriebsferien statt. Feste Programmpunkte sind dabei ein gutes Essen, das Überreichen eines Preises an den Mitarbeiter mit der \"Idee des Jahres\" und Tanz zu Live-Musik. Anders als beim Betriebsausflug können wichtige Geschäftspartner als geladene Gäste daran teilnehmen.\\n\\n## Betriebssport\\n\\nSportliche Aktivitäten werden bei uns großgeschrieben. Die Laufgruppe hat sogar schon an einem\",
    \"Aufgaben\": [
      {
        \"type\": \"richtig/falsch\",
        \"frage\": \"Zu allen Gemeinschaftsveranstaltungen dürfen Gäste mitgebracht werden.\",
        \"loesung\": \"falsch\"
      },
      {
        \"type\": \"multiple-choice\",
        \"frage\": \"Der Arbeitgeber veranstaltet ein Sommerfest,\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"da man in den Betriebsferien gut feiern kann.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"das von ausgewählten Mitarbeitern organisiert wird.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"weil die meisten Mitarbeiter im Dezember viele Termine haben.\"
          }
        ],
        \"loesung\": \"c\"
      }
    ]
}
  

Example 3:

{
    \"thema\": \"Willkommensmappe für neue Mitarbeiter*innen\",
    \"text\": \"## Bürostrukturen\\n\\nWie Sie wissen, haben Sie Anspruch auf drei Tage Homeoffice pro Woche. Für die Zeit, in der Sie im Unternehmen arbeiten (Präsenztage), bieten wir Ihnen im Rahmen des \"Desk-Sharings\" flexible Arbeitsplätze.\\n\\nIn unserem Großraumbüro stehen acht Schreibtische mit gleicher Ausstattung inklusive Steckdosen und USB-Anschlüssen, die von allen Teammitgliedern genutzt werden können. Die Schreibtische sind frei wählbar – nach dem Prinzip \"Wer zuerst kommt, mahlt zuerst\".\\n\\nDamit das \"Desk-Sharing\" funktioniert, bitten wir Sie, einige Richtlinien zu beachten: Belegen Sie einen Schreibtisch bitte nur, wenn Sie wirklich daran arbeiten. Das heißt, dass der Arbeitsplatz auch für längere Pausen wieder geräumt werden muss. Für Ihre Unterlagen und Ihre persönlichen Gegenstände erhalten Sie einen Rollcontainer zur alleinigen Nutzung.\\n\\nNeben dem Großraumbüro stehen Ihnen im ersten Stock mehrere Besprechungsräume und kleine Büros, in denen Sie Telefonate führen können, zur Verfügung. Auch der Pausenraum kann außerhalb der Mittagszeit für informelle Meetings genutzt werden.\",
    \"Aufgaben\": [
      {
        \"type\": \"richtig/falsch\",
        \"frage\": \"Die Angestellten werden gebeten, die Schreibtische nicht unnötig zu blockieren.\",
        \"loesung\": \"richtig\"
      },
      {
        \"type\": \"multiple-choice\",
        \"frage\": \"Sie dürfen\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"Meetings auch außerhalb der Besprechungsräume abhalten.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"ihre Sachen während der Pausen auf dem Schreibtisch lassen.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"persönliche Dinge nicht mit ins Großraumbüro bringen.\"
          }
        ],
        \"loesung\": \"a\"
      }
    ]
}
  
Example 4:

{
    \"thema\": \"Willkommensmappe für neue Mitarbeiter*innen\",
    \"text\": \"## Urlaubsvertretung\\n\\nUm sicherzustellen, dass der Arbeitsalltag auch während Ihrer Abwesenheit störungsfrei funktioniert, wird zusammen mit der Teamleitung eine Vertretung bestimmt. In einem gemeinsamen Gespräch wird geklärt, welche Aufgaben Priorität haben. Falls nötig, werden mehrere Personen mit der Vertretung beauftragt.\\n\\nEinige Tage vor Ihrem Urlaubsbeginn findet eine Übergabe statt, bei der Sie in einem persönlichen Gespräch mit Ihrer Vertretung die Aufgaben durchgehen und wichtige Informationen austauschen. Denken Sie bitte daran, Ihrer Vertretung alle relevanten Zugangsdaten mitzuteilen, damit sie auf wichtige Informationen und Dokumente zugreifen kann. Damit es keine Unklarheiten oder Missverständnisse gibt, empfehlen wir, zusätzlich ein Übergabeprotokoll zu erstellen, in dem Sie alle wichtigen Informationen schriftlich festhalten.\\n\\nDamit Kundenanfragen innerhalb der vorgesehenen 48 Stunden beantwortet werden können, werden E-Mails bei Abwesenheit grundsätzlich weitergeleitet. Ein entsprechender Hinweis dazu sowie die namentliche Nennung der zuständigen Vertreterin oder des Vertreters muss in der automatischen Antwort enthalten sein. Verwenden Sie dafür bitte ausschließlich unseren Standardtext (siehe S. 6) und denken Sie daran, die Abwesenheitsnotiz rechtzeitig zu aktivieren.\\n\\nDamit der Wiedereinstieg nach dem Urlaub gut gelingt, vereinbaren Sie für den ersten Arbeitstag bitte einen Termin mit Ihrer Vertretung. Dort bringt die Kollegin oder der Kollege Sie auf den aktuellen Stand und ermöglicht Ihnen so, schnell wieder in die eigenen Aufgaben hineinzufinden.\",
    \"Aufgaben\": [
      {
        \"type\": \"richtig/falsch\",
        \"frage\": \"Die Firma erwartet, dass vor und nach dem Urlaub eine persönliche Übergabe gemacht wird.\",
        \"loesung\": \"richtig\"
      },
      {
        \"type\": \"multiple-choice\",
        \"frage\": \"Die Angestellten entscheiden selbst,\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"ob sie ein Übergabeprotokoll schreiben möchten.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"ob sie ihre E-Mails an die Vertretung weiterleiten.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"wie sie die Abwesenheitsnotiz formulieren.\"
          }
        ],
        \"loesung\": \"a\"
      }
    ]
}
  
Example 5:

{
    \"thema\": \"Willkommensmappe für neue Mitarbeiterinnen und Mitarbeiter\",
    \"text\": \"## Essensgutscheine\\n\\nUm in der Mittagspause vergünstigt zu essen, können Sie Gutscheine im Wert von 6,50 € erwerben. Diese sind uneingeschränkt in unserer Cafeteria sowie im Restaurant Krönchen in der Sigmundstraße 12 einlösbar, dort allerdings nur für das Tagesmenü.\\n\\nSie können die Essensgutscheine über unser Internetportal anfordern. Geben Sie bis zum 25. jeden Monats die Anzahl der Gutscheine an, die Sie für den Folgemonat einlösen möchten. Die Abrechnung erfolgt über die Gehaltsabrechnung. Gutscheine, die Sie nicht einlösen, sind auch in den nächsten Monaten noch gültig.\\n\\nBis jeweils zum Donnerstag der Vorwoche müssen Sie außerdem angeben, welche Mittagsmenüs Sie in der folgenden Woche in der Cafeteria essen möchten. Eine kurzfristige Abmeldung ist bis 10:30 Uhr am Vortag möglich, dies sollte aber nicht zur Regel werden, da die Küche planen muss.\\nBitte beachten Sie, dass die Gutscheine nur durch Mitarbeiter eingelöst werden dürfen. Für Geschäftsbesuch sind Gästekarten über die jeweilige Assistenz oder direkt in der Personalabteilung erhältlich.\",
    \"Aufgaben\": [
      {
        \"type\": \"richtig/falsch\",
        \"frage\": \"Das Mittagessen muss in der Woche vorher gewählt werden.\",
        \"loesung\": \"richtig\"
      },
      {
        \"type\": \"multiple-choice\",
        \"frage\": \"Die Gutscheine für das vergünstigte Essen\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"kann man am Monatsende abholen.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"sind nur für Angestellte der Firma erhältlich.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"verfallen nach einem Monat.\"
          }
        ],
        \"loesung\": \"b\"
      }
    ]
}
  

Example 6:

{
    \"thema\": \"Willkommensmappe für neue Mitarbeiterinnen und Mitarbeiter\",
    \"text\": \"## Arbeitszeit und Arbeitszeitgestaltung\\n\\nDie wöchentliche Arbeitszeit in der Produktion beträgt 36,5 Stunden. Für den Verwaltungsbereich gelten 39 Stunden. Sollte mit Ihnen arbeitsvertraglich eine andere Wochenarbeitszeit vereinbart worden sein oder Sie in Teilzeit arbeiten, gelten dennoch die in Ihrem Arbeitsbereich üblichen Arbeitszeitregelungen wie Arbeitsantritt und Pausenzeiten.\\n\\nVon Ihnen geleistete Mehrarbeit wird auf Ihrem Arbeitszeitkonto gutgeschrieben. Nach Absprache mit Ihrer Teamleitung können Sie einen Freizeitausgleich vornehmen. Urlaubsanträge reichen Sie bitte ebenfalls für das gesamte Jahr dort ein.\\n\\nAls einer der ersten Arbeitgeber in der Region haben wir als Instrument der flexiblen Arbeitszeitgestaltung das Sabbatical eingeführt. Das Sabbatical ist eine befristete Unterbrechung des Arbeitslebens, die von drei Monaten bis zu einem Jahr reichen kann. Das Arbeitsentgelt in dieser Zeit kann durch unterschiedliche Möglichkeiten finanziert werden, z.B. durch freiwilligen Lohnverzicht, die Umwandlung in eine Teilzeitbeschäftigung oder das Ansparen von Arbeitszeitguthaben. Stimmt die Geschäftsleitung zu, kann das Sabbatical beliebig oft wiederholt werden. Nach Ihrer Rückkehr tritt Ihr ursprünglicher Arbeitsvertrag wieder in Kraft und Sie werden in der gleichen Position weiterbeschäftigt.\\n\\nWeitere Informationen zu diesem Angebot erhalten Sie im Personalbüro. Falls Sie sich zu diesem Schritt entscheiden, sprechen Sie bitte unsere Juniorchefin Renate Schrader an.\",
    \"Aufgaben\": [
      {
        \"type\": \"richtig/falsch\",
        \"frage\": \"In diesem Betrieb gibt es unterschiedliche Arbeitszeitmodelle.\",
        \"loesung\": \"richtig\"
      },
      {
        \"type\": \"multiple-choice\",
        \"frage\": \"Wer ein Sabbatical macht,\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"arbeitet zwei Monate weniger im Jahr.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"kehrt danach an den alten Arbeitsplatz zurück.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"verdient in dieser Zeit kein Geld.\"
          }
        ],
        \"loesung\": \"b\"
      }
    ]
}
  
Example 7:

{
    \"thema\": \"Willkommensmappe für neue Mitarbeiterinnen und Mitarbeiter\",
    \"text\": \"## Arbeiten im Großraumbüro\\n\\nIn unserem Unternehmen gibt es in der dritten Etage einen großen Raum, in dem mehrere Schreibtische stehen. Jeder Schreibtisch hat ein Telefon und Anschlüsse für mobile digitale Arbeitsgeräte. Eigene Kopfhörer mit Mikrophon für Videokonferenzen mit Kundinnen und Kunden bzw. Kolleginnen und Kollegen können mitgebracht werden, zwei Headsets befinden sich aber auch im Raum.\\n\\nDer Raum steht Teilzeitkräften ohne eigenes Büro sowie Gästen zur Verfügung. Bitte tragen Sie einen Bedarf möglichst frühzeitig in die digitale Raumliste ein.\\n\\nDie Schreibtische sind nach drei Seiten durch Stellwände abgetrennt, sodass man auch in einem Großraumbüro konzentriert arbeiten kann. Außerdem gibt es einen extra Tisch, auf dem Unterlagen oder größere Pläne abgelegt werden können. Büromaterialien und Kopierer befinden sich in einem Nebenraum am Eingang des Großraumbüros, dort hängt auch die jeweils aktuelle Raumliste aus.\\n\\nBitte räumen Sie am Ende des Arbeitstages alle Unterlagen auf und hinterlassen Sie den Schreibtisch sauber. Getränke sind am Arbeitsplatz erlaubt. Essen dagegen dürfen Sie nur in den Pausenräumen und in der Kantine. Achten Sie bitte darauf, beim Telefonieren oder Kommunizieren per Videokonferenz nicht zu laut zu sprechen.\\n\\n## Pausenräume und Kantine\\n\\nEine erholsame Atmosphäre in den Pausen wird bei uns großgeschrieben. Die Kantine verfügt über\",
    \"Aufgaben\": [
      {
        \"type\": \"richtig/falsch\",
        \"frage\": \"Im Unternehmen arbeiten die Mitarbeitenden in Großraumbüros.\",
        \"loesung\": \"richtig\"
      },
      {
        \"type\": \"multiple-choice\",
        \"frage\": \"Die Unternehmensleitung bittet darum,\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"Essensreste von den Schreibtischen zu räumen.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"keine privaten Arbeitsmittel zu nutzen.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"sich beim Telefonieren leise zu verhalten.\"
          }
        ],
        \"loesung\": \"c\"
      }
    ]
}
  

Example 8:

{
    \"thema\": \"Willkommensmappe für neue Mitarbeiterinnen und Mitarbeiter\",
    \"text\": \"## Freizeitangebote\\n\\nWir wollen, dass Sie sich auch in einem großen Betrieb wohlfühlen und fördern gemeinsame Unternehmungen.\\n\\nJeden letzten Freitag im Monat treffen sich interessierte Mitarbeitende um 18 Uhr, um ungezwungen zusammen zu sein und miteinander ins Gespräch zu kommen. Treffpunkt ist im Foyer, der Veranstaltungsort wechselt, achten Sie bitte auf den Aushang am Schwarzen Brett. Besonders beliebt ist im Sommer auch der Besuch im Biergarten im Stadtpark.\\n\\nDort trifft sich jeden Donnerstag um 17 Uhr eine betriebsinterne Laufgruppe, der Sie sich anschließen können. Die verschiedenen Laufstrecken sind auch für Anfänger geeignet – besonders neu zugezogene Mitarbeitende finden hier schnell Anschluss und lernen die Umgebung kennen.\\n\\nWer das attraktive Umland kennenlernen will, kann sich unserer seit fünf Jahren aktiven Wandergruppe anschließen.\\n\\nDie Unternehmensleitung hat außerdem einen Vertrag mit dem Fitness-Center \"Gehrlich\" geschlossen. Alle Mitarbeitenden können dort trainieren. Das Unternehmen beteiligt sich an den Kosten.\\n\\nKulturell Interessierte sollten auf die Informationen unserer PR-Abteilung achten, über die regelmäßig Eintrittskarten für Oper, Theater, Lesungen, aber auch für Fußballspiele verlost werden.\\n\\n## Sprachen lernen\\n\\nGeplant sind für das nächste Jahr mehrere Inhouse-Sprachkurse. Neben Englisch soll auch der Besuch\",
    \"Aufgaben\": [
      {
        \"type\": \"richtig/falsch\",
        \"frage\": \"Im Unternehmen gibt es regelmäßig Aktivitäten nach der Arbeit.\",
        \"loesung\": \"richtig\"
      },
      {
        \"type\": \"multiple-choice\",
        \"frage\": \"Die Mitarbeiterinnen und Mitarbeiter\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"bekommen eine Ermäßigung im Fitnesscenter.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"besuchen donnerstags gerne den Biergarten.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"haben Anspruch auf Veranstaltungstickets.\"
          }
        ],
        \"loesung\": \"a\"
      }
    ]
}
  
Example 9:

{
    \"thema\": \"Willkommensmappe für neue Mitarbeiterinnen und Mitarbeiter\",
    \"text\": \"## Gemeinschaftsküchen\\n\\nIn unserem Betrieb haben wir zwei kleine Gemeinschaftsküchen, die alle Mitarbeitenden nutzen können. Für die Benutzung der Küchen gelten folgende Regeln:\\n\\nDie Küchen sind mit Geschirrspülautomaten, Kaffeevollautomaten und Wasserkochern ausgestattet, die Küche im 2. OG verfügt auch über eine Mikrowelle. Die Geräte werden von einer externen Firma gewartet, für das Be- und Entladen (Geschirrspüler) bzw. das Nachfüllen von Kaffee, Wasser und Milch (Kaffeevollautomat) sowie das Entkalken der Wasserkocher sind jeweils zwei Mitarbeitende verantwortlich. Wer Küchendienst hat, wird auf Plänen in den Küchen ausgehängt. Die Einteilung erfolgt automatisch in alphabetischer Reihenfolge nach den Nachnamen der Mitarbeitenden und berücksichtigt Urlaubszeiten, soweit sie frühzeitig eingereicht wurden. Wenn Änderungen notwendig sind (Urlaub, Krankheit usw.), bitten wir diese schnellstmöglich an Frau Schubert zu melden, die Änderungen vornehmen kann.\\n\\nIn beiden Küchen stehen Wasserspender für gekühltes Wasser. Das Wasser ist für alle Mitarbeitenden kostenlos. Die Tanks werden täglich einmal am Abend von Herrn Nguyen vom externen Facilitymanagement ausgetauscht. Sollte ein weiterer Austausch nötig sein, wenden sich die Mitarbeitenden des Küchendienstes bitte an Herrn Nguyen.\",
    \"Aufgaben\": [
      {
        \"type\": \"richtig/falsch\",
        \"frage\": \"In beiden Küchen ist eine Kochmöglichkeit vorhanden.\",
        \"loesung\": \"falsch\"
      },
      {
        \"type\": \"multiple-choice\",
        \"frage\": \"Der Küchendienst\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"erfolgt nach einem festen System.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"ist für die Mitarbeitenden freiwillig.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"wird von einer Mitarbeiterin eingeteilt.\"
          }
        ],
        \"loesung\": \"a\"
      }
    ]
}
  

Example 10:

{
    \"thema\": \"Willkommensmappe für neue Mitarbeiterinnen und Mitarbeiter\",
    \"text\": \"## Elektronisches Zugangs- und Zeiterfassungssystem\\n\\nFür den Zugang zu unserem Firmengebäude und die Erfassung der Arbeitszeit wurde Ihnen eine elektronische Karte ausgehändigt, auf der auch Ihre Mitarbeiternummer und Ihr vollständiger Name hinterlegt sind.\\n\\nBeim Betreten und Verlassen des Firmengebäudes halten Sie Ihre Karte an das elektronische Lesegerät, das neben dem Haupteingang an der Wand befestigt ist. Warten Sie unbedingt das grüne Signal ab, das anzeigt, dass Ihre Karte gelesen und Ihre Zeit automatisch erfasst wurde.\\n\\nDie Pausenzeiten (siehe Anlage F) sind einzuhalten. Die gesetzlichen Ruhepausen werden vom Erfassungssystem automatisch abgezogen, wenn Sie es versäumen, sich zur Pause ab- und wieder anzumelden. Die Länge der Ruhepausen variiert je nach Arbeitszeit zwischen 30 bis 45 Minuten, Details hierzu finden Sie in Anlage G.\\n\\nSind Anpassungen der erfassten Zeit erforderlich (z. B. bei Fehlfunktion des Lesegeräts), wenden Sie sich an Herrn Sangkam (Raum 169, Durchwahl -29).\\n\\nSollten Sie Probleme bei der Verwendung haben, wenden Sie sich an das Büro des Officemanagements (Raum 132). Sollte das Büro nicht besetzt sein, erreichen Sie in dringenden Fällen die Assistenz der Geschäftsführung, Frau Schneider, unter der Durchwahl -22.\",
    \"Aufgaben\": [
      {
        \"type\": \"richtig/falsch\",
        \"frage\": \"Die elektronische Karte wird auch als Schlüssel verwendet.\",
        \"loesung\": \"falsch\"
      },
      {
        \"type\": \"multiple-choice\",
        \"frage\": \"Die von dem System erfassten Zeiten\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"beinhalten die Ruhepausen.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"kann man nachträglich ändern lassen.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"werden am Ladegerät korrigiert.\"
          }
        ],
        \"loesung\": \"b\"
      }
    ]
}

Example 11:

{
    \"thema\": \"Willkommensmappe für neue Mitarbeiterinnen und Mitarbeiter\",
    \"text\": \"## Gesundheitsvorsorge\\n\\nIhre Gesundheit liegt uns am Herzen! Deshalb bieten wir verschiedene Kurse an. Vormittags können Sie einmal pro Woche an der Rückengymnastik teilnehmen. Es gibt eine Anfänger- und eine Fortgeschrittenengruppe. Kontaktieren Sie unseren Trainer, Herrn Mattus, und vereinbaren Sie eine Probestunde. Danach wird er Sie in die passende Gruppe einteilen.\\n\\nDes Weiteren haben Sie die Möglichkeit, an einem Achtsamkeitstraining teilzunehmen. Da die Kursinhalte hier aufeinander aufbauen, gibt es feste Gruppen, und es ist eine Anmeldung erforderlich. Die aktuelle Ansprechpartnerin ist Frau Gadoni. Beide Angebote können Sie in Ihrer Arbeitszeit wahrnehmen!\\n\\nAußerhalb der Arbeitszeit bieten wir mehrere offene Gruppen an.\\n\\nEinmal im Monat bekommen Sie in der Kantine Ernährungstipps mit aktuellen Rezepten. Außerdem existieren eine Laufgruppe und eine Radwandergruppe. Details zu Terminen und Treffpunkten finden Sie im Intranet. Aus versicherungstechnischen Gründen sind diese Angebote Angehörigen unserer Firma vorbehalten.\\n\\nSie können gerne auch eine neue Gruppe gründen. Kontaktieren Sie dazu Herrn Siebert.\",
    \"Aufgaben\": [
      {
        \"type\": \"richtig/falsch\",
        \"frage\": \"Die Rückenkurse finden in festen Gruppen statt.\",
        \"loesung\": \"falsch\"
      },
      {
        \"type\": \"multiple-choice\",
        \"frage\": \"Zu den offenen Angeboten\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"bekommt man aktuelle Informationen bei Frau Gadoni.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"kann man auch Freunde oder Familienmitglieder mitbringen.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"kann man auch selbst etwas beitragen.\"
          }
        ],
        \"loesung\": \"c\"
      }
    ]
}
  

Example 12:

{
    \"thema\": \"Willkommensmappe für neue Mitarbeiterinnen und Mitarbeiter\",
    \"text\": \"## Umgang mit Diversität\\n\\nBei uns arbeiten rund 250 Personen aus über 20 verschiedenen Ländern – und darauf sind wir stolz! Unser Motto ist: \"Je vielfältiger desto besser!\" Wir sind bemüht, jede einzelne Person mit ihren besonderen Bedürfnissen wahrzunehmen und zu unterstützen.\\n\\nHierzu ein paar Beispiele: Sie können an religiösen Feiertagen, die in Deutschland keine gesetzlichen Feiertage sind, freibekommen, wenn Sie die Arbeitszeit nachholen. Stellen Sie dafür bitte mindestens 2 Wochen vorher schriftlich einen Antrag bei Ihrem oder Ihrer direkten Vorgesetzten.\\n\\nIm zweiten Stock unserer Firma steht Ihnen ein interreligiöser Andachtsraum zur Verfügung, den Sie in Arbeitspausen nutzen können.\\n\\nFür Personen, die Deutsch nicht als Muttersprache sprechen, finanzieren wir Deutschkurse sowie Kommunikations- und Schreibtrainings.\\n\\nMit Personen, die sich um kleine Kinder oder pflegebedürftige Angehörige kümmern, suchen wir gemeinsam nach flexiblen Arbeitszeitmodellen.\\n\\nFalls Sie besondere körperliche Herausforderungen haben, unterstützen wir Sie individuell. Besprechen Sie bitte alles zunächst mit Ihrem oder Ihrer direkten Vorgesetzten.\\n\\nUnd wenn Sie der Meinung sind, dass Sie – aus welchen Gründen auch immer – benachteiligt werden, kontaktieren Sie bitte unsere Gleichbehandlungsbeauftragte Sophia Gebert.\",
    \"Aufgaben\": [
      {
        \"type\": \"richtig/falsch\",
        \"frage\": \"Die Firma berücksichtigt die verschiedenen Bedürfnisse der Mitarbeiter.\",
        \"loesung\": \"richtig\"
      },
      {
        \"type\": \"multiple-choice\",
        \"frage\": \"Wenn man sich diskriminiert fühlt, soll man\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"an einem Kommunikationstraining teilnehmen.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"sich an Frau Gebert wenden.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"sich schriftlich bei der Teamleitung beschweren.\"
          }
        ],
        \"loesung\": \"b\"
      }
    ]
}

"""),
        ],
    )
    output = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        output += chunk.text
        if debug:
            print(chunk.text, end="")
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
    # ```json
    # {
    #   "thema": "Willkommensmappe für neue Mitarbeiterinnen und Mitarbeiter",
    #   "text": "## [Generated Text Title in German]\n\n[Generated German text, paragraph 1]\n\n[Generated German text, paragraph 2]\n\n[Generated German text, paragraph 3-5... Use Markdown for paragraphs/structure]",
    #   "Aufgaben": [
    #     {
    #       "type": "richtig/falsch",
    #       "frage": "[Generated Richtig/Falsch statement in German]",
    #       "loesung": "[Correct solution: 'richtig' or 'falsch']"
    #     },
    #     {
    #       "type": "multiple-choice",
    #       "frage": "[Generated Multiple-Choice question stem in German]",
    #       "optionen": [
    #         {
    #           "key": "a",
    #           "text": "[Generated Option A text in German]"
    #         },
    #         {
    #           "key": "b",
    #           "text": "[Generated Option B text in German]"
    #         },
    #         {
    #           "key": "c",
    #           "text": "[Generated Option C text in German]"
    #         }
    #       ],
    #       "loesung": "[Correct solution: 'a', 'b', or 'c']"
    #     }
    #   ]
    # }
    # ```
    # check if the json_data has the same structure as above
    
    if not isinstance(json_data, dict):
        return False, "JSON data is not a dictionary"
    
    # Check for required top-level keys
    required_keys = ["thema", "text", "Aufgaben"]
    for key in required_keys:
        if key not in json_data:
            return False, f"Missing required key: {key}"
    
    # Check thema and text
    if not isinstance(json_data["thema"], str) or not json_data["thema"]:
        return False, "thema must be a non-empty string"
    
    if not isinstance(json_data["text"], str) or not json_data["text"]:
        return False, "text must be a non-empty string"
    
    # Check Aufgaben
    if not isinstance(json_data["Aufgaben"], list):
        return False, "Aufgaben must be a list"
    
    if len(json_data["Aufgaben"]) == 0:
        return False, "Aufgaben list cannot be empty"
    
    for i, aufgabe in enumerate(json_data["Aufgaben"]):
        if not isinstance(aufgabe, dict):
            return False, f"Aufgabe {i} is not a dictionary"
        
        # Check common fields for all task types
        if "type" not in aufgabe:
            return False, f"Aufgabe {i} is missing 'type' field"
        
        if "frage" not in aufgabe:
            return False, f"Aufgabe {i} is missing 'frage' field"
        
        if not isinstance(aufgabe["frage"], str) or not aufgabe["frage"]:
            return False, f"Aufgabe {i}: 'frage' must be a non-empty string"
        
        if "loesung" not in aufgabe:
            return False, f"Aufgabe {i} is missing 'loesung' field"
        
        # Check specific task types
        if aufgabe["type"] == "richtig/falsch":
            if aufgabe["loesung"] not in ["richtig", "falsch"]:
                return False, f"Aufgabe {i}: 'loesung' for richtig/falsch must be 'richtig' or 'falsch'"
        
        elif aufgabe["type"] == "multiple-choice":
            if "optionen" not in aufgabe:
                return False, f"Aufgabe {i}: multiple-choice task missing 'optionen' field"
            
            if not isinstance(aufgabe["optionen"], list):
                return False, f"Aufgabe {i}: 'optionen' must be a list"
            
            if len(aufgabe["optionen"]) < 2:
                return False, f"Aufgabe {i}: multiple-choice task must have at least 2 options"
            
            valid_keys = []
            for j, option in enumerate(aufgabe["optionen"]):
                if not isinstance(option, dict):
                    return False, f"Aufgabe {i}: option {j} is not a dictionary"
                
                if "key" not in option:
                    return False, f"Aufgabe {i}: option {j} is missing 'key' field"
                
                if "text" not in option:
                    return False, f"Aufgabe {i}: option {j} is missing 'text' field"
                
                if not isinstance(option["text"], str) or not option["text"]:
                    return False, f"Aufgabe {i}: option {j}: 'text' must be a non-empty string"
                
                valid_keys.append(option["key"])
            
            if aufgabe["loesung"] not in valid_keys:
                return False, f"Aufgabe {i}: 'loesung' must be one of {valid_keys}"
        
        else:
            return False, f"Aufgabe {i}: unknown task type '{aufgabe['type']}'"
    
    # If we've made it here, the structure is valid
    return True, "JSON structure is valid"

def generate_mocktest():
    json_str = generate(debug=True)
    json_data = format_json(json_str)
    is_valid, message = verify_json_structure(json_data)
    if not is_valid:
        print(f"Invalid JSON structure: {message}")
        raise Exception(f"Invalid JSON structure: {message}")    # json_data = shuffle_solutions(json_data)
    return json_data

if __name__ == "__main__":
    # Generate 100 more mocktests. 
    idx = 0
    while idx < 100:
        try:
            mocktest = generate_mocktest()
            with open(f"/Users/binhnguyen/Workspaces/TELC_B2_test/data_mocktest/lesen/teil_2/mocktest_generated_{idx + 111}.json", "w", encoding="utf-8") as f:
                json.dump(mocktest, f, indent=4, ensure_ascii=False)
            idx += 1
        except Exception as e:
            print(f"Error generating mocktest {idx}: {e}")