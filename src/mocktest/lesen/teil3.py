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

In the second step generate markdown for 3 ideas about the needs content and 3 post idea to which can answer for the need. Make sure the mapping is not too trivial but have to comprehensive understanding.

In the third step generate markdown for 3 more distractor which *can not* answer for the three needs above.

In the fourth step, generate markdown for one more person's need that acks like a distractor. Make sure the need *can not* use any above posts that generated to answer. However, the need must be related a post that generated above to make it more challenging.

In the fifth step, generate the json format for the final mocktest. Fowllow exactly the same structure as the example in the system instruction 

*Mocktest have to be in json format starting with ```json and ending with ```*"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1.5,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""**Prompt for Generating a B2 German Reading Comprehension Task (Lesen Teil 3 Format) with Sophisticated Distractors**

**Objective:** Generate a German language reading comprehension exercise conforming precisely to the format and difficulty of \"Lesen Teil 3\" typical for B2 level exams (e.g., Test für den Beruf B2, telc B2). The task requires matching four people's work-related situations to one relevant forum post out of six, with one situation having no match. Crucially, the non-matching posts (distractors) must be carefully designed to test precise comprehension and differentiate nuanced situations, mirroring the complexity observed in authentic test materials.

**Core Task Structure:**

1.  **Situations/Scenarios (People Seeking Info):** Create **four (4)** distinct short texts.
    *   **Persona:** Assign a plausible German first name and ID (1-4) to each person.
    *   **Content:** Describe a specific, realistic work-related problem, question, or situation in Germany (referencing themes below). The situations must contain nuances and specific details (e.g., probation period, specific type of contract issue, precise reason for absence, type of work clothing mentioned) that differentiate them clearly, even if the general topic is similar. One situation should be deliberately crafted to be slightly more complex, multi-faceted, or involve a less common legal point, making it suitable for the eventual 'x' (no match) designation. 
    *   **Themes (Examples):** Salary (negotiation, equal pay, deductions), Working Hours (overtime, breaks, weekends), Vacation (entitlement, illness during), Termination (probation, redundancy, misconduct), Employee Rights (pregnancy, parental leave, disability), Workplace Conflicts, Accidents (workplace, commute), Insurance, Work Clothing (safety vs. uniform, costs), Contracts (oral vs. written), Work-Life Balance, Apprentice Rights.
    *   **Language Level:** Strict B2 CEFR German. Natural tone, appropriate vocabulary, concluding with a clear question/request.
    *   **Format:** Single paragraph per person.

2.  **Forum Posts (Information/Advice):** Create **six (6)** distinct short texts.
    *   **Persona:** Assign a plausible German first name, ID ('a'-'f'), and a relative timestamp (e.g., \"vor 30 Minuten\", \"vor 5 Stunden\") to each post author.
    *   **Content:** Offer advice, information, opinion, or experience related to the general themes. **Crucially, the design of these posts must follow the distractor strategy outlined below.**
    *   **Language Level:** Strict B2 CEFR German. Typical online forum tone (helpful, sometimes opinionated, semi-formal/informal).
    *   **Format:** Single paragraph per post.

3.  **Matching Logic and Strategic Distractor Design (CRITICAL):**
    *   **Basic Rule:** **Exactly three (3)** situations (1-4) must match exactly **one** post ('a'-'f') each. This post must directly and accurately address the core issue(s) raised in the person's situation. **Exactly one (1)** situation must have **no** suitable match among the six posts (designate its solution as 'x'). Consequently, **three (3)** posts will be unused distractors.
    *   **Designing Effective Distractors (Apply these techniques strategically):**
        *   **Keyword Overlap, Different Context:** Intentionally use key vocabulary from a situation (e.g., \"Kündigung\", \"Überstunden\", \"Arbeitskleidung\") in a distractor post, but apply it to a *different specific context* or legal scenario than the one described in the situation. Make it superficially relevant but incorrect upon close reading.
        *   **Similar Topic, Different Legal Specifics:** Create posts addressing the same general topic (e.g., dismissal, accidents) but focusing on a *different legal nuance* than required by the situation (e.g., probation dismissal vs. long-term employee dismissal; commute accident vs. workplace accident; safety clothing cost vs. uniform cost).
        *   **Address Only Part of the Question:** Design a post (especially targeting the likely 'x' situation) that addresses only *one aspect* of a multi-part question or concern raised in a situation, leaving the core issue or another key part unanswered, making it an incomplete/unsatisfactory match.
        *   **Offer Opinion/Experience vs. Specific Advice:** Include posts that express personal opinions, general feelings, or anecdotes related to a topic, rather than providing the specific factual, legal, or procedural information requested in a situation.
        *   **Plausible but Irrelevant Information:** Ensure the three unused posts discuss plausible work-related topics but are clearly *not relevant* to any of the four specific situations presented. They serve to increase reading load and test elimination skills.
    *   **Process:** First, finalize the four situations (including the intended 'x'). Second, write the three 'correct' matching posts. Third, *strategically design* the remaining three distractor posts using the techniques above, explicitly aiming to create ambiguity and test precise reading skills related to the initial situations.

4.  **Overall Theme:** Define and state a clear overarching theme (e.g., \"Rund um den Beruf\", \"Tipps für Arbeitnehmerinnen und Arbeitnehmer\", \"Arbeitsrechtliche Fragen\").

5.  **Text Length Guidelines (Approximate Targets):**

*   **Thema (Overall Theme):** Keep this very brief and descriptive. Aim for **2-6 words**.
    *   *Example:* \"Rund um den Beruf\", \"Tipps für Azubis\", \"Arbeitsrecht Kompakt\".

*   **Person Situation (people\\_seeking\\_info):** Each situation should be concise but contain enough detail to present the problem clearly, including necessary nuances for matching/distraction. Aim for a length of approximately **50-80 words** (roughly 3-6 standard sentences). Ensure the core question or request for help is clearly stated at the end.

*   **Post Content (posts):** Each forum post should feel like a realistic response. It should be long enough to convey a piece of advice, information, or opinion, but remain succinct. Aim for a length of approximately **40-70 words** (roughly 2-5 standard sentences). This allows for specific details or effective distraction without unnecessary length.

*   **Flexibility:** These word counts are guidelines, not absolute limits. Slight variations are acceptable if needed for clarity or to effectively implement a distractor strategy. However, maintain overall balance – avoid excessively long or extremely short texts compared to the others in the set, as this can affect timing and perceived difficulty.

6.  **Output Format:** Present the result in the following strict JSON format:
    ```json
    {
      \"thema\": \"...\", // The overall theme
      \"people_seeking_info\": [
        {
          \"id\": 1,
          \"name\": \"...\",
          \"situation\": \"...\"
        },
        {
          \"id\": 2,
          \"name\": \"...\",
          \"situation\": \"...\"
        },
        {
          \"id\": 3,
          \"name\": \"...\",
          \"situation\": \"...\"
        },
        {
          \"id\": 4,
          \"name\": \"...\",
          \"situation\": \"...\"
        }
      ],
      \"posts\": [
        {
          \"id\": \"a\",
          \"author\": \"...\",
          \"timestamp\": \"...\",
          \"content\": \"...\"
        },
        // ... entries for b, c, d, e, f
      ],
      \"solutions\": {
        \"1\": \"...\", // e.g., \"c\" or \"x\"
        \"2\": \"...\", // e.g., \"f\" or \"x\"
        \"3\": \"...\", // e.g., \"a\" or \"x\"
        \"4\": \"...\"  // e.g., \"d\" or \"x\"
         // Exactly one value MUST be \"x\". The letters must correspond to the correct matches.
      }
    }
    ```

7.  **Quality Control / Final Check:** Before concluding, review the generated task:
    *   Confirm adherence to all constraints (4 situations, 6 posts, 3 matches, 1 'x', 3 unused posts).
    *   Verify the B2 language level consistency.
    *   Critically assess the effectiveness of the distractors: Are they genuinely tempting? Do they require careful reading of nuances?
    *   Ensure the 'x' situation truly lacks a satisfactory answer, considering all posts.
    *   Double-check the accuracy of the `solutions` provided in the JSON.

Example 1:

{
    \"thema\": \"Rund um den Beruf\",
    \"people_seeking_info\": [
      {
        \"id\": 1,
        \"name\": \"Daniel\",
        \"situation\": \"Ich arbeite bei einer Spedition im Büro. Eine meiner Kolleginnen hat fast die gleichen Aufgaben wie ich. Nun habe ich erfahren, dass sie deutlich mehr verdient. Das ist doch unfair! Habe ich nicht Anspruch auf die gleiche Bezahlung?\"
      },
      {
        \"id\": 2,
        \"name\": \"Kamila\",
        \"situation\": \"Ich arbeite normalerweise sehr sorgfältig, aber vorgestern ist mir ein dummer Fehler passiert, durch den meinem Arbeitgeber zusätzliche Kosten entstanden sind (etwa 500 Euro). Jetzt habe ich Angst, dass ich das Geld vom Lohn abgezogen bekomme. Könnte das passieren?\"
      },
      {
        \"id\": 3,
        \"name\": \"Marlene\",
        \"situation\": \"In dem letzten Gespräch mit meinem Chef hat er mir fest versprochen, dass ich im neuen Jahr eine Gehaltserhöhung bekommen würde. Nun haben wir Januar und er kann sich plötzlich nicht mehr daran erinnern. Was kann ich tun?\"
      },
      {
        \"id\": 4,
        \"name\": \"Ümit\",
        \"situation\": \"Letzte Woche bin ich drei Tage nicht zur Arbeit gegangen, weil mein siebenjähriger Sohn Fieber hatte. Ich bin alleinerziehend und hatte in dieser Zeit niemanden, der sich um mein Kind kümmern konnte. Wird jetzt mein Gehalt gekürzt?\"
      }
    ],
    \"posts\": [
      {
        \"id\": \"a\",
        \"author\": \"Sekou\",
        \"timestamp\": \"vor 11 Minuten\",
        \"content\": \"Wenn das nur eine mündliche Zusage war und Sie nichts Schriftliches in der Hand haben (z. B. ein Protokoll von Ihrem Gespräch), können Sie leider gar nichts machen. Mein Tipp: Überzeugen Sie weiterhin mit guten Leistungen und sprechen Sie Ihren Chef zu einem späteren Zeitpunkt noch mal auf das Thema an.\"
      },
      {
        \"id\": \"b\",
        \"author\": \"Natalia\",
        \"timestamp\": \"vor 30 Minuten\",
        \"content\": \"Ich finde es auch ungerecht, dass Frauen in vielen Berufen immer noch weniger verdienen als Männer in den gleichen Berufen. Wir reden ja hier nicht von ein paar Euro, sondern von fast 20 Prozent! Dieser Unterschied ist für mich nicht nachvollziehbar. Gleicher Lohn für Frauen und Männer – das ist meine Meinung!\"
      },
      {
        \"id\": \"c\",
        \"author\": \"Eduardo\",
        \"timestamp\": \"vor 58 Minuten\",
        \"content\": \"Die Höhe des Gehalts ist in der Regel Verhandlungssache zwischen Arbeitgeber und Arbeitnehmer. Das heißt, wer geschickt verhandelt, verdient mehr. Oft gibt es auch ganz sachliche Erklärungen für Gehaltsunterschiede (Dauer der Betriebszugehörigkeit, Berufserfahrung, unterschiedliche Qualifikationen etc.).\"
      },
      {
        \"id\": \"d\",
        \"author\": \"André\",
        \"timestamp\": \"vor 2 Stunden\",
        \"content\": \"Das verstehe ich! Lohnkürzungen sind immer ein Schock für die Angestellten, aber sie sind tatsächlich zulässig – vorausgesetzt, das Unternehmen befindet sich in einer wirtschaftlichen Notsituation. Wichtig zu wissen: Wenn der Arbeitgeber aus betrieblichen Gründen die Löhne kürzt, betrifft das alle Mitarbeiter*innen, nicht nur einzelne.\"
      },
      {
        \"id\": \"e\",
        \"author\": \"Yeliz\",
        \"timestamp\": \"vor 3 Stunden\",
        \"content\": \"Eltern haben das Recht, sich nach der Geburt ihres Kindes eine Auszeit von der Arbeit nehmen, die sogenannte \"Elternzeit\". Der Arbeitgeber muss dir in dieser Zeit kein Gehalt zahlen, ein Einkommen hast du aber trotzdem – über das Elterngeld.\"
      },
      {
        \"id\": \"f\",
        \"author\": \"Marie-Luise\",
        \"timestamp\": \"vor 4 Stunden\",
        \"content\": \"Mach dir keine Sorgen. Wo Menschen arbeiten, läuft nicht immer alles perfekt. Das ist ganz normal und keinesfalls ein Grund für eine Lohn- oder Gehaltskürzung. Diese erlaubt das Arbeitsrecht nur in Ausnahmesituationen, z. B. wenn ein Mitarbeiter absichtlich seinem Arbeitgeber Schaden zufügt.\"
      }
    ],
    \"solutions\": {
      \"1\": \"c\",
      \"2\": \"f\",
      \"3\": \"a\",
      \"4\": \"x\"
    }
}
  

Example 2:

{
    \"thema\": \"Tipps für junge Auszubildende\",
    \"people_seeking_info\": [
      {
        \"id\": 1,
        \"name\": \"Martha\",
        \"situation\": \"Ich habe eine einfache Frage. Wie viele Tage Urlaub sollte ein Azubi unter 18 Jahren bekommen? Bei uns in der Firma haben fast alle Azubis unter 18 Jahren 24 Urlaubstage. Sie haben auch eine 40-Stunden-Woche, brauchen aber samstags nicht zu arbeiten. Wie ist das bei euch? Antwortet mal fleißig, wenn's geht, mit einem Link zum Gesetz.\"
      },
      {
        \"id\": 2,
        \"name\": \"Tomas\",
        \"situation\": \"Hallo Leute, unser Chef möchte, dass wir auch am Samstag arbeiten. Wir sind noch in der Ausbildung. Wir haben gehört, dass Auszubildende am Samstag nicht arbeiten dürfen. Kann jemand schnell Auskunft geben?\"
      },
      {
        \"id\": 3,
        \"name\": \"Egle\",
        \"situation\": \"Eine Frage an alle. Hat jemand hier schon Erfahrungen gemacht? Ich hatte vor Monaten Urlaub beantragt, dann wurde ich zwei Tage vorher krank. Ich musste eine Woche zu Hause bleiben. Danach konnte ich dann zu meiner Familie nach Litauen in Urlaub fahren. Mein Chef sagt nun, dass ich Pech hatte, weil ich im Urlaub krank war. Die Krankentage hat er mir als Urlaubstage abgezogen. Eine Kollegin sagt, ich soll mich beschweren. Was soll ich tun?\"
      },
      {
        \"id\": 4,
        \"name\": \"Paul\",
        \"situation\": \"Bei uns erhalten junge Leute unter 18 Jahren in der Ausbildung nur 25 Tage Urlaub. Wenn sie über 18 Jahre alt sind, kriegen sie sogar nur 24 Tage. Ich habe gehört, dass viele Betriebe einen Betriebsrat und eine Betriebsvereinbarung dazu haben. Was können wir hier machen, um mehr Informationen zu bekommen?\"
      }
    ],
    \"posts\": [
      {
        \"id\": \"a\",
        \"author\": \"Suszanna\",
        \"timestamp\": \"vor 3 Stunden\",
        \"content\": \"Ich finde es total ungerecht, dass minderjährige Azubis mehr Urlaub bekommen als volljährige. Man sagt doch immer, jüngere Menschen seien belastbarer als ältere. Bei uns ist das aber auch so.\"
      },
      {
        \"id\": \"b\",
        \"author\": \"Hanna\",
        \"timestamp\": \"vor 56 Minuten\",
        \"content\": \"Also, grundsätzlich ist der Samstag ein ganz normaler Werktag, ihr dürft da also auch arbeiten. Geschützt sind allerdings minderjährige Auszubildende, die nur dann samstags arbeiten dürfen, wenn sie dafür in derselben oder der darauffolgenden Woche einen Tag frei machen dürfen.\"
      },
      {
        \"id\": \"c\",
        \"author\": \"Veronica\",
        \"timestamp\": \"vor 9 Stunden\",
        \"content\": \"Krankheitszeiten haben keinen Einfluss auf den Urlaubsanspruch. Die Fehltage dürfen nicht auf den Urlaubsanspruch angerechnet werden. Im Gegenteil: Erkrankt der Azubi im Urlaub, werden die Krankentage nicht auf den Urlaub angerechnet, wenn er eine Krankmeldung vorlegt.\"
      },
      {
        \"id\": \"d\",
        \"author\": \"Franziska\",
        \"timestamp\": \"vor 42 Minuten\",
        \"content\": \"Urlaub ist Urlaub und Krankheit ist Krankheit. Wenn du krank bist, musst du das in der Berufsschule melden. Am besten, du reichst das Attest vom Arzt dort ein. Mach das aber möglichst sofort, sonst fehlen dir eventuell einige Tage in deiner Berufsschule.\"
      },
      {
        \"id\": \"e\",
        \"author\": \"Chiara\",
        \"timestamp\": \"vor 3 Stunden\",
        \"content\": \"Samstags arbeiten ist immer blöd. Ich mache das auch nicht gerne. Aber manchmal muss es eben sein. Viele ältere Kollegen müssen auf jeden Fall Samstag ran. Ich würde das auch unbedingt machen, das macht einen guten Eindruck!\"
      },
      {
        \"id\": \"f\",
        \"author\": \"Louis\",
        \"timestamp\": \"vor 49 Minuten\",
        \"content\": \"Das kann eigentlich nicht sein, denn das Gesetz schreibt vor, dass minderjährige Auszubildende mindestens 25 Werktage Urlaub haben müssen. Die wöchentliche Arbeitszeit beträgt für Minderjährige maximal 40 Stunden, Azubis über 18 dürfen sogar 48 Stunden pro Woche arbeiten, allerdings verteilt auf 6 Tage. Den Link dazu findest du unter www.azubi-azubine.de.\"
      }
    ],
    \"solutions\": {
      \"1\": \"f\",
      \"2\": \"b\",
      \"3\": \"c\",
      \"4\": \"x\"
    }
}
  

Example 3:

{
    \"thema\": \"Tipps für Arbeitnehmerinnen und Arbeitnehmer\",
    \"people_seeking_info\": [
      {
        \"id\": 1,
        \"name\": \"Ansgar\",
        \"situation\": \"Ich arbeite seit Kurzem in leitender Position und muss jetzt das erste Mal einen Mitarbeiter entlassen. Der Angestellte ist älter als ich und arbeitet schon sehr lange in der Firma. Ich kenne natürlich die gesetzlichen Vorgaben und Fristen, weiß aber nicht, wie ich in dem Fall am besten vorgehen soll. Kann mir jemand einen Rat geben?\"
      },
      {
        \"id\": 2,
        \"name\": \"Will\",
        \"situation\": \"Hallo liebe Forumsmitglieder! Ich stehe noch unter Schock. Soeben ist mir in der Probezeit gekündigt worden. Ich bin schon fünf Monate im Betrieb und noch letzte Woche hat man mich gelobt. Was mache ich jetzt?\"
      },
      {
        \"id\": 3,
        \"name\": \"Bahar\",
        \"situation\": \"Weiß jemand Bescheid? Ich bin in der achten Woche schwanger und frage mich, wann ich das meinem Arbeitgeber mitteilen muss. Eigentlich wollte ich warten, bis ich im vierten Monat bin, aber jetzt habe ich gehört, dass das zu spät ist. Stimmt das? Ich möchte durch meine Schwangerschaft keine Nachteile in meinem Job!\"
      },
      {
        \"id\": 4,
        \"name\": \"Serena\",
        \"situation\": \"Ich bin mit meiner Arbeit unzufrieden und langweile mich. Jetzt habe ich etwas Besseres in Aussicht und möchte kündigen. Meine Chefin war immer sehr bemüht, mich zu halten, und hat mir gerade den Lohn erhöht. Nun weiß ich nicht so richtig, wie ich das Kündigungsschreiben angemessen formulieren soll. Hat jemand einen Tipp für mich?\"
      }
    ],
    \"posts\": [
      {
        \"id\": \"a\",
        \"author\": \"Verena\",
        \"timestamp\": \"vor einem Tag\",
        \"content\": \"Ich habe auch gekündigt und war davor wie du in einem absoluten Gefühlschaos. Tue ich das Richtige? Was, wenn ich nach so langer Betriebszugehörigkeit keinen neuen Job finde? Ich war danach dann auch ziemlich lange arbeitslos, aber bereut habe ich es keine Sekunde.\"
      },
      {
        \"id\": \"b\",
        \"author\": \"Alexej\",
        \"timestamp\": \"vor vier Stunden\",
        \"content\": \"Wer redet Ihnen denn so etwas ein? Wer ein Kind erwartet und zur Welt bringt, hat auch im Arbeitsleben Rechte! Selbstverständlich gilt für Sie das Mutterschutzgesetz und Sie können Ihren Job nicht verlieren. Hier können Sie nachfragen: info@bmfsfjservice.bund.de\"
      },
      {
        \"id\": \"c\",
        \"author\": \"Lale\",
        \"timestamp\": \"vor neun Stunden\",
        \"content\": \"Vorgesetzte sind auch nur Menschen und niemand kündigt gerne. Meine Empfehlung: Sie sind nicht verpflichtet, ein Trennungsgespräch zu führen, aber machen Sie es und erklären Sie die Gründe, bevor die schriftliche Kündigung rausgeht.\"
      },
      {
        \"id\": \"d\",
        \"author\": \"Fritz\",
        \"timestamp\": \"vor dreißig Minuten\",
        \"content\": \"Wenn Sie Ihr Arbeitsverhältnis lösen möchten, dann müssen Sie das fristgerecht und schriftlich tun. Selbstverständlich brauchen Sie keine Gründe zu nennen. In Ihrem Fall können Sie ja zuerst mit Ihrer Vorgesetzen sprechen und erklären, dass Sie private Motive haben, dann ist niemand gekränkt.\"
      },
      {
        \"id\": \"e\",
        \"author\": \"Bettina\",
        \"timestamp\": \"vor 12 Stunden\",
        \"content\": \"Nicht immer ist eine Kündigung rechtens! Besonders langjährige Arbeitnehmer genießen einen allgemeinen Kündigungsschutz. Und bestimmte Personengruppen, zum Beispiel Schwangere, haben erweiterten Schutz nach dem Sonderkündigungsgesetz.\"
      },
      {
        \"id\": \"f\",
        \"author\": \"Tina\",
        \"timestamp\": \"vor zwei Tagen\",
        \"content\": \"Ich habe in meiner Firma schon früh Bescheid gesagt, dass wir Nachwuchs erwarten. Aber da ich Zwillinge bekomme, war es auch ziemlich schnell zu sehen. Der Gesetzgeber schreibt keine Fristen vor. Machen Sie es aber bald, damit man für Sie eine Vertretung suchen kann.\"
      }
    ],
    \"solutions\": {
      \"1\": \"e\",
      \"2\": \"x\",
      \"3\": \"b\",
      \"4\": \"d\"
    }
}
  

Example 4:

{
    \"thema\": \"Tipps zu Work-Life-Balance\",
    \"people_seeking_info\": [
      {
        \"id\": 1,
        \"name\": \"Lea\",
        \"situation\": \"Ich weiß nicht, wie's euch geht, aber mir wachsen Familie und Vollzeitjob allmählich über den Kopf. Wir haben zwei Kinder und wir teilen uns den Haushalt, aber der Job von meinem Mann fordert ihn auch sehr. Zu viele Aufgaben bleiben an mir hängen, sodass ich mich immer häufiger frage, wie ich das alles schaffen soll.\"
      },
      {
        \"id\": 2,
        \"name\": \"Luciano\",
        \"situation\": \"Hallo! In meiner Firma ist flexible Arbeitszeit möglich und ich nutze sie auch gern. Oft fange ich erst um 10:30 Uhr an, weil es für mich so besser ist. Ich kann dann morgens noch Sport machen und mich um meine gehbehinderte Mutter kümmern. Aber meine Kollegen machen mir jetzt Stress deswegen. Sie wollen die Team-Besprechung (zweimal pro Woche) um 8:30 Uhr abhalten. Kann ich mich dagegen wehren?\"
      },
      {
        \"id\": 3,
        \"name\": \"Jorges\",
        \"situation\": \"Eigentlich gefällt mir meine Arbeit. Sie ist interessant und abwechslungsreich und aufgrund meiner langen Erfahrung kann ich anderen helfen. Mein Chef hat das gemerkt und fragt mich immer öfter, ob ich Überstunden machen oder für jemand einspringen kann. Wie soll ich ihm sagen, dass ich das nicht will?\"
      },
      {
        \"id\": 4,
        \"name\": \"Kiara\",
        \"situation\": \"Kennt ihr das auch? Ich habe total viel Arbeit im Büro, mache viele Überstunden und pendle auch noch eine Stunde zur Arbeit. Manchmal ruft dann am Abend auch noch ein Kunde oder die Chefin auf dem Firmenhandy an. Das geht die ganze Woche so. Ich bin total gestresst, habe oft Kopfschmerzen und kann gar nicht mehr abschalten! Habt ihr einen Tipp für mich?\"
      }
    ],
    \"posts\": [
      {
        \"id\": \"a\",
        \"author\": \"Jonas\",
        \"timestamp\": \"vor 30 Minuten\",
        \"content\": \"So ging es mir auch und irgendwann bin ich davon krank geworden. Lass es nicht dazu kommen. Ein Arbeitgeber hat eine Fürsorgepflicht seinen Mitarbeitern gegenüber. Dazu gehört auch, die Gesundheit zu schützen und für die Einhaltung der Ruhezeiten zu sorgen. Hier findest du noch gute Hinweise dazu: www.gewerkschaft.org/gesundheit und arbeit\"
      },
      {
        \"id\": \"b\",
        \"author\": \"Lukas\",
        \"timestamp\": \"vor 5 Stunden\",
        \"content\": \"Die Elternzeit kannst du pro Kind bis zu drei Jahren nehmen – und du kannst sie auch aufteilen! Das gilt übrigens für Mütter und Väter. Keine Angst, dein Arbeitgeber kann dir in dieser Zeit nicht kündigen.\"
      },
      {
        \"id\": \"c\",
        \"author\": \"Miriam\",
        \"timestamp\": \"vor 3 Stunden\",
        \"content\": \"Es ist unfair: Von Frauen erwartet man, dass sie Arbeit und Familie perfekt bewältigen. Was dir helfen könnte, sind flexible Arbeitszeiten. Frag doch deine Chefin, ob du für eine Zeit lang deine Stunden reduzieren kannst. Man hat einen Anspruch auf Teilzeitarbeit. Das gilt natürlich auch für Männer. 😊\"
      },
      {
        \"id\": \"d\",
        \"author\": \"Johanna\",
        \"timestamp\": \"vor 40 Minuten\",
        \"content\": \"Man kann nicht emig Überstunden machen. Irgendwann muss dir dein Arbeitgeber die Möglichkeit geben, deine Überstunden abzubauen oder sie dir auszahlen zu lassen. Wie das bei euch geregelt ist, musst du mal in deinem Arbeitsvertrag nachlesen. Oder sprich auch mal mit dem Betriebsrat.\"
      },
      {
        \"id\": \"e\",
        \"author\": \"Clara\",
        \"timestamp\": \"vor 2 Stunden\",
        \"content\": \"Ein Burnout erkennst du daran, dass sich der Betroffene immer schlechter konzentrieren kann und immer mehr Fehler bei der Arbeit macht. Manche Leute sagen, dass sie nicht einmal mehr in der Freizeit Energie haben. Dein Kollege sollte auf jeden Fall zu einem Arzt gehen.\"
      },
      {
        \"id\": \"f\",
        \"author\": \"Tobias\",
        \"timestamp\": \"vor 32 Minuten\",
        \"content\": \"Mit flexiblen Arbeitszeiten kann man das Privatleben und die Arbeit besser vereinbaren, das ist richtig. Trotzdem muss man aber auch darauf achten, dass die Zusammenarbeit im Team noch funktioniert. Sich gut abzusprechen, ist dabei sehr wichtig, z. B. was die Zeiten für Meetings betrifft. Da musst du auch Kompromisse eingehen.\"
      }
    ],
    \"solutions\": {
      \"1\": \"c\",
      \"2\": \"f\",
      \"3\": \"x\",
      \"4\": \"a\"
    }
}
  

Example 5:

{
  \"thema\": \"Tipps für Arbeitnehmerinnen und Arbeitnehmer\",
  \"people_seeking_info\": [
    {
      \"id\": 1,
      \"name\": \"Achim\",
      \"situation\": \"Ich bin Aufzugsmonteur, mein Job ist körperlich sehr anstrengend und ich habe Probleme mit den Gelenken. Mein Hausarzt meinte neulich, ich könne nicht mehr Vollzeit arbeiten. Ich brauche aber mein volles Gehalt und habe Angst vor finanziellen Einschränkungen. Mein Arzt brachte dann eine Erwerbsminderungsrente ins Spiel. Wo kann ich mich darüber informieren, weiß das jemand?\"
    },
    {
      \"id\": 2,
      \"name\": \"Ute\",
      \"situation\": \"Ich bin vorhin auf dem Weg von der Arbeit nach Hause mit dem Fahrrad gestürzt. Zum Glück ist außer ein paar Schrammen an den Händen nichts passiert, aber jetzt meinte mein Mann gerade, dass ich das dem Arbeitgeber melden muss, auch wegen möglicher Spätfolgen. Ist das nicht übertrieben? Ich bin in der Probezeit und will keinen Ärger.\"
    },
    {
      \"id\": 3,
      \"name\": \"Liane\",
      \"situation\": \"Ich habe gerade die Stelle gewechselt und in meinem neuen Betrieb findet demnächst ein Ausflug in einen Klettergarten statt. Ich will kein Spielverderber sein, aber klettern ist echt nicht mein Ding und ich mache mir Sorgen, was ist, wenn was passiert? Eine Kollegin meinte, wir wären da auch unfallversichert, weil die Firma das organisiert. Ist das richtig?\"
    },
    {
      \"id\": 4,
      \"name\": \"Wolfgang\",
      \"situation\": \"Letzte Woche bin ich wie so oft aus der Werkstatt gegangen, um eine Zigarette anzuzünden, und dann bin ich draußen ganz blöd gestolpert und habe mir das Handgelenk gebrochen. Heute meinte mein Chef, dass die gesetzliche Unfallversicherung nichts zahlt, weil ich privat draußen war. Stimmt das?! Das würde mich echt schockieren. Ich brauche irgendwann auch eine Reha, das kostet doch alles Geld!\"
    }
  ],
  \"posts\": [
    {
      \"id\": \"a\",
      \"author\": \"Heinrich\",
      \"timestamp\": \"vor drei Stunden\",
      \"content\": \"Das ist tatsächlich nicht einfach, denn auch im Büro hat man mal private Minuten, zum Beispiel in WC-Räumen. Wenn da was passiert, ist das nicht automatisch ein Arbeitsunfall. Schau mal im Internet unter www.arbeitsrecht-aktuell24.eu, da findest du ein Urteil zu dem Fall, den ich gerade erwähnt habe.\"
    },
    {
      \"id\": \"b\",
      \"author\": \"Niloofar\",
      \"timestamp\": \"vor acht Stunden\",
      \"content\": \"Berufskrankheiten können einen schwer treffen. In meiner Firma ist eine Kollegin lange Zeit ausgefallen. Alle dachten, sie hätte Probleme mit der Lunge, weil sie Raucherin ist, aber wegen der Arbeit am Computer hatte sie Rückenprobleme. Sie kann jetzt nur noch 2 Stunden am Tag am Schreibtisch sitzen und unser Chef hat für sie einen höhenverstellbaren Schreibtisch besorgt. Das hilft ihr. Vielleicht ist das auch was für dich?\"
    },
    {
      \"id\": \"c\",
      \"author\": \"Chris\",
      \"timestamp\": \"vor einem Tag\",
      \"content\": \"Ich fürchte, dein Arbeitgeber hat gute Karten. Wege zum Imbiss oder Restaurant in der Mittagspause sind genauso wenig versichert wie deine Raucherpause. Das gehört einfach nicht zur Arbeitszeit. Tut mir leid, dass ich keine bessere Nachricht habe.\"
    },
    {
      \"id\": \"d\",
      \"author\": \"Petra\",
      \"timestamp\": \"vor einer Stunde\",
      \"content\": \"Das ist kein Problem. Du musst nicht von der Adresse losfahren, unter der du gemeldet bis, um versichert zu sein. Als Arbeitsweg gilt auch, wenn du zum Beispiel am Wochenende immer bei deinem Freund oder deinen Eltern bist und dann Freitag nach Feierabend direkt vom Arbeitsort dort hinfährst.\"
    },
    {
      \"id\": \"e\",
      \"author\": \"Shakuntala\",
      \"timestamp\": \"vor vierzig Minuten\",
      \"content\": \"Das kann man so pauschal nicht sagen. Wenn zum Beispiel regelmäßig Sport in der Firma stattfindet, ist das versichert, genauso wie eine Weihnachtsfeier, die veranstaltet wird, um den Zusammenhalt der Belegschaft zu stärken. In deinem Fall ist es fraglich, ob das dem Zusammenhalt dient oder nicht einfach eine gemeinsame Freizeitunternehmung ist. Sprich mal die Vorgesetzten an.\"
    },
    {
      \"id\": \"f\",
      \"author\": \"Arkardi\",
      \"timestamp\": \"vor zwölf Stunden\",
      \"content\": \"Ob dir das wirklich hilft, weiß ich nicht, denn natürlich bekommst du dann nicht so viel Geld wie jetzt durch eine volle Stelle. Aber wenn das, was du hast, eine anerkannte Berufskrankheit ist, dann hast du schon Anspruch auf Leistungen. Am besten kann dir da die Deutsche Rentenversicherung helfen.\"
    }
  ],
  \"solutions\": {
    \"1\": \"f\",
    \"2\": \"x\",
    \"3\": \"e\",
    \"4\": \"c\"
  }
}

Example 6:

{
  \"thema\": \"Tipps für Arbeitnehmerinnen und Arbeitnehmer\",
  \"people_seeking_info\": [
    {
      \"id\": 1,
      \"name\": \"Franz\",
      \"situation\": \"Meine Firma hat Dienstkleidung eingeführt: Für die Männer Anzüge, die Frauen können zwischen Hosenanzug oder Kostüm wählen. Das soll zum Unternehmensimage beitragen – nur leider sind Anzüge nicht mein Stil. Kann mir gekündigt werden, wenn ich es ablehne, diese Anzüge zu tragen?\"
    },
    {
      \"id\": 2,
      \"name\": \"Isabelle\",
      \"situation\": \"Hallo, ich würde gerne wissen, wer die Arbeitsschutzkleidung bezahlen muss: Ich arbeite in einem Labor und muss laut Arbeitsvertrag welche tragen. Die Schutzbrille und die Einmalhandschuhe werden vor Ort gestellt, die Kittel und Schuhe muss ich aber aus eigener Tasche bezahlen. Auf meine Frage, ob das korrekt ist, wurde mir mit \"ja\" geantwortet, ich solle die Kosten dafür bei der Steuer angeben.\"
    },
    {
      \"id\": 3,
      \"name\": \"Andrés\",
      \"situation\": \"Ich bin Leiter des Serviceteams in einem bayerischen Lokal und muss wie alle Angestellten als Dienstkleidung eine Lederhose und ein kariertes Hemd tragen, die Frauen ein Dirndl. Wir schwitzen bei der Arbeit und ich brauche jeden Tag sogar ein bis zwei frische Hemden. Unser Arbeitgeber will, dass wir die Kleidung selbst bezahlen. Ich finde das nicht ok. Meine Frage: Müssen mein Team und ich das akzeptieren?\"
    },
    {
      \"id\": 4,
      \"name\": \"Tobias\",
      \"situation\": \"Wer kann mir helfen? Ich arbeite als Altenpfleger bei einem häuslichen Pflegedienst. Wir können bei der Arbeit unsere private Kleidung tragen. Meine Frage ist, ob ich den Kaufpreis und die Kosten für die Instandhaltung und das Waschen meiner Kleidung bei der Steuer angeben kann? Wäre super, wenn ich dafür Geld zurückbekommen könnte.\"
    }
  ],
  \"posts\": [
    {
      \"id\": \"a\",
      \"author\": \"Wael\",
      \"timestamp\": \"vor einer Stunde\",
      \"content\": \"Dienstkleidung soll für ein einheitliches Aussehen des Teams sorgen und so das Image des Unternehmens repräsentieren. Die Arbeitsschutzkleidung, z.B. in einem Labor, schützt den Träger und die Umwelt. Was hast du gegen weiße Kittel in einer Praxis? Das gehört doch zum Beruf.\"
    },
    {
      \"id\": \"b\",
      \"author\": \"Sabrina\",
      \"timestamp\": \"vor neun Stunden\",
      \"content\": \"Arbeitgeber dürfen ihren Angestellten die Arbeitskleidung vorschreiben. Man muss zwischen \"Dienstkleidung\" und \"Arbeitsschutzkleidung\" unterscheiden. Ihre Frage bezieht sich aber auf die \"Dienstkleidung\", die Sie theoretisch auch privat tragen könnten, auch wenn viele das nicht machen. Der Arbeitgeber kann hier verlangen, dass Sie dafür selbst aufkommen.\"
    },
    {
      \"id\": \"c\",
      \"author\": \"Gerhard\",
      \"timestamp\": \"vor einem Tag\",
      \"content\": \"Klare Antwort: Ja! Das Interesse des Arbeitgebers an der angemessenen Kleidung seiner Mitarbeiter wiegt schwerer als Ihr Interesse, sich individuell zu kleiden. Wenn Sie sich weigern, die Dienstkleidung zu tragen, kann es Ihnen passieren, dass Sie nach zwei Abmahnungen Ihren Job verlieren.\"
    },
    {
      \"id\": \"d\",
      \"author\": \"Matteo\",
      \"timestamp\": \"vor acht Stunden\",
      \"content\": \"Arbeitsschutzkleidung ist eine persönliche Schutzkleidung zur Verhütung von Arbeitsunfällen und Berufskrankheiten. Dein Arbeitgeber ist verpflichtet, darauf zu achten, dass die Kleidung immer den neuesten Standards entspricht. Schau mal hier rein: www.arbeitsschutzgesetz.org/ arbeitsschutzkleidung\"
    },
    {
      \"id\": \"e\",
      \"author\": \"Chiara\",
      \"timestamp\": \"vor zwei Stunden\",
      \"content\": \"Arbeitsbekleidung muss typisch und als Arbeitsbekleidung erkennbar sein. Auch wenn der Arbeitgeber Kleidung wie Anzüge, Kostüme oder weiße Hemden, die man auch privat tragen könnte, vorschreibt – diese werden steuerlich weder beim Kauf, noch bei der Reparatur oder der Reinigung anerkannt. Das wird also wohl leider nichts mit der Rückzahlung.\"
    },
    {
      \"id\": \"f\",
      \"author\": \"Tina\",
      \"timestamp\": \"vor fünf Minuten\",
      \"content\": \"Ich finde das Tragen von Berufskleidung sehr sinnvoll. In einem Baumarkt kann ich so erkennen, wer Angestellter und wer Kunde oder Kundin ist. Auch in einem Krankenhaus kann ich durch die einheitliche Berufskleidung erkennen, wer zum Personal gehört.\"
    }
  ],
  \"solutions\": {
    \"1\": \"c\",
    \"2\": \"x\",
    \"3\": \"b\",
    \"4\": \"e\"
  }
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
    # Check if the json_data has the required structure
    try:
        # Check if the required keys exist at the top level
        required_keys = ["thema", "people_seeking_info", "posts", "solutions"]
        for key in required_keys:
            if key not in json_data:
                return False, f"Missing required key: {key}"
        
        # Check people_seeking_info structure
        if not isinstance(json_data["people_seeking_info"], list):
            return False, "people_seeking_info must be a list"
        
        if len(json_data["people_seeking_info"]) != 4:
            return False, f"people_seeking_info must contain exactly 4 entries, found {len(json_data['people_seeking_info'])}"
        
        # Check each person entry
        for i, person in enumerate(json_data["people_seeking_info"]):
            required_person_keys = ["id", "name", "situation"]
            for key in required_person_keys:
                if key not in person:
                    return False, f"Missing required key '{key}' in people_seeking_info[{i}]"
            
            # Check if id is between 1 and 4
            if person["id"] not in [1, 2, 3, 4]:
                return False, f"Person id must be between 1 and 4, found {person['id']}"
        
        # Check posts structure
        if not isinstance(json_data["posts"], list):
            return False, f"posts must be a list"
        
        if len(json_data["posts"]) != 6:
            return False, f"posts must contain exactly 6 entries, found {len(json_data['posts'])}"
        
        # Check each post entry
        valid_post_ids = ["a", "b", "c", "d", "e", "f"]
        for i, post in enumerate(json_data["posts"]):
            required_post_keys = ["id", "author", "timestamp", "content"]
            for key in required_post_keys:
                if key not in post:
                    return False, f"Missing required key '{key}' in posts[{i}]"
            
            # Check if id is between a and f
            if post["id"] not in valid_post_ids:
                return False, f"Post id must be one of {valid_post_ids}, found {post['id']}"
        
        # Check solutions structure
        if not isinstance(json_data["solutions"], dict):
            return False, f"solutions must be a dictionary"
        
        if len(json_data["solutions"]) != 4:
            return False, f"solutions must contain exactly 4 entries, found {len(json_data['solutions'])}"
        
        # Check each solution entry
        valid_solution_keys = ["1", "2", "3", "4"]
        valid_solution_values = ["a", "b", "c", "d", "e", "f", "x"]
        
        # Count occurrences of "x"
        x_count = 0
        
        for key, value in json_data["solutions"].items():
            if key not in valid_solution_keys:
                return False, f"Solution key must be one of {valid_solution_keys}, found {key}"
            
            if value not in valid_solution_values:
                return False, f"Solution value must be one of {valid_solution_values}, found {value}"
            
            if value == "x":
                x_count += 1
        
        # Ensure exactly one "x" is present in solutions
        if x_count != 1:
            return False, f"solutions must contain exactly one 'x', found {x_count}"
        
        return True, "JSON structure is valid"
    
    except Exception as e:
        return False, f"Error validating JSON structure: {e}"

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
            with open(f"/Users/binhnguyen/Workspaces/TELC_B2_test/data_mocktest/lesen/teil_3/mocktest_generated_{idx + 7}.json", "w", encoding="utf-8") as f:
                json.dump(mocktest, f, indent=4, ensure_ascii=False)
            idx += 1
        except Exception as e:
            print(f"Error generating mocktest {idx}: {e}")