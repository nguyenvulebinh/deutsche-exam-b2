/**
 * SprachbausteineTeil2 - Implementation for Sprachbausteine Teil 2 test type
 * This extends the base TestEngine class
 */

import TestEngine from '../core/test-engine.js';
import Utils from '../core/utils.js';

class SprachbausteineTeil2 extends TestEngine {
    /**
     * Constructor for SprachbausteineTeil2
     * @param {Object} options - Configuration options
     */
    constructor(options = {}) {
        // Set default options specific to Sprachbausteine Teil 2
        const defaultOptions = {
            testDataDir: '/data_mocktest/sprachbausteine/teil_2',  // Use absolute path from root
            testType: 'Sprachbausteine Teil 2',
            defaultInstructions: 'Lesen Sie den folgenden Text. Wählen Sie bei jeder Lücke (1-6) aus den drei Antwortmöglichkeiten die richtige aus.',
            defaultTestData: {
                "title": "Beispiel-Titel",
                "textinhalt": "Dies ist ein Beispieltext mit Lücken __1__, __2__, __3__, __4__, __5__, __6__.",
                "aufgaben": [
                    {
                        "id": 1,
                        "options": {
                            "a": "Option A",
                            "b": "Option B",
                            "c": "Option C"
                        },
                        "loesung": "a"
                    },
                    {
                        "id": 2,
                        "options": {
                            "a": "Option A",
                            "b": "Option B",
                            "c": "Option C"
                        },
                        "loesung": "b"
                    },
                    // Add more default questions as needed
                ]
            }
        };
        
        // Merge with provided options
        super({...defaultOptions, ...options});
        
        // Store user answers
        this.userAnswers = {};
    }
    
    /**
     * Initialize the test engine
     * @returns {Promise<void>}
     */
    async initialize() {
        try {
            // Store reference to marked library
            this.marked = window.marked;
            
            // Get reference to key DOM elements
            this.setupDOMReferences();
            
            // Show loading screen
            Utils.showElement(this.elements.loading);
            Utils.hideElement(this.elements.testContent);
            
            // Load all test data
            await this.loadAllTestData();
            
            // Select a random test and display it
            if (this.allTestData.length > 0) {
                this.loadRandomTest();
            } else {
                console.warn('SprachbausteineTeil2: No tests could be loaded, using default test');
                this.loadDefaultTest();
            }
            
            // Set up event listeners
            this.setupEventListeners();
            
            // Hide loading screen
            Utils.hideElement(this.elements.loading);
            Utils.showElement(this.elements.testContent);
        } catch (error) {
            console.error('SprachbausteineTeil2: Error initializing test engine:', error);
            this.loadDefaultTest();
        }
    }
    
    /**
     * Load all test data - override the base method to handle the manifest file location
     * @returns {Promise<void>}
     */
    async loadAllTestData() {
        try {
            let testFileList = [];
            
            // Try to load from manifest file directly
            try {
                const manifestUrl = '/data_mocktest/sprachbausteine/teil_2_manifest.json';  // Use absolute path from root
                
                const response = await fetch(manifestUrl);
                
                if (response.ok) {
                    const manifest = await response.json();
                    testFileList = manifest.files || [];
                } else {
                    // Fall back to the parent implementation
                    return super.loadAllTestData();
                }
            } catch (error) {
                console.warn('SprachbausteineTeil2: Error loading teil_2 manifest directly:', error);
                // Fall back to the parent implementation
                return super.loadAllTestData();
            }
            
            if (!testFileList || testFileList.length === 0) {
                console.warn('SprachbausteineTeil2: No test files found in manifest, falling back to default method');
                return super.loadAllTestData();
            }
            
            // Fetch each test file and add to the allTestData array
            const fetchPromises = testFileList.map(file => this.fetchTestData(file));
            const testsData = await Promise.all(fetchPromises);
            
            // Filter out any null results (failed fetches)
            this.allTestData = testsData.filter(test => test !== null);
            
            // If no tests were loaded successfully, use the default test
            if (this.allTestData.length === 0) {
                console.warn('SprachbausteineTeil2: No tests could be loaded from external files');
            }
        } catch (error) {
            console.error('SprachbausteineTeil2: Error loading test data:', error);
            // Fall back to the parent implementation
            return super.loadAllTestData();
        }
    }
    
    /**
     * Fetch a single test file
     * @param {string} filename - Name of the file to fetch
     * @returns {Promise<Object|null>} - Test data or null if fetch failed
     */
    async fetchTestData(filename) {
        try {
            // Use absolute path from root
            const filePath = `/data_mocktest/sprachbausteine/teil_2/${filename}`;
            
            const response = await fetch(filePath);
            
            if (!response.ok) {
                throw new Error(`Failed to fetch ${filename}: ${response.statusText}`);
            }
            const data = await response.json();
            
            // Validate the test data
            if (!this.validateTestData(data)) {
                throw new Error(`Invalid test data in ${filename}`);
            }
            
            // Store the source filename in the test data for later reference
            data._sourceFilename = filename;
            
            return data;
        } catch (error) {
            console.error(`SprachbausteineTeil2: Error loading ${filename}:`, error);
            return null; // Return null for failed fetches
        }
    }
    
    /**
     * Set up references to DOM elements
     * @override
     */
    setupDOMReferences() {
        // Call the parent method to set up basic elements
        super.setupDOMReferences();
        
        // Set up additional elements specific to Sprachbausteine Teil 2
        this.elements.thema = document.getElementById('thema');
        this.elements.textContent = document.getElementById('text-content');
        this.elements.questionsContainer = document.getElementById('questions-container');
        
        // Add references to buttons
        this.elements.finishBtn = document.getElementById('finish-btn');
        this.elements.newTestBtn = document.getElementById('new-test-btn');
        
        // Add reference to the results section
        this.elements.results = document.getElementById('results');
        this.elements.score = document.getElementById('score');
    }
    
    /**
     * Validate that test data has the required structure for Sprachbausteine Teil 2
     * @override
     * @param {Object} data - Test data to validate
     * @returns {boolean} - Whether the data is valid
     */
    validateTestData(data) {
        return (
            data && 
            typeof data.title === 'string' &&
            typeof data.textinhalt === 'string' &&
            Array.isArray(data.aufgaben) &&
            data.aufgaben.length >= 6
        );
    }
    
    /**
     * Display the test content
     * @override
     * @param {Object} test - Test data to display
     */
    displayTest(test) {
        // Save the current test data
        this.currentTest = test;
        
        // Log the file being used
        if (test._sourceFilename) {
            console.log(`Loaded test from file: ${test._sourceFilename}`);
        }
        
        // Clear previous answers
        this.userAnswers = {};
        
        // Set instructions if not already set in the HTML
        if (this.elements.instructions && (!this.elements.instructions.textContent || this.elements.instructions.textContent.trim() === '')) {
            this.elements.instructions.textContent = this.config.defaultInstructions;
        }
        
        // Display the thema (title)
        this.elements.thema.textContent = test.title;
        
        // Process and display the text with blanks
        this.displayText(test.textinhalt);
        
        // Display the questions
        this.displayQuestions(test.aufgaben);
        
        // Hide results and show finish button
        Utils.hideElement(this.elements.results);
        Utils.hideElement(this.elements.newTestBtn);
        Utils.showElement(this.elements.finishBtn);
    }
    
    /**
     * Format the text content with proper markdown-like parsing and highlight blanks
     * @param {string} text - The text to format with blanks
     * @returns {string} - Formatted HTML
     */
    formatText(text) {
        // Convert multiple consecutive newlines to double newlines (markdown paragraph break)
        // Then remove any remaining single newlines that aren't part of paragraph breaks
        let cleanedText = text.replace(/\n{3,}/g, '\n\n')  // Convert 3+ newlines to 2
                             .replace(/([^\n])\n([^\n])/g, '$1 $2');  // Replace single newlines with spaces
        
        // Check if marked library is available
        if (typeof marked !== 'undefined') {
            try {
                // Configure marked options
                marked.setOptions({
                    breaks: true,        // Convert \n to <br>
                    gfm: true,           // GitHub Flavored Markdown
                    headerIds: true,     // Add ids to headers for linking
                    mangle: false,       // Don't mangle header IDs
                    sanitize: false,     // Don't sanitize HTML
                    silent: false,       // Show errors
                    smartLists: true,    // Use smarter list behavior
                    smartypants: true,   // Use "smart" typographic punctuation
                    xhtml: false         // Don't close single tags with /
                });
                
                // First, temporarily replace the blank placeholders to avoid markdown parsing them
                let tempText = cleanedText.replace(/__(\d+)__/g, '{{BLANK_$1}}');
                
                // Parse markdown
                let parsedText = marked.parse(tempText);
                
                // Replace the temporary placeholders back with styled spans (showing just the number)
                return parsedText.replace(/{{BLANK_(\d+)}}/g, '<span class="blank">$1</span>');
            } catch (error) {
                console.error('Error parsing markdown with marked:', error);
                // Fall back to the basic parsing if marked fails
                return this.basicTextFormat(cleanedText);
            }
        } else {
            console.warn('Marked library not found, falling back to basic parsing');
            // Fall back to basic parsing if marked isn't available
            return this.basicTextFormat(cleanedText);
        }
    }
    
    /**
     * Basic text formatting as fallback if marked library isn't available
     * @param {string} text - The text to format
     * @returns {string} - Basic formatted HTML
     */
    basicTextFormat(text) {
        // First temporarily replace blank placeholders to avoid issues with markdown processing
        let tempText = text.replace(/__(\d+)__/g, '{{BLANK_$1}}');
        
        // Basic markdown to HTML conversion
        let formattedText = tempText
            // Headers
            .replace(/## (.*?)$/gm, '<h2>$1</h2>')
            .replace(/### (.*?)$/gm, '<h3>$1</h3>')
            .replace(/#### (.*?)$/gm, '<h4>$1</h4>')
            
            // Bold and italic
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
            .replace(/\*(.*?)\*/g, '<em>$1</em>') // Italic
            
            // Lists
            .replace(/^\* (.*?)$/gm, '<li>$1</li>'); // Unordered list items
        
        // Handle paragraphs
        formattedText = '<p>' + formattedText.replace(/\n\n/g, '</p><p>') + '</p>';
        
        // Fix lists
        formattedText = formattedText
            .replace(/<p><li>/g, '<ul><li>')
            .replace(/<\/li><\/p>/g, '</li></ul>');
        
        // Replace the temporary blank placeholders back with styled spans (showing just the number)
        return formattedText.replace(/{{BLANK_(\d+)}}/g, '<span class="blank">$1</span>');
    }
    
    /**
     * Display the text with blanks
     * @param {string} text - Text content with placeholders for blanks
     */
    displayText(text) {
        this.elements.textContent.innerHTML = this.formatText(text);
    }
    
    /**
     * Display the multiple-choice questions
     * @param {Array} questions - Array of question objects
     */
    displayQuestions(questions) {
        // Clear existing questions
        this.elements.questionsContainer.innerHTML = '';
        
        // Create a container for each question
        questions.forEach(question => {
            const questionContainer = document.createElement('div');
            questionContainer.className = 'question';
            questionContainer.dataset.id = question.id;
            
            // Add question label/number
            const questionLabel = document.createElement('div');
            questionLabel.className = 'question-label';
            questionLabel.textContent = `${question.id}:`;
            questionContainer.appendChild(questionLabel);
            
            // Create options container
            const optionsContainer = document.createElement('div');
            optionsContainer.className = 'options';
            
            // Add radio buttons for each option
            Object.entries(question.options).forEach(([key, text]) => {
                const option = document.createElement('div');
                option.className = 'option';
                option.dataset.questionId = question.id;
                option.dataset.optionKey = key;
                option.addEventListener('click', this.handleOptionClick.bind(this));
                
                const radio = document.createElement('input');
                radio.type = 'radio';
                radio.name = `question-${question.id}`;
                radio.value = key;
                radio.id = `q${question.id}-${key}`;
                
                const label = document.createElement('label');
                label.className = 'option-text';
                label.htmlFor = `q${question.id}-${key}`;
                label.textContent = `${key}) ${text}`;
                
                option.appendChild(radio);
                option.appendChild(label);
                optionsContainer.appendChild(option);
            });
            
            questionContainer.appendChild(optionsContainer);
            this.elements.questionsContainer.appendChild(questionContainer);
        });
    }
    
    /**
     * Handle click on an option
     * @param {Event} event - Click event
     */
    handleOptionClick(event) {
        let optionElement = event.target;
        
        // Find the option element if clicked on child
        if (!optionElement.classList.contains('option')) {
            optionElement = optionElement.closest('.option');
        }
        
        if (!optionElement) return;
        
        const questionId = optionElement.dataset.questionId;
        const optionKey = optionElement.dataset.optionKey;
        
        // Select the radio button
        const radio = optionElement.querySelector('input[type="radio"]');
        if (radio) {
            radio.checked = true;
        }
        
        // Store the user's answer
        this.userAnswers[questionId] = optionKey;
    }
    
    /**
     * Set up event listeners
     * @override
     */
    setupEventListeners() {
        // Set up finish button
        this.elements.finishBtn.addEventListener('click', () => this.checkAnswers());
        
        // Set up new test button
        this.elements.newTestBtn.addEventListener('click', () => this.loadRandomTest());
    }
    
    /**
     * Check the user's answers and display results
     */
    checkAnswers() {
        // Hide finish button and show new test button
        Utils.hideElement(this.elements.finishBtn);
        Utils.showElement(this.elements.newTestBtn);
        
        // Calculate score
        const totalQuestions = this.currentTest.aufgaben.length;
        let correctAnswers = 0;
        
        // Check each question
        this.currentTest.aufgaben.forEach(question => {
            const questionId = question.id;
            const correctOptionKey = question.loesung;
            const userAnswer = this.userAnswers[questionId];
            
            // Find all options for this question
            const optionElements = document.querySelectorAll(`.option[data-question-id="${questionId}"]`);
            
            // Find the selected option and correct option
            let selectedOption = null;
            let correctOptionElement = null;
            
            optionElements.forEach(option => {
                const value = option.dataset.optionKey;
                
                if (value === userAnswer) {
                    selectedOption = option;
                }
                
                if (value === question.loesung) {
                    correctOptionElement = option;
                }
                
                // Disable all radio buttons
                const radio = option.querySelector('input[type="radio"]');
                if (radio) {
                    radio.disabled = true;
                }
            });
            
            // Mark selected option as correct or incorrect
            if (selectedOption) {
                if (userAnswer === correctOptionKey) {
                    // Correct answer
                    selectedOption.classList.add('correct');
                    correctAnswers++;
                } else {
                    // Incorrect answer
                    selectedOption.classList.add('incorrect');
                }
            }
            
            // Highlight the correct answer if user was wrong or didn't answer
            if (userAnswer !== correctOptionKey && correctOptionElement) {
                correctOptionElement.classList.add('correct');
            }
        });
        
        // Display score with simplified results
        const scorePercentage = Math.round((correctAnswers / totalQuestions) * 100);
        
        // Display simple score without detailed results
        this.elements.score.textContent = `${correctAnswers} von ${totalQuestions} Punkten (${scorePercentage}%)`;
        
        // Show results section
        Utils.showElement(this.elements.results);
        
        // Scroll to results
        this.elements.results.scrollIntoView({ behavior: 'smooth' });
        
    }
    
    /**
     * Provide a fallback list of test files
     * @returns {Array<string>} - List of test files
     */
    static getFallbackFileList() {
        return [
            'mock_1.json',
            'mock_2.json',
            'mock_3.json',
            'mock_4.json',
            'mock_5.json',
            'mock_6.json'
        ];
    }
    
    /**
     * Load a random test from the available tests
     * @override
     */
    loadRandomTest() {
        Utils.hideElement(this.elements.results);
        Utils.showElement(this.elements.loading);
        Utils.hideElement(this.elements.testContent);
        
        try {
            // Reset user answers
            this.userAnswers = {};
            
            // Shuffle the tests and pick the first one
            const shuffledTests = Utils.shuffleArray(this.allTestData);
            this.currentTest = shuffledTests[0];
            
            // Display the test
            this.displayTest(this.currentTest);
            
            Utils.hideElement(this.elements.loading);
            Utils.showElement(this.elements.testContent);
        } catch (error) {
            console.error('Error loading test:', error);
            this.loadDefaultTest();
        }
    }
    
    /**
     * Load the default test data as a fallback
     * @override
     */
    loadDefaultTest() {
        try {
            // Reset user answers
            this.userAnswers = {};
            
            // Use default test data from config
            this.currentTest = this.config.defaultTestData;
            
            // Display the test
            this.displayTest(this.currentTest);
            
            Utils.hideElement(this.elements.loading);
            Utils.showElement(this.elements.testContent);
        } catch (error) {
            console.error('Error loading default test:', error);
            // Display a user-friendly error message
            this.elements.testContent.innerHTML = `
                <div class="error-message">
                    <h2>Fehler beim Laden des Tests</h2>
                    <p>Es ist ein Fehler aufgetreten. Bitte aktualisieren Sie die Seite oder versuchen Sie es später erneut.</p>
                </div>
            `;
        }
    }
}

// Export the class
export default SprachbausteineTeil2; 