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
│   ├── components/         # Reusable UI components
│   ├── test-types/         # Specific test implementations
│   │   ├── lesen-teil-1.js                # Lesen Teil 1 implementation
│   │   ├── lesen-teil-2.js                # Lesen Teil 2 implementation
│   │   ├── lesen-teil-3.js                # Lesen Teil 3 implementation
│   │   ├── lesen-teil-4.js                # Lesen Teil 4 implementation
│   │   ├── lesen-exam.js                  # Complete Lesen exam implementation
│   │   └── lesen-und-schreiben-teil-1-2.js # Lesen und Schreiben Teil 1&2 implementation
│   └── app.js              # Main application script
├── data_mocktest/          # Test data files
│   ├── lesen/              # Reading test data
│   │   ├── teil_1/         # Lesen Teil 1 test files
│   │   ├── teil_1_manifest.json  # Manifest for Teil 1
│   │   ├── teil_2/         # Lesen Teil 2 test files
│   │   ├── teil_2_manifest.json  # Manifest for Teil 2
│   │   ├── teil_3/         # Lesen Teil 3 test files
│   │   ├── teil_3_manifest.json  # Manifest for Teil 3
│   │   ├── teil_4/         # Lesen Teil 4 test files
│   │   └── teil_4_manifest.json  # Manifest for Teil 4
│   └── lesen_und_schreiben/ # Reading and writing test data
│       ├── teil_1_2/       # Lesen und Schreiben Teil 1&2 test files
│       └── teil_1_2_manifest.json # Manifest for Teil 1&2
├── tests/                  # HTML test files
│   ├── lesen_teil_1.html   # Lesen Teil 1 test page
│   ├── lesen_teil_2.html   # Lesen Teil 2 test page
│   ├── lesen_teil_3.html   # Lesen Teil 3 test page
│   ├── lesen_teil_4.html   # Lesen Teil 4 test page
│   ├── lesen_exam.html     # Complete Lesen exam page
│   └── lesen_und_schreiben_teil_1_2.html # Lesen und Schreiben Teil 1&2 page
├── index.html              # Main HTML file
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies for local development
└── test.py                 # Test script for backend/data processing
```

## Architecture Overview

The application follows a modular architecture:

1. **Core Engine**: The `TestEngine` class in `js/core/test-engine.js` provides the foundation for all test types, handling:
   - Test data loading with multiple fallback mechanisms
   - Test selection and display
   - Answer checking and scoring
   - UI state management

2. **Test Types**: Each test type (e.g., `lesen-teil-1.js`) extends the base `TestEngine` class, implementing:
   - Test-specific UI rendering
   - Validation logic for test data
   - Answer checking logic
   - Custom event handling

3. **Data Organization**: Test data is organized in JSON files within the `data_mocktest/` directory, with separate subdirectories for each test type. Each test type has a manifest file that lists all available test files.

## How to Run

1. Clone the repository
2. Open `index.html` in a web browser, or run it on a local server:
   ```
   python -m http.server 8000
   ```
3. Navigate to `http://localhost:8000` in your browser

## Test Types

The application currently supports the following test types:

### Lesen (Reading)

#### Lesen Teil 1
This test involves matching people/situations (numbered 1-5) to articles/texts (lettered a-h). Users select the appropriate article for each person through an interactive grid.

#### Lesen Teil 2
This test presents a reading passage followed by multiple-choice questions. Users read the text and then select the correct answer for each question.

#### Lesen Teil 3
This test focuses on understanding workplace conditions with text passages and comprehension questions.

#### Lesen Teil 4
This test involves understanding tasks and task distribution with text-based exercises.

#### Lesen Exam
A complete exam simulation that combines all four Lesen parts into one test experience.

### Lesen und Schreiben (Reading and Writing)

#### Teil 1&2: Email Correspondence
This test focuses on understanding and responding to email correspondence. Users read emails, answer comprehension questions, and write a response according to specific instructions. The test features:
- Reading comprehension of professional emails
- Multiple-choice questions about email content
- Interactive writing task with a rich text editor
- Self-assessment checklist for the writing task

## Core Components

### TestEngine

The `TestEngine` class (`js/core/test-engine.js`) is the core of the application, providing:

1. **Test data loading** with multiple fallback mechanisms:
   - Manifest file: `data_mocktest/[test_type]/[part]_manifest.json`
   - Default test data embedded in the code
   - Hardcoded fallback lists

2. **Test lifecycle management**:
   - Initialization
   - Random test selection
   - Test display
   - Answer checking
   - Score calculation
   - Results display

3. **DOM interaction**:
   - Element references
   - Event listeners
   - UI state management

### Utils

The `Utils` class (`js/core/utils.js`) provides utility functions for:
- DOM manipulation
- File operations
- Data processing
- UI helpers

## Deployment

The application is designed to work on web servers without server-side code:

1. **Static File Hosting**: The application can be hosted on any static file hosting service, including:
   - GitHub Pages
   - Netlify
   - Vercel
   - Any standard web hosting service

2. **Deployment process**:
   - Push the entire repository to your hosting service
   - For GitHub Pages:
     - Go to Settings > Pages
     - Set the source branch (usually 'main')
     - Your site will be published at `https://username.github.io/repository-name/`

3. **Verifying everything works**:
   - Make sure your file paths are relative and not absolute
   - Test the site after deployment to make sure all test files load properly
   - If tests don't load, check browser console for errors

## Adding a New Test Type

To add a new test type:

1. Create test data files in a new directory (e.g., `data_mocktest/new_test_type/`)
2. Create a manifest file to list all test files (e.g., `data_mocktest/new_test_type/manifest.json`)
3. Create a new test type implementation in `js/test-types/` that extends the `TestEngine` class
4. Create an HTML test page in the `tests/` directory
5. Register the new test type in `app.js`

### Example: Creating a New Test Type

1. Create a new class that extends the `TestEngine` class:

```javascript
// js/test-types/new-test-type.js
import TestEngine from '../core/test-engine.js';
import Utils from '../core/utils.js';

class NewTestType extends TestEngine {
    constructor(options = {}) {
        // Set default options specific to this test type
        const defaultOptions = {
            testDataDir: 'data_mocktest/new_test_type',
            testType: 'New Test Type',
            defaultTestData: { ... }
        };
        
        super({...defaultOptions, ...options});
    }
    
    // Override necessary methods
    validateTestData(data) { ... }
    displayTest(test) { ... }
    checkAnswers() { ... }
    
    // Provide a fallback list of files
    static getFallbackFileList() {
        return [
            'test1.json',
            'test2.json',
            // etc.
        ];
    }
}

export default NewTestType;
```

2. Register the new test type in `app.js`:

```javascript
import NewTestType from './test-types/new-test-type.js';

const testTypes = {
    // ...existing test types
    'new-test-type': NewTestType
};
```

3. Create a manifest file:
```json
{
    "files": [
        "test1.json",
        "test2.json",
        "test3.json"
    ]
}
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch for your feature
3. Add your changes
4. Create a pull request

## License

This project is available for educational purposes.

## Contact

For questions or feedback, please contact: [nguyenvulebinh@gmail.com](mailto:nguyenvulebinh@gmail.com) 