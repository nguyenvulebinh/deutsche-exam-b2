import base64
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
import random
import re
load_dotenv()
import json


def generate(task_example, debug=False):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    input_task = f"""Input task:
    Thema: {task_example["thema"]}
    Aufgabe: {task_example["aufgabe"]}
    """
    
    model = "gemini-2.5-pro-preview-03-25"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text= input_task + """

The generated will follow this sequence, reflecting the typical guideline generation process:

1. Write a markdown to brainstorm the idea of how should handling the task
2. Write a markdown to describe the idea of which should be include in each level of the helping level for the given task
3. Output the whole response in json format as the example in the instruction. *Make sure all guidance content is write in German*"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""# Prompt for Generating B2 Schreiben Guideline (Forumsbeitrag)

## Objective:
Generate a comprehensive, multi-level guideline for a B2 German test taker preparing for the "Schreiben" task, specifically the "Meinungen begründen und durch Argumente stützen (Forumsbeitrag schreiben)" type. The guideline should be based on a specific test item and the provided B2 evaluation criteria images.

## B2 Level Expectations for this Task (Schreiben - Forumsbeitrag)

*   **Purpose:** Explain what is generally expected from a B2-level response for *this specific task type* (Forumsbeitrag - justifying opinions), directly referencing the official criteria.
*   **Content Focus (Kriterium I: Kommunikative Aufgabenbewältigung):**
    *   **Task Adherence:** Address the task (`{aufgabe}`) appropriately for the given situation and cover the specified points. Your handling of the content should be **"voll adäquat" (fully adequate) to "überwiegend adäquat" (mostly adequate)**. This means you clearly understand and respond to the core issue (e.g., the debate around `{thema}`).
    *   **Opinion & Justification:** Clearly express your opinion and support it with relevant arguments. Ensure your reasoning is logical and directly relates to the `{thema}`.
    *   **Formality & Address:** Address the intended audience (colleagues/management) appropriately. Use a level of formality that is **"meistens angemessen" (mostly appropriate)** for a workplace forum (Column B).
*   **Language Focus (Sprachliche Angemessenheit):**
    *   **Coherence & Cohesion (Kriterium II: Kommunikative Gestaltung):**
        *   Write a text that is **"weitgehend klar [und] zusammenhängend" (largely clear and coherent)**.
        *   Use a **"begrenzte Anzahl von Verknüpfungsmitteln" (limited number of linking devices)** effectively to connect ideas and ensure the text flows logically, making it a clear contribution to the discussion. Structure should include a recognizable introduction, body, and conclusion.
    *   **Accuracy (Kriterium III: Formale Richtigkeit):**
        *   Demonstrate good grammatical control. Use **"einfache sowie einige komplexere sprachliche Strukturen" (simple as well as some more complex structures)**.
        *   These structures should be **"weitgehend korrekt" (largely correct)**. Errors, especially in more complex sentences, are permissible but should not hinder overall understanding.
        *   Spelling and punctuation must be **"hinreichend korrekt" (sufficiently correct)** for the text to be easily readable.
    *   **Range (Kriterium IV: Spektrum sprachlicher Mittel):**
        *   Employ a **"hinreichend breites Spektrum sprachlicher Mittel" (sufficiently broad spectrum of linguistic means)** allowing you to discuss the topic (`{thema}`), including potentially more complex aspects.
        *   Show ability to **"variiert Formulierungen" (vary formulations)** to avoid repetition.
        *   Use vocabulary effectively. **"Lücken im Wortschatz können [...] zu Umschreibungen führen" (Gaps in vocabulary can lead to circumlocutions)**, which is acceptable at this level.
        *   Successfully use **"einige komplexe Satzstrukturen" (some complex sentence structures)**, such as subordinate clauses (e.g., using *weil, obwohl, damit, wenn*) or passive constructions where appropriate.
*   **Overall:** Your goal is to write a well-structured, relevant, and clearly argued forum post on `{thema}` that demonstrates competent B2-level German, even if not entirely error-free.
*   **Language:** Write this section in clear, instructional **English**, incorporating the key German phrases from the criteria (in italics or quotes) for precision.


## Input Variables:
*   `{thema}`: The specific topic of the forum post task.
*   `{aufgabe}`: The specific task description text provided to the test taker.

## Output Structure and Content Requirements:


### 1. Level 1 Guidance: Understanding the Task (`{thema}`)

*   **Title:** "Level 1: Wichtige Punkte in der Aufgabe verstehen" (Level 1: Understanding Key Points in the Task)
*   **Purpose:** Help the test taker identify and understand the crucial elements within the specific `{aufgabe}` text.
*   **Content:**
    *   Quote or paraphrase the most important parts/phrases from the `{aufgabe}`.
    *   For each key part, explain *why* it's important (e.g., "This states the main conflict," "This is a potential advantage you can discuss," "This defines the context").
    *   Provide a very simple explanation of each key part in **German** (target audience: learner needing basic clarification).
    *   Conclude with a brief summary of the core task derived from these key points.
*   **Language:** Main explanations in **English**, simple clarifications in **German**.

---

### 2. Level 2 Guidance: Step-by-Step Checklist for Writing

*   **Title:** "Level 2: Schritt-für-Schritt zum guten Forumsbeitrag" (Level 2: Step-by-Step to a Good Forum Post)
*   **Purpose:** Provide a practical checklist guiding the test taker through the writing process, aligned with B2 criteria.
*   **Content:** Create a checklist with steps like:
    1.  **Understand & Position:** Re-read `{aufgabe}`, decide on your stance (pro/con/mixed). *Why:* Crucial for Kriterium I (Aufgabenbewältigung - "adäquat").
    2.  **Plan Arguments:** Brainstorm points for your stance (linking to `{thema}`). *Why:* Supports Kriterium I & IV (Spektrum - relevant vocabulary/ideas).
    3.  **Structure:** Outline intro, body paragraphs (argument + justification), conclusion. *Why:* Essential for Kriterium II (Gestaltung - "zusammenhängend").
    4.  **Write Introduction:** State the topic (`{thema}`) and your general view/purpose. *Example:* Provide a 1-2 sentence example **in German (B2 level)** relevant to `{thema}`.
    5.  **Write Body Paragraphs:** Develop arguments with justifications. Use linking words ("Verknüpfungsmittel"). *Why:* Shows argumentation (I), coherence (II), language range (IV). *Examples:* Provide example phrases/linking words **in German (B2 level)** for introducing arguments (e.g., *Einerseits..., Andererseits..., Ein wichtiger Punkt ist..., Dagegen spricht, dass..., Hinzu kommt, dass...*). Aim for *some* complex sentences here.
    6.  **Write Conclusion:** Summarize your view, possibly offer a suggestion/compromise related to `{thema}`. *Example:* Provide a 1-2 sentence example **in German (B2 level)**.
    7.  **Check Language:** Review grammar (aim for "weitgehend korrekt", include "einige komplexere Strukturen"), vocabulary variety ("hinreichend breites Spektrum", vary formulations), spelling/punctuation ("hinreichend korrekt"). *Why:* Addresses Kriterium III & IV.
    8.  **Check Formality:** Ensure appropriate tone and salutation/closing for a forum ("meistens angemessen"). *Why:* Part of Kriterium I.
*   **Language:** Main instructions/explanations in **English**. Titles, examples, and key argumentative phrases in **German (B2 level)**. Explicitly reference criteria benefits where relevant.

---

### 3. Level 3 Guidance: Full B2 Sample Answer

*   **Title:** "Level 3: Beispiel für einen vollständigen Forumsbeitrag (B2)" (Level 3: Example of a Complete Forum Post (B2))
*   **Purpose:** Provide a concrete example of a high-quality B2 response to the *specific* `{aufgabe}`, demonstrating the target criteria.
*   **Content:**
    *   Write a complete forum post that directly answers the `{aufgabe}` about `{thema}`.
    *   The post must exemplify:
        *   Appropriate subject line, salutation & closing (Kriterium I).
        *   Clear introduction referencing the situation (Kriterium II).
        *   Well-developed arguments supporting a clear stance (Kriterium I).
        *   Logical structure and paragraphing, using linking words (Kriterium II - "zusammenhängend", "Verknüpfungsmittel").
        *   Use of varied B2-level vocabulary ("hinreichend breites Spektrum") and sentence structures ("einige komplexe Satzstrukturen", "variiert Formulierungen") (Kriterium IV).
        *   Grammar and spelling that are largely correct ("weitgehend korrekt", "hinreichend korrekt") (Kriterium III).
        *   A concluding statement/summary (Kriterium II).
*   **Language:** The entire sample answer must be written in **German (B2 level)**.

---

### Expectation output:
```json
{
  "level1": {
    "title": "Level 1: Wichtige Punkte in der Aufgabe verstehen",
    "guidance": "Markdown-Text für Level 1, einschließlich hervorgehobener Abschnitte der „Aufgabe“, Erklärungen ihrer Wichtigkeit, einfacher deutscher Erläuterungen und einer abschließenden Zusammenfassung."
  },
  "level2": {
    "title": "Level 2: Schritt-für-Schritt zum guten Forumsbeitrag",
    "guidance": "Markdown-Text für Level 2, strukturiert als Checkliste mit detaillierten Schritten, Erklärungen, Verweisen auf Kriterien und spezifischen Beispielen/Phrasen auf B2‑Niveau."
  },
  "level3": {
    "title": "Level 3: Beispiel für einen vollständigen Forumsbeitrag (B2)",
    "guidance": "Markdown-Text mit dem vollständigen Muster‑Forumbeitrag auf B2‑Niveau, komplett auf Deutsch verfasst, der die spezifische „Aufgabe“ und das „Thema“ behandelt. Der Inhalt enthält ausschließlich den Brief. Keine Erläuterungen auf dieser Ebene."
  }
}
```"""),
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
        json_data = json.loads(extracted_json)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"JSON content: {extracted_json[:100]}...")  # Print part of the content for debugging
        raise


def verify_json_structure(json_data):
    """
    Verifies that the JSON data has the expected structure for a Sprachbausteine Teil 2 test.
    
    Expected structure:
    {
        "level1": {
            "title": "Level 1: Wichtige Punkte in der Aufgabe verstehen",
            "guidance": "Markdown-Text für Level 1, einschließlich hervorgehobener Abschnitte der „Aufgabe“, Erklärungen ihrer Wichtigkeit, einfacher deutscher Erläuterungen und einer abschließenden Zusammenfassung."
        },
        "level2": {
            "title": "Level 2: Schritt-für-Schritt zum guten Forumsbeitrag",
            "guidance": "Markdown-Text für Level 2, strukturiert als Checkliste mit detaillierten Schritten, Erklärungen, Verweisen auf Kriterien und spezifischen Beispielen/Phrasen auf B2‑Niveau."
        },
        "level3": {
            "title": "Level 3: Beispiel für einen vollständigen Forumsbeitrag (B2)",
            "guidance": "Markdown-Text mit dem vollständigen Muster‑Forumbeitrag auf B2‑Niveau, komplett auf Deutsch verfasst, der die spezifische „Aufgabe“ und das „Thema“ behandelt. Der Inhalt enthält ausschließlich den Brief. Keine Erläuterungen auf dieser Ebene."
        }
    }

    Returns:
        tuple: (is_valid, message) where is_valid is a boolean and message is an error message if not valid
    """
    # Check if json_data is a dictionary
    if not isinstance(json_data, dict):
        return False, "JSON is not a dictionary"
    
    # Check if all required keys are present
    required_keys = ["level1", "level2", "level3"]
    for key in required_keys:
        if key not in json_data:
            return False, f"Key '{key}' is missing"
    
    # Check if each level has the correct structure
    for level in ["level1", "level2", "level3"]:
        if not isinstance(json_data[level], dict):
            return False, f"Level '{level}' is not a dictionary"
        
    # Check if title and guidance are present
    if "title" not in json_data[level] or "guidance" not in json_data[level]:
        return False, f"Level '{level}' is missing title or guidance"
    
    # Check if title is a string
    if not isinstance(json_data[level]["title"], str):
        return False, f"Level '{level}' title is not a string"
    
    # Check if guidance is a string
    if not isinstance(json_data[level]["guidance"], str):
        return False, f"Level '{level}' guidance is not a string"
    
    return True, "JSON structure is valid"


def generate_mocktest(task_example, debug=False):
    json_str = generate(task_example, debug=debug)
    json_data = format_json(json_str)
    is_valid, message = verify_json_structure(json_data)
    if not is_valid:
        if debug:
            print(f"Invalid JSON structure: {message}")
        raise ValueError(f"Invalid JSON structure: {message}")
    return json_data