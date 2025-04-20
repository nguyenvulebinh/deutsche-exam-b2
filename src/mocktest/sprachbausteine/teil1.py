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
                types.Part.from_text(text="""I want to generate a complete, coherent, and realistic task for the "Sprachbausteine teil 1" module of the German B2 Beruf test. 

The generated task will follow this sequence, reflecting the typical test presentation:

1. Write a markdown to brainstorm the idea of the thema will implement (don't use thema Vorstellungsgespräch since it's already used in the example)
2. Write a markdown to describe the idea of the text content (textinhalt), which part will be good to make the blank part for filling out and maybe a good part to have a distractor.
3. Write a markdown to describe the idea of the distractor options, which can be confuse for the examinee.
5. Output the whole task in json format as the example in the instruction"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""# Prompt for Designing a B2 German "Sprachbausteine" Mock Test

## 1. Core Parameters

*   **Target Level:** B2 (GER / CEFR) - Focus on professional context (Beruf).
*   **Format:** Formal Email / Letter
*   **Number of Blanks:** 6
*   **Number of Options:** 10 (6 correct answers + 4 distractors)
*   **Approximate Text Length:** 100-150 words, 3-5 paragraphs.

## 2. Thema (Topic)

*   **Choose a specific scenario from professional communication related to job applications/work life.**
    *   *Examples:*
        *   Following up after sending an application (no response yet).
        *   Responding to an interview invitation (confirming, suggesting alternative dates).
        *   Following up after an interview (reiterating interest, providing additional info).
        *   Inquiring about application status after a delay.
        *   Clarifying details mentioned in a job offer or interview.
        *   Reporting a technical problem with an online application portal.
    *   **Selected Thema:** [Clearly state the chosen scenario, e.g., "Email requesting to reschedule an interview due to a prior commitment."]

## 3. Textinhalt (Content Design)

*   **Draft the full text *without* blanks first.** Ensure it's a coherent, logical, and polite formal email/letter fitting the chosen Thema.
*   **Include standard formal elements:**
    *   Clear Subject Line (Betreff)
    *   Formal Salutation (Sehr geehrte/r Frau/Herr [Name], Sehr geehrte Damen und Herren,)
    *   Opening: Reference the context (Ihre Anzeige, unser Gespräch am..., Ihre Einladung zum...)
    *   Body: State the main purpose/problem clearly. Provide concise reasons or explanations.
    *   Closing: Express hope/request action (Ich freue mich auf..., Ich bitte um Ihr Verständnis..., Über eine baldige Nachricht würde ich mich freuen.)
    *   Formal Closing (Mit freundlichen Grüßen)
    *   Signature (Your Name)
*   **Integrate opportunities for B2-level grammatical structures naturally within the text.** Focus on areas where choices are required (conjunctions, prepositions, adverbs, etc.).

## 4. Blank Selection (Choosing Words to Remove)

*   **Identify 6 words/short phrases to turn into blanks.**
*   **Target specific B2 grammatical/lexical points:**
    *   **Conjunctions:** Subordinating (weil, da, obwohl, während, als, wenn, dass, ob...) and Coordinating (aber, doch, sondern, denn...)
    *   **Prepositions:** Those requiring specific cases (mit+D, für+A, wegen+G/D, trotz+G/D, innerhalb+G, während+G...) or used in specific contexts/collocations (Einblick *in*, Frage *nach*, interessiert *an*).
    *   **Adverbs:** Temporal (dann, danach, inzwischen, seitdem, bereits, noch), Causal (deshalb, deswegen, daher, darum), Modal (gerne, leider, vielleicht), Concessive (trotzdem).
    *   **Prepositional Adverbs:** darüber, darauf, davon, danach, worüber, wofür, womit... (especially when referring back to something).
    *   **Particles/Modal Particles:** vielleicht, ja, doch (Use sparingly, often subtle).
    *   **Context-Specific Vocabulary:** Occasionally, a noun or verb might be blanked if the context strongly implies it and distractors are possible.
*   **List the words removed and their corresponding blank numbers (e.g., 1-6 or 46-51).**

## 5. Option Generation (Correct Answers and Distractors)

*   **List the 6 Correct Answers:** These are the words removed in step 4.
*   **Generate 4 Distractors:** These should be plausible but incorrect. Design them based on:
    *   **Grammatical Fit, Semantic Mismatch:** Fits the sentence structure but not the meaning (e.g., using *obwohl* where *weil* is needed).
    *   **Semantic Similarity, Grammatical Mismatch:** Similar meaning but wrong word type or case requirement (e.g., offering *trotz* when *trotzdem* is needed).
    *   **Common Errors:** Words often confused by B2 learners (e.g., *als/wenn*, *seit/vor*, prepositions with wrong cases).
    *   **Contextual Near Misses:** Words that almost fit or might fit another blank.
    *   **Subtle Distinctions:** Pairs like *danach/darüber*, *deshalb/deswegen*, *seit/seitdem*.
    *   **Avoid:** Completely unrelated words or obvious grammatical errors that make the choice too easy. Distractors should tempt the examinee who isn't reading carefully or fully understanding the grammar/context.
*   **Final List of 10 Options:** Combine correct answers and distractors. Assign letters (a-j).

## 6. Final Review

*   Read the text with the blanks. Does it still make sense?
*   Read the text inserting each correct answer. Does it flow correctly and mean what's intended?
*   Consider each blank and its options. Are the distractors genuinely plausible for a B2 learner? Is there only ONE clearly correct answer for each blank based on grammar and context?
*   Check if any option could ambiguously fit more than one blank. Adjust if necessary.

## 7. Output Format (JSON)

*   **Structure the final output in the requested JSON format:**
    ```json
    {
      "thema": "...",
      "textinhalt": "...", // Text with __blank_number__ placeholders
      "options": [
        { "id": "a", "content": "..." },
        // ... up to j
      ],
      "loesung": [
        { "blank": "blank_number_1", "option_id": "correct_letter_1" },
        // ... up to blank 6
      ]
    }
    ```

Example 1:

{
    "thema": "Betreff: Meine Bewerbung vom 24.02.",
    "textinhalt": "Sehr geehrte Damen und Herren,\n\nbezugnehmend auf Ihr Stellenangebot unter der Nummer DA-501921 bei der Bundesagentur für Arbeit hatte ich mich am 24.07. bei Ihrem Unternehmen als Maschinenschlosser beworben. Den Eingang meiner Unterlagen hatte man mir auch __1__ bestätigt.\n\n__2__ sind fast fünf Wochen vergangen, doch leider habe ich __3__ heute noch keine Antwort von Ihnen erhalten. Es wäre sehr hilfreich, wenn Sie mir kurz mitteilen könnten, __4__ ich frühestens mit einer Antwort rechnen kann, da ich gerade noch von einem anderen Unternehmen auch ein interessantes Angebot erhalten habe. Eine Tätigkeit bei Ihnen würde mir jedoch mehr zusagen, allein schon __5__ der guten Erreichbarkeit des Arbeitsplatzes.\n\n__6__ möchte ich sicher sein, dass meine Bewerbung bei Ihnen nicht vergessen wurde. Über eine baldige Nachricht würde ich mich freuen.\n\nVielen Dank im Voraus für Ihre Bemühungen.\n\nFreundliche Grüße\n\nValdis Jagodinskis",
    "options": [
      {
        "id": "a",
        "content": "AUFGRUND"
      },
      {
        "id": "b",
        "content": "BIS"
      },
      {
        "id": "c",
        "content": "DAHER"
      },
      {
        "id": "d",
        "content": "DARÜBER"
      },
      {
        "id": "e",
        "content": "OB"
      },
      {
        "id": "f",
        "content": "SEITDEM"
      },
      {
        "id": "g",
        "content": "SOBALD"
      },
      {
        "id": "h",
        "content": "SOFORT"
      },
      {
        "id": "i",
        "content": "WANN"
      },
      {
        "id": "j",
        "content": "ZWISCHEN"
      }
    ],
    "loesung": [
      {
        "blank": "1",
        "option_id": "h"
      },
      {
        "blank": "2",
        "option_id": "f"
      },
      {
        "blank": "3",
        "option_id": "b"
      },
      {
        "blank": "4",
        "option_id": "i"
      },
      {
        "blank": "5",
        "option_id": "a"
      },
      {
        "blank": "6",
        "option_id": "c"
      }
    ]
}
  

Example 2:

{
    "thema": "Betreff: Bewerbung als Tourismuskaufmann",
    "textinhalt": "Sehr geehrter Herr Frenzel,\n\nauf der Internetseite Ihres Unternehmens bin ich auf das Stellenangebot "Reiseberater Südamerika" aufmerksam geworden. __1__ Tourismuskaufmann mit chilenischen Wurzeln und ausgezeichneten Kenntnissen der Zielregionen passe ich sehr gut in Ihr Anforderungsprofil und möchte mich gern bewerben.\n\nDas Online-Bewerbungsformular habe ich auch __2__ ausgefüllt und die erforderlichen Dokumente hochgeladen, allerdings gibt es ein technisches Problem: Die Bewerbung lässt sich nicht abschicken. Jedes Mal, __3__ ich auf "Senden" klicke, erhalte ich die Meldung "Senden fehlgeschlagen".\n\nKann ich Ihnen meine Bewerbung in diesem Fall __4__ per E-Mail zukommen lassen – obwohl in der Stellenanzeige steht, __5__ Sie ausschließlich Online-Bewerbungen akzeptieren?\n\nIch freue mich über Ihre Rückmeldung. Sie erreichen mich telefonisch unter 0555 26 09 19 30 oder per E-Mail. Telefonisch bin ich in der Regel __6__ 8:00 und 20:00 Uhr gut erreichbar.\n\nVielen Dank.\n\nMit freundlichen Grüßen\n\nJavier Guzmán",
    "options": [
      {
        "id": "a",
        "content": "ALS"
      },
      {
        "id": "b",
        "content": "AUSNAHMSWEISE"
      },
      {
        "id": "c",
        "content": "BEREITS"
      },
      {
        "id": "d",
        "content": "DASS"
      },
      {
        "id": "e",
        "content": "EBENFALLS"
      },
      {
        "id": "f",
        "content": "VON"
      },
      {
        "id": "g",
        "content": "WENN"
      },
      {
        "id": "h",
        "content": "WOBEI"
      },
      {
        "id": "i",
        "content": "ZEITWEISE"
      },
      {
        "id": "j",
        "content": "ZWISCHEN"
      }
    ],
    "loesung": [
      {
        "blank": "1",
        "option_id": "a"
      },
      {
        "blank": "2",
        "option_id": "c"
      },
      {
        "blank": "3",
        "option_id": "g"
      },
      {
        "blank": "4",
        "option_id": "b"
      },
      {
        "blank": "5",
        "option_id": "d"
      },
      {
        "blank": "6",
        "option_id": "j"
      }
    ]
}
  

Example 3:

{
    "thema": "Betreff: Meine Bewerbung am 25.06. auf der Job-Messe",
    "textinhalt": "Sehr geehrter Herr Radebrecht,\n\nim Juni hatte ich mich Ihnen auf der Job-Messe in Dresden persönlich vorgestellt und Ihnen __1__ auch meine Bewerbungsunterlagen gegeben. Nach einem intensiven Gespräch über die Tätigkeiten als Social-Media-Manager, haben Sie mir angeboten, meine Unterlagen an Ihre Marketingleiterin weiterzuleiten, __2__ ich mich sehr gefreut habe.\nLeider habe ich __3__ nichts mehr von Ihrem Unternehmen gehört und bin nun unsicher, ob die Unterlagen vielleicht verlorengegangen sind. __4__ melde ich mich schriftlich bei Ihnen und hänge meine Bewerbungsunterlagen zur Sicherheit noch einmal an.\nFür Ihr Unternehmen habe ich schon einige Ideen, __5__ Sie Ihr Online-Kundenmagazin noch interessanter machen können und mehr junge Menschen über soziale Medien erreichen.\nGerne führe ich diese in einem persönlichen Gespräch aus.\n\n__6__ ich zurzeit in keinem Beschäftigungsverhältnis stehe, bin ich zeitlich flexibel.\n\nVielen Dank im Voraus und mit freundlichen Grüßen\n\nKevin Murr",
    "options": [
      {
        "id": "a",
        "content": "DA"
      },
      {
        "id": "b",
        "content": "DABEI"
      },
      {
        "id": "c",
        "content": "DESHALB"
      },
      {
        "id": "d",
        "content": "MITTLERWEILE"
      },
      {
        "id": "e",
        "content": "OB"
      },
      {
        "id": "f",
        "content": "SEITDEM"
      },
      {
        "id": "g",
        "content": "WANN"
      },
      {
        "id": "h",
        "content": "WIE"
      },
      {
        "id": "i",
        "content": "WORAUF"
      },
      {
        "id": "j",
        "content": "WORÜBER"
      }
    ],
    "loesung": [
      {
        "blank": "1",
        "option_id": "b"
      },
      {
        "blank": "2",
        "option_id": "j"
      },
      {
        "blank": "3",
        "option_id": "f"
      },
      {
        "blank": "4",
        "option_id": "c"
      },
      {
        "blank": "5",
        "option_id": "h"
      },
      {
        "blank": "6",
        "option_id": "a"
      }
    ]
}
  

Example 4:

{
    "thema": "Betreff: Mein Vorstellungsgespräch am 12. Juni",
    "textinhalt": "Sehr geehrte Frau Kiensle,\n\ndanke, dass Sie mir am 12. Juni die Chance gegeben haben, mich __1__ bei Ihnen persönlich vorzustellen. Unser Gespräch hat mir gute Einblicke in die Abläufe und das kollegiale Betriebsklima in Ihrem Haus gegeben, __2__ war ich sehr beeindruckt.\n\n__3__ gut hat mir gefallen, dass Sie den Mitarbeitenden genug Zeit geben, auch auf Menschen mit geistigen Einschränkungen angemessen einzugehen.\n\nEin wenig verunsichert hat mich Ihre Frage __4__, wie ich mir einen guten Umgang mit Seniorinnen und Senioren in Ihrer Einrichtung vorstelle. Aber __5__ bin ich mir sicher, dass ich mit meinen Erfahrungen, die ich in zwei Demenz-WGs gemacht habe, sehr gut in Ihr Team passen würde.\n\nWie gewünscht möchte ich Ihnen deshalb zurückmelden, dass ich __6__ sehr an der Stelle interessiert bin.\n\nIch hoffe auf eine positive Rückmeldung und verbleibe\n\nmit freundlichen Grüßen\n\nKarina Nowitzky",
    "options": [
      {
        "id": "a",
        "content": "AUCH"
      },
      {
        "id": "b",
        "content": "BESONDERS"
      },
      {
        "id": "c",
        "content": "DANACH"
      },
      {
        "id": "d",
        "content": "DARÜBER"
      },
      {
        "id": "e",
        "content": "DAVON"
      },
      {
        "id": "f",
        "content": "FOLGLICH"
      },
      {
        "id": "g",
        "content": "JETZT"
      },
      {
        "id": "h",
        "content": "NICHT"
      },
      {
        "id": "i",
        "content": "WEITERHIN"
      },
      {
        "id": "j",
        "content": "ZURZEIT"
      }
    ],
    "loesung": [
      {
        "blank": "1",
        "option_id": "a"
      },
      {
        "blank": "2",
        "option_id": "e"
      },
      {
        "blank": "3",
        "option_id": "b"
      },
      {
        "blank": "4",
        "option_id": "c"
      },
      {
        "blank": "5",
        "option_id": "g"
      },
      {
        "blank": "6",
        "option_id": "i"
      }
    ]
}
  

Example 5:

{
    "thema": "Betreff: Unser Gespräch am 19.9.",
    "textinhalt": "Sehr geehrte Frau Peters,\n\nzunächst noch einmal herzlichen Dank für das angenehme Vorstellungsgespräch in Ihrem Unternehmen.\n\nEs hat mich sehr gefreut, Sie und Ihren Kollegen Herrn Schubert kennenzulernen.\nBesonders interessant waren die Einblicke __1__ die Pläne für die Expansion. Ich würde mich sehr freuen, __2__ ich Ihr Unternehmen zukünftig unterstützen könnte.\nWie Sie wissen, bin ich derzeit __3__ in einem ungekündigten Arbeitsverhältnis und reise ab Montag kurzfristig beruflich ins Ausland. __4__ werde ich telefonisch nicht gut erreichbar sein. Ich wollte Sie nur kurz __5__ informieren, da Sie sich ja in den nächsten zwei Wochen wieder bei mir melden wollten.\nIch bin nach wie vor sehr an der Stelle interessiert und ab übernächster Woche auch wieder in Deutschland. Natürlich können Sie mich __6__ aber immer per E-Mail erreichen.\n\nIch freue mich darauf, wieder von Ihnen zu hören!\n\nMit freundlichen Grüßen\nSabrina Sturm",
    "options": [
      {
        "id": "a",
        "content": "DA"
      },
      {
        "id": "b",
        "content": "DAHER"
      },
      {
        "id": "c",
        "content": "DARÜBER"
      },
      {
        "id": "d",
        "content": "DAZWISCHEN"
      },
      {
        "id": "e",
        "content": "FÜR"
      },
      {
        "id": "f",
        "content": "IN"
      },
      {
        "id": "g",
        "content": "NOCH"
      },
      {
        "id": "h",
        "content": "SCHON"
      },
      {
        "id": "i",
        "content": "WENN"
      },
      {
        "id": "j",
        "content": "ZWISCHENZEITLICH"
      }
    ],
    "loesung": [
      {
        "blank": "1",
        "option_id": "f"
      },
      {
        "blank": "2",
        "option_id": "i"
      },
      {
        "blank": "3",
        "option_id": "g"
      },
      {
        "blank": "4",
        "option_id": "b"
      },
      {
        "blank": "5",
        "option_id": "c"
      },
      {
        "blank": "6",
        "option_id": "j"
      }
    ]
}
  

Example 6:

{
    "thema": "Betreff: Meine Bewerbung vom 27.3., Stellenzeichen JU-2022",
    "textinhalt": "Sehr geehrte Damen und Herren,\n\nvor einiger Zeit habe ich mich bei Ihnen auf die Stelle als Erzieher beworben und eine Einladung zu einem Vorstellungsgespräch am fünften Mai erhalten, __1__ ich mich sehr gefreut habe. Dürfte ich Sie __2__ bitten, das Gespräch zu verschieben, __3__ ich genau an diesem Tag meine letzte mündliche Prüfung absolvieren muss? Wenn das Gespräch nicht __4__ der Prüfungszeit stattfinden würde, sondern erst danach, wäre ich sehr dankbar. __5__ dem fünften Mai bin ich flexibel.\nAnbei schicke ich Ihnen außerdem wie telefonisch besprochen die Referenz meiner derzeitigen Praktikumsanleiterin. Das Abschlusszeugnis erhalte ich __6__ nach der mündlichen Prüfung und werde es Ihnen dann so schnell wie möglich nachreichen.\n\nVielen Dank für Ihr Verständnis.\n\nMit freundlichen Grüßen\nJonathan Spielberger",
    "options": [
      {
        "id": "a",
        "content": "AB"
      },
      {
        "id": "b",
        "content": "DEMNÄCHST"
      },
      {
        "id": "c",
        "content": "DESWEGEN"
      },
      {
        "id": "d",
        "content": "ERST"
      },
      {
        "id": "e",
        "content": "NUN"
      },
      {
        "id": "f",
        "content": "SEIT"
      },
      {
        "id": "g",
        "content": "TROTZDEM"
      },
      {
        "id": "h",
        "content": "WÄHREND"
      },
      {
        "id": "i",
        "content": "WEIL"
      },
      {
        "id": "j",
        "content": "WORÜBER"
      }
    ],
    "loesung": [
      {
        "blank": "1",
        "option_id": "j"
      },
      {
        "blank": "2",
        "option_id": "c"
      },
      {
        "blank": "3",
        "option_id": "i"
      },
      {
        "blank": "4",
        "option_id": "h"
      },
      {
        "blank": "5",
        "option_id": "a"
      },
      {
        "blank": "6",
        "option_id": "d"
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
    Verifies that the JSON data has the expected structure for a Sprachbausteine Teil 1 test.
    
    Expected structure:
    {
      "thema": "...",
      "textinhalt": "...", // Text with __blank_number__ placeholders
      "options": [
        { "id": "a", "content": "..." },
        // ... up to j
      ],
      "loesung": [
        { "blank": "blank_number_1", "option_id": "correct_letter_1" },
        // ... up to blank 6
      ]
    }
    
    Returns:
        tuple: (is_valid, message) where is_valid is a boolean and message is an error message if not valid
    """
    # Check if json_data is a dictionary
    if not isinstance(json_data, dict):
        return False, "JSON data is not a dictionary"
    
    # Check for required keys
    required_keys = ["thema", "textinhalt", "options", "loesung"]
    for key in required_keys:
        if key not in json_data:
            return False, f"Missing required key: '{key}'"
    
    # Check thema
    if not isinstance(json_data["thema"], str) or not json_data["thema"].strip():
        return False, "Invalid 'thema': must be a non-empty string"
    
    # Check textinhalt
    if not isinstance(json_data["textinhalt"], str) or not json_data["textinhalt"].strip():
        return False, "Invalid 'textinhalt': must be a non-empty string"
    
    # Check if textinhalt contains blank placeholders (numbered from 1 to 6)
    blank_placeholders = re.findall(r"__(\d+)__", json_data["textinhalt"])
    if len(blank_placeholders) != 6:
        return False, f"Expected 6 blank placeholders in 'textinhalt', found {len(blank_placeholders)}"
    
    # Check that all placeholders are numbered from 1 to 6
    expected_blanks = set(str(i) for i in range(1, 7))
    if set(blank_placeholders) != expected_blanks:
        return False, f"Expected blanks numbered 1-6, found {sorted(set(blank_placeholders))}"
    
    # Check options
    if not isinstance(json_data["options"], list):
        return False, "'options' must be a list"
    
    if len(json_data["options"]) != 10:
        return False, f"Expected 10 options, found {len(json_data['options'])}"
    
    # Expected IDs for options (a through j)
    expected_ids = set(chr(ord('a') + i) for i in range(10))
    option_ids = set()
    
    for i, option in enumerate(json_data["options"]):
        if not isinstance(option, dict):
            return False, f"Option at index {i} is not a dictionary"
        
        if "id" not in option:
            return False, f"Option at index {i} is missing 'id'"
        
        if "content" not in option:
            return False, f"Option at index {i} is missing 'content'"
        
        if not isinstance(option["id"], str):
            return False, f"Option 'id' at index {i} must be a string"
        
        if not isinstance(option["content"], str) or not option["content"].strip():
            return False, f"Option 'content' at index {i} must be a non-empty string"
        
        option_ids.add(option["id"])
    
    # Check if all expected option IDs are present
    if option_ids != expected_ids:
        return False, f"Expected option IDs a-j, found {sorted(option_ids)}"
    
    # Check loesung
    if not isinstance(json_data["loesung"], list):
        return False, "'loesung' must be a list"
    
    if len(json_data["loesung"]) != 6:
        return False, f"Expected 6 solutions, found {len(json_data['loesung'])}"
    
    solution_blanks = set()
    
    for i, solution in enumerate(json_data["loesung"]):
        if not isinstance(solution, dict):
            return False, f"Solution at index {i} is not a dictionary"
        
        if "blank" not in solution:
            return False, f"Solution at index {i} is missing 'blank'"
        
        if "option_id" not in solution:
            return False, f"Solution at index {i} is missing 'option_id'"
        
        if not isinstance(solution["blank"], str):
            return False, f"Solution 'blank' at index {i} must be a string"
        
        if not isinstance(solution["option_id"], str):
            return False, f"Solution 'option_id' at index {i} must be a string"
        
        # Check if the blank reference is valid (1-6)
        if solution["blank"] not in expected_blanks:
            return False, f"Solution at index {i} has invalid blank reference: {solution['blank']}"
        
        # Check if the option_id reference is valid (a-j)
        if solution["option_id"] not in expected_ids:
            return False, f"Solution at index {i} has invalid option_id reference: {solution['option_id']}"
        
        solution_blanks.add(solution["blank"])
    
    # Check if all expected blank solutions are present
    if solution_blanks != expected_blanks:
        return False, f"Expected solutions for blanks 1-6, found {sorted(solution_blanks)}"
    
    # If all validations pass, return success
    return True, "JSON structure is valid"

def generate_mocktest(debug=False):
    json_str = generate(debug=debug)
    json_data = format_json(json_str)
    is_valid, message = verify_json_structure(json_data)
    if not is_valid:
        if debug:
            print(f"Invalid JSON structure: {message}")
        raise ValueError(f"Invalid JSON structure: {message}")
    return json_data

if __name__ == "__main__":

    # Generate more mocktests
    num_tests = 200  # Number of tests to generate
    start_idx = 130   # Starting index for filenames
    idx = 0
    print(f"Generating {num_tests} mock tests...")
    
    while idx < num_tests:
        try:
            print(f"Generating test {idx+1}/{num_tests}...")
            mocktest = generate_mocktest(debug=True)
            output_path = f"/Users/binhnguyen/Workspaces/TELC_B2_test/data_mocktest/sprachbausteine/teil_1/mocktest_generated_{idx + start_idx}.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(mocktest, f, indent=4, ensure_ascii=False)
            print(f"Successfully generated test {idx+1}/{num_tests}")
            idx += 1
        except Exception as e:
            print(f"Error generating mocktest {idx}: {e}")
    
    print("Generation complete!")