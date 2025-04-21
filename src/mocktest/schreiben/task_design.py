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
from help_design import generate_mocktest as generate_help_design

with open('data_mocktest/schreiben/mock.json', "r", encoding="utf-8") as f:
    example_samples = json.load(f)

def generate(debug=False):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )
    
    random.shuffle(example_samples)
    example_for_prompt = [example_samples[i] for i in range(5)]

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
                types.Part.from_text(text="""I want to generate a complete, coherent, and realistic task for the "Test für den Beruf B2 - Schreiben task: Meinungen begründen und durch Argumente stützen (Forumsbeitrag schreiben)" module of the German B2 Beruf test. 

The generated task will follow this sequence, reflecting the typical test presentation:

1. Write a markdown to brainstorm the idea of the thema will implement
2. Write a markdown to describe the idea of the text content of aufgabe. Discuss about what is expected to have from the test taker, what is the difficulty part that may good to have for the task
5. Output the whole task in json format as the example in the instruction"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""# Prompt: Generate B2 German Mock Test Items (Meinungen begründen - Forumsbeitrag)

## 1. Goal:
Generate [Number] new mock test items for the Goethe/Telc B2 German exam task "Schreiben: Meinungen begründen und durch Argumente stützen (Forumsbeitrag schreiben)".

## 2. Input / Context:
The generated items should be similar in style, format, and difficulty to the provided examples (list of Themen/Aufgaben). They should simulate realistic workplace scenarios or proposals within a fictional company.

## 3. Output Format:
Provide the output as a JSON list, where each item is an object with two keys:
*   `"thema"`: A short, descriptive topic title (String, 1-5 words).
*   `"aufgabe"`: The task description outlining the situation/proposal (String, approx. 25-60 words, 2-4 sentences).

## 4. Design Guidelines & Constraints:

### 4.1 `thema`:
*   **Content:** Choose topics relevant to the modern workplace (e.g., work organization, environment, benefits, technology, costs, company culture, health, sustainability).
*   **Style:** Concise, neutral, and descriptive.
*   **Length:** 1 to 5 words.

### 4.2 `aufgabe`:
*   **Structure:**
    *   Start with a brief context (e.g., "Ihre Firma plant...", "Die Geschäftsleitung schlägt vor...", "Es gibt die Idee...").
    *   Clearly state the specific proposal, change, or situation.
    *   Introduce an element that requires argumentation (see Difficulty).
*   **Content:**
    *   The scenario must directly impact employees.
    *   It should present a situation with potential advantages AND disadvantages.
    *   It must implicitly require the test-taker to form an opinion and justify it with arguments in a forum post format.
*   **Language:** Use clear B2-level German. Employ appropriate workplace vocabulary.
*   **Length:** Approximately 25-60 words (2-4 sentences).

### 4.3 Difficulty (B2 Level):
*   **Focus on Argumentation:** The core challenge must be formulating, structuring, and justifying an opinion.
*   **Potential for Debate:** Ensure the `Aufgabe` describes a situation that is not universally positive or negative. Test-takers should need to weigh pros and cons.
*   **Introduce Conflict/Trade-offs:** A good way to ensure debatability is to include:
    *   A benefit linked to a cost or restriction (e.g., new tech but employees pay partly; flexibility but with core hours).
    *   A cost-saving measure that removes a benefit.
    *   A policy change that benefits some but inconveniences others (e.g., open office vs. individual offices; mandatory event).
    *   An obligation added to a benefit (e.g., company phone but must be reachable).
*   **Realism:** The scenarios should be plausible workplace situations.

## 5. Example of a Desired Output Item:
```json
{
"thema": "Thema example",
"aufgabe": "Aufgabe content example"
}
```

----

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
        json_data = json.loads(extracted_json)
        if type(json_data) == list:
            return json_data[0]
        else:
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
        "thema": "Thema example",
        "aufgabe": "Aufgabe content example"
    }

    Returns:
        tuple: (is_valid, message) where is_valid is a boolean and message is an error message if not valid
    """
    # Check if json_data is a dictionary
    if not isinstance(json_data, dict):
        return False, "JSON is not a dictionary"
    
    # Check if thema and aufgabe are present
    if "thema" not in json_data or "aufgabe" not in json_data:
        return False, "thema or aufgabe is missing"
    
    # Check if thema is a string
    if not isinstance(json_data["thema"], str):
        return False, "thema is not a string"
    
    # Check if aufgabe is a string
    if not isinstance(json_data["aufgabe"], str):
        return False, "aufgabe is not a string"
    
    return True, "JSON structure is valid"


def generate_mocktest(task_example = None, debug=False):
    if task_example is None:
        json_str = generate(debug=debug)
        json_data = format_json(json_str)
    else:
        json_data = task_example
    is_valid, message = verify_json_structure(json_data)
    if not is_valid:
        if debug:
            print(f"Invalid JSON structure: {message}")
        raise ValueError(f"Invalid JSON structure: {message}")
    
    print(f"Generating help design for the task: {json_data['thema']}")
    help_design = generate_help_design(json_data, debug=debug)
    json_data["solution"] = help_design
    return json_data

if __name__ == "__main__":

    # Generate for example_samples first
    idx = 0
    while idx < len(example_samples):
        try:
            mocktest = generate_mocktest(example_samples[idx], debug=True)
            output_path = f"/Users/binhnguyen/Workspaces/TELC_B2_test/data_mocktest/schreiben/teil_1/mocktest_generated_{idx + 1}.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(mocktest, f, indent=4, ensure_ascii=False)
            print(f"Successfully generated test {idx+1}/{len(example_samples)}")
            idx += 1
        except Exception as e:
            print(f"Error generating mocktest {idx + 1}: {e}")
    exit()

    # Generate more mocktests
    # num_tests = 50  # Number of tests to generate
    # shard_idx = 4
    # total_shard = 5
    # start_idx = len(example_samples) + shard_idx * num_tests  # Starting index for filenames
    # idx = 0
    # print(f"Generating {num_tests} mock tests...")
    
    # while idx < num_tests:
    #     try:
    #         print(f"Generating test {idx+1}/{num_tests}...")
    #         mocktest = generate_mocktest(debug=True)
    #         output_path = f"/Users/binhnguyen/Workspaces/TELC_B2_test/data_mocktest/schreiben/teil_1/mocktest_generated_{idx + 1 + start_idx}.json"
    #         with open(output_path, "w", encoding="utf-8") as f:
    #             json.dump(mocktest, f, indent=4, ensure_ascii=False)
    #         print(f"Successfully generated test {idx+1}/{num_tests}")
    #         idx += 1
    #     except Exception as e:
    #         print(f"Error generating mocktest {idx + 1}: {e}")
    
    # print("Generation complete!")