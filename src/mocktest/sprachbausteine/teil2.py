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

example_paths = [
    "data_mocktest/sprachbausteine/teil_2/mock_1.json",
    "data_mocktest/sprachbausteine/teil_2/mock_2.json",
    "data_mocktest/sprachbausteine/teil_2/mock_3.json",
    "data_mocktest/sprachbausteine/teil_2/mock_4.json",
    "data_mocktest/sprachbausteine/teil_2/mock_5.json",
    "data_mocktest/sprachbausteine/teil_2/mock_6.json",
]
example_sample = []
for path in example_paths:
    with open(path, "r", encoding="utf-8") as f:
        example_sample.append(json.load(f))

def generate(debug=False):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )
    
    random.shuffle(example_sample)
    example_for_prompt = [example_sample[i] for i in range(3)]

    example_for_prompt_str = ""
    for idx, example in enumerate(example_for_prompt):
        example_for_prompt_str += f"Example {idx+1}:\n\n"
        example_for_prompt_str += json.dumps(example, indent=4, ensure_ascii=False)
        example_for_prompt_str += "\n\n-----\n\n"

    model = "gemini-2.5-pro-preview-03-25"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""I want to generate a complete, coherent, and realistic task for the "Sprachbausteine teil 2" module of the German B2 Beruf test. 

The generated task will follow this sequence, reflecting the typical test presentation:

1. Write a markdown to brainstorm the idea of the thema will implement
2. Write a markdown to describe the idea of the text content (textinhalt), which phrases will be good to make the blank part for filling out and maybe a good part to have a distractor phrases.
3. Write a markdown to describe the idea of the distractor options, which can be confuse for the examinee.
5. Output the whole task in json format as the example in the instruction"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""## Designing a B2 "Sprachbausteine Teil 2" Mock Test

Here's a breakdown of the design process:

1.  **Thema (Theme) Selection:**
    *   Choose realistic scenarios relevant to work, study, or daily administrative life at a B2 level.
    *   **Examples:**
        *   **Business Communication:** Responding to a complaint, making a counter-offer, requesting specific information, confirming an order/booking, writing an internal announcement, following up on a meeting, clarifying delivery issues.
        *   **Applications/Formal Requests:** Applying for a course/program, requesting official documents, responding to a job application.
        *   **Service Interactions:** Querying an invoice, arranging a service appointment, providing feedback to a service provider.
    *   The theme dictates the tone (usually formal/semi-formal) and the likely vocabulary domain.

2.  **Title:**
    *   Should be brief and clearly indicate the communicative purpose of the text.
    *   Use standard German conventions for subject lines or titles.
    *   **Examples:** "Ihre Anfrage vom [Date]", "Angebot für [Product/Service]", "Bestätigung Ihrer Buchung", "Beschwerde: Rechnungsnummer [Number]", "Informationen zu unserem neuen Service".

3.  **Content Design (Textinhalt):**
    *   **Length:** Aim for approximately 100-150 words (excluding salutation and closing). This is long enough for context but short enough for a focused test item.
    *   **Structure:** Typically a standard letter/email format: Salutation, opening (referencing prior contact or purpose), main body (developing the points), closing remarks, sign-off.
    *   **Complexity:** Use B2-level sentence structures (e.g., relative clauses, passive voice, complex conjunctions like `obwohl`, `während`, `trotzdem`, `daher`). Employ precise vocabulary relevant to the chosen theme.
    *   **Cohesion:** The text must flow logically. Each sentence should build upon the previous one.
    *   **Gap Placement:** While writing, identify natural points where specific vocabulary, collocations, or linking words are essential for meaning. Mark 6 potential gaps. Don't cluster them too closely.

4.  **Difficulty Aspect & Distractor Design (The Core Challenge):**
    *   **Targeted Gaps:** Each gap should test something specific:
        *   **Precise Vocabulary:** Choosing the exact noun, verb, or adjective required by the context (e.g., `erläutern` vs. `erklären` vs. `beschreiben`).
        *   **Collocations:** Fixed or strong word combinations (e.g., `Interesse an`, `in Rechnung stellen`, `zur Verfügung stehen`, `eine Entscheidung treffen`).
        *   **Linking Words/Conjunctions:** Words that signal logical relationships (e.g., `allerdings`, `dennoch`, `folglich`, `zunächst`).
        *   **Prepositional Phrases:** Correct prepositions governed by verbs/nouns or expressing specific relationships (`abhängig von`, `im Rahmen von`).
    *   **Distractor Creation Strategy:** This makes the test challenging and requires careful reading. For each gap:
        *   **Semantic Similarity:** Include options that are in the same semantic field but don't fit the *exact* context or nuance (e.g., for a gap requiring `Kosten`, distractors might be `Preis`, `Gebühr`, `Betrag` – each has a specific usage).
        *   **Collocation Clashes:** Offer words that *could* grammatically fit but violate common collocations (e.g., if the correct answer is `Vorschlag unterbreiten`, a distractor might involve a verb like `geben` or `machen` which are less formal or slightly off).
        *   **Contextual Mismatch:** Provide options that would make sense in a *different* sentence or slightly altered context, tempting test-takers who skim or rely on general meaning.
        *   **Grammatical Near-Misses (Less Common but Possible):** Options that might seem grammatically okay in isolation but create an awkward or incorrect sentence structure overall.
        *   **Formal vs. Informal Register:** Include options that are too informal for the text's overall register.
        *   **Plausibility:** Distractors should *look like* they could be correct at first glance. Avoid obviously wrong answers. The choice should often hinge on reading the *full* sentence or even adjacent sentences.

---

## Markdown Prompt Structure for Automatic Design (Conceptual)

```markdown
# Prompt: Design a B2 German Mock Test (Sprachbausteine Teil 2)

**1. Test Goal:**
Generate a B2-level German "Sprachbausteine Teil 2" mock test item, simulating the format and difficulty of standardized exams like Telc B2 or Goethe-Zertifikat B2. The output should be a JSON object.

**2. Thema (Theme):**
Select ONE specific, realistic theme from the following categories (or propose a similar one):
    *   Business Communication (e.g., Order Confirmation, Response to Inquiry, Complaint Handling, Project Update, Service Offer)
    *   Formal Request/Application (e.g., Course Registration Inquiry, Document Request, Information Request)
    *   Service Interaction (e.g., Invoice Clarification, Appointment Arrangement)
*   **Chosen Theme:** [Specify the chosen theme here, e.g., "Responding to a customer inquiry about event catering services"]

**3. Title:**
Create a concise, appropriate German title reflecting the chosen theme and communicative purpose.
*   **Proposed Title:** [e.g., "Ihre Anfrage bezüglich Catering für Firmenevent"]

**4. Text Content (Textinhalt):**
*   **Generate** a coherent German text (email or letter format) based on the chosen theme.
*   **Length:** Approximately 100-150 words 3-6 paragraphs (excluding salutation/closing).
*   **Register:** Formal or semi-formal.
*   **Complexity:** Use B2-level grammar (subordinate clauses, passive, appropriate conjunctions) and precise vocabulary relevant to the theme.
*   **Structure:** Include Salutation, Opening, Main Body, Closing, Sign-off.
*   **Identify & Mark Gaps:** Mark exactly 6 places within the text suitable for B2-level cloze gaps. Use placeholders like `__1__`, `__2__`, ..., `__6__`. Ensure gaps are distributed reasonably.

**5. Gap Analysis & Option Generation:**
For each gap (`__1__` to `__6__`):
    *   **a. Identify Target:** Specify what the gap primarily tests (e.g., "Precise Verb Choice", "Noun Collocation", "Linking Conjunction", "Prepositional Phrase").
    *   **b. Correct Answer (Lösung):** Determine the **short phrase (typically 2-4 words)** that correctly and most appropriately fills the gap according to context, collocation, register, and B2-level expectations. Single-word answers should be avoided unless absolutely necessary for the specific linguistic point being tested.
    *   **c. Distractor Design (2 Distractors per Gap):** Create two plausible but incorrect distractors. Follow these principles:
        *   Distractors should also be **short phrases (typically 2-4 words)** to maintain structural parallelism and plausibility.
        *   Use phrases semantically related but contextually wrong (wrong nuance, wrong collocation).
        *   Use phrases that might fit in a slightly different context, requiring careful reading of the *current* context.
        *   Avoid obviously wrong answers. Distractors should tempt a B2 learner who reads superficially.
        *   Ensure distractors fit the *local* grammatical structure but violate the overall sentence meaning or established collocations/expressions.

**6. Output Format:**
Structure the final output as a JSON object containing:
*   `title`: The generated title string.
*   `textinhalt`: The generated text string in Markdown format, including the `__1__` to `__6__` placeholders.
*   `aufgaben`: An array of 6 objects, where each object corresponds to a gap and contains:
    *   `id`: The gap number (1 to 6).
    *   `options`: An object with keys `a`, `b`, `c` containing the three choices (correct answer and two distractors, randomly ordered).
    *   `loesung`: The key (`a`, `b`, or `c`) corresponding to the correct answer.

**Example JSON Structure Reference:**
```json
{
  "title": "Example Title",
  "textinhalt": "Sehr geehrte/r ..., \n\nText text __1__ text. Text text __2__ text text. \n\nText __3__ text. Text __4__ text text __5__ text. \n\nText __6__ text.\n\nMit freundlichen Grüßen\n[Name]",
  "aufgaben": [
    { "id": 1, "options": { "a": "OptionA1", "b": "CorrectAnswer1", "c": "OptionC1" }, "loesung": "b" },
    { "id": 2, "options": { "a": "CorrectAnswer2", "b": "OptionB2", "c": "OptionC2" }, "loesung": "a" },
    // ... objects for gaps 3, 4, 5, 6
  ]
}

---
                                 

""" + example_for_prompt_str),
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
    Verifies that the JSON data has the expected structure for a Sprachbausteine Teil 2 test.
    
    Expected structure:
    {
      "title": "Example Title",
      "textinhalt": "Sehr geehrte/r ..., \n\nText text __1__ text. Text text __2__ text text. \n\nText __3__ text. Text __4__ text text __5__ text. \n\nText __6__ text.\n\nMit freundlichen Grüßen\n[Name]",
      "aufgaben": [
        { "id": 1, "options": { "a": "OptionA1", "b": "CorrectAnswer1", "c": "OptionC1" }, "loesung": "b" },
        { "id": 2, "options": { "a": "CorrectAnswer2", "b": "OptionB2", "c": "OptionC2" }, "loesung": "a" },
        // ... objects for gaps 3, 4, 5, 6
      ]
    }

    Returns:
        tuple: (is_valid, message) where is_valid is a boolean and message is an error message if not valid
    """
    # Check if json_data is a dictionary
    if not isinstance(json_data, dict):
        return False, "JSON data is not a dictionary"
    
    # Check required fields
    required_fields = ["title", "textinhalt", "aufgaben"]
    for field in required_fields:
        if field not in json_data:
            return False, f"Missing required field: {field}"
    
    # Validate title
    if not isinstance(json_data["title"], str) or len(json_data["title"].strip()) == 0:
        return False, "Title must be a non-empty string"
    
    # Validate textinhalt
    if not isinstance(json_data["textinhalt"], str) or len(json_data["textinhalt"].strip()) == 0:
        return False, "Textinhalt must be a non-empty string"
    
    # Check if textinhalt contains the expected number of gaps
    expected_gaps = 6
    actual_gaps = 0
    for i in range(1, expected_gaps + 1):
        if f"__{i}__" in json_data["textinhalt"]:
            actual_gaps += 1
    
    if actual_gaps != expected_gaps:
        return False, f"Textinhalt should have exactly {expected_gaps} gaps, but found {actual_gaps}"
    
    # Validate aufgaben
    if not isinstance(json_data["aufgaben"], list):
        return False, "Aufgaben must be a list"
    
    if len(json_data["aufgaben"]) != expected_gaps:
        return False, f"Aufgaben should have exactly {expected_gaps} items, but found {len(json_data['aufgaben'])}"
    
    # Check each aufgabe
    used_ids = set()
    for idx, aufgabe in enumerate(json_data["aufgaben"]):
        # Check if aufgabe is a dictionary
        if not isinstance(aufgabe, dict):
            return False, f"Aufgabe at index {idx} is not a dictionary"
        
        # Check required fields for aufgabe
        aufgabe_required_fields = ["id", "options", "loesung"]
        for field in aufgabe_required_fields:
            if field not in aufgabe:
                return False, f"Aufgabe at index {idx} is missing required field: {field}"
        
        # Validate id
        if not isinstance(aufgabe["id"], int) or not (1 <= aufgabe["id"] <= expected_gaps):
            return False, f"Aufgabe at index {idx} has invalid id: {aufgabe['id']}. Must be an integer between 1 and {expected_gaps}"
        
        # Check for duplicate ids
        if aufgabe["id"] in used_ids:
            return False, f"Duplicate aufgabe id: {aufgabe['id']}"
        used_ids.add(aufgabe["id"])
        
        # Validate options
        if not isinstance(aufgabe["options"], dict):
            return False, f"Options for aufgabe id {aufgabe['id']} must be a dictionary"
        
        # Check required options
        required_options = ["a", "b", "c"]
        for option in required_options:
            if option not in aufgabe["options"]:
                return False, f"Aufgabe id {aufgabe['id']} is missing option: {option}"
            
            # Validate each option value
            if not isinstance(aufgabe["options"][option], str) or len(aufgabe["options"][option].strip()) == 0:
                return False, f"Option {option} for aufgabe id {aufgabe['id']} must be a non-empty string"
        
        # Validate loesung
        if not isinstance(aufgabe["loesung"], str) or aufgabe["loesung"] not in required_options:
            return False, f"Loesung for aufgabe id {aufgabe['id']} must be one of {required_options}"
    
    # Check if all expected ids are present
    expected_ids = set(range(1, expected_gaps + 1))
    if used_ids != expected_ids:
        missing_ids = expected_ids - used_ids
        return False, f"Missing aufgabe ids: {missing_ids}"
    
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
    num_tests = 30  # Number of tests to generate
    shard_idx = 4
    total_shard = 5
    start_idx = 7 + shard_idx * num_tests  # Starting index for filenames
    idx = 0
    print(f"Generating {num_tests} mock tests...")
    
    while idx < num_tests:
        try:
            print(f"Generating test {idx+1}/{num_tests}...")
            mocktest = generate_mocktest(debug=True)
            output_path = f"/Users/binhnguyen/Workspaces/TELC_B2_test/data_mocktest/sprachbausteine/teil_2/mocktest_generated_{idx + start_idx}.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(mocktest, f, indent=4, ensure_ascii=False)
            print(f"Successfully generated test {idx+1}/{num_tests}")
            idx += 1
        except Exception as e:
            print(f"Error generating mocktest {idx}: {e}")
    
    print("Generation complete!")