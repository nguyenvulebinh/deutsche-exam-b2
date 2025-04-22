import base64
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
import random
import re
load_dotenv()


example_paths = [
  "data_mocktest/sprachbausteine/teil_1_refine/mock_1.json",
  "data_mocktest/sprachbausteine/teil_1_refine/mock_2.json",
  "data_mocktest/sprachbausteine/teil_1_refine/mock_3.json",
  "data_mocktest/sprachbausteine/teil_1_refine/mock_4.json",
  "data_mocktest/sprachbausteine/teil_1_refine/mock_5.json",
  "data_mocktest/sprachbausteine/teil_1_refine/mock_6.json",
  "data_mocktest/sprachbausteine/teil_1_refine/mock_7.json",
  "data_mocktest/sprachbausteine/teil_1_refine/mock_8.json",
  "data_mocktest/sprachbausteine/teil_1_refine/mock_9.json",
  "data_mocktest/sprachbausteine/teil_1_refine/mock_10.json",
  "data_mocktest/sprachbausteine/teil_1_refine/mock_11.json",
  "data_mocktest/sprachbausteine/teil_1_refine/mock_12.json",
  "data_mocktest/sprachbausteine/teil_1_refine/mock_13.json",
  "data_mocktest/sprachbausteine/teil_1_refine/mock_14.json",
  "data_mocktest/sprachbausteine/teil_1_refine/mock_15.json",
  "data_mocktest/sprachbausteine/teil_1_refine/mock_16.json"
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
    example_for_prompt = [example_sample[i] for i in range(5)]

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
                types.Part.from_text(text="""I want to generate a complete, coherent, and realistic task for the "Sprachbausteine teil 1" module of the German B2 Beruf test. 

The generated task will follow this sequence, reflecting the typical test presentation:

1. Write a markdown to brainstorm the idea of the thema will implement
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

## 1. Objective

Generate a realistic German language test exercise in the format of "Sprachbausteine Teil 1" targeting the **B2 level** of the Common European Framework of Reference for Languages (CEFR/GER). The exercise should simulate a common professional communication scenario: **writing an email or letter to follow up on a job application**. The primary focus is on creating plausible and challenging multiple-choice options (distractors) that test common B2-level grammatical and lexical nuances.

## 2. Input Parameters

*   **Target Level:** B2 (GER / CEFR)
*   **Exercise Format:** Sprachbausteine Teil 1 (Multiple-choice gap-fill)
*   **Context:** Professional Communication - Follow-up regarding a job application (email or formal letter).
*   **Number of Gaps:** 6
*   **Number of Options:** 10
*   **Focus Scenario (Choose one or combine elements):**
    *   Inquiring about the application status after some time has passed.
    *   Responding to a request for more information/documents.
    *   Confirming receipt of an interview invitation / Requesting to reschedule an interview.
    *   Expressing continued interest after an interview / Thanking for the interview.
    *   Inquiring about a missing promised document (e.g., *Arbeitszeugnis*).
    *   Reporting a technical issue with an online application portal.
    *   Following up after submitting missing documents.
    *   Inquiring about the next steps in the process.
*   **Potential `Thema` (Subject Lines - Choose one relevant to the Focus Scenario - Or can expand the list to relevant scenario):**
    *   Betreff: Nachfrage zum Stand meiner Bewerbung als [Job Title] vom [Date]
    *   Betreff: Meine Bewerbung als [Job Title] - Kennziffer [Reference Number]
    *   Betreff: Rückfrage zu meiner Bewerbung vom [Date]
    *   Betreff: Nachfrage zu meinem Vorstellungsgespräch am [Date]
    *   Betreff: Benötigte Unterlagen für meine Bewerbung als [Job Title]
    *   Betreff: Terminbestätigung / Terminanfrage Vorstellungsgespräch [Job Title]
    *   Betreff: Fehlendes Arbeitszeugnis - Meine Bewerbung vom [Date]
    *   Betreff: Problem mit Online-Bewerbung - [Your Name]

## 3. Text Generation Guidelines

*   **Authenticity:** The text should sound like a genuine email or formal letter written in a professional German context. Use appropriate salutations (`Sehr geehrte/r Frau/Herr [Name]`, `Sehr geehrte Damen und Herren`) and closings (`Mit freundlichen Grüßen`).
*   **Content:** The text must logically develop the chosen "Focus Scenario". It should include:
    *   A clear reference to the previous application or contact (e.g., date, job title, interview, reference number).
    *   The reason for writing (the follow-up action).
    *   Relevant details (e.g., mentioning a deadline, another job offer, availability, specific document).
    *   A polite request or statement.
*   **Length:** The `textinhalt` (excluding salutation and closing) should be approximately **100-150 words** long **3-5 paragraphs**. This is typical for this type of communication and provides enough context for B2-level structures without being overwhelming.
*   **B2 Complexity:**
    *   **Vocabulary:** Use appropriate professional vocabulary related to applications, deadlines, documents, communication, interviews, etc. Avoid overly simplistic or highly specialized C1/C2 terms. Examples: `fristgerecht`, `bezugnehmend auf`, `Unterlagen`, `zeitnah`, `Rückmeldung`, `erkundigen`, `vereinbaren`, `nachreichen`, `bedauerlicherweise`, `gegebenenfalls`.
    *   **Grammar:** Incorporate typical B2 structures: subordinate clauses (causal `weil/da`, temporal `als/wenn/während/seitdem/bis`, concessive `obwohl`, conditional `wenn/falls`, relative clauses, indirect questions `ob/wann/wie`), appropriate use of prepositions (especially two-way prepositions, prepositions governing specific cases, or those with specific meanings like `aufgrund`, `trotz`, `bezüglich`), conjunctions and connectors (adverbs like `deshalb/deswegen`, `trotzdem`, `allerdings`, `zudem`, `anschließend`; conjunctions like `sowohl...als auch`), passive voice where natural (e.g., `wurde mir mitgeteilt`), Konjunktiv II for politeness/hypothetical situations (`könnten Sie mir mitteilen`, `wäre es möglich`).
*   **Gaps (`__1__` to `__6__`):** Place the gaps strategically to test understanding of connectors, prepositions, specific adverbs, modal particles, conjunctions, or verbs requiring specific prepositions/cases that are crucial for coherence and correctness at the B2 level.

## 4. Gap & Option List Generation Guidelines (CRITICAL FOCUS)

*   **Targeted Testing:** Each gap should test a specific grammatical or lexical point relevant to B2. Avoid gaps that test only basic A1/A2 vocabulary if other options are possible.
*   **Correct Answers:** Select the grammatically and semantically correct word for each gap from the B2 range.
*   **Distractor Design Strategy:** The remaining 4 options must be carefully crafted distractors. They should *not* be randomly chosen words. Design them based on the following principles, aiming for confusion if the test-taker lacks precise knowledge:
    *   **Strategy 1: Grammatically Similar, Semantically Different:**
        *   Include options from the **same word class** (e.g., another conjunction, another preposition, another temporal adverb) as the correct answer, but with a **meaning inappropriate** for the context.
        *   *Example:* If the answer is the causal conjunction `weil`, a distractor could be the concessive conjunction `obwohl` or the temporal conjunction `während`.
    *   **Strategy 2: Semantically Similar, Grammatically Different:**
        *   Include options with a **similar meaning** to the correct answer but belonging to a **different word class** or requiring **different grammatical structures/case government**.
        *   *Example:* If the answer is the preposition `wegen` (+ Genitive/Dativ), distractors could be the causal conjunction `weil` (requires a subordinate clause) or the causal adverb `deshalb` (requires specific sentence structure).
        *   *Example:* If the answer is the concessive preposition `trotz` (+ Genitive/Dativ), a distractor could be `obwohl` (conjunction).
    *   **Strategy 3: Common Learner Confusions:**
        *   Include words frequently confused by learners at the B1/B2 level.
        *   *Examples:* `seit` vs. `vor` (temporal), `wann` vs. `wenn` vs. `als` (temporal/conditional), `damit` vs. `um...zu` (final clauses), case confusion with prepositions (`für` + Acc vs. `wegen` + Gen/Dat vs. `dank` + Dat/Gen), modal particles (`doch`, `ja`, `wohl`, `eigentlich`), similar looking adverbs (`bereits` vs. `bereit`).
    *   **Strategy 4: Contextual Plausibility (but Incorrect):**
        *   Distractors should seem *somewhat plausible* in the sentence flow at first glance but be definitively wrong upon closer grammatical or semantic analysis within the specific sentence context. Avoid options that are completely nonsensical or belong to a completely unrelated topic.
    *   **Grammatical Consistency (Distractors):** Ensure distractors generally fit the *potential* grammatical slot type (e.g., don't put a clear adjective where a connector is needed), unless exploiting Strategy 2/3.
*   **Option List Finalization:**
    *   The final list must contain 10 options (a-j), including the 6 correct answers and 4 well-designed distractors.
    *   Randomize the order of options.
    *   Ensure each option ID (a-j) is unique.

## 5. Output Format

Present the generated exercise in the following JSON format:

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

## 6. Quality Check

*   Review the generated text for natural flow, grammatical correctness, and B2-level appropriateness.
*   Verify that each correct answer is indeed the only correct option.
*   Critically evaluate the distractors: Are they genuinely plausible yet incorrect? Do they effectively test the targeted B2 challenges based on the strategies outlined above?
*   Ensure the JSON format is correct.

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
    num_tests = 30  # Number of tests to generate
    shard_idx = 5
    total_shard = 6
    start_idx = len(example_sample) + shard_idx * num_tests  # Starting index for filenames
    idx = 0
    print(f"Generating {num_tests} mock tests...")
    
    while idx < num_tests:
        try:
            print(f"Generating test {idx+1}/{num_tests}...")
            mocktest = generate_mocktest(debug=True)
            output_path = f"/Users/binhnguyen/Workspaces/TELC_B2_test/data_mocktest/sprachbausteine/teil_1_refine/mocktest_generated_{idx + 1 + start_idx}.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(mocktest, f, indent=4, ensure_ascii=False)
            print(f"Successfully generated test {idx+1}/{num_tests}")
            idx += 1
        except Exception as e:
            print(f"Error generating mocktest {idx}: {e}")
    
    print("Generation complete!")