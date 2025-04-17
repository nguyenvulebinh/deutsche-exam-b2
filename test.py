import base64
import os
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        api_key='',
    )

    model = "gemini-2.5-pro-preview-03-25"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""In the first step, generate 5 correct pairs and 3 distractors. In the second step, generate the mocktest follow the examples in json format"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""Guideline for Creating a TELC B2 Lesen Teil 1 Exercise**

**1. Objective & Goal:**
Create a complete, new mock examination exercise for **TELC Deutsch B2, Lesen Teil 1**. The exercise must accurately replicate the format, difficulty level (B2 CEFR), content style, and specific task requirements of the official TELC B2 exam for this part.

**2. Target Level & Skill:**
*   **Level:** CEFR B2 (Common European Framework of Reference for Languages)
*   **Skill:** Reading Comprehension (Leseverstehen) – specifically, matching specific needs to relevant information.

**3. Core Task:**
The test-taker must read descriptions of 5 individuals with specific needs or interests and match each person to the *one* most suitable article summary out of 8 options provided.

**4. Required Components to Create:**

*   **Overall Instructions:** Standard introductory text and task explanation.
*   **People Descriptions (Personen 1-5):** 5 descriptions of individuals' situations/needs.
*   **Article Snippets (Artikel a-h):** 8 short article summaries/teasers.
*   **Solution Key:** Clear mapping of people to their correct articles.

**5. Detailed Specifications for Each Component:**

    **a. Overall Instructions:**
        *   **Content:**
            *   Start with the standard scenario: "Sie lesen online in einer [Specify Source, e.g., Wirtschaftszeitung, Berufsportal, Ratgeber-Magazin] und möchten Ihren Freunden/Kollegen einige Artikel schicken."
            *   State the task clearly: "Entscheiden Sie, welcher Artikel a–h zu welcher Person 1–5 passt."
            *   Include the marking instruction: "Markieren Sie Ihre Lösungen auf dem Antwortbogen."
        *   **Language:** Use standard B2-level German instructional language.

    **b. People Descriptions (Personen 1-5):**
        *   **Number:** Exactly **5** distinct individuals, numbered 1 to 5.
        *   **Content:** For each person, write a **single sentence** describing a specific situation, need, interest, question, or problem.
            *   Focus on common B2 themes: work, career (starting, changing, advancing), further education/training, job searching, starting a business, work-life balance, specific professional challenges (e.g., dealing with stress, understanding regulations), finding specific services.
            *   Each description must point towards a specific type of information needed, allowing for a clear match.
            *   Ensure the needs are distinct enough that one article doesn't plausibly fit multiple people.
        *   **Length:** Keep each description concise and direct, ideally **approx. 6 to 12 words**.
        *   **Language:** Clear, unambiguous B2-level German vocabulary and sentence structure.

    **c. Article Snippets (Artikel a-h):**
        *   **Number:** Exactly **8** distinct article snippets, lettered a to h.
        *   **Format:** Each snippet must include:
            *   A concise and relevant **Title (Titel)**.
            *   A **Descriptive Text (Beschreibung)** summarizing the article's content.
            *   A placeholder link, typically "**mehr ...**".
        *   **Content:**
            *   **5 snippets** must be the correct, clear matches for the 5 people. The connection should be logical and identifiable upon careful B2-level reading (may involve synonyms or paraphrasing, not just identical keywords).
            *   **3 snippets** must be **distractors** (see Section 6 below).
        *   **Length (Descriptive Text only):** The descriptive text for each snippet should be approximately **3-4 sentences** long, totaling roughly **30 to 50 words**. This excludes the title and "mehr..." link.
        *   **Language:** Use B2-level German. Topics should generally align with the themes presented in the people's descriptions but also include plausible distractor topics.

    **d. Solution Key:**
        *   Provide a simple, clear key listing the correct article letter for each person number (e.g., 1:f, 2:c, 3:h, 4:a, 5:d).

**6. Distractor Design (Crucial for the 3 non-matching articles):**

*   **Purpose:** Distractors must be plausible enough to seem like potential matches upon a quick glance but incorrect upon careful reading. They test comprehension beyond simple keyword matching.
*   **Strategies for Creation:** Use one or more of these techniques for each distractor:
    *   **Topic Overlap, Wrong Focus:** Article discusses the general theme (e.g., "job") but not the specific aspect needed (e.g., article on *finding* a job when the person needs advice on *leaving* a job).
    *   **Keyword Similarity, Different Context:** Uses keywords from a person's description, but the article addresses a completely different situation (e.g., "Teilzeit" mentioned in an article about student jobs when the person is a full-time employee considering reduction).
    *   **Related but Irrelevant Information:** Offers information tangentially related to the overall theme but doesn't solve any specific person's problem (e.g., article on healthy office lunches when people need career advice).
    *   **Different Target Audience:** The article is clearly aimed at a different group (e.g., employers vs. employees, advanced experts vs. beginners, specific professions not represented).
    *   **Too General/Too Specific:** The article is too vague to be helpful (e.g., "The Future of Work") or too niche (e.g., tax law for beekeepers) for the described needs.
*   **Avoid:** Do not make distractors obviously wrong, nonsensical, or completely unrelated to the general themes of the exercise.

**7. Quality Control & Constraints:**

*   **Theme Coherence:** Maintain a reasonably consistent overall theme (e.g., work/business/education/professional life) across the people and articles.
*   **B2 Level Consistency:** Ensure all texts rigorously adhere to B2 vocabulary, grammar, and complexity. Avoid both lower-level simplicity and higher-level complexity.
*   **Uniqueness of Matches:** Each person (1-5) must have only ONE clearly best article match. Each article (a-h) can match AT MOST one person. The correct matches should be logical and defensible, avoiding excessive ambiguity.
*   **Plausibility:** Scenarios, needs, and article topics should be realistic and relatable within a general European/German context.
*   **Clarity:** The language should be clear. The challenge lies in matching and discriminating, not in deciphering poorly written text or obscure vocabulary/cultural references.

**8. Final Output Format:**
Present the complete exercise clearly structured with headings for:
*   Instructions
*   Personen 1-5
*   Artikel a-h (presented cleanly, perhaps in a table or list format as in the examples)
*   Solution Key

Refer to official TELC B2 materials or the provided examples for visual layout and stylistic conventions.


Example 1:

{
    \"exercise_type\": \"TELC B2\",
    \"skill\": \"Lesen\",
    \"part\": \"Teil 1\",
    \"instructions\": \"Sie lesen online in einer Wirtschaftszeitung und möchten Ihren Freunden einige Artikel schicken. Entscheiden Sie, welcher Artikel a–h zu welcher Person 1–5 passt.\",
    \"people\": [
      {
        \"id\": 1,
        \"description\": \"Elena weiß nicht, wie es nach ihrer Ausbildung weitergeht.\"
      },
      {
        \"id\": 2,
        \"description\": \"Joaquin überlegt, welche Weiterbildung er als Nächstes machen kann.\"
      },
      {
        \"id\": 3,
        \"description\": \"Katrin interessiert sich für erfolgreiche Familienunternehmen.\"
      },
      {
        \"id\": 4,
        \"description\": \"Monika fragt sich, ob sie zu hilfsbereit ist.\"
      },
      {
        \"id\": 5,
        \"description\": \"Timo will eine eigene Firma gründen.\"
      }
    ],
    \"articles\": [
      {
        \"id\": \"a\",
        \"title\": \"Vom „Geben und Nehmen“\",
        \"description\": \"Das neue Buch des amerikanischen Erfolgsautors Philip Vaughn wurde sehnsüchtig erwartet. Nun ist es da. „Vom Geben und Nehmen“ heißt es und erklärt uns, warum man beim Netzwerken nicht nur an sich selbst denken sollte, sondern auch das Geben, also anderen zu helfen, eine wichtige Rolle spielt.\"
      },
      {
        \"id\": \"b\",
        \"title\": \"Gleichberechtigung nicht einmal beim Urlaubsgeld\",
        \"description\": \"Sogar beim Urlaubsgeld, das viele Unternehmen ihren Mitarbeiterinnen und Mitarbeitern mittlerweile zur Sommerzeit zahlen, gibt es Unterschiede zwischen Frauen und Männern. Männer erhalten deutlich öfter Urlaubsgeld als Frauen. Warum?\"
      },
      {
        \"id\": \"c\",
        \"title\": \"Beruflich erfolgreicher mit Weiterbildungen\",
        \"description\": \"Durch die schnell fortschreitende Digitalisierung fallen Berufe und ganze Branchen weg oder verändern sich stark. Wer hier nicht verlieren möchte, sollte berufliche Weiterbildungen nach der Ausbildung nutzen. Welche genau, erfahren Sie hier.\"
      },
      {
        \"id\": \"d\",
        \"title\": \"„Ich wollte allen zeigen, was ich kann“\",
        \"description\": \"Sie hat die Schule ohne Abschluss abgebrochen und gehört nun zu den erfolgreichsten Gründerinnen Europas. Lydia van Elten spricht mit uns über Lehrer, die nicht an sie geglaubt haben, über ihr junges Unternehmen und ihren Willen, nie aufzugeben.\"
      },
      {
        \"id\": \"e\",
        \"title\": \"Mahlzeit! 30 leckere Rezepte für die Mittagspause\",
        \"description\": \"Der Starkoch Vincent Hohmann hat sich etwas ganz Besonderes einfallen lassen. 30 Rezepte für ein Mittagessen, das einfach und schnell in zehn Minuten am Morgen vorbereitet werden kann. Die Zutaten dazu finden sich in jeder Küche. Lecker, günstig und – empfehlenswert.\"
      },
      {
        \"id\": \"f\",
        \"title\": \"So gelingt der Berufseinstieg\",
        \"description\": \"Direkt nach dem Studium oder der Ausbildung einen Job zu finden, der zu einem passt, ist gar nicht so einfach, wie viele denken. Der Karriereberater Jost Mout gibt Tipps, wie der Einstieg in die Berufswelt gelingt, und zeigt, welche Stolperfallen auf die Bewerberinnen und Bewerber warten.\"
      },
      {
        \"id\": \"g\",
        \"title\": \"Tattoos am Arbeitsplatz tabu?\",
        \"description\": \"Hier ein kleines Herz am Handgelenk, dort ein großes Bild auf dem Oberarm – viele Chefs sehen diese Körperverschönerungen nicht gerne. Aber darf der Arbeitgeber seinen Angestellten verbieten, sich tätowieren zu lassen?\"
      },
      {
        \"id\": \"h\",
        \"title\": \"Hempelmann hat große Pläne\",
        \"description\": \"Der Familienbetrieb Hempelmann möchte seine Produkte zukünftig nicht nur in Deutschland, sondern weltweit verkaufen. Dafür braucht er starke Partner. Der Junior-Geschäftsführer Tom Arnold schreibt in einem Gastbeitrag über diese neue Herausforderung.\"
      }
    ],
    \"solutions\": {
      \"1\": \"f\",
      \"2\": \"c\",
      \"3\": \"h\",
      \"4\": \"a\",
      \"5\": \"d\"
    }
  }
  

Example 2: 

{
  \"exercise_type\": \"TELC B2\",
  \"skill\": \"Lesen\",
  \"part\": \"Teil 1\",
  \"instructions\": \"Sie suchen Informationen zu beruflichen Themen. Entscheiden Sie, welcher Text a–h zu welcher Person 1–5 passt.\",
  \"people\": [
    {
      \"id\": 1,
      \"description\": \"Alexandru überlegt, sich mit einem Partyservice selbstständig zu machen.\"
    },
    {
      \"id\": 2,
      \"description\": \"Johanna will nach ihrem Realschulabschluss einen technischen Beruf erlernen.\"
    },
    {
      \"id\": 3,
      \"description\": \"Katrin sucht nach 20 Jahren Büroarbeit eine neue Tätigkeit.\"
    },
    {
      \"id\": 4,
      \"description\": \"Lars ist ausgebildeter Dachdecker und möchte in seinem Beruf Karriere machen.\"
    },
    {
      \"id\": 5,
      \"description\": \"Navin hat einen Uniabschluss aus Indien und möchte in Deutschland arbeiten.\"
    }
  ],
  \"articles\": [
    {
      \"id\": \"a\",
      \"title\": \"MINT für Mädchen\",
      \"description\": \"Mathematik, Informatik, Naturwissenschaften, Technik gelten immer noch als Männerdomänen – aber die Zeiten ändern sich. Beweis dafür ist das überwältigende Interesse junger Frauen am ersten Tag der diesjährigen Ausbildungsmesse, bei der (Fach-)Hochschulen und Unternehmen ihre MINT-Studienfächer und Ausbildungsberufe vorstellen. Das weitere Programm finden Sie hier.\"
    },
    {
      \"id\": \"b\",
      \"title\": \"Fürs Leben lernen\",
      \"description\": \"Bei „START-UP junior“ gründen Schüler*innen ihre eigene Firma, verkaufen Produkte oder bieten Dienstleistungen an – und verdienen sogar Geld damit. Hier erklärt der Projektleiter Paulo Goncalves, wie junge Menschen mit unternehmerischem Denken vertraut gemacht werden und lernen, Verantwortung zu übernehmen.\"
    },
    {
      \"id\": \"c\",
      \"title\": \"Neue Podcastfolge\",
      \"description\": \"Ahmed El-Shamy kam aus Ägypten nach Deutschland. Nach mehreren Sprachkursen und der Anerkennung seines Diploms arbeitet er heute als Ingenieur. In unserem heutigen Podcast erzählt er von seinem beruflichen Werdegang und gibt internationalen Fachkräften und Akademiker*innen, die in Deutschland durchstarten möchten, wertvolle Tipps.\"
    },
    {
      \"id\": \"d\",
      \"title\": \"Persönliches Coaching\",
      \"description\": \"Wie viele Leute kennen Sie, die schon jahrelang denselben Job machen und damit zufrieden sind? Niemanden? Kein Wunder. Veränderung gehört zum Leben – auch zum Arbeitsleben. Erfahren Sie hier, wie Sie den richtigen Coach finden, der Ihnen neue Perspektiven eröffnet.\"
    },
    {
      \"id\": \"e\",
      \"title\": \"Wieder eine Fortbildung?\",
      \"description\": \"Mitarbeitende wissen oft nicht, wozu sie sich weiterbilden sollen: Sie machen schließlich ihren Job schon seit Jahren und wollen keine Karriere machen. Diese Meinung hört man häufig in Betrieben. Lesen Sie hier, wie Sie geeignete Fortbildungen für Ihre Mitarbeitenden auswählen.\"
    },
    {
      \"id\": \"f\",
      \"title\": \"Tausendundeine Frage\",
      \"description\": \"Wie viel Startkapital brauche ich? Muss ich einen Businessplan schreiben? Wie finde ich gutes Personal? Wer eine Firma gründen möchte, hat anfangs viele Fragen. Antworten gibt’s hier von den Experten.\"
    },
    {
      \"id\": \"g\",
      \"title\": \"Kaufmann/-frau: der absolute Klassiker\",
      \"description\": \"Kaufmännische Berufe sind nach wie vor populär: Sie bieten abwechslungsreiche Tätigkeiten, sind in den unterschiedlichsten Branchen zu finden und in der Wirtschaft überall gefragt. Auch die Verdienstmöglichkeiten sind attraktiv. Hier finden Sie die zehn beliebtesten Bürojobs.\"
    },
    {
      \"id\": \"h\",
      \"title\": \"Qualifikationen, die sich lohnen\",
      \"description\": \"Auch Handwerker haben Aufstiegsmöglichkeiten! Mit erfolgreich abgeschlossener Berufsausbildung kann man sich für leitende Positionen qualifizieren oder selbstständig machen. Mehr über die Meisterausbildung und andere weiterführende Ausbildungen erfahren Sie beim kostenlosen Informationstag.\"
    }
  ],
  \"solutions\": {
    \"1\": \"f\",
    \"2\": \"a\",
    \"3\": \"d\",
    \"4\": \"h\",
    \"5\": \"c\"
  }
}

Example 3:

{
  \"exercise_type\": \"TELC B2\",
  \"skill\": \"Lesen\",
  \"part\": \"Teil 1\",
  \"instructions\": \"Sie lesen online in einer Wirtschaftszeitung und möchten Ihren Freunden einige Artikel schicken.\\nEntscheiden Sie, welcher Artikel a–h zu welcher Person 1–5 passt.\\nMarkieren Sie Ihre Lösungen auf dem Antwortbogen.\",
  \"people\": [
    {
      \"id\": 1,
      \"description\": \"Almin überlegt, welche Ausbildung zu ihm passt.\"
    },
    {
      \"id\": 2,
      \"description\": \"Franz möchte sein Geschäft um Online-Handel erweitern.\"
    },
    {
      \"id\": 3,
      \"description\": \"Monique interessiert sich für kreative Berufe.\"
    },
    {
      \"id\": 4,
      \"description\": \"Asra fragt sich, warum sie beruflich nicht weiterkommt.\"
    },
    {
      \"id\": 5,
      \"description\": \"Xaver braucht eine Webseite für seine Firma.\"
    }
  ],
  \"articles\": [
    {
      \"id\": \"a\",
      \"title\": \"Unter der Lupe: Berufe für Menschen mit Fantasie\",
      \"description\": \"Designerin, Spieleentwickler, Goldschmied, Mediengestalterin: Es gibt für fantasievolle Menschen viele Möglichkeiten, einen passenden Beruf zu finden. Für nicht alle diese Tätigkeiten braucht man eine formale Ausbildung. Wir stellen Ihnen die Top-Jobs vor.\"
    },
    {
      \"id\": \"b\",
      \"title\": \"Kundenwünsche im Online-Handel\",
      \"description\": \"Wussten Sie, dass 62 % aller Verbraucher einen Bestellvorgang im Online-Handel abbrechen, weil ihnen die Versandkosten zu hoch sind? Unser Beitrag befasst sich mit Kundenwünschen an Online-Plattformen und wie Sie als Händler diese Wünsche besser erfüllen können.\"
    },
    {
      \"id\": \"c\",
      \"title\": \"Die 10 besten Homepage-Baukästen\",
      \"description\": \"Ob Online-Handel oder Geschäft in der City: Man braucht immer eine technisch einwandfrei funktionierende Webseite. Die kostet und selbst machen lohnt sich! Lesen Sie unser Ranking der besten Do-it-yourself Anleitungen für Webseiten.\"
    },
    {
      \"id\": \"d\",
      \"title\": \"Studium, Ausbildung oder Quereinstieg?\",
      \"description\": \"Viele, die heute erfolgreich als Programmierer arbeiten, haben ihren Beruf dadurch gelernt, dass sie ihn einfach machen. Allerdings ist eine Ausbildung in diesem Beruf der sicherere Weg zu einer Karriere als Programmierer. Welcher Weg für Sie der richtige sein kann, erfahren Sie in diesem Insider-Bericht von Franz Ball.\"
    },
    {
      \"id\": \"e\",
      \"title\": \"Kreativer Gründer: Zusätzliches Standbein für Start-ups\",
      \"description\": \"Benni Wagner, der Gründer des erfolgreichen Online-Start-ups hot-soup.com erzählt, wie er seinem Geschäft im Internet eine zweite Verdienstquelle durch den Verkauf über die traditionelle Ladentheke erschlossen hat – und wie er damit mehr Umsatz als beim Online-Handel macht.\"
    },
    {
      \"id\": \"f\",
      \"title\": \"Schnellstart Vertrieb übers Internet\",
      \"description\": \"Immer mehr Menschen kaufen nicht mehr an der Ladentheke, sondern bestellen vom heimischen Computer aus. Professor Wendel von Struntz stellt außergewöhnliche Verkaufs-Plattformen im Internet vor und gibt Einsteigern in den Online-Handel eine praktische Anleitung – lesenswert!\"
    },
    {
      \"id\": \"g\",
      \"title\": \"„Du schaffst das!“ Umgang mit dem Karriereknick\",
      \"description\": \"Wer hatte nicht schon einmal das Gefühl, sich beruflich im Kreis zu drehen oder im Job keine Zukunft zu haben? Allen, die sich die Frage stellen, warum eine Beförderung auf sich warten lässt, sei das Buch von Sanna Nickel empfohlen. Sie zeigt Wege aus der Sackgasse.\"
    },
    {
      \"id\": \"h\",
      \"title\": \"Lena fragt! Beruf oder Berufung?\",
      \"description\": \"Lena Kudruff stellt jungen Menschen Fragen: Was genau machst du in deinem Beruf? Was begeistert dich an deinem Beruf? Erfahren Sie alles über Berufe, für die man sich in Deutschland ausbilden lassen kann, und machen Sie am Ende einen Berufseignungstest.\"
    }
  ],
  \"solutions\": {
    \"1\": \"h\",
    \"2\": \"f\",
    \"3\": \"a\",
    \"4\": \"g\",
    \"5\": \"c\"
  }
}


Example 4:

{
    \"exercise_type\": \"TELC B2\",
    \"skill\": \"Lesen\",
    \"part\": \"Teil 1\",
    \"instructions\": \"Sie lesen online in einer Wirtschaftszeitung und möchten Ihren Freunden einige Artikel schicken.\\nEntscheiden Sie, welcher Artikel a–h zu welcher Person 1–5 passt.\\nMarkieren Sie Ihre Lösungen auf dem Antwortbogen.\",
    \"people\": [
      {
        \"id\": 1,
        \"description\": \"Karolina überlegt, sich selbständig zu machen.\"
      },
      {
        \"id\": 2,
        \"description\": \"Lena fragt sich, ob sie ihre Vorgesetzte duzen kann.\"
      },
      {
        \"id\": 3,
        \"description\": \"Andrey hat Probleme mit dem steigenden Arbeitsdruck.\"
      },
      {
        \"id\": 4,
        \"description\": \"Sarah interessiert sich für eine Tätigkeit im Ausland.\"
      },
      {
        \"id\": 5,
        \"description\": \"Lukas möchte Beruf und Familie besser verbinden.\"
      }
    ],
    \"articles\": [
      {
        \"id\": \"a\",
        \"title\": \"Es ist alles zu viel!\",
        \"description\": \"Ohne Pause durchgearbeitet, noch nichts gegessen und dann muss man auch noch ängstliche Patienten, besorgte Eltern oder unzufriedene Klienten beruhigen. Eine Krankenhausärztin, ein Lehrer und ein Sozialarbeiter berichten über den alltäglichen Wahnsinn und wie sie damit klarkommen.\"
      },
      {
        \"id\": \"b\",
        \"title\": \"Kinder oder Arbeit?\",
        \"description\": \"Immer mehr Arbeitnehmerinnen und Arbeitnehmer wollen mehr Zeit für ihre Kinder und ihren Partner / ihre Partnerin haben. Doch der Job lässt oft wenig Spielraum, die Arbeitsbelastung ist hoch. Neue Arbeitszeitmodelle helfen dabei, die richtige Balance zu finden.\"
      },
      {
        \"id\": \"c\",
        \"title\": \"Siezen oder duzen?\",
        \"description\": \"In der Korrespondenz mit Kundinnen und Kunden sollte man genau hinschauen. Ein saloppes Du kommt nicht bei allen Kundinnen und Kunden gut an, auch wenn Sie in einem modernen Start-up arbeiten. Fingerspitzengefühl ist gefragt.\"
      },
      {
        \"id\": \"d\",
        \"title\": \"Elternzeit\",
        \"description\": \"In Deutschland gibt es viele Förderungen für Familien. Die Elternzeit wird nicht nur von Frauen, sondern zunehmend auch von Männern gerne genutzt. Kinderwagen schieben statt am Computer sitzen: Wir zeigen Ihnen, wie Sie die Elternzeit richtig beantragen.\"
      },
      {
        \"id\": \"e\",
        \"title\": \"Das Problem mit der Anrede\",
        \"description\": \"In vielen Firmen sprechen sich die Mitarbeitenden mit Vornamen an und duzen sich. Aber kann man das auch mit dem Chef oder der Chefin machen? Das hat Vor- und Nachteile, die neue Mitarbeitende unbedingt beachten sollten.\"
      },
      {
        \"id\": \"f\",
        \"title\": \"Ein gutes Konzept ist wichtig\",
        \"description\": \"Wer sein eigener Chef werden will, muss sich gut vorbereiten. Man muss sich von Routinen verabschieden und mit finanzieller Unsicherheit leben können. Der Lohn ist ein selbstbestimmtes Arbeitsleben. Der Ratgeber „Der große Schritt“ hilft Ihnen, Schwierigkeiten beim Weg in die Selbständigkeit zu meistern.\"
      },
      {
        \"id\": \"g\",
        \"title\": \"Das Internationale im Lebenslauf\",
        \"description\": \"Madrid, Paris, New York ... Viele Mitarbeitende wollen gerne mal für einen bestimmten Zeitraum in einem anderen Land arbeiten. Das ist nicht nur eine sehr wertvolle Berufserfahrung, sondern beeindruckt auch Arbeitgeber. Diese Tipps helfen bei der Suche nach einer geeigneten Stelle.\"
      },
      {
        \"id\": \"h\",
        \"title\": \"Ich muss mal raus aus Deutschland!\",
        \"description\": \"Der Urlaubsantrag sorgt immer wieder für Konflikte in Unternehmen. Wer darf wann gehen? Viele wollen den Frühbucherrabatt von Auslandsreisen nutzen und den Urlaub möglichst früh beantragen. Wie sieht das arbeitsrechtlich aus?\"
      }
    ],
    \"solutions\": {
      \"1\": \"f\",
      \"2\": \"e\",
      \"3\": \"a\",
      \"4\": \"g\",
      \"5\": \"b\"
    }
  }
  

Example 5: 

{
    \"exercise_type\": \"TELC B2\",
    \"skill\": \"Lesen\",
    \"part\": \"Teil 1\",
    \"instructions\": \"Sie lesen online in einer Wirtschaftszeitung und möchten Ihren Freunden einige Artikel schicken.\\nEntscheiden Sie, welcher Artikel a–h zu welcher Person 1–5 passt.\\nMarkieren Sie Ihre Lösungen auf dem Antwortbogen.\",
    \"people\": [
      {
        \"id\": 1,
        \"description\": \"Wanda möchte im Internet Werbung für ihre Firma machen.\"
      },
      {
        \"id\": 2,
        \"description\": \"Kasimir überlegt, seine Arbeitszeit zu reduzieren.\"
      },
      {
        \"id\": 3,
        \"description\": \"Floris interessiert sich für das Netzwerken.\"
      },
      {
        \"id\": 4,
        \"description\": \"Gladis fragt sich, ob sie sich einen Steuerberater nehmen sollte.\"
      },
      {
        \"id\": 5,
        \"description\": \"Stephan hat das Gefühl, ständig überlastet zu sein.\"
      }
    ],
    \"articles\": [
      {
        \"id\": \"a\",
        \"title\": \"Mehr Zeit für das Wichtige?\",
        \"description\": \"Für die meisten Firmen ist es Pflicht, viele Berufstätige finden es praktisch: professionelle Unterstützung bei der Buchhaltung. Nicht nur sind viele damit überfordert, sondern diese Arbeit hält einen auch davon ab, wichtigere Dinge zu erledigen – oder? Wir zeigen Ihnen anhand von Beispielen, worauf Sie achten müssen und wann es sich rentiert.\"
      },
      {
        \"id\": \"b\",
        \"title\": \"Modernes Marketing\",
        \"description\": \"Große Firmen setzen nicht mehr nur auf das Internet, um erfolgreich Marketing zu betreiben. „Die Mischung macht’s!“, sagt Werner Claussen vom Netzwerk „Modernes Marketing“. In einem Interview berichtet er, was genau damit gemeint ist.\"
      },
      {
        \"id\": \"c\",
        \"title\": \"Ein Gesetz, das viele nicht kennen\",
        \"description\": \"Vielen ist nicht bewusst, dass es einen gesetzlichen Anspruch auf Teilzeitarbeit gibt. Wenn der bzw. die Angestellte möchte, muss der Arbeitgeber kürzere Arbeitszeiten ermöglichen. Bevor man diesen Wunsch äußert, sollte man sich allerdings über die Konsequenzen für Karriere, Steuern und Rente im Klaren sein. Wir haben eine Checkliste zusammengestellt.\"
      },
      {
        \"id\": \"d\",
        \"title\": \"Im Fokus: Arbeitszeitmodelle\",
        \"description\": \"In unserer Reihe zu unterschiedlichen Arbeitszeitmodellen stellen wir Ihnen heute anhand von drei Best-Practice-Beispielen vor, wie unterschiedliche Unternehmen die Gleitzeit in ihrem Betrieb umgesetzt haben. Lesen Sie außerdem, was die Geschäftsführung und Mitarbeitende berichten.\"
      },
      {
        \"id\": \"e\",
        \"title\": \"Alles im Lot?\",
        \"description\": \"Wenn Ihnen alles zu viel wird, kann das unterschiedliche Ursachen haben: die Menge der Arbeit, zu schwierige Aufgaben oder in Ihrem Privatleben gibt es Probleme, die Ihnen zu schaffen machen. Was Sie tun können, lesen Sie in einem Gastbeitrag der Psychologin Tamara Feuer.\"
      },
      {
        \"id\": \"f\",
        \"title\": \"Neues aus der Welt der Steuern\",
        \"description\": \"Die wenigsten mögen sie, und doch muss sie jeder zahlen: Steuern. Für Unternehmen ist dieser Bereich oft schwer zu durchschauen, deshalb fassen wir alle gesetzlichen Neuregelungen für Betriebe zusammen, die seit unserer letzten Ausgabe in Kraft getreten sind.\"
      },
      {
        \"id\": \"g\",
        \"title\": \"Der Weg zu mehr Kunden\",
        \"description\": \"Die Möglichkeiten, Produkte und Dienstleistungen zu bewerben, sind kaum zu überblicken. Gerade in kleineren Firmen sind die Mittel für das Marketing außerdem begrenzt. Hier ist Online-Marketing eine vergleichsweise günstige Möglichkeit, mehr Kunden zu erreichen. Wir zeigen Ihnen wie.\"
      },
      {
        \"id\": \"h\",
        \"title\": \"Vergessen Sie Zertifikate!\",
        \"description\": \"In vielen Branchen sind sie wichtiger als ein gutes Zeugnis: gute Kontakte. Das gilt umso mehr in einer internationalen Berufswelt, in der Sie wichtige Kontakte schnell und einfach auch über Kontinente hinweg knüpfen können. Unser Autor Felix Schubert zeigt, worauf es ankommt.\"
      }
    ],
    \"solutions\": {
      \"1\": \"g\",
      \"2\": \"c\",
      \"3\": \"h\",
      \"4\": \"a\",
      \"5\": \"e\"
    }
  }
  

Example 6:

{
    \"exercise_type\": \"TELC B2\",
    \"skill\": \"Lesen\",
    \"part\": \"Teil 1\",
    \"instructions\": \"Sie lesen online in einer Wirtschaftszeitung und möchten Ihren Freunden einige Artikel schicken.\\nEntscheiden Sie, welcher Artikel a–h zu welcher Person 1–5 passt.\\nMarkieren Sie Ihre Lösungen auf dem Antwortbogen.\",
    \"people\": [
      {
        \"id\": 1,
        \"description\": \"Clara plant, einen eigenen Laden zu eröffnen.\"
      },
      {
        \"id\": 2,
        \"description\": \"Simon will lernen, wie man Webseiten programmiert.\"
      },
      {
        \"id\": 3,
        \"description\": \"Mariana überlegt, die Stelle zu wechseln.\"
      },
      {
        \"id\": 4,
        \"description\": \"Nader möchte nach seinem Schulabschluss erste Berufserfahrungen sammeln.\"
      },
      {
        \"id\": 5,
        \"description\": \"Leah fragt sich, ob sie zu wenig verdient.\"
      }
    ],
    \"articles\": [
      {
        \"id\": \"a\",
        \"title\": \"Fertig mit der Schule – was jetzt?\",
        \"description\": \"Wer vor einer Ausbildung oder einem Studium zuerst einmal herausfinden möchte, welcher Beruf gut zur eigenen Persönlichkeit passt, kann bei einem Praktikum in einem größeren Betrieb gleich verschiedene Berufe kennenlernen. Lesen Sie hier den Erfahrungsbericht unserer derzeitigen Praktikantin.\"
      },
      {
        \"id\": \"b\",
        \"title\": \"In wenigen Schritten zum eigenen Internetauftritt\",
        \"description\": \"Ohne Selbstdarstellung im World Wide Web kommt man heutzutage im Arbeitsleben nicht weit, ganz egal in welcher Branche. Aber vor allem junge Unternehmer*innen können sich oft keine teuren externen Profis leisten und gestalten und erstellen ihre Webseiten selbst. Wir haben deshalb für Sie entsprechende Anleitungen bewertet.\"
      },
      {
        \"id\": \"c\",
        \"title\": \"Entspannt durch den Büroalltag\",
        \"description\": \"Wer kennt das nicht? Sie sitzen den ganzen Tag am Computer und schon vormittags schmerzen die Schultern, der Nacken und der Rücken. Das muss nicht sein! Mit unserem zehnminütigen Gymnastikprogramm kommen Sie gut durch den Bürotag!\"
      },
      {
        \"id\": \"d\",
        \"title\": \"Vom Traum zur Gründung\",
        \"description\": \"Die Erfolgsautorin Tatjana Vollmer beschreibt in ihrem neuesten Buch, wie Sie sich erfolgreich selbstständig machen können. Von der Geschäftsidee über den Businessplan und die Finanzierung bis zum passenden Internetauftritt: Hier bekommen Sie wertvolle Tipps, worauf Sie wirklich achten müssen!\"
      },
      {
        \"id\": \"e\",
        \"title\": \"Gründer raus aus der Schuldenfalle\",
        \"description\": \"Ihre Firma hat weniger Aufträge als erwartet und Sie können Ihre Verbindlichkeiten wie Kredite oder die Gewerbemiete für Ihre Geschäftsräume nicht mehr bezahlen? Unsere Finanzberaterin Constanze Hansen gibt Tipps, wie Sie die Finanzen Ihres Unternehmens wieder in den Griff bekommen können.\"
      },
      {
        \"id\": \"f\",
        \"title\": \"Gleicher Lohn für gleiche Arbeit –\",
        \"description\": \"so sollte es eigentlich sein, aber oft sieht die Realität in Deutschland noch anders aus. Häufig verdienen Frauen mit denselben Abschlüssen und Qualifikationen weniger als ihre männlichen Kollegen. Warum das so ist und was man dagegen tun kann, erfahren Sie hier.\"
      },
      {
        \"id\": \"g\",
        \"title\": \"Die Jobs der Zukunft\",
        \"description\": \"Die Digitalisierung verändert unser Arbeitsleben zunehmend. In unserer Hintergrundreportage stellen wir Ihnen in diesem Zusammenhang neu entstehende Berufsfelder vor und fragen uns, wie die Menschen in 20 Jahren arbeiten werden.\"
      },
      {
        \"id\": \"h\",
        \"title\": \"Wie zufrieden sind Sie mit Ihrer Arbeit?\",
        \"description\": \"Für alle, die sich fragen, ob sie nach neuen beruflichen Herausforderungen suchen sollten, hat unsere Arbeitspsychologin Sandra Hauser einen Fragebogen entwickelt. Dieser erleichtert die Entscheidung, ob man besser bleibt oder doch lieber geht.\"
      }
    ],
    \"solutions\": {
      \"1\": \"d\",
      \"2\": \"b\",
      \"3\": \"h\",
      \"4\": \"a\",
      \"5\": \"f\"
    }
  }
  

Your task is to generate the mock test and answer. 

"""),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()
