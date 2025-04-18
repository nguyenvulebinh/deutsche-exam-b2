/**
 * LesenTeil4 - Implementation for Lesen Teil 4 test type
 * This extends the base TestEngine class
 */

import TestEngine from '../core/test-engine.js';
import Utils from '../core/utils.js';

class LesenTeil4 extends TestEngine {
    /**
     * Constructor for LesenTeil4
     * @param {Object} options - Configuration options
     */
    constructor(options = {}) {
        // Set default options specific to Lesen Teil 4
        const defaultOptions = {
            testDataDir: '/data_mocktest/lesen/teil_4',  // Use absolute path from root
            testType: 'Lesen Teil 4',
            defaultInstructions: 'Lesen Sie das Protokoll und die Aufgaben dazu. Welche Antwort (a, b oder c) passt am besten? Markieren Sie Ihre Lösungen auf dem Antwortbogen.',
            defaultTestData: {
                "meeting_note": "## Protokoll\n\n**19. Februar 20XX, 10.00–11.45 Uhr**\n**Konferenzraum 7, Ort: Neuburger Allee 28, 87341 Ballhausen**\n\n**Anwesende:**\n*   Maria Loppinet (ML, Geschäftsführung)\n*   Lukas Meier (LM, Leitung Einkauf)\n*   Magda Nauner (MN, Leitung Personal)\n*   Gert Schrader (GS, Leitung Produktion)\n*   Peter Schuldt (PS, Leitung Verkauf)\n*   Katja Stevens (KS, Leitung Qualitätskontrolle)\n*   Volha Schäfer (VS, Leitung Finanzen)\n*   Gast: Wanda Lubic (WL, IT-Beauftragte)\n\n**Sitzungsleitung:** Magda Nauner\n**Protokollantin:** Volha Schäfer\n\n**Tagesordnungspunkte**\n\n1.  Begrüßung und Genehmigung des letzten Protokolls\n2.  Stand des Projekts \"Fertigungsanlage\"\n3.  Berichte\n4.  Neue Mitarbeiterinnen und Mitarbeiter\n5.  Update der Software\n6.  Sonstiges",
                "aufgaben_list": [
                    {
                        "frage": "Das Protokoll",
                        "optionen": [
                            {
                                "key": "a",
                                "text": "der letzten Sitzung ist nach Überarbeitung genehmigt."
                            },
                            {
                                "key": "b",
                                "text": "nennt die Teilnehmer der Januar-Sitzung."
                            },
                            {
                                "key": "c",
                                "text": "wird heute von Frau Schäfer geschrieben."
                            }
                        ],
                        "loesung": "c"
                    }
                ]
            }
        };
        
        // Merge with provided options
        super({...defaultOptions, ...options});
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
                const manifestUrl = '/data_mocktest/lesen/teil_4_manifest.json';  // Use absolute path from root
                
                // console.log(`Attempting to load manifest from: ${manifestUrl}`);
                const response = await fetch(manifestUrl);
                
                if (response.ok) {
                    const manifest = await response.json();
                    testFileList = manifest.files || [];
                } else {
                    // Fall back to the parent implementation
                    return super.loadAllTestData();
                }
            } catch (error) {
                console.warn('Error loading teil_4 manifest directly:', error);
                // Fall back to the parent implementation
                return super.loadAllTestData();
            }
            
            if (!testFileList || testFileList.length === 0) {
                console.warn('No test files found in manifest, falling back to default method');
                return super.loadAllTestData();
            }
            
            // Fetch each test file and add to the allTestData array
            const fetchPromises = testFileList.map(file => this.fetchTestData(file));
            const testsData = await Promise.all(fetchPromises);
            
            // Filter out any null results (failed fetches)
            this.allTestData = testsData.filter(test => test !== null);
            
            // If no tests were loaded successfully, use the default test
            if (this.allTestData.length === 0) {
                console.warn('No tests could be loaded from external files');
            }
        } catch (error) {
            console.error('Error loading test data:', error);
            // Fall back to the parent implementation
            return super.loadAllTestData();
        }
    }
    
    /**
     * Set up references to DOM elements
     * @override
     */
    setupDOMReferences() {
        // Call the parent method to set up basic elements
        super.setupDOMReferences();
        
        // Set up additional elements specific to Lesen Teil 4
        this.elements.meetingContent = document.getElementById('meeting-content');
        this.elements.questionsContainer = document.getElementById('questions-container');
    }
    
    /**
     * Validate that test data has the required structure for Lesen Teil 4
     * @override
     * @param {Object} data - Test data to validate
     * @returns {boolean} - Whether the data is valid
     */
    validateTestData(data) {
        return (
            data && 
            data.meeting_note && 
            Array.isArray(data.aufgaben_list) && 
            data.aufgaben_list.length > 0
        );
    }
    
    /**
     * Display the Lesen Teil 4 test
     * @override
     * @param {Object} test - Test data to display
     */
    displayTest(test) {
        // Call the parent method to handle basic display
        super.displayTest(test);
        
        // Clear previous answers
        this.userAnswers = {};
        
        // Set instructions if not already set in the HTML
        if (this.elements.instructions && (!this.elements.instructions.textContent || this.elements.instructions.textContent.trim() === '')) {
            this.elements.instructions.textContent = this.config.defaultInstructions;
        }
        
        // Display meeting note content
        if (this.elements.meetingContent) {
            // console.log('Setting meeting content...');
            this.elements.meetingContent.innerHTML = this.formatText(test.meeting_note);
        } else {
            console.error('Meeting content element not found!');
        }
        
        // Display questions
        this.displayQuestions(test.aufgaben_list);

        // Make sure the UI is properly updated
        // console.log('Ensuring UI visibility...');
        
        // Several ways to hide loading and show content
        if (this.elements.loading) {
            this.elements.loading.classList.add('loaded');
            Utils.hideElement(this.elements.loading);
        }
        
        if (this.elements.testContent) {
            this.elements.testContent.classList.remove('hidden');
            Utils.showElement(this.elements.testContent);
        }
    }
    
    /**
     * Format the text content with proper markdown-like parsing
     * @param {string} text - The text to format
     * @returns {string} - Formatted HTML
     */
    formatText(text) {
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
                
                // Use marked to parse markdown
                return marked.parse(text);
            } catch (error) {
                console.error('Error parsing markdown with marked:', error);
                // Fall back to the basic parsing if marked fails
                return this.basicMarkdownParse(text);
            }
        } else {
            console.warn('Marked library not found, falling back to basic parsing');
            // Fall back to basic parsing if marked isn't available
            return this.basicMarkdownParse(text);
        }
    }
    
    /**
     * Basic markdown parsing as fallback if marked library isn't available
     * @param {string} text - The text to format
     * @returns {string} - Basic formatted HTML
     */
    basicMarkdownParse(text) {
        // Basic markdown to HTML conversion
        let formattedText = text
            // Headers
            .replace(/## (.*?)$/gm, '<h2>$1</h2>')
            .replace(/### (.*?)$/gm, '<h3>$1</h3>')
            .replace(/#### (.*?)$/gm, '<h4>$1</h4>')
            
            // Bold and italic
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
            .replace(/\*(.*?)\*/g, '<em>$1</em>') // Italic
            .replace(/__(.*?)__/g, '<strong>$1</strong>') // Bold with underscore
            .replace(/_(.*?)_/g, '<em>$1</em>') // Italic with underscore
            
            // Lists
            .replace(/^\* (.*?)$/gm, '<li>$1</li>') // Unordered list items
            .replace(/^\d+\. (.*?)$/gm, '<li>$1</li>') // Ordered list items
            
            // Links
            .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>');
        
        // Handle paragraphs and line breaks
        // Replace double newlines with paragraph breaks
        formattedText = formattedText.replace(/\n\n/g, '</p><p>');
        
        // Replace single newlines with <br> tags if they're not part of a list or heading
        formattedText = formattedText.replace(/\n(?!<h|<li|<\/li|<ul|<ol)/g, '<br>');
        
        // Wrap the content in paragraphs
        formattedText = '<p>' + formattedText + '</p>';
        
        // Fix lists
        formattedText = formattedText
            .replace(/<p><li>/g, '<ul><li>')
            .replace(/<\/li><\/p>/g, '</li></ul>')
            .replace(/<p><li>\d+\. /g, '<ol><li>')
            .replace(/<\/li><\/p>/g, '</li></ol>');
        
        // Fix multiple consecutive list items
        formattedText = formattedText
            .replace(/<\/li><li>/g, '</li>\n<li>');
        
        return formattedText;
    }
    
    /**
     * Display the questions for the test
     * @param {Array} questions - Array of question objects
     */
    displayQuestions(questions) {
        if (!this.elements.questionsContainer) {
            console.error('Questions container element not found');
            return;
        }
        
        // Clear previous questions
        this.elements.questionsContainer.innerHTML = '';
        
        // Create and display each question
        questions.forEach((question, index) => {
            const questionDiv = document.createElement('div');
            questionDiv.className = 'question';
            questionDiv.dataset.questionIndex = index;
            
            // Create the question text
            const questionText = document.createElement('div');
            questionText.className = 'question-text';
            questionText.textContent = question.frage;
            questionDiv.appendChild(questionText);
            
            // Create options container
            const optionsDiv = document.createElement('div');
            optionsDiv.className = 'options';
            
            // Create options
            this.createMultipleChoiceOptions(optionsDiv, question.optionen, index);
            
            // Add options to question
            questionDiv.appendChild(optionsDiv);
            
            // Add question to container
            this.elements.questionsContainer.appendChild(questionDiv);
        });
        
        // Add option click event listeners
        const options = this.elements.questionsContainer.querySelectorAll('.option');
        options.forEach(option => {
            option.addEventListener('click', (event) => this.handleOptionClick(event));
        });
    }
    
    /**
     * Create multiple choice options
     * @param {HTMLElement} container - Container to add options to
     * @param {Array} options - Array of option objects
     * @param {number} questionIndex - Index of the question
     */
    createMultipleChoiceOptions(container, options, questionIndex) {
        options.forEach(option => {
            const optionDiv = document.createElement('div');
            optionDiv.className = 'option';
            optionDiv.dataset.questionIndex = questionIndex;
            optionDiv.dataset.optionKey = option.key;
            
            const radio = document.createElement('input');
            radio.type = 'radio';
            radio.name = `question-${questionIndex}`;
            radio.id = `option-${questionIndex}-${option.key}`;
            radio.value = option.key;
            
            const label = document.createElement('label');
            label.className = 'option-text';
            label.htmlFor = `option-${questionIndex}-${option.key}`;
            label.textContent = `${option.key}) ${option.text}`;
            
            optionDiv.appendChild(radio);
            optionDiv.appendChild(label);
            container.appendChild(optionDiv);
        });
    }
    
    /**
     * Handle option click events
     * @param {Event} event - Click event
     */
    handleOptionClick(event) {
        const optionDiv = event.currentTarget;
        const questionIndex = optionDiv.dataset.questionIndex;
        const optionKey = optionDiv.dataset.optionKey;
        
        // Store the user's answer
        this.userAnswers[questionIndex] = optionKey;
        
        // Update the UI to show the selected option
        const questionContainer = optionDiv.closest('.question');
        const options = questionContainer.querySelectorAll('.option');
        
        options.forEach(option => {
            option.classList.remove('selected');
            const radio = option.querySelector('input[type="radio"]');
            if (radio) {
                radio.checked = false;
            }
        });
        
        optionDiv.classList.add('selected');
        const radio = optionDiv.querySelector('input[type="radio"]');
        if (radio) {
            radio.checked = true;
        }
    }
    
    /**
     * Check the user's answers and display results
     */
    checkAnswers() {
        // Hide questions and show results
        Utils.hideElement(this.elements.finishButton);
        Utils.showElement(this.elements.results);
        Utils.showElement(this.elements.newTestButton);
        
        let correctCount = 0;
        const questions = this.currentTest.aufgaben_list;
        
        // Check each question
        for (let i = 0; i < questions.length; i++) {
            const userAnswer = this.userAnswers[i];
            const correctAnswer = questions[i].loesung;
            
            // Get the question element
            const questionElement = this.elements.questionsContainer.querySelector(`.question[data-question-index="${i}"]`);
            
            if (questionElement) {
                // Get all options for this question
                const options = questionElement.querySelectorAll('.option');
                
                // Mark correct and incorrect options
                options.forEach(option => {
                    const optionKey = option.dataset.optionKey;
                    
                    if (optionKey === correctAnswer) {
                        option.classList.add('correct');
                    } else if (optionKey === userAnswer && userAnswer !== correctAnswer) {
                        option.classList.add('incorrect');
                    }
                });
            }
            
            // Count correct answers
            if (userAnswer === correctAnswer) {
                correctCount++;
            }
        }
        
        // Display score with percentage like in Lesen Teil 2
        if (this.elements.score) {
            const total = questions.length;
            const percentage = Math.round((correctCount / total) * 100);
            this.elements.score.textContent = `${correctCount} von ${total} Punkten (${percentage}%)`;
        }
    }
    
    /**
     * Static method to provide a fallback file list if directory listing fails
     * @returns {Array} - List of test files
     */
    static getFallbackFileList() {
        return [
            'mock_1.json',
            'mock_2.json',
            'mock_3.json',
            'mock_4.json',
            'mock_5.json',
            'mock_6.json',
            'mocktest_generated_7.json',
            'mocktest_generated_8.json',
            'mocktest_generated_9.json',
            'mocktest_generated_10.json',
            'mocktest_generated_11.json',
            'mocktest_generated_12.json',
            'mocktest_generated_13.json',
            'mocktest_generated_14.json',
            'mocktest_generated_15.json',
            'mocktest_generated_16.json'
        ];
    }
    
    /**
     * Fetch a single test file
     * @param {string} filename - Name of the file to fetch
     * @returns {Promise<Object|null>} - Test data or null if fetch failed
     */
    async fetchTestData(filename) {
        try {
            // console.log(`Fetching test file: ${filename}`);
            // Use absolute path from root, consistent with Lesen Teil 2
            const filePath = `/data_mocktest/lesen/teil_4/${filename}`;
            // console.log(`Full path: ${filePath}`);
            
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
            // console.log(`Successfully loaded test: ${filename}`);
            
            return data;
        } catch (error) {
            console.error(`Error loading ${filename}:`, error);
            return null; // Return null for failed fetches
        }
    }
    
    /**
     * Load the default test when no tests are available
     * @override
     */
    loadDefaultTest() {
        console.log('Loading default test...');
        if (this.config.defaultTestData) {
            this.currentTest = this.config.defaultTestData;
            
            // Set a filename identifier for the default test
            this.currentTest._sourceFilename = 'default_test_data';
            
            this.displayTest(this.currentTest);
            
            // Make sure the UI is properly updated - handle same as displayTest
            console.log('Showing default test UI...');
            
            // Several ways to hide loading and show content
            if (this.elements.loading) {
                this.elements.loading.classList.add('loaded');
                Utils.hideElement(this.elements.loading);
            }
            
            if (this.elements.testContent) {
                this.elements.testContent.classList.remove('hidden');
                Utils.showElement(this.elements.testContent);
            }
        } else {
            console.error('No default test data available');
            alert('Fehler: Keine Testdaten verfügbar!');
        }
    }
    
    /**
     * Initialize the test engine
     * @override
     * @returns {Promise<void>}
     */
    async initialize() {
        try {
            // Call the parent initialize method
            await super.initialize();
        } catch (error) {
            console.error('Error initializing test engine:', error);
            
            // Make sure loading is always hidden even if there's an error
            if (this.elements.loading) {
                this.elements.loading.classList.add('loaded');
                Utils.hideElement(this.elements.loading);
            }
            
            // Show an error message
            alert('Fehler beim Initialisieren des Tests. Bitte laden Sie die Seite neu.');
        }
    }
    
    /**
     * Load a random test
     * @override
     */
    loadRandomTest() {
        console.log('Loading random test...');
        Utils.showElement(this.elements.loading);
        Utils.hideElement(this.elements.testContent);
        
        try {
            // Shuffle the tests and pick the first one
            const shuffledTests = Utils.shuffleArray(this.allTestData);
            this.currentTest = shuffledTests[0];
            
            // Display the test
            this.displayTest(this.currentTest);
            
            // Make sure the UI is properly updated
            // console.log('Showing random test UI...');
            
            // Several ways to hide loading and show content
            if (this.elements.loading) {
                this.elements.loading.classList.add('loaded');
                Utils.hideElement(this.elements.loading);
            }
            
            if (this.elements.testContent) {
                this.elements.testContent.classList.remove('hidden');
                Utils.showElement(this.elements.testContent);
            }
        } catch (error) {
            console.error('Error loading test:', error);
            
            // Make sure loading is always hidden even if there's an error
            if (this.elements.loading) {
                this.elements.loading.classList.add('loaded');
                Utils.hideElement(this.elements.loading);
            }
            
            alert('Fehler beim Laden des Tests!');
        }
    }
}

export default LesenTeil4; 