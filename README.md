# TELC B2 Test Platform

This platform provides interactive practice tests for the TELC B2 German language exam.

## Project Structure

The project has been structured in a modular way to easily support different test types:

```
telc_b2_test/
├── css/                    # CSS styles
│   └── styles.css          # Main stylesheet
├── js/                     # JavaScript files
│   ├── core/               # Core functionality
│   │   ├── test-engine.js  # Base test engine
│   │   └── utils.js        # Utility functions
│   ├── test-types/         # Specific test implementations
│   │   ├── lesen-teil-1.js # Lesen Teil 1 implementation
│   │   ├── lesen-teil-2.js # Lesen Teil 2 implementation
│   │   └── ...             # Other test types
│   └── app.js              # Main application script
├── data_mocktest/          # Test data files
│   ├── lesen/
│   │   ├── teil_1/         # Lesen Teil 1 test files
│   │   ├── teil_1_manifest.json  # Manifest for Teil 1
│   │   ├── teil_2/         # Lesen Teil 2 test files
│   │   ├── teil_2_manifest.json  # Manifest for Teil 2
│   │   └── ...             # Other Lesen test parts
│   ├── hoeren/             # Hörverstehen tests
│   └── ...                 # Other test skills
├── tests/                  # HTML test files
│   ├── lesen_teil_1.html   # Lesen Teil 1 test page
│   ├── lesen_teil_2.html   # Lesen Teil 2 test page
│   └── ...                 # Other test pages
└── index.html              # Main HTML file
```

## How to Run

1. Clone the repository
2. Open `index.html` in a web browser, or run it on a local server:
   ```
   python -m http.server 8000
   ```
3. Navigate to `http://localhost:8000` in your browser

## Test Types

The application supports multiple test types with different formats:

### Lesen Teil 1
This test involves matching people/situations (numbered 1-5) to articles/texts (lettered a-h). Users select the appropriate article for each person through an interactive grid.

### Lesen Teil 2
This test presents a reading passage followed by multiple-choice questions. Users read the text and then select the correct answer for each question.

## GitHub Pages Deployment

The application is designed to work on GitHub Pages with special consideration for its limitations:

1. **Directory listing**: Since GitHub Pages doesn't support directory listing, we use fallback mechanisms to load test files:
   - First try direct directory listing (works on local servers)
   - Then try to load the manifest file in the new format: `data_mocktest/lesen/teil_1_manifest.json`
   - If that fails, fall back to the old format: `data_mocktest/lesen/teil_1/file_manifest.json`
   - Finally, use any hardcoded fallback list from the test type class if defined

2. **Deployment instructions**:
   - Push the entire repository to GitHub
   - Go to Settings > Pages
   - Set the source branch (usually 'main')
   - Your site will be published at `https://username.github.io/repository-name/`

3. **Verifying everything works**:
   - Make sure your file paths are relative and not absolute
   - Test the site after deployment to make sure all test files load properly
   - If tests don't load, check browser console for errors

## Adding a New Test Type

To add a new test type:

1. Create test data files in the appropriate directory (e.g., `data_mocktest/lesen/teil_3/`)
2. Create a manifest file using the new format: `data_mocktest/lesen/teil_3_manifest.json`
3. Create a new test type implementation in `js/test-types/` (e.g., `lesen-teil-3.js`)
4. Create an HTML test page in the `tests/` directory
5. Register the new test type in `app.js`

### Example: Creating a New Test Type

1. Create a new class that extends the `TestEngine` class:

```javascript
// js/test-types/lesen-teil-3.js
import TestEngine from '../core/test-engine.js';
import Utils from '../core/utils.js';

class LesenTeil3 extends TestEngine {
    constructor(options = {}) {
        // Set default options specific to this test type
        const defaultOptions = {
            testDataDir: 'data_mocktest/lesen/teil_3',
            testType: 'Lesen Teil 3',
            defaultTestData: { ... }
        };
        
        super({...defaultOptions, ...options});
    }
    
    // Override necessary methods...
    validateTestData(data) { ... }
    displayTest(test) { ... }
    checkAnswers() { ... }
    
    // Important for GitHub Pages - provide a fallback list of files as a last resort
    static getFallbackFileList() {
        return [
            'test1.json',
            'test2.json',
            // etc.
        ];
    }
}

export default LesenTeil3;
```

2. Register the new test type in `app.js`:

```javascript
import LesenTeil1 from './test-types/lesen-teil-1.js';
import LesenTeil2 from './test-types/lesen-teil-2.js';
import LesenTeil3 from './test-types/lesen-teil-3.js';

const testTypes = {
    'lesen-teil-1': LesenTeil1,
    'lesen-teil-2': LesenTeil2,
    'lesen-teil-3': LesenTeil3
    // Add more test types as needed
};
```

3. Create a manifest file using the new format:
```json
{
    "files": [
        "test1.json",
        "test2.json",
        "test3.json"
    ]
}
```

## Test Data Format

Each test type has its own specific JSON format:

### Lesen Teil 1 Format

```json
{
    "exercise_type": "TELC B2",
    "skill": "Lesen",
    "part": "Teil 1",
    "instructions": "Sie lesen online in einer Wirtschaftszeitung und möchten Ihren Freunden einige Artikel schicken...",
    "people": [
        { "id": 1, "description": "Person description..." },
        ...
    ],
    "articles": [
        { "id": "a", "title": "Article title", "description": "Article description..." },
        ...
    ],
    "solutions": {
        "1": "a",
        "2": "b",
        ...
    }
}
```

### Lesen Teil 2 Format

```json
{
    "thema": "Topic title",
    "text": "Reading passage content...",
    "Aufgaben": [
        {
            "type": "richtig/falsch",
            "frage": "Question text...",
            "loesung": "richtig"
        },
        {
            "type": "multiple-choice",
            "frage": "Question text...",
            "optionen": [
                { "key": "a", "text": "Option text..." },
                { "key": "b", "text": "Option text..." },
                { "key": "c", "text": "Option text..." }
            ],
            "loesung": "a"
        }
    ]
}
```

## License

This project is open source and available under the [MIT License](LICENSE). 