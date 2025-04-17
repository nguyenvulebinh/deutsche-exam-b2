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
│   │   └── ...             # Other test types
│   └── app.js              # Main application script
├── data_mocktest/          # Test data files
│   ├── lesen/
│   │   ├── teil_1/         # Lesen Teil 1 test files
│   │   ├── teil_1_manifest.json  # Manifest for Teil 1 (new format)
│   │   └── ...             # Other Lesen test parts
│   ├── hoeren/             # Hörverstehen tests
│   └── ...                 # Other test skills
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

The application is designed to support multiple test types. By default, it loads the "Lesen Teil 1" test, but you can specify other test types by adding a `testType` parameter to the URL:

```
http://localhost:8000/?testType=lesen-teil-1
```

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

1. Create test data files in the appropriate directory (e.g., `data_mocktest/lesen/teil_2/`)
2. Create a manifest file using the new format: `data_mocktest/lesen/teil_2_manifest.json`
3. Create a new test type implementation in `js/test-types/` (e.g., `lesen-teil-2.js`)
4. Register the new test type in `app.js`

### Example: Creating a New Test Type

1. Create a new class that extends the `TestEngine` class:

```javascript
// js/test-types/lesen-teil-2.js
import TestEngine from '../core/test-engine.js';
import Utils from '../core/utils.js';

class LesenTeil2 extends TestEngine {
    constructor(options = {}) {
        // Set default options specific to this test type
        const defaultOptions = {
            testDataDir: 'data_mocktest/lesen/teil_2',
            testType: 'Lesen Teil 2',
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

export default LesenTeil2;
```

2. Register the new test type in `app.js`:

```javascript
import LesenTeil1 from './test-types/lesen-teil-1.js';
import LesenTeil2 from './test-types/lesen-teil-2.js';

const testTypes = {
    'lesen-teil-1': LesenTeil1,
    'lesen-teil-2': LesenTeil2
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

Test data files are in JSON format. The specific format depends on the test type, but they generally follow this structure:

```json
{
    "exercise_type": "TELC B2",
    "skill": "Lesen",
    "part": "Teil 1",
    "instructions": "Instructions for the test...",
    "content": [...],  // Test content (varies by test type)
    "solutions": {...}  // Correct answers
}
```

## License

This project is open source and available under the [MIT License](LICENSE). 