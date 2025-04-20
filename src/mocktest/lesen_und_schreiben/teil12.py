import base64
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
import random
import re
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
                types.Part.from_text(text="""I want to generate a complete, coherent, and realistic task for the "Lesen und Schreiben" module of the German B2 Beruf test. This includes a customer complaint email, an internal forwarding email, two multiple-choice reading comprehension questions based on the complaint, and the instruction for the writing task (replying to the complaint). All components must be consistent and interconnected.

The generated task will follow this sequence, reflecting the typical test presentation:

1. Write a markdown to describe the idea of the Customer Complaint Email
2. Write a markdown to describe the idea of the Team Leader Forwarding Email
3. Write a markdown to describe the idea of the Multiple-Choice Questions also what the distractor should be and the correct answer
4. Write a markdown to describe the idea of the Writing Task Instruction, also brainstorm what the test-taker should do to reply to the complaint
5. Output the whole task in json format as the example in the instruction"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""# Customer Complaint Email Generation

## Goal:
To automatically generate realistic complaint letters (Beschwerdebriefe/Reklamations-E-Mails) in German at a B2 level, suitable for the \"Lesen und Schreiben\" part of the B2 Beruf test. These letters should serve as the basis for reading comprehension questions and a subsequent email writing task (replying to the complaint).

## Core Components of the Complaint Letter:

1.  **Metadata:**
    *   **`Gesendet/Erhalten:`**: Date and time (e.g., `gestern, 16:49 Uhr`, `heute, 11:22 Uhr`). Keep it simple and relative (\"gestern\", \"heute\").
    *   **`Von:`**: Sender's full name (the customer). Can be an individual or imply a company role.
    *   **`An:`**: Recipient's full name (the contact person at the service provider, often the team leader mentioned in the forwarding email).
    *   **`Betreff:`**: Clear and concise subject line indicating the topic. Use keywords like `Beschwerde`, `Reklamation`, `[Service/Product Name]`, `[Date/Reference]`. (e.g., `Beschwerde Verschlechterung des Services`, `Renovierungsarbeiten`, `Reklamation Kücheneinbau`, `Beschwerde Hochzeitsbuffet am 20.08.`).

2.  **Salutation:**
    *   Formal: `Sehr geehrte Frau [Nachname],` or `Sehr geehrter Herr [Nachname],`.

3.  **Introduction:**
    *   Briefly state the reason for writing, referencing the specific service, product, contract, or date.
    *   Length: 1-2 sentences.
    *   Example: `hiermit möchte ich mich über [Service/Produkt] beschweren, den/die Sie am [Datum] für uns durchgeführt/geliefert haben.` or `ich schreibe Ihnen bezüglich [Situation/Service], mit dem wir in letzter Zeit leider unzufrieden sind.`

4.  **Context/Background (Optional but Recommended):**
    *   Briefly mention the relationship (e.g., long-term customer) or initial positive experience to contrast with the current problem. This adds realism.
    *   Length: 1-2 sentences.
    *   Example: `Bisher waren wir mit Ihrem Service/Ihren Leistungen immer sehr zufrieden.` or `Wir haben uns für Ihre Firma entschieden, da sie für [positive Eigenschaft] bekannt ist.`

5.  **Detailed Description of the Problem(s):**
    *   This is the core part. Clearly and factually describe what went wrong.
    *   Be specific: Mention dates, times, locations (if applicable), and exact issues (e.g., what was dirty, what was broken, what was missing, what was delayed).
    *   Mention the *consequences* of the problem (e.g., had to clean ourselves, event delayed, couldn't use facility, important meeting disrupted).
    *   Mention the timeline/frequency if it's an ongoing issue (e.g., `seit einigen Wochen`, `in den letzten drei Wochen`, `bei den letzten X Besuchen`, `am [Datum]`).
    *   Length: 1-3 paragraphs (3-7 sentences total).

6.  **Customer's Expectation/Demand:**
    *   Clearly state what the customer wants the service provider to do.
    *   Options: Fix the problem, provide an explanation, offer compensation (discount, refund, partial refund), ensure future quality, request specific actions (repair, replacement).
    *   Often includes a call for prompt action or a deadline.
    *   Length: 1-2 sentences.
    *   Example: `Bitte sorgen Sie umgehend wieder für [gewünschter Zustand].`, `Wir erwarten, dass [konkrete Forderung, z.B. das Spülbecken repariert oder ausgetauscht wird].`, `Bitte teilen Sie mir bis [Datum] mit, wie Sie weiter vorgehen wollen.`, `Wir erwarten, dass Sie uns mit dem noch offenen Betrag entgegenkommen.`

7.  **Closing:**
    *   Formal closing phrase.
    *   Examples: `Mit freundlichen Grüßen`, `Freundliche Grüße`.

8.  **Signature:**
    *   Sender's full name.

## Key Variables & Parameters for Generation:

1.  **Thema (Topic):** Choose a plausible topic from a professional/service context.
    *   **Options:** Cleaning Services, Renovation Work, Fitness Center Services, Kitchen Installation, Event Catering/Facility Rental, IT Support Issues, Software Problems, Delivery Delays/Errors (e.g., office supplies, ordered goods), Faulty Office Equipment, Incorrect Billing, Seminar/Workshop Organization, Travel/Accommodation Booking Issues.
    *   **Focus:** Services or products relevant to businesses or professional individuals.

2.  **Specific Service/Product:** Define the exact service/product being complained about (e.g., `tägliche Reinigung der Büroräume`, `Renovierung unserer Geschäftsräume`, `Kurs Rückenfit`, `Einbau eines Keramik-Spülbeckens`, `Hochzeitsbuffet Premium`).

3.  **Nature of the Problem(s):** Select 1-3 specific, related problems.
    *   **Quality Issues:** Poor cleaning, faulty workmanship, defective product, bad food quality.
    *   **Timeliness Issues:** Delays in service/delivery, missed deadlines, slow progress.
    *   **Completeness Issues:** Missing items, incomplete service, tasks not performed.
    *   **Logistical/Organizational Issues:** Wrong room, missing equipment (beamer, pens), incorrect order fulfillment (food), booking errors.
    *   **Hygiene Issues:** Lack of cleanliness (showers, toilets), lack of consumables (soap, paper towels).
    *   **Communication Issues:** Lack of information, no response to inquiries (can be mentioned as an aggravating factor).
    *   **Damage:** Product damaged during delivery/installation.

4.  **Timeline:**
    *   **Service Date:** When was the service performed/product delivered? (e.g., `am 20.08.`, `am 28. und 29. Juni`).
    *   **Problem Start/Occurrence:** When did the problem begin or happen? (e.g., `seit drei Wochen`, `bei den letzten drei Besuchen`, `am letzten Samstag`).
    *   **Deadline for Response:** (Optional) When does the customer expect an answer/solution? (e.g., `bis kommenden Freitag`, `bis 4. Juli`, `umgehend`).

5.  **Customer Demand:** Choose a suitable demand based on the problem.
    *   `Rectification`: Fix the issue, clean properly, repair/replace item.
    *   `Explanation`: Provide reasons for the failure.
    *   `Compensation`: Price reduction, partial/full refund, voucher, waiving fees.
    *   `Future Prevention`: Assurance that it won't happen again, explanation of preventative measures.
    *   `Threat (Implied or Explicit)`: Hinting at changing providers, canceling contract, leaving bad reviews, withholding payment.

6.  **Tone:** Consistently formal, polite but firm, clearly expressing dissatisfaction. Use appropriate B2 vocabulary and sentence structures (subordinate clauses, passive voice where appropriate, formal connectors).

7.  **Length:** Aim for approximately 100-180 words, 3 - 5 paragraphs (similar to the examples). Should be concise but contain enough detail for the tasks.

## Important Considerations for B2 Beruf Context:

*   **Plausibility:** The scenario must be realistic within a German professional or service environment.
*   **Clarity:** The problem and the expectation must be clearly understandable.
*   **Task Relevance:** The letter must contain enough specific information to allow for:
    *   Formulating 2 multiple-choice comprehension questions (checking understanding of the core problem, timeline, or demand).
    *   Writing a formal reply email that addresses the customer's points (apology, explanation, solution/compensation proposal, future prevention).
*   **Language Level:** Use varied B2 vocabulary and grammatical structures, but avoid overly complex or obscure language. Ensure correctness.
*   **Avoid Extremes:** The complaint should be serious enough to warrant a formal reply but generally avoid overly aggressive, emotional, or insulting language (unless the task specifically requires dealing with such a tone).

---

# Team Leader Forwarding Email Generation

## Goal:
To automatically generate realistic internal forwarding emails from a team leader (Teamleiter/in) in German. These emails accompany a customer complaint email and provide instructions to an employee on how to respond. They are suitable for the \"Lesen und Schreiben\" part of the B2 Beruf test.

## Core Components of the Team Leader's Email:

1.  **Metadata:**
    *   **`Erhalten:`**: Date and time (e.g., `heute, 08:27 Uhr`, `gestern 17:57 Uhr`). Usually \"heute\" or \"gestern\".
    *   **`Von:`**: Sender's full name (the team leader).
    *   **`An:`**: Recipient's name (the employee tasked with replying, can be a specific name or `...`).
    *   **`Betreff:`**: Subject line, typically starting with `FW:` followed by the original subject or a related keyword. (e.g., `FW: Beschwerde...`, `FW: Renovierungsarbeiten`, `FW Reklamation Kücheneinbau`).

2.  **Salutation:**
    *   Informal or semi-formal internal greeting.
    *   Examples: `Hallo,`, `Guten Morgen,`.

3.  **Opening Statement:**
    *   Briefly state that the customer's email (usually referred to as \"unten stehend\" or \"diese Mail\") has just been received.
    *   Length: 1 sentence.
    *   Example: `die unten stehende Mail habe ich gerade bekommen.`, `ich habe eben diese Mail von einer Kundin bekommen.`

4.  **Core Instructions (Standard):**
    *   Tell the employee to take care of the issue (`Bitte kümmern Sie sich darum`).
    *   Tell the employee to reply to the customer (`antworten Sie der Kundin/dem Kunden`).
    *   Emphasize politeness (`höflich`).
    *   Length: 1-2 sentences.

5.  **Specific Instructions for the Reply Content:**
    *   This is the most crucial part and varies based on the complaint and the desired response strategy. It dictates what the employee *must* include in their reply to the customer.
    *   **Possible Instructions (Combine as needed):**
        *   **Acknowledge/Explain the Cause:** `Nennen Sie ruhig die Gründe für den entstandenen Defekt.`, `Schreiben Sie der Kundin ruhig, warum es bei uns diese Probleme gab.`, `Bitte erklären Sie ihr, wie es zu der Situation gekommen ist.` (The word `ruhig` implies explaining factually, without making excuses).
        *   **Propose a Solution / Future Prevention:** `Schreiben Sie ihm bitte auch, wie wir das Problem lösen können.`, `Bitte schreiben Sie der Kundin auch, wie wir so etwas in Zukunft vermeiden wollen.`, `Schreiben Sie Herrn Stemmler auch, wie wir diese Probleme zukünftig lösen werden.`
        *   **Address Specific Customer Demands:** `Bitte erklären Sie ihr, ... wie wir den vereinbarten Termin trotzdem halten können.` (Directly addresses a customer concern from the complaint).
        *   **Offer Compensation/Goodwill Gesture:** `Sie können ihr auch etwas anbieten, damit sie nicht mehr so verärgert ist.`, `Bitte schreiben Sie der Kundin auch, was wir ihr als Ausgleich für die Unannehmlichkeiten vorschlagen.`
    *   Length: 1-3 sentences.

6.  **Justification / Motivation / Context (Optional but common):**
    *   Briefly explain *why* a careful response is important.
    *   Focus on: Customer retention, company reputation, customer value.
    *   Examples: `Herr Stemmler ist seit Jahren Kunde bei uns und ich möchte ihn ungern verlieren.`, `Wir möchten den guten Ruf unserer Firma nicht gefährden.`, `Ich möchte nicht, dass sie schlecht über uns und das Studio spricht. Und natürlich möchten wir sie auch nicht als Kundin verlieren.`, `Die Firma ist seit vielen Jahren unser Kunde und das soll auch so bleiben.`, `Ich möchte nicht, dass Frau McEvoy uns eine schlechte Bewertung im Internet gibt.`
    *   Length: 1-2 sentences.

7.  **Closing:**
    *   Standard internal closing phrase.
    *   Examples: `Vielen Dank und (mit) Grüßen`, `Danke schon mal und beste Grüße`, `Viele Grüße`, `Danke und beste Grüße`.

8.  **Signature:**
    *   Team leader's full name.
    *   Team leader's title (e.g., `Teamleiterin`, `Teamleiter`, `Küchenstudio Gärtner`).

## Key Variables & Parameters for Generation:

1.  **Thema (Link to Complaint):** The subject and context must directly relate to the accompanying customer complaint email.
2.  **Team Leader Persona:** Name, gender (affects `Teamleiter/in`), company context (e.g., `Küchenstudio Gärtner`).
3.  **Recipient:** Employee name or generic `...`.
4.  **Urgency/Tone:** Generally professional but internal. Can vary slightly in formality (`Hallo` vs. `Guten Morgen`).
5.  **Specific Instructions Mix:** Which combination of instructions (Explain Cause? Offer Solution? Offer Compensation? Address Specific Point?) is given. This is the key variable part that shapes the employee's task.
6.  **Justification Focus:** Emphasize customer value, company reputation, or preventing negative consequences (bad reviews).

## Important Considerations for B2 Beruf Context:

*   **Brevity:** These emails are typically short and direct (approx. 50-100 words).
*   **Internal Tone:** Language is less formal than customer communication but still professional. Avoid slang.
*   **Clarity of Instruction:** The instructions given to the employee must be unambiguous and directly relevant to solving the customer's complaint.
*   **Direct Link to Tasks:** This email acts as the *instructions* for the writing task. The test-taker must fulfill all points mentioned by the team leader in their reply to the customer.
*   **Plausibility:** The instructions should make sense in the context of the customer complaint (e.g., offering compensation for a minor issue might be less plausible than for a major failure like the wedding buffet).

---

# Multiple-Choice Question Generation (Lesen)

## Goal:
To automatically generate realistic multiple-choice questions (MCQs) with appropriate options (correct answer and distractors) based on a provided German B2 Beruf customer complaint letter. These questions should test reading comprehension skills relevant to understanding customer issues in a professional context.

## Overall Structure (per Complaint Letter):
Typically, **two** multiple-choice questions are associated with each complaint letter.

## Structure of Each Question Item:

1.  **Question Stem (`Frage`):**
    *   **Purpose:** To direct the test-taker to identify a specific piece of information or understanding derived from the customer's complaint letter.
    *   **Format:** Usually an incomplete sentence introducing the topic or subject of the question. Less commonly, a direct question.
        *   Examples (Incomplete Sentence): `Herr Stemmler...`, `Die Probleme...`, `Frau Mauch schreibt, dass die Arbeiten...`, `Um die Renovierungsarbeiten zu beenden, hat die Firma noch...`, `Frau Hafiz und ihre Kolleginnen...`, `Das Problem...`, `Herr Raueisen...`, `Das Küchenstudio soll...`, `Frau Steffens...`, `Das Problem...`, `Frau McEvoy beschwert sich, dass...`, `Die Firma soll...`
    *   **Focus:**
        *   **Question 1 Focus:** Often targets the **main reason for the complaint** or the **overall subject** of dissatisfaction (e.g., Who is complaining? What is the general topic of the complaint? What is the primary issue?).
        *   **Question 2 Focus:** Often targets a **specific detail** mentioned in the text (e.g., Timeline/Duration of the problem? Scope of the problem? A specific consequence? A specific demand? What is expected from the company?).
    *   **Length:** Concise, typically 2 to 8 words.
    *   **Language:** Clear, unambiguous German, directly related to the text's subject.

2.  **Options List (`Optionen`):**
    *   **Quantity:** Three options (labelled `a`, `b`, `c`).
    *   **Structure:** Each option consists of:
        *   `key`: \"a\", \"b\", or \"c\".
        *   `text`: The text of the option, completing the sentence stem or answering the implicit question.
    *   **Length per Option:** Keep options relatively concise and parallel in length/structure where possible, typically 5 to 15 words.
    *   **Content:** Should relate plausibly to the question stem and the overall topic of the complaint letter.

3.  **Correct Answer (`Loesung`):**
    *   **Basis:** Must be demonstrably correct based *only* on the information provided in the **customer's complaint letter**.
    *   **Wording:** Often a **paraphrase** of information from the text, testing understanding rather than just keyword matching. Sometimes it might use key phrases from the text.
    *   **Accuracy:** Must accurately reflect the meaning and details stated in the text.

4.  **Distractors (Incorrect Options):**
    *   **Quantity:** Two distractors per question.
    *   **Purpose:** To challenge the test-taker and differentiate between superficial reading and thorough comprehension. They should be plausible but clearly incorrect upon careful reading of the text.
    *   **Design Strategies for Distractors:**
        *   **Plausible but Unmentioned:** Relates to the general topic but isn't actually stated in the text (e.g., Text complains about dirty showers; distractor mentions complaining about *unfriendly staff* – plausible for a gym, but not in *this* text).
        *   **Contradiction:** States the opposite of what the text says (e.g., Text says work slowed down recently; distractor says work was *too slow from the start*).
        *   **Detail Distortion:** Takes a detail from the text but changes it slightly (e.g., Text mentions problems in the *last three weeks*; distractor says *last three months*).
        *   **Misinterpretation/Overgeneralization:** Generalizes a specific point incorrectly or misinterprets the reason for a complaint (e.g., Text mentions missing *pens* for a whiteboard; distractor says the *trainer was unprepared*).
        *   **Keyword Misuse:** Uses keywords from the text but in a context that makes the statement incorrect (e.g., Text mentions *renovation*; distractor suggests the customer wants *different furniture*).
        *   **Focus Shift:** Answers a different implicit question than the stem asks (e.g., Stem asks about the *problem*; distractor describes the *customer's proposed solution*).
        *   **Partially Correct / Incomplete:** Contains some truth but is less accurate or complete than the correct answer.
        *   **Similar Sounding / Looking Concepts:** (Less common at B2, but possible) Uses words that sound like or relate to text concepts but mean something different in context.

## Important Factors for Design:

*   **Text Dependency:** All questions and the correct answer MUST be directly derivable from the customer complaint letter. No outside knowledge should be required.
*   **Clarity:** Both the question stem and all options must be clearly worded and unambiguous.
*   **Level Appropriateness (B2):** Vocabulary and sentence structure in questions and options should align with the B2 level, matching the complexity of the complaint letter.
*   **Plausibility of Distractors:** Distractors should be tempting to someone who has misread or only skimmed the text. Avoid obviously silly or irrelevant options.
*   **Uniqueness of Correct Answer:** Only one option should be fully and accurately correct based on the text.
*   **No Trivial Questions:** Questions should focus on understanding the core issues, relevant details, or consequences mentioned in the complaint. Avoid testing obscure vocabulary or insignificant details unless they are central to the problem described.
*   **Consistency:** Maintain a consistent style and difficulty level across questions for different texts within the test module.

---

# Writing Task Instruction Generation (Schreiben)

## Goal:
To automatically generate the standardized instruction text for the email writing task (Schreiben) in the B2 Beruf test. This instruction directs the test-taker to write a formal reply to the customer, based on the customer's complaint and the specific instructions given in the team leader's forwarding email.

## Core Components of the Writing Task Instruction:

1.  **Main Task Instruction:**
    *   **Action:** Clearly state the primary action required: writing an email.
    *   **Recipient:** Specify the recipient as the customer (`Kunden` or `Kundin`, matching the gender from the complaint email).
    *   **Format:** `Schreiben Sie eine E-Mail an den Kunden/die Kundin.`
    *   **Variable:** Gender of the customer (`Kunden` vs. `Kundin`).

2.  **Key Constraint - Implementing Team Leader's Points:**
    *   **Mandate:** Explicitly instruct the test-taker to implement *all* points/instructions mentioned in the preceding team leader's email. This is the core link between the internal email and the required output.
    *   **Format:** `Setzen Sie dabei alle Punkte Ihrer Teamleitung um.`
    *   **Importance:** This ensures the writing task directly assesses the ability to follow internal instructions while responding to a customer.

3.  **Language and Style Requirements:**
    *   **Instruction:** Remind the test-taker to use appropriate language for formal business communication.
    *   **Specification:** Explicitly mention key elements of formal style: appropriate address (`Anrede`), politeness (`Höflichkeit`), formal language (`formelle Sprache`). Often includes `etc.` to imply general formality.
    *   **Format:** `Achten Sie darauf, dass Sie dem Kunden/der Kundin gegenüber eine angemessene Sprache verwenden (Anrede, Höflichkeit, formelle Sprache etc.).`
    *   **Variable:** Gender of the customer (`dem Kunden` vs. `der Kundin`).

## Variables & Parameters for Generation:

1.  **Customer Gender:** The primary variable determining `Kunden`/`Kundin` and `dem Kunden`/`der Kundin`. This must be consistent with the customer complaint email.

## Output Format:

*   The generated text should be a concise paragraph combining the three core components listed above.
*   Typically presented under a heading like `Schreiben Sie eine E-Mail...` or directly as task number (e.g., `21`).
*   Example Combined Output (for a female customer):
    ```
    Schreiben Sie eine E-Mail an die Kundin. Setzen Sie dabei alle Punkte Ihrer Teamleitung um.
    Achten Sie darauf, dass Sie der Kundin gegenüber eine angemessene Sprache verwenden (Anrede, Höflichkeit, formelle Sprache etc.).
    ```

## Important Considerations for B2 Beruf Context:

*   **Standardization:** The instruction format is highly standardized across different test versions, as seen in the examples. Only the customer's gender typically changes the wording.
*   **Clarity and Conciseness:** The instruction is brief and to the point, clearly outlining the task and constraints.
*   **Direct Linkage:** This instruction serves as the bridge, explicitly requiring the test-taker to synthesize information/directives from the team leader's email into their own formal customer response.
*   **Assessment Focus:** It sets the stage for assessing key B2 Beruf writing skills: task fulfillment (addressing all required points), register/formality, language accuracy (grammar, vocabulary), text structure, and politeness.
*   **Implicit Requirements:** While not explicitly stated in this short instruction, the test-taker is expected to structure their email appropriately (subject line, salutation, body paragraphs addressing the issue, closing, signature) based on general formal email conventions.

---

# Prompt for Generating B2 Beruf Writing Task Checklist Points

## Goal:
To automatically generate a detailed, specific checklist of points that defines a good response email for the B2 Beruf \"Schreiben\" task. This checklist serves as a guide for the test-taker or an evaluation rubric, ensuring all requirements derived from the customer complaint and the team leader's instructions are met.

## Basis for Checklist Generation:
The checklist points are derived *directly* from the combination of:
1.  **The Customer Complaint Email:** Identifies the specific problems, customer's tone, stated expectations/demands, and any deadlines mentioned.
2.  **The Team Leader's Forwarding Email:** Provides *explicit instructions* on what *must* be included in the reply (e.g., explaining the cause, proposing a solution, offering compensation, preventing future issues).
3.  **General Standards for Formal German Business Emails (B2 Level):** Includes politeness, appropriate structure, and formal language.

## Structure of the Checklist (`check_list`):
The checklist should be a list of concise, actionable points. Each point should represent a specific element required in the response email.

## Types of Checklist Points to Include (Adapt and Select Based on Specific Scenario):

1.  **Formalities & Structure:**
    *   **Purpose:** Ensure basic email etiquette and format are followed.
    *   **Derivation:** General business communication standards.
    *   **Examples:**
        *   `Schreiben Sie eine formelle E-Mail an [Customer's Full Name].`
        *   `Verwenden Sie eine passende, formelle Anrede (z.B. 'Sehr geehrte/r Frau/Herr [Customer's Last Name],').`
        *   `Strukturieren Sie die E-Mail logisch (Einleitung, Hauptteil, Schluss).`
        *   `Beenden Sie die E-Mail mit einer passenden, formellen Grußformel (z.B. 'Mit freundlichen Grüßen').`
        *   `(Optional) Fügen Sie eine passende Betreffzeile hinzu (z.B. 'Ihre Beschwerde vom [Date] bezüglich [Topic]').`

2.  **Reference & Acknowledgement:**
    *   **Purpose:** Show the customer their specific message has been received and understood.
    *   **Derivation:** Customer complaint email (topic, date).
    *   **Examples:**
        *   `Beziehen Sie sich klar auf die Beschwerde/Reklamations-E-Mail des Kunden vom [Date] bezüglich [Specific Topic/Service, e.g., 'der Reinigung', 'des Hochzeitsbuffets'].`
        *   `Bestätigen Sie den Eingang der Beschwerde.`

3.  **Empathy & Apology:**
    *   **Purpose:** Address the customer's negative experience politely and professionally.
    *   **Derivation:** Customer's expressed dissatisfaction; general politeness rules.
    *   **Examples:**
        *   `Zeigen Sie Verständnis für die Unzufriedenheit/Verärgerung des Kunden.`
        *   `Entschuldigen Sie sich höflich und angemessen für die entstandenen Unannehmlichkeiten / Probleme / Fehler.`
        *   `Drücken Sie Ihr Bedauern über die Situation aus.`

4.  **Explanation of the Cause (Reason):**
    *   **Purpose:** Fulfill the team leader's instruction to explain *why* the problem occurred.
    *   **Derivation:** **Directly from Team Leader's instruction** + Plausible reason consistent with the complaint.
    *   **Examples:**
        *   `Erklären Sie (ruhig/sachlich) den Grund für die Probleme/den Defekt, wie von der Teamleitung vorgegeben.`
        *   `Nennen Sie einen nachvollziehbaren Grund (Beispiel: [Plausible Reason like 'kurzfristiger Personalengpass', 'technisches Problem', 'Lieferverzögerung beim Material', 'Kommunikationsfehler']).` *(The specific example should align with the scenario)*.

5.  **Proposed Solution / Action Taken:**
    *   **Purpose:** Fulfill the team leader's instruction to state *what* will be done to fix the immediate problem.
    *   **Derivation:** **Directly from Team Leader's instruction** + Concrete actions relevant to the complaint.
    *   **Examples:**
        *   `Erklären Sie konkret, welche Maßnahmen ergriffen werden/wurden, um das Problem zu lösen (gemäß Anweisung der Teamleitung).`
        *   `Schlagen Sie eine konkrete Lösung vor (Beispiel: [Specific Solution like 'Reparatur/Austausch des Produkts', 'sofortige Nachbesserung der Reinigung', 'Einsatz zusätzlichen Personals', 'Terminverschiebung anbieten']).` *(The specific example should align with the scenario)*.
        *   `Informieren Sie über das weitere Vorgehen (z.B. 'Wir werden uns zur Terminvereinbarung melden').`

6.  **Compensation / Goodwill Gesture:**
    *   **Purpose:** Fulfill the team leader's instruction (if given) to offer something as compensation.
    *   **Derivation:** **Directly from Team Leader's instruction (if applicable)** + Plausible offer.
    *   **Examples:** *(Only include if instructed by Team Leader)*
        *   `Bieten Sie der Kundin/dem Kunden eine Entschädigung/einen Ausgleich an, wie von der Teamleitung vorgegeben.`
        *   `Machen Sie einen konkreten Vorschlag für einen Ausgleich (Beispiel: [Specific Offer like 'Preisnachlass auf die Rechnung', 'Gutschein für den nächsten Einkauf/Service', 'kostenlose Zusatzleistung']).` *(The specific example should align with the scenario)*.

7.  **Future Assurance / Prevention:**
    *   **Purpose:** Fulfill the team leader's instruction to explain how such problems will be avoided in the future; rebuild trust.
    *   **Derivation:** **Directly from Team Leader's instruction** + Plausible preventative measures.
    *   **Examples:**
        *   `Erklären Sie, wie ähnliche Probleme in Zukunft vermieden werden sollen (gemäß Anweisung der Teamleitung).`
        *   `Versichern Sie dem Kunden, dass Maßnahmen zur Qualitätssicherung ergriffen werden (Beispiel: [Specific Measure like 'verstärkte Kontrollen', 'verbesserte interne Kommunikation', 'zusätzliche Schulungen']).` *(The specific example should align with the scenario)*.
        *   `Betonen Sie, dass die Zufriedenheit des Kunden wichtig ist.`

8.  **Addressing Specific Customer Demands:**
    *   **Purpose:** Ensure any direct requests or deadlines from the customer are addressed.
    *   **Derivation:** Customer complaint email.
    *   **Examples:**
        *   `Gehen Sie auf die spezifische Forderung des Kunden ein (z.B. Reparatur *oder* Austausch, Entgegenkommen beim Preis).`
        *   `Reagieren Sie auf eine vom Kunden gesetzte Frist (z.B. Antwort bis [Date]).`

9.  **Language and Tone:**
    *   **Purpose:** Reinforce the need for appropriate register and style.
    *   **Derivation:** General B2 Beruf requirements, Team Leader's instruction for politeness.
    *   **Examples:**
        *   `Verwenden Sie durchgehend eine höfliche, formelle und kundenorientierte/serviceorientierte Sprache (B2 Niveau).`
        *   `Wahren Sie einen professionellen Ton.`
        *   `Stellen Sie sicher, dass Grammatik und Rechtschreibung korrekt sind.`

## General Considerations for Checklist Design:

*   **Specificity:** Points should be as specific as possible to the given scenario (mentioning the exact service, problem, or team leader's instruction). Use placeholders in the prompt that get filled with scenario details.
*   **Action-Oriented:** Phrase points as actions the writer needs to perform (e.g., \"Erklären Sie...\", \"Bieten Sie an...\", \"Stellen Sie sicher...\").
*   **Completeness:** Ensure all explicit instructions from the team leader translate into checklist points. Also cover implicit expectations based on the customer's complaint.
*   **Conciseness:** Keep each point brief and clear.
*   **Relevance:** Only include points directly relevant to the specific task scenario.
*   **Number of Points:** Aim for a reasonable number (e.g., 8-12 points) that cover the essential aspects without being overwhelming.


---

Output Format:

```json
{
  \"beschwerde_teamleiterin\": {
    \"typ\": \"E-Mail von Teamleitung\",
    \"text\": \"```markdown\\n[Markdown formatted text of the team leader's forwarding email, including Von, An, Erhalten, Betreff, Salutation, Body, Closing, Signature, Title]\\n```\"
  },
  \"beschwerde_kunde\": {
    \"typ\": \"E-Mail von Kunde/Kundin\",
    \"text\": \"```markdown\\n[Markdown formatted text of the customer's complaint email, including Von, An, Gesendet, Betreff, Salutation, Body, Closing, Signature]\\n```\"
  },
  \"aufgaben_list\": [
    {
      \"frage\": \"[Text of the first multiple-choice question stem, usually incomplete sentence]\",
      \"optionen\": [
        {
          \"key\": \"a\",
          \"text\": \"[Text for option a]\"
        },
        {
          \"key\": \"b\",
          \"text\": \"[Text for option b]\"
        },
        {
          \"key\": \"c\",
          \"text\": \"[Text for option c]\"
        }
      ],
      \"loesung\": \"[Correct option key, e.g., 'a', 'b', or 'c']\"
    },
    {
      \"frage\": \"[Text of the second multiple-choice question stem]\",
      \"optionen\": [
        {
          \"key\": \"a\",
          \"text\": \"[Text for option a]\"
        },
        {
          \"key\": \"b\",
          \"text\": \"[Text for option b]\"
        },
        {
          \"key\": \"c\",
          \"text\": \"[Text for option c]\"
        }
      ],
      \"loesung\": \"[Correct option key, e.g., 'a', 'b', or 'c']\"
    }
  ],
  \"schreibaufgabe\": {
    \"aufgaben_text\": \"[Standardized text instructing the user to write the reply email, incorporating team leader's points and maintaining formal style, e.g., 'Schreiben Sie eine E-Mail an den Kunden/die Kundin. Setzen Sie dabei alle Punkte Ihrer Teamleitung um. Achten Sie darauf, dass Sie dem Kunden/der Kundin gegenüber eine angemessene Sprache verwenden (Anrede, Höflichkeit, formelle Sprache etc.).']\",
    \"check_list\": [
      \"[Checklist Point 1: e.g., Use formal salutation]\",
      \"[Checklist Point 2: e.g., Refer to the complaint email of specific date/topic]\",
      \"[Checklist Point 3: e.g., Apologize politely for the inconvenience]\",
      \"[Checklist Point 4: e.g., Explain the reason for the problem (as instructed)]\",
      \"[Checklist Point 5: e.g., Propose the specific solution/action (as instructed)]\",
      \"[Checklist Point 6: e.g., Offer compensation (if instructed)]\",
      \"[Checklist Point 7: e.g., Explain future prevention measures (as instructed)]\",
      \"[Checklist Point 8: e.g., Address specific customer demand/deadline]\",
      \"[Checklist Point 9: e.g., Maintain formal and polite tone throughout]\",
      \"[Checklist Point 10: e.g., Use appropriate formal closing]\"
    ]
  }
}
```

**Explanation of the Structure:**

1.  **Root Object:** The entire output is a single JSON object `{}`.
2.  **`beschwerde_teamleiterin` / `beschwerde_teamleiter` (Object):**
    *   `typ` (String): Identifies the type of email (e.g., \"E-Mail von Teamleitung\").
    *   `text` (String): Contains the full text of the team leader's email, formatted as a Markdown string (including headers like Von, An, etc., and the body).
3.  **`beschwerde_kunde` / `beschwerde_kundin` (Object):**
    *   `typ` (String): Identifies the type of email (e.g., \"E-Mail von Kunde\", \"E-Mail von Kundin\").
    *   `text` (String): Contains the full text of the customer's complaint email, formatted as a Markdown string.
4.  **`aufgaben_list` (Array):**
    *   Contains multiple objects, each representing one multiple-choice question.
    *   **Each Question Object:**
        *   `frage` (String): The question stem.
        *   `optionen` (Array): Contains objects for each choice (a, b, c).
            *   **Each Option Object:**
                *   `key` (String): \"a\", \"b\", or \"c\".
                *   `text` (String): The text of the option.
        *   `loesung` (String): The key (\"a\", \"b\", or \"c\") of the correct answer.
5.  **`schreibaufgabe` (Object):**
    *   `aufgaben_text` (String): The standardized instruction text for the writing task.
    *   `check_list` (Array): Contains strings, where each string is a specific point that should be included or considered when writing the response email. This list is generated based on the specifics of the complaint and the team leader's instructions.

--- 

Example 1:

{
    \"beschwerde_teamleiterin\": {
      \"typ\": \"E-Mail von Teamleiterin\",
      \"text\": \"```markdown\\n**Von:** Marisa Leon\\n**Erhalten:** heute, 8:23 Uhr\\n**An:** ...\\n\\n**Betreff:** FW: Beschwerde Verschlechterung des Services\\n\\nHallo,\\n\\nunten stehende E-Mail erreichte mich gestern. Bitte kümmern Sie sich darum und antworten Sie dem Kunden höflich. Herr Stemmler ist seit Jahren Kunde bei uns und ich möchte ihn ungern verlieren. Sie können ihm ruhig den Grund für unsere aktuellen Probleme nennen. Ganz wichtig: Bitte schreiben Sie Herrn Stemmler auch, wie wir diese Probleme zukünftig lösen werden.\\n\\nVielen Dank und beste Grüße\\n\\nMarisa Leon\\nTeamleiterin\\n```\"
    },
    \"beschwerde_kunde\": {
      \"typ\": \"E-Mail von Kunde\",
      \"text\": \"```markdown\\n**Gesendet:** gestern, 12:54 Uhr\\n**Von:** Frank Stemmler\\n**An:** Marisa Leon\\n\\n**Betreff:** Beschwerde Verschlechterung des Services\\n\\nSehr geehrte Frau Leon,\\n\\nleider bin ich mit Ihrem Service gar nicht mehr zufrieden. Sie führen bei uns die tägliche Reinigung aller Büroräume aus. Dazu gehört auch, in den Küchen aufzuräumen und die Konferenzräume für den nächsten Tag vorzubereiten. Bisher waren wir mit Ihrem Personal sehr zufrieden.\\n\\nIn den letzten drei Wochen kam es immer wieder vor, dass vor allem die Konferenzräume nicht ordentlich waren. Das führt zu Problemen, wenn dort am nächsten Tag bereits am Vormittag eine Besprechung stattfindet. Wir können uns nicht auf die Qualität Ihrer Arbeit verlassen und müssen selbst aufräumen. Auch die Reinigung der Büros und Küchen war in letzter Zeit oft nicht zufriedenstellend.\\n\\nBitte sorgen Sie wieder für einen einwandfreien Service in gewohnter Qualität.\\nIch erwarte Ihre Antwort bis kommenden Freitag.\\n\\nMit freundlichen Grüßen\\nFrank Stemmler\\n```\"
    },
    \"aufgaben_list\": [
      {
        \"frage\": \"Herr Stemmler\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"beschwert sich über Probleme während einer Konferenz.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"ist mit der Reinigung der Konferenzräume unzufrieden.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"möchte für den Reinigungsservice anderes Personal.\"
          }
        ],
        \"loesung\": \"b\"
      },
      {
        \"frage\": \"Die Probleme\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"bestehen schon länger.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"sind seit einigen Wochen zu beobachten.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"treten seit drei Monaten auf.\"
          }
        ],
        \"loesung\": \"b\"
      }
    ],
    \"schreibaufgabe\": {
      \"aufgaben_text\": \"Schreiben Sie eine E-Mail an den Kunden. Setzen Sie dabei alle Punkte Ihrer Teamleitung um.\\nAchten Sie darauf, dass Sie dem Kunden gegenüber eine angemessene Sprache verwenden (Anrede, Höflichkeit, formelle Sprache etc.).\",
      \"check_list\": [
        \"Schreiben Sie eine formelle E-Mail an Herrn Stemmler.\",
        \"Verwenden Sie eine passende Anrede (z.B. 'Sehr geehrter Herr Stemmler,').\",
        \"Beziehen Sie sich auf seine Beschwerde-E-Mail.\",
        \"Zeigen Sie Verständnis für seine Unzufriedenheit und entschuldigen Sie sich höflich für die Unannehmlichkeiten.\",
        \"Nennen Sie (ggf. einen plausiblen) Grund für die aktuellen Probleme (gemäß Anweisung der Teamleiterin). Beispiel: kurzfristige Personalausfälle, Einarbeitung neuer Mitarbeiter.\",
        \"Erklären Sie, welche konkreten Maßnahmen ergriffen werden, um die Probleme zukünftig zu lösen und die gewohnte Qualität sicherzustellen. Beispiel: zusätzliche Qualitätskontrollen, Nachschulung des Personals, Sicherstellung ausreichender Personaldeckung.\",
        \"Versichern Sie ihm, dass die Servicequalität wiederhergestellt wird.\",
        \"Verwenden Sie eine höfliche und formelle Sprache.\",
        \"Beenden Sie die E-Mail mit einer passenden Grußformel (z.B. 'Mit freundlichen Grüßen').\"
      ]
    }
}

Example 2:

{
    \"beschwerde_teamleiter\": {
      \"typ\": \"E-Mail von Teamleitung\",
      \"text\": \"```markdown\\n**Erhalten:** heute, 13:27 Uhr\\n**Von:** Michael Kögel\\n**An:** Darius Liutikas\\n\\n**Betreff:** FW: Renovierungsarbeiten\\n\\nHallo,\\n\\nich habe eben diese Mail von einer Kundin bekommen. Bitte erklären Sie ihr, wie es zu der Situation gekommen ist und wie wir den vereinbarten Termin trotzdem halten können. Antworten Sie bitte sehr höflich. Wir möchten den guten Ruf unserer Firma nicht gefährden.\\n\\nViele Grüße\\nM. Kögel\\n```\"
    },
    \"beschwerde_kundin\": {
      \"typ\": \"E-Mail von Kundin\",
      \"text\": \"```markdown\\n**Erhalten:** heute, 12:43 Uhr\\n**Von:** Zofia Mauch\\n**An:** Michael Kögel\\n\\n**Betreff:** Renovierungsarbeiten\\n\\nSehr geehrter Herr Kögel,\\n\\nIhre Firma ist für qualitativ hochwertige und termingerechte Leistungen bekannt. Aus diesem Grund haben wir uns auch entschieden, Sie mit der Renovierung unserer Geschäftsräume zu beauftragen. Die Arbeiten sind anfangs gut angelaufen und zügig vorangekommen, aber seit einigen Wochen sehen wir kaum noch Fortschritte. Die Arbeiter kommen entweder gar nicht oder nur stundenweise. Auf unsere Nachfrage hin erklärten sie uns, dass sie auf einer anderen Baustelle gebraucht würden.\\n\\nUnser 30-jähriges Firmenjubiläum soll am 6. September in den renovierten Räumlichkeiten gefeiert werden. Sie hatten uns zugesichert, dass alle Arbeiten zehn Tage vor diesem Termin abgeschlossen wären. Inzwischen frage ich mich allerdings, ob Sie diese Vereinbarung einhalten können: Das Parkett wurde noch nicht verlegt, die Türen und Fenster sind noch nicht eingebaut und die Beleuchtung wurde nicht einmal geliefert.\\n\\nBitte teilen Sie mir umgehend mit, wie es mit der Renovierung nun weitergeht.\\n\\nFreundliche Grüße\\nZofia Mauch\\n```\"
    },
    \"aufgaben_list\": [
      {
        \"frage\": \"Frau Mauch schreibt, dass die Arbeiten\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"in der letzten Zeit öfter liegengeblieben sind.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"schnell, aber nicht sorgfältig ausgeführt werden.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"von Anfang an zu langsam durchgeführt wurden.\"
          }
        ],
        \"loesung\": \"a\"
      },
      {
        \"frage\": \"Um die Renovierungsarbeiten zu beenden, hat die Firma noch\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"bis Ende August Zeit.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"bis zum 6. September Zeit.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"zehn Tage Zeit.\"
          }
        ],
        \"loesung\": \"c\"
      }
    ],
    \"schreibaufgabe\": {
      \"aufgaben_text\": \"Schreiben Sie eine E-Mail an die Kundin. Setzen Sie dabei alle Punkte Ihrer Teamleitung um.\\nAchten Sie darauf, dass Sie der Kundin gegenüber eine angemessene Sprache verwenden (Anrede, Höflichkeit, formelle Sprache etc.).\",
      \"check_list\": [
        \"Schreiben Sie eine formelle E-Mail an Frau Mauch.\",
        \"Verwenden Sie eine passende Anrede (z.B. 'Sehr geehrte Frau Mauch,').\",
        \"Beziehen Sie sich auf ihre E-Mail bezüglich der Renovierungsarbeiten.\",
        \"Drücken Sie Ihr Bedauern über die Verzögerungen und die entstandenen Unannehmlichkeiten höflich aus.\",
        \"Erklären Sie nachvollziehbar den Grund für die Verzögerung (gemäß Anweisung der Teamleitung: 'erklären Sie ihr, wie es zu der Situation gekommen ist'). Bestätigen oder präzisieren Sie ggf. die bereits gegebene Information (Arbeiter auf anderer Baustelle benötigt) oder nennen Sie einen anderen plausiblen Grund (z.B. unerwartete Komplexität, Lieferengpässe bei Materialien wie Parkett/Türen/Fenster/Beleuchtung - passend zu den genannten Problemen).\",
        \"Erklären Sie konkret, wie der vereinbarte Termin (Fertigstellung 10 Tage vor dem 6. September) dennoch eingehalten werden kann (gemäß Anweisung der Teamleitung: 'wie wir den vereinbarten Termin trotzdem halten können'). Nennen Sie spezifische Maßnahmen, z.B. Aufstockung des Personals auf der Baustelle, Einführung von Wochenend- oder Schichtarbeit, Priorisierung der Materiallieferungen.\",
        \"Versichern Sie der Kundin, dass alles unternommen wird, um die Arbeiten rechtzeitig und in hoher Qualität abzuschließen.\",
        \"Bitten Sie umgehend um Rückmeldung oder Bestätigung (optional, aber passend zur Aufforderung der Kundin).\",
        \"Wahren Sie durchgehend einen höflichen, formellen und professionellen Ton, um den guten Ruf der Firma zu schützen.\",
        \"Beenden Sie die E-Mail mit einer passenden Grußformel (z.B. 'Mit freundlichen Grüßen').\"
      ]
    }
}

Example 3:

{
    \"beschwerde_teamleiterin\": {
      \"typ\": \"E-Mail von Teamleiterin\",
      \"text\": \"```markdown\\n**Erhalten:** heute 08:27 Uhr\\n**Von:** Helena Nadal\\n**An:** ...\\n\\n**Betreff:** FW Beschwerde: Schmutzige Duschen in Ihrem Fitnesscenter seit dem 1.04.\\n\\nHallo,\\n\\ndie unten stehende Mail habe ich gerade bekommen. Bitte kümmern Sie sich darum und antworten Sie der Kundin höflich. Ich möchte nicht, dass sie schlecht über uns und das Studio spricht. Und natürlich möchten wir sie auch nicht als Kundin verlieren.\\nSchreiben Sie der Kundin ruhig, warum es bei uns diese Probleme gab. Sie können ihr auch etwas anbieten, damit sie nicht mehr so verärgert ist.\\n\\nVielen Dank und mit Grüßen\\nHelena Nadal\\nTeamleiterin\\n```\"
    },
    \"beschwerde_kundin\": {
      \"typ\": \"E-Mail von Kundin\",
      \"text\": \"```markdown\\n**Gesendet:** heute 08:14 Uhr\\n**Von:** Zara Hafiz\\n**An:** Helena Nadal\\n\\n**Betreff:** Beschwerde: Schmutzige Duschen in Ihrem Fitnesscenter seit dem 1.04.\\n\\nSehr geehrte Frau Nadal,\\n\\nmeine Kolleginnen und ich besuchen seit mehreren Monaten Ihr Fitnesscenter. Wir nehmen zwei Mal in der Woche um 7:30 Uhr am Kurs *Rückenfit* teil. Unsere Trainerin Kasia ist qualifiziert und es lohnt sich, bei ihr zu trainieren.\\nBisher waren wir mit allem sehr zufrieden, aber bei unseren letzten drei Besuchen lagen viele Haare in der Dusche und die Toiletten waren nicht geputzt. Das ist eklig! An den Waschbecken waren außerdem wiederholt die Seifenspender leer und es gab keine Papierhandtücher.\\nWir haben mit anderen Mitgliedern gesprochen, die uns versicherten, dass nach 15 Uhr wieder alles in Ordnung ist - das ist für uns aber zu spät!\\n\\nIn einem hochpreisigen Studio wie Ihrem erwarten wir, dass alles stimmt. Wir werden nicht sofort kündigen, unsere Beiträge für diesen Monat aber zurückbuchen, wenn Sie diese Probleme nicht schnell beheben!\\n\\nMit freundlichen Grüßen\\n\\nZara Hafiz\\n```\"
    },
    \"aufgaben_list\": [
      {
        \"frage\": \"Frau Hafiz und ihre Kolleginnen\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"beschweren sich über mangelnde Hygiene.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"bezahlen zu hohe Beiträge.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"sind mit dem Kurs unzufrieden.\"
          }
        ],
        \"loesung\": \"a\"
      },
      {
        \"frage\": \"Das Problem\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"besteht seit mehreren Monaten.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"ist auch anderen Mitgliedern bekannt.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"tritt vor allem nachmittags auf.\"
          }
        ],
        \"loesung\": \"b\"
      }
    ],
    \"schreibaufgabe\": {
      \"aufgaben_text\": \"Schreiben Sie eine E-Mail an die Kundin. Setzen Sie dabei alle Punkte Ihrer Teamleitung um.\\nAchten Sie darauf, dass Sie der Kundin gegenüber eine angemessene Sprache verwenden (Anrede, Höflichkeit, formelle Sprache etc.).\",
      \"check_list\": [
        \"Schreiben Sie eine formelle E-Mail an Frau Hafiz.\",
        \"Verwenden Sie eine passende Anrede (z.B. 'Sehr geehrte Frau Hafiz,').\",
        \"Beziehen Sie sich auf ihre Beschwerde-E-Mail wegen der Sauberkeit, insbesondere der Duschen und Toiletten.\",
        \"Zeigen Sie Verständnis für ihre Verärgerung und entschuldigen Sie sich höflich für die unhygienischen Zustände und die Unannehmlichkeiten.\",
        \"Erklären Sie (ruhig) den Grund für die Probleme (gemäß Anweisung der Teamleiterin). Beispiel: kurzfristiger Ausfall des Reinigungspersonals am Vormittag, Engpass bei Verbrauchsmaterialien (Seife, Papierhandtücher).\",
        \"Erklären Sie, welche Maßnahmen sofort ergriffen werden, um die Sauberkeit sicherzustellen (z.B. zusätzliche Reinigungskräfte, verstärkte Kontrollen, Sicherstellung der Materialversorgung).\",
        \"Bieten Sie der Kundin 'etwas an', um ihre Verärgerung zu mildern (gemäß Anweisung der Teamleiterin). Beispiel: eine Gutschrift für den nächsten Monatsbeitrag, einen Gutschein für eine Zusatzleistung (z.B. Sauna, Getränk).\",
        \"Versichern Sie ihr, dass die Probleme behoben sind/werden und die gewohnte Sauberkeit wiederhergestellt wird.\",
        \"Verwenden Sie eine höfliche, formelle und serviceorientierte Sprache.\",
        \"Beenden Sie die E-Mail mit einer passenden Grußformel (z.B. 'Mit freundlichen Grüßen').\"
      ]
    }
  }
  

Example 4:

{
    \"beschwerde_teamleiterin\": {
      \"typ\": \"E-Mail von Teamleitung\",
      \"text\": \"```markdown\\n**Erhalten:** heute 09:25 Uhr\\n**Von:** Lisa Gärtner\\n**An:** ...\\n\\n**Betreff:** FW Reklamation Kücheneinbau\\n\\nGuten Morgen,\\n\\ngestern habe ich unten stehende E-Mail bekommen. Bitte klären Sie mit den Kollegen, die bei dem Kunden waren, was genau passiert ist. Antworten Sie dann dem Kunden höflich und nennen Sie ruhig die Gründe für den entstandenen Defekt. Schreiben Sie ihm bitte auch, wie wir das Problem lösen können.\\n\\nDanke schon mal und beste Grüße\\nLisa Gärtner\\n\\nKüchenstudio Gärtner\\n```\"
    },
    \"beschwerde_kunde\": {
      \"typ\": \"E-Mail von Kunde\",
      \"text\": \"```markdown\\n**Gesendet:** gestern 16:49 Uhr\\n**Von:** Ludwig Raueisen\\n**An:** Lisa Gärtner\\n**Betreff:** Reklamation Kücheneinbau\\n\\nSehr geehrte Frau Gärtner,\\n\\nam 28. und 29. Juni haben Sie in unserem Gästehaus eine neue Küche eingebaut. Dazu gehörte ein großes Spülbecken aus Keramik und mehrere Einbauschränke darüber.\\n\\nMit der zügigen Durchführung der Arbeiten waren wir auch sehr zufrieden. Auch die von Ihnen empfohlene Farbe der Schränke gefällt uns sehr.\\nNun mussten wir aber feststellen, dass das Spülbecken an einer Stelle einen Defekt hat. Wir nehmen an, dass einem Ihrer Mitarbeiter beim Einbauen der Schränke etwas Schweres in das Spülbecken gefallen ist, sodass dort ein Kratzer entstanden ist.\\n\\nWir verlangen deshalb, dass das Spülbecken entweder repariert oder ausgetauscht wird. Bitte teilen Sie mir bis 4. Juli mit, wie Sie vorgehen, damit wir entsprechend planen können.\\n\\nMit freundlichen Grüßen\\n\\nLudwig Raueisen\\n```\"
    },
    \"aufgaben_list\": [
      {
        \"frage\": \"Herr Raueisen\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"beschwert sich über ein beschädigtes Produkt.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"besteht auf dem Austausch der Einbauschränke.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"war mit der Dauer der Arbeiten unzufrieden.\"
          }
        ],
        \"loesung\": \"a\"
      },
      {
        \"frage\": \"Das Küchenstudio soll\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"die Küche anders planen.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"eine Lösung vorschlagen.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"einen Mitarbeiter vorbeischicken.\"
          }
        ],
        \"loesung\": \"b\"
      }
    ],
    \"schreibaufgabe\": {
      \"aufgaben_text\": \"Schreiben Sie eine E-Mail an den Kunden. Setzen Sie dabei alle Punkte Ihrer Teamleitung um.\\nAchten Sie darauf, dass Sie dem Kunden gegenüber eine angemessene Sprache verwenden (Anrede, Höflichkeit, formelle Sprache etc.).\",
      \"check_list\": [
        \"Schreiben Sie eine formelle E-Mail an Herrn Raueisen.\",
        \"Verwenden Sie eine passende Anrede (z.B. 'Sehr geehrter Herr Raueisen,').\",
        \"Beziehen Sie sich auf seine Reklamations-E-Mail bezüglich des eingebauten Spülbeckens.\",
        \"Drücken Sie Ihr Bedauern über den Defekt und die entstandenen Unannehmlichkeiten höflich aus.\",
        \"Bestätigen Sie den Eingang seiner Reklamation.\",
        \"Erklären Sie (ruhig) den Grund für den Defekt, nachdem Sie dies intern geklärt haben (gemäß Anweisung der Teamleitung: 'klären Sie mit den Kollegen', 'nennen Sie ruhig die Gründe'). Beispiel: Bestätigung seiner Vermutung, dass etwas hineingefallen ist, oder ein anderer plausibler Grund.\",
        \"Schlagen Sie eine konkrete Lösung vor (Reparatur oder Austausch des Spülbeckens), wie von der Teamleitung gefordert ('wie wir das Problem lösen können'). Gehen Sie auf die vom Kunden genannten Optionen ein.\",
        \"Informieren Sie ihn über das weitere Vorgehen (z.B. Terminvereinbarung für Reparatur/Austausch).\",
        \"Beantworten Sie seine Bitte um Information bis zum 4. Juli (oder erklären Sie, warum eine endgültige Antwort bis dahin ggf. nicht möglich ist, aber wann er sie erwarten kann).\",
        \"Verwenden Sie durchgehend eine höfliche, formelle und kundenorientierte Sprache.\",
        \"Beenden Sie die E-Mail mit einer passenden Grußformel (z.B. 'Mit freundlichen Grüßen').\"
      ]
    }
}
  
Example 5:

{
    \"beschwerde_teamleiter\": {
      \"typ\": \"E-Mail von Teamleiter\",
      \"text\": \"```markdown\\n**Erhalten:** gestern 17:57 Uhr\\n**Von:** Bernd Hauser\\n**An:** ...\\n\\n**Betreff:** FW Unsere Schulungen in Ihrem Tagungshaus\\n\\nHallo,\\n\\ndie unten stehende Mail habe ich gerade bekommen. Bitte kümmern Sie sich darum und antworten Sie der Kundin höflich. Die Firma ist seit vielen Jahren unser Kunde und das soll auch so bleiben.\\nSie können der Kundin ruhig schreiben, warum es bei uns diese Probleme gab. Ganz wichtig: Bitte schreiben Sie der Kundin auch, wie wir so etwas in Zukunft vermeiden wollen.\\n\\nDanke und beste Grüße\\n\\nBernd Hauser\\nTeamleiter\\n```\"
    },
    \"beschwerde_kundin\": {
      \"typ\": \"E-Mail von Kundin\",
      \"text\": \"```markdown\\n**Gesendet:** gestern 17:44 Uhr\\n**Von:** Anke Steffens\\n**An:** Bernd Hauser\\n\\n**Betreff:** Unsere Schulungen in Ihrem Tagungshaus\\n\\nSehr geehrter Herr Hauser,\\n\\nwie Sie wissen, führen wir unsere Mitarbeiterschulungen und Fortbildungen in Ihrem Tagungshaus durch. Bislang waren wir mit dem Service vor Ort (Ausstattung der Räume, Sauberkeit, Verpflegung etc.) immer sehr zufrieden.\\nLeider haben einige Mitarbeitende berichtet, dass es in letzter Zeit nicht reibungslos lief.\\nEine Fortbildung vor zwei Wochen wurde kurzfristig und ohne Rückfrage in einen anderen Raum verlegt, dort hatte die Trainerin dann keinen Beamer, obwohl das so abgesprochen war, und für das Whiteboard fehlten die Stifte. Zum Glück hatte die Trainerin Stifte dabei, aber der Beamer musste erst gebracht und angeschlossen werden, sodass Zeit verlorenging.\\nFür eine Mitarbeiterschulung am letzten Samstag hatten wir eine Suppe und Salate als Mittagsimbiss bestellt, aber nur einige Kekse bekommen. Das war natürlich alles nicht gut!\\n\\nBitte sorgen Sie wieder für die gewohnte Qualität, sonst werden wir uns nach anderen Schulungsräumen umsehen müssen.\\n\\nMit freundlichen Grüßen\\nAnke Steffens\\n```\"
    },
    \"aufgaben_list\": [
      {
        \"frage\": \"Frau Steffens\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"beschwert sich über die Raumgröße.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"ist mit der Trainerin unzufrieden.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"nennt organisatorische Mängel.\"
          }
        ],
        \"loesung\": \"c\"
      },
      {
        \"frage\": \"Das Problem\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"beschränkt sich auf Wochenenden.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"gibt es an unterschiedlichen Wochentagen.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"trat erstmals letzte Woche auf.\"
          }
        ],
        \"loesung\": \"b\"
      }
    ],
    \"schreibaufgabe\": {
      \"aufgaben_text\": \"Schreiben Sie eine E-Mail an die Kundin. Setzen Sie dabei alle Punkte Ihrer Teamleitung um.\\nAchten Sie darauf, dass Sie der Kundin gegenüber eine angemessene Sprache verwenden (Anrede, Höflichkeit, formelle Sprache etc.).\",
      \"check_list\": [
        \"Schreiben Sie eine formelle E-Mail an Frau Steffens.\",
        \"Verwenden Sie eine passende Anrede (z.B. 'Sehr geehrte Frau Steffens,').\",
        \"Beziehen Sie sich auf ihre E-Mail bezüglich der Probleme bei den Schulungen.\",
        \"Drücken Sie Ihr Bedauern über die Vorkommnisse (Raumwechsel, fehlender Beamer/Stifte, falsches Essen) und die entstandenen Unannehmlichkeiten höflich aus.\",
        \"Erklären Sie (ruhig) die Gründe für die Probleme (gemäß Anweisung des Teamleiters). Beispiel: Interne Kommunikationsfehler, kurzfristige organisatorische Änderungen, Fehler beim Catering-Service.\",
        \"Erklären Sie konkret, wie solche Probleme in Zukunft vermieden werden sollen (gemäß Anweisung des Teamleiters: 'wie wir so etwas in Zukunft vermeiden wollen'). Beispiel: Einführung von Checklisten für die Raumvorbereitung, verbesserte Abstimmungsprozesse intern und mit dem Catering, doppelte Prüfung der Bestellungen.\",
        \"Versichern Sie der Kundin, dass Maßnahmen ergriffen werden, um die gewohnte Servicequalität wieder sicherzustellen.\",
        \"Betonen Sie, dass ihre Zufriedenheit als langjährige Kundin wichtig ist.\",
        \"Verwenden Sie durchgehend eine höfliche, formelle und lösungsorientierte Sprache.\",
        \"Beenden Sie die E-Mail mit einer passenden Grußformel (z.B. 'Mit freundlichen Grüßen').\"
      ]
    }
}
  

Example 6:

{
    \"beschwerde_teamleiterin\": {
      \"typ\": \"E-Mail von Teamleiterin\",
      \"text\": \"```markdown\\n**Erhalten:** heute 11:40 Uhr\\n**Von:** Petra Speichert\\n**An:** ...\\n\\n**Betreff:** FW Beschwerde: Hochzeitsbuffet am 20.08.\\n\\nHallo,\\n\\ndie unten stehende Mail habe ich gerade bekommen. Bitte kümmern Sie sich darum und antworten Sie der Kundin höflich. Ich möchte nicht, dass Frau McEvoy uns eine schlechte Bewertung im Internet gibt.\\nSie können der Kundin ruhig schreiben, warum es bei dem Hochzeitsbuffet Probleme gab.\\nGanz wichtig: Bitte schreiben Sie der Kundin auch, was wir ihr als Ausgleich für die Unannehmlichkeiten vorschlagen.\\n\\nVielen Dank und mit Grüßen\\nPetra Speichert\\nTeamleiterin\\n```\"
    },
    \"beschwerde_kundin\": {
      \"typ\": \"E-Mail von Kundin\",
      \"text\": \"```markdown\\n**Gesendet:** heute 11:22 Uhr\\n**Von:** Donna McEvoy\\n**An:** Petra Speichert\\n\\n**Betreff:** Beschwerde Hochzeitsbuffet am 20.08.\\n\\nSehr geehrte Frau Speichert,\\n\\nwir hatten für unsere Hochzeit am 20.08. bei Ihnen das Hochzeitsbuffet Premium (Mittagessen, 25 Personen) bestellt. Das Buffet sollte bis 12 Uhr geliefert und bis 12:30 Uhr aufgebaut sein. Ebenfalls sollten Sie für verschiedene Getränke zum Abschluss des Essens (Kaffee, Espresso etc.) sorgen.\\nLeider ist alles schiefgegangen: Das Buffet war um 12:35 Uhr noch nicht da und wir konnten erst um halb zwei mit dem Essen beginnen. Als die Hochzeitstorte um 15 Uhr serviert wurde, waren alle noch satt.\\nIhr Essen war nicht schlecht, aber Sie haben uns einen Tag, den wir lange im Voraus und mit Liebe geplant hatten, fast verdorben. Wir haben bereits eine hohe Anzahlung geleistet und erwarten jetzt, dass Sie uns mit dem noch offenen Betrag entgegenkommen. Nur eine Entschuldigung reicht nicht aus!\\n\\nGrüße\\nDonna McEvoy\\n```\"
    },
    \"aufgaben_list\": [
      {
        \"frage\": \"Frau McEvoy beschwert sich, dass\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"das falsche Buffet geliefert wurde.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"das Essen nicht geschmeckt hat.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"das Essen zu spät kam.\"
          }
        ],
        \"loesung\": \"c\"
      },
      {
        \"frage\": \"Die Firma soll\",
        \"optionen\": [
          {
            \"key\": \"a\",
            \"text\": \"auf die Anzahlung verzichten.\"
          },
          {
            \"key\": \"b\",
            \"text\": \"die Rechnung mindern.\"
          },
          {
            \"key\": \"c\",
            \"text\": \"Geld zurückbezahlen.\"
          }
        ],
        \"loesung\": \"b\"
      }
    ],
    \"schreibaufgabe\": {
      \"aufgaben_text\": \"Schreiben Sie eine E-Mail an die Kundin. Setzen Sie dabei alle Punkte Ihrer Teamleitung um.\\nAchten Sie darauf, dass Sie der Kundin gegenüber eine angemessene Sprache verwenden (Anrede, Höflichkeit, formelle Sprache etc.).\",
      \"check_list\": [
        \"Schreiben Sie eine formelle E-Mail an Frau McEvoy.\",
        \"Verwenden Sie eine passende Anrede (z.B. 'Sehr geehrte Frau McEvoy,').\",
        \"Beziehen Sie sich auf ihre Beschwerde bezüglich des Hochzeitsbuffets am 20.08.\",
        \"Drücken Sie Ihr aufrichtiges Bedauern über die erheblichen Verzögerungen und die dadurch entstandenen Unannehmlichkeiten an ihrem Hochzeitstag höflich aus.\",
        \"Entschuldigen Sie sich ausdrücklich für die Probleme.\",
        \"Erklären Sie (ruhig) den Grund für die Probleme mit dem Buffet (gemäß Anweisung der Teamleiterin). Beispiel: Unerwarteter Fahrzeugausfall, extreme Verkehrslage, kurzfristiger Personalausfall in der Küche/Logistik.\",
        \"Machen Sie einen konkreten Vorschlag als Ausgleich/Entschädigung für die Unannehmlichkeiten (gemäß Anweisung der Teamleiterin: 'was wir ihr als Ausgleich ... vorschlagen'). Gehen Sie dabei auf die Erwartung der Kundin ein ('mit dem noch offenen Betrag entgegenkommen'). Beispiel: Ein signifikanter Preisnachlass auf den Gesamtbetrag / die Restrechnung, Verzicht auf einen Teil der Kosten.\",
        \"Versichern Sie ihr, dass dies ein Ausnahmefall war und Maßnahmen ergriffen werden, um so etwas zukünftig zu verhindern.\",
        \"Verwenden Sie durchgehend eine sehr höfliche, formelle, verständnisvolle und lösungsorientierte Sprache, um eine schlechte Bewertung zu vermeiden.\",
        \"Beenden Sie die E-Mail mit einer passenden Grußformel (z.B. 'Mit freundlichen Grüßen').\"
      ]
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


def format_json(json_str, debug=False):
    """
    Extract and parse JSON from the model output string.
    
    Args:
        json_str (str): The string output from the model
        debug (bool): Whether to print debug information
        
    Returns:
        dict: The parsed JSON object
        
    Raises:
        ValueError: If no valid JSON with the expected structure could be found
    """
    if debug:
        print(f"Debug: Input JSON string length: {len(json_str)}")
    
    # Try to find the exact JSON object with the expected fields first
    expected_fields_pattern = re.compile(r'(\{[\s\S]*?(?:beschwerde_teamleiterin|beschwerde_teamleiter)[\s\S]*?(?:beschwerde_kunde|beschwerde_kundin)[\s\S]*?aufgaben_list[\s\S]*?schreibaufgabe[\s\S]*?\})')
    
    # Try to find a match with our expected structure
    matches = expected_fields_pattern.findall(json_str)
    if matches:
        if debug:
            print(f"Debug: Found {len(matches)} potential matches with expected fields")
        # Try the matches from largest to smallest
        matches.sort(key=len, reverse=True)
        
        for i, match in enumerate(matches[:2]):  # Try the 2 largest matches
            if debug:
                print(f"Debug: Trying match {i+1} with expected fields, length: {len(match)}")
            try:
                parsed = json.loads(match)
                # Check if this has our required structure
                if ('beschwerde_teamleiterin' in parsed or 'beschwerde_teamleiter' in parsed) and ('beschwerde_kunde' in parsed or 'beschwerde_kundin' in parsed):
                    if debug:
                        print(f"Debug: Successfully parsed match {i+1} with expected fields")
                    return parsed
                elif debug:
                    print(f"Debug: Match {i+1} is valid JSON but missing expected fields")
                    print(f"Debug: Found keys: {list(parsed.keys())}")
            except json.JSONDecodeError as e:
                if debug:
                    print(f"Debug: Failed to parse match {i+1} with expected fields: {e}")
    
    # Look for any JSON objects as a fallback
    json_patterns = re.findall(r'(\{[\s\S]*?\})', json_str)
    
    # If we found potential JSON objects, try them from largest to smallest
    if json_patterns:
        # Sort by length (largest first) to try the most complete JSON first
        json_patterns.sort(key=len, reverse=True)
        if debug:
            print(f"Debug: Found {len(json_patterns)} potential JSON objects")
        
        for i, pattern in enumerate(json_patterns[:5]):  # Try the 5 largest patterns
            if debug:
                print(f"Debug: Trying JSON pattern {i+1}, length: {len(pattern)}")
            try:
                parsed = json.loads(pattern)
                if debug:
                    print(f"Debug: Successfully parsed JSON pattern {i+1}")
                    print(f"Debug: Found keys in pattern {i+1}: {list(parsed.keys())}")
                
                # Check if this JSON has the fields we need
                if ('beschwerde_teamleiterin' in parsed or 'beschwerde_teamleiter' in parsed) and ('beschwerde_kunde' in parsed or 'beschwerde_kundin' in parsed):
                    if debug:
                        print(f"Debug: JSON pattern {i+1} contains expected fields")
                    return parsed
            except json.JSONDecodeError as e:
                if debug:
                    print(f"Debug: Failed to parse JSON pattern {i+1}: {e}")
    
    # Look for the complete JSON output at the end of the response
    if debug:
        print("Debug: Looking for complete JSON output in the full response")
    
    # Try to extract a JSON between ```json and ```
    json_block_pattern = re.compile(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```')
    json_blocks = json_block_pattern.findall(json_str)
    
    if json_blocks:
        if debug:
            print(f"Debug: Found {len(json_blocks)} JSON blocks in code blocks")
        # Try the blocks from largest to smallest
        json_blocks.sort(key=len, reverse=True)
        
        for i, block in enumerate(json_blocks[:3]):  # Try the 3 largest blocks
            if debug:
                print(f"Debug: Trying JSON block {i+1}, length: {len(block)}")
            try:
                parsed = json.loads(block)
                if debug:
                    print(f"Debug: Successfully parsed JSON block {i+1}")
                    print(f"Debug: Found keys in block {i+1}: {list(parsed.keys())}")
                
                # Check if this JSON has the fields we need
                if ('beschwerde_teamleiterin' in parsed or 'beschwerde_teamleiter' in parsed) and ('beschwerde_kunde' in parsed or 'beschwerde_kundin' in parsed):
                    if debug:
                        print(f"Debug: JSON block {i+1} contains expected fields")
                    return parsed
            except json.JSONDecodeError as e:
                if debug:
                    print(f"Debug: Failed to parse JSON block {i+1}: {e}")
    
    # If all else fails and we're in debug mode, print some diagnostic info
    if debug:
        print("\nDebug: Could not find valid JSON with expected structure. Here's a sample of the model output:")
        print(json_str[:500])
        print("...[truncated]...")
        print(json_str[-500:])
    
    # Look for the final example JSON in the response - it might be at the end
    example_start = json_str.rfind("{")
    if example_start != -1:
        # Find the corresponding closing brace by counting
        depth = 0
        final_json = None
        for i, char in enumerate(json_str[example_start:]):
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    # We found a potential complete JSON
                    final_json = json_str[example_start:example_start+i+1]
                    break
        
        if final_json:
            try:
                result = json.loads(final_json)
                if debug:
                    print(f"Debug: Found final JSON object with length: {len(final_json)}")
                return result
            except json.JSONDecodeError as e:
                if debug:
                    print(f"Debug: Final JSON parsing failed: {e}")
    
    # If we get here, we couldn't parse the JSON
    raise ValueError("Could not extract valid JSON with the expected structure from the model output")


def verify_json_structure(json_data):
    """
    Verify the structure of the JSON data to ensure it matches the expected format.
    
    Args:
        json_data (dict): The JSON data to verify.
        
    Returns:
        tuple: (is_valid, message) where is_valid is a boolean indicating if the JSON data is valid
               and message is a string explaining why the JSON data is invalid if it's not valid.
    """
    # Check if either beschwerde_teamleiterin or beschwerde_teamleiter is present
    if 'beschwerde_teamleiterin' not in json_data and 'beschwerde_teamleiter' not in json_data:
        return False, "Missing required field: either 'beschwerde_teamleiterin' or 'beschwerde_teamleiter'"
    
    # Check if either beschwerde_kunde or beschwerde_kundin is present
    if 'beschwerde_kunde' not in json_data and 'beschwerde_kundin' not in json_data:
        return False, "Missing required field: either 'beschwerde_kunde' or 'beschwerde_kundin'"
    
    # Check if other required fields are present
    required_fields = ['aufgaben_list', 'schreibaufgabe']
    for field in required_fields:
        if field not in json_data:
            return False, f"Missing required field: '{field}'"
    
    # Get the team leader field name (either beschwerde_teamleiterin or beschwerde_teamleiter)
    team_leader_field = 'beschwerde_teamleiterin' if 'beschwerde_teamleiterin' in json_data else 'beschwerde_teamleiter'
    
    # Check if the beschwerde_teamleiterin/teamleiter has the required fields
    team_leader_data = json_data[team_leader_field]
    if not isinstance(team_leader_data, dict):
        return False, f"'{team_leader_field}' must be a dictionary"
    
    if 'typ' not in team_leader_data:
        return False, f"Missing required field: '{team_leader_field}.typ'"
    
    if 'text' not in team_leader_data:
        return False, f"Missing required field: '{team_leader_field}.text'"
    
    # Check if the text field has markdown formatting
    if not team_leader_data['text'].startswith("```markdown"):
        return False, f"'{team_leader_field}.text' must start with markdown formatting"
    
    # Check if the beschwerde_kunde/kundin has the required fields
    customer_field = 'beschwerde_kunde' if 'beschwerde_kunde' in json_data else 'beschwerde_kundin'
    
    customer_data = json_data[customer_field]
    if not isinstance(customer_data, dict):
        return False, f"'{customer_field}' must be a dictionary"
    
    if 'typ' not in customer_data:
        return False, f"Missing required field: '{customer_field}.typ'"
    
    if 'text' not in customer_data:
        return False, f"Missing required field: '{customer_field}.text'"
    
    # Check if the text field has markdown formatting
    if not customer_data['text'].startswith("```markdown"):
        return False, f"'{customer_field}.text' must start with markdown formatting"
    
    # Check if the aufgaben_list is a list with at least one item
    aufgaben_list = json_data['aufgaben_list']
    if not isinstance(aufgaben_list, list):
        return False, "'aufgaben_list' must be a list"
    
    if len(aufgaben_list) < 1:
        return False, "'aufgaben_list' must have at least one item"
    
    # Check if each item in the aufgaben_list has the required fields
    for i, aufgabe in enumerate(aufgaben_list):
        if not isinstance(aufgabe, dict):
            return False, f"'aufgaben_list[{i}]' must be a dictionary"
        
        if 'frage' not in aufgabe:
            return False, f"Missing required field: 'aufgaben_list[{i}].frage'"
        
        if 'optionen' not in aufgabe:
            return False, f"Missing required field: 'aufgaben_list[{i}].optionen'"
        
        if 'loesung' not in aufgabe:
            return False, f"Missing required field: 'aufgaben_list[{i}].loesung'"
        
        # Check if the optionen is a list with exactly 3 items
        optionen = aufgabe['optionen']
        if not isinstance(optionen, list):
            return False, f"'aufgaben_list[{i}].optionen' must be a list"
        
        if len(optionen) != 3:
            return False, f"'aufgaben_list[{i}].optionen' must have exactly 3 items"
        
        # Check if each option has the required fields
        for j, option in enumerate(optionen):
            if not isinstance(option, dict):
                return False, f"'aufgaben_list[{i}].optionen[{j}]' must be a dictionary"
            
            if 'key' not in option:
                return False, f"Missing required field: 'aufgaben_list[{i}].optionen[{j}].key'"
            
            if 'text' not in option:
                return False, f"Missing required field: 'aufgaben_list[{i}].optionen[{j}].text'"
            
            # Check if the key is 'a', 'b', or 'c'
            if option['key'] not in ['a', 'b', 'c']:
                return False, f"'aufgaben_list[{i}].optionen[{j}].key' must be 'a', 'b', or 'c'"
        
        # Check if the solution is 'a', 'b', or 'c'
        if aufgabe['loesung'] not in ['a', 'b', 'c']:
            return False, f"'aufgaben_list[{i}].loesung' must be 'a', 'b', or 'c'"
    
    # Check if the schreibaufgabe has the required fields
    schreibaufgabe = json_data['schreibaufgabe']
    if not isinstance(schreibaufgabe, dict):
        return False, "'schreibaufgabe' must be a dictionary"
    
    if 'aufgaben_text' not in schreibaufgabe:
        return False, "Missing required field: 'schreibaufgabe.aufgaben_text'"
    
    if 'check_list' not in schreibaufgabe:
        return False, "Missing required field: 'schreibaufgabe.check_list'"
    
    # Check if the check_list is a list with at least one item
    check_list = schreibaufgabe['check_list']
    if not isinstance(check_list, list):
        return False, "'schreibaufgabe.check_list' must be a list"
    
    if len(check_list) < 1:
        return False, "'schreibaufgabe.check_list' must have at least one item"
    
    # All checks passed
    return True, "JSON structure is valid"

def generate_mocktest(debug=False):
    """
    Generate a mock test for the B2 Beruf Lesen und Schreiben module.
    
    Args:
        debug (bool): Whether to print debug information during generation
        
    Returns:
        dict: The generated mock test data
    """
    json_str = generate(debug=debug)
    json_data = format_json(json_str, debug=False)
    is_valid, message = verify_json_structure(json_data)
    if not is_valid:
        if debug:
            print(f"Invalid JSON structure: {message}")
        raise ValueError(f"Invalid JSON structure: {message}")
    return json_data

if __name__ == "__main__":

    # Generate more mocktests
    num_tests = 100  # Number of tests to generate
    start_idx = 7   # Starting index for filenames
    
    print(f"Generating {num_tests} mock tests...")
    
    for idx in range(num_tests):
        try:
            print(f"Generating test {idx+1}/{num_tests}...")
            mocktest = generate_mocktest(debug=True)
            output_path = f"/Users/binhnguyen/Workspaces/TELC_B2_test/data_mocktest/lesen_und_schreiben/teil_1_2/mocktest_generated_{idx + start_idx}.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(mocktest, f, indent=4, ensure_ascii=False)
            print(f"Successfully generated test {idx+1}/{num_tests}")
        except Exception as e:
            print(f"Error generating mocktest {idx}: {e}")
    
    print("Generation complete!")