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
  "data_mocktest/sprachbausteine/teil_1/mock_1.json",
  "data_mocktest/sprachbausteine/teil_1/mock_2.json",
  "data_mocktest/sprachbausteine/teil_1/mock_3.json",
  "data_mocktest/sprachbausteine/teil_1/mock_4.json",
  "data_mocktest/sprachbausteine/teil_1/mock_5.json",
  "data_mocktest/sprachbausteine/teil_1/mock_6.json",
  "data_mocktest/sprachbausteine/teil_1/mock_7.json",
  "data_mocktest/sprachbausteine/teil_1/mock_8.json",
  "data_mocktest/sprachbausteine/teil_1/mock_9.json",
  "data_mocktest/sprachbausteine/teil_1/mock_10.json",
  "data_mocktest/sprachbausteine/teil_1/mock_11.json",
  "data_mocktest/sprachbausteine/teil_1/mock_12.json",
  "data_mocktest/sprachbausteine/teil_1/mock_13.json",
  "data_mocktest/sprachbausteine/teil_1/mock_14.json",
  "data_mocktest/sprachbausteine/teil_1/mock_15.json",
  "data_mocktest/sprachbausteine/teil_1/mock_16.json"
]
example_sample = []
for path in example_paths:
    with open(path, "r", encoding="utf-8") as f:
        example_sample.append(json.load(f))

def generate(debug=False, previous_options=[]):
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
                types.Part.from_text(text="""I want to generate a complete, coherent, and realistic task for the "Sprachbausteine teil 1" module of the German B2 Beruf test.""" + """

In the previous mocktests, here is the list of options that have been used:
""" + str(previous_options) + """

The generated task will follow this sequence, reflecting the typical test presentation:

1. Write a markdown to brainstorm the idea of the topic will implement
2. Write a markdown to describe the idea of the text content (textinhalt), 
- Brainstorm which part will be good to make the blank part for filling out, explain why it can be tricky.
- Brainstorm which part will be good to have a distractor, explain why it can be tricky.
3. Write a markdown to brainstorm the 6 single words that can be used to fill the blank part, which can be tricky for the examinee because of the similar meaning, similar grammar, or similar spelling,.... Explain why it can be tricky. Try not to reuse the options in previous generated mocktests (provied above).
4. Write a markdown to describe the idea of the 4 single words distractor options, which can be confuse for the examinee. The distractor options try to confuse which correct answer and by what factor? Explain why it can be tricky.
5. Try to generate a markdown the textinhalt with the blank from 1 to 6 to see:
- If it fit the idea of the text content and the blank part and the options. 
- Check if the distractor options and the answer options are good and hard enough. Explain why it can be tricky.
- Check if the textinhalt is not acidently leak the answer. 
- Blank id in the textinhalt must be in the range from 1 to 6 in the correct order from the begining to the end.
- If any condition not match, back to step 3.
6. Output the whole task in json format as the example in the instruction"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""# Prompt: Generate B2 Beruf Sprachbausteine Teil 1 Mock Test

## Objective:
Generate a complete and realistic mock test item for the Goethe-Zertifikat B2 / telc B2 Beruf German exam, specifically the "Sprachbausteine Teil 1" format. The test item must focus on scenarios relevant to professional life (Beruf).

## Constraints & Requirements:

**1. Topic Brainstorming & Selection (`thema`):**
    *   **Task:** Select a specific, realistic scenario from a professional context suitable for B2 level.
    *   **Context:** Focus on formal written communication (email or letter).
    *   **Examples:** Following up on a job application, inquiring about application status, requesting information about training/seminars, responding to an offer, asking for clarification on a process, requesting documentation (e.g., Arbeitszeugnis), rescheduling appointments, addressing logistical issues (e.g., payment, deadlines), formal complaints about service/process related to work or applications.
    *   **Output:** Define a concise and descriptive subject line (`thema`).
    *   **`thema` Length:** Approximately 3-8 words.

**2. Target Word Selection (The "Sprachbausteine"):**
    *   **Task:** Pre-select exactly **6 target German words** that will be the correct answers for the blanks. These words are the core items being tested.
    *   **Word Types:** Choose primarily from:
        *   Connecting Adverbs (Konjunktionaladverbien: e.g., `deshalb`, `trotzdem`, `allerdings`, `inzwischen`, `anschließend`, `folglich`, `zudem`, `dennoch`)
        *   Subordinating Conjunctions (e.g., `obwohl`, `während`, `seitdem`, `falls`, `damit`, `sobald`, `ob`)
        *   Prepositions (requiring specific cases or common in formal contexts, e.g., `aufgrund`, `bezüglich`, `trotz`, `innerhalb`, `während`, `einschließlich`, `anhand`)
        *   Pronominal Adverbs (e.g., `hierfür`, `darauf`, `wobei`, `wodurch`, `damit`)
        *   Modal/Temporal Adverbs clarifying context (e.g., `bereits`, `umgehend`, `erst`, `selbstverständlich`, `ausschließlich`, `gegebenenfalls`, `nochmals`)
    *   ***Word Length*: Have to be a single word.
    *   **Difficulty:** Aim for a mix within the B2 level – some medium difficulty (common connectors, clear prepositions) and 3-4 harder ones (less frequent connectors, nuanced meanings, tricky pronominal adverbs like `insofern`, `gleichwohl`, `gegebenenfalls`).
    *   **Crucial:** These 6 selected words **must** be the grammatically and semantically correct answers for the blanks later inserted into the `textinhalt`.

**3. Text Content Design (`textinhalt`):**
    *   **Task:** Write the body of the formal email/letter.
    *   **Structure:** Follow standard formal German communication structure:
        *   Appropriate Salutation (`Sehr geehrte/r...` or `Sehr geehrte Damen und Herren,`).
        *   Logical flow: Introduction/Reference -> Development/Explanation/Problem/Request -> Conclusion/Next Steps -> Closing (`Mit freundlichen Grüßen`).
    *   **Integration:** Naturally integrate the 6 pre-selected target words into the text where they fit logically and grammatically.
    *   **Context Provision:** Design the sentences *around* the locations where the target words will be removed. The surrounding text **must** provide sufficient **grammatical context** (e.g., verb position indicating conjunction vs. adverb, noun requiring a specific preposition) and **semantic/logical context** (e.g., contrast, cause/effect, time sequence) so that only the target word fits perfectly.
    *   **Blank Insertion:** Replace the 6 target words with blanks numbered `__1__` through `__6__`.
    *   **Register:** Maintain a consistently formal, polite, and professional tone (B2 level vocabulary and structures).
    *   **`textinhalt` Length:** Approximately 150-200 words, 3-5 paragraphs (excluding salutation and closing).

**4. Option Generation (`options`):**
    *   **Task:** Create a list of 10 possible answer options (labeled `a` through `j`).
    *   **Content:**
        *   Include the **6 pre-selected target words** (which are the correct answers).
        *   Include **4 plausible distractors**.
    *   **Distractor Design Principles:** Distractors should be incorrect but tempting, designed based on:
        *   *Semantic Near Miss:* Similar meaning but wrong nuance for the specific context (e.g., `deswegen` vs. `trotzdem`).
        *   *Grammatical Mismatch:* Would create incorrect word order (e.g., adverb vs. conjunction), require the wrong case, or be the wrong preposition for a verb/noun collocation.
        *   *Logical Disconnect:* Creates an illogical relationship between clauses/sentences.
        *   *Common Learner Errors:* Target typical B2 confusion points (e.g., `wann`/`wenn`, `da`/`weil`, incorrect pronominal adverb).
        *   *Plausibility:* Distractors should look like reasonable German words that *could* fit in some context, but not *this specific* blank.
        *   *Consistency:* All options should generally fit the formal register.
    *   ***Word Length*: Have to be a single word.
    *   **Format:** List the 10 options alphabetically (a-j) below the `textinhalt`. Each option should be relatively short, typically a single word.
    *   **`options` Entry Length:** Mostly single words, max 2 words if absolutely necessary (e.g., "des Weiteren").

**5. Solution Mapping (`loesung`):**
    *   **Task:** Create the solution key.
    *   **Format:** Map each blank number (`1` to `6`) to the corresponding letter (`a` to `j`) of the correct target word from the options list. Use the specified JSON array format.

**6. Final Quality Check:**
    *   **Correctness:** Verify that the 6 target words are unambiguously the only correct answers for their respective blanks.
    *   **Context:** Ensure the context provided is sufficient but not overly simplistic. Does it require B2-level analysis?
    *   **Distractors:** Confirm distractors are genuinely plausible but clearly incorrect upon careful review.
    *   **Grammar/Spelling:** Proofread the entire text (`thema`, `textinhalt`, `options`) for errors.
    *   **B2 Level:** Assess if the vocabulary, sentence structures, target words, and distractors are appropriate for the B2 Beruf level.
    *   **Realism:** Does the overall scenario feel like authentic professional communication?
    *   **Formatting:** Double-check adherence to the JSON output format.
    *   **Length Constraints:** Verify `thema` and `textinhalt` lengths.

**7. JSON Output Format:**
    *   **Task:** Format the entire generated test item strictly according to the following JSON structure:

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

def generate_mocktest(debug=False, previous_options=[]):
    json_str = generate(debug=debug, previous_options=previous_options)
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
    previous_options = []
    while idx < num_tests:
        try:
            print(f"Generating test {idx+1}/{num_tests}...")
            mocktest = generate_mocktest(debug=True, previous_options=previous_options)
            output_path = f"/Users/binhnguyen/Workspaces/TELC_B2_test/data_mocktest/sprachbausteine/teil_1/mocktest_generated_{idx + 1 + start_idx}.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(mocktest, f, indent=4, ensure_ascii=False)
            print(f"Successfully generated test {idx+1}/{num_tests}")
            idx += 1

            # "options": [       {         "id": "a",         "content": "AUFGRUND"       },       {         "id": "b",         "content": "BIS"       },       {         "id": "c",         "content": "DAHER"       },       {         "id": "d",         "content": "DARÜBER"       },       {         "id": "e",         "content": "OB"       },       {         "id": "f",         "content": "SEITDEM"       },       {         "id": "g",         "content": "SOBALD"       },       {         "id": "h",         "content": "SOFORT"       },       {         "id": "i",         "content": "WANN"       },       {         "id": "j",         "content": "ZWISCHEN"       }     ],     "loesung": [       {         "blank": "1",         "option_id": "h"       },       {         "blank": "2",         "option_id": "f"       },       {         "blank": "3",         "option_id": "b"       },       {         "blank": "4",         "option_id": "i"       },       {         "blank": "5",         "option_id": "a"       },       {         "blank": "6",         "option_id": "c"       }     ]
            losung_option_ids = [item['option_id'] for item in mocktest['loesung']]
            losung_words = [item['content'] for item in mocktest['options'] if item['id'] in losung_option_ids]
            previous_options.extend(losung_words)
            previous_options = list(set(previous_options))
            random.shuffle(previous_options)
            if len(previous_options) > 20:
                previous_options = previous_options[:20]
        except Exception as e:
            print(f"Error generating mocktest {idx}: {e}")
    
    print("Generation complete!")