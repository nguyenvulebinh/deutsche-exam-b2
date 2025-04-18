/**
 * LesenTeil2 - Implementation for Lesen Teil 2 test type
 * This extends the base TestEngine class
 */

import TestEngine from '../core/test-engine.js';
import Utils from '../core/utils.js';

class LesenTeil2 extends TestEngine {
    /**
     * Constructor for LesenTeil2
     * @param {Object} options - Configuration options
     */
    constructor(options = {}) {
        // Set default options specific to Lesen Teil 2
        const defaultOptions = {
            testDataDir: '/data_mocktest/lesen/teil_2',  // Use absolute path from root
            testType: 'Lesen Teil 2',
            defaultInstructions: 'Lesen Sie die Texte und die Aufgaben. Ist die Aussage dazu richtig oder falsch und welche Antwort (a, b oder c) passt am besten?\nMarkieren Sie Ihre Lösungen auf dem Antwortbogen.',
            defaultTestData: {
                "thema": "Sicherheitshinweise für Labormitarbeiter",
                "text": "## Sicherheit im Labor beachten:\n\n### LABORKLEIDUNG\n\nBeim Arbeiten im Labor muss eine angemessene Kleidung getragen werden, um einerseits sich selbst, andererseits auch bestimmte Materialien zu schützen. Dazu gehört zunächst ein weißer Schutzkittel aus Baumwolle, der immer geschlossen und sauber sein muss.\n\nDa ein Kittel nicht den ganzen Körper schützt, ist darauf zu achten, dass stets geschlossenes, festes Schuhwerk (keine hohen Absätze oder offene Sandalen) sowie lange Hosen zu tragen sind. Das feste, flache Schuhwerk dient nebenbei auch dem Zweck, in Notsituationen das Labor zügig verlassen zu können.\n\nAus hygienischen Gründen müssen auch die Haare durch eine Haube bedeckt sein. Lange Haare müssen zusätzlich zu einem Zopf zusammengebunden werden. Häufig kommt auch noch eine Schutzbrille zum Einsatz.\n\nBeim Hantieren mit empfindlichen oder gefährlichen Substanzen sind Handschuhe zu tragen, um die Hände vor Kontamination zu schützen. Das heißt jedoch nicht, dass die Handschuhe bei Arbeitsbeginn im Labor angezogen und erst wieder abends ausgezogen werden. Da die Handschuhe durch die Arbeit mit chemischen Substanzen verunreinigt sein könnten, sollten diese nach durchgeführter Arbeit stets abgelegt und nicht auch noch während anderer Tätigkeiten im Labor getragen werden. Auf keinen Fall darf das Labor mit Handschuhen verlassen werden.",
                "Aufgaben": [
                    {
                        "type": "richtig/falsch",
                        "frage": "Beim Arbeiten im Labor darf man weder kurze Hosen tragen noch längere Haare offen lassen.",
                        "loesung": "richtig"
                    },
                    {
                        "type": "multiple-choice",
                        "frage": "Im Labor müssen Handschuhe",
                        "optionen": [
                            {
                                "key": "a",
                                "text": "bei allen Arbeiten getragen werden."
                            },
                            {
                                "key": "b",
                                "text": "gleich bei Arbeitsantritt angelegt werden."
                            },
                            {
                                "key": "c",
                                "text": "nach Arbeiten mit Chemikalien ausgezogen werden."
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
                const manifestUrl = '/data_mocktest/lesen/teil_2_manifest.json';  // Use absolute path from root
                
                const response = await fetch(manifestUrl);
                
                if (response.ok) {
                    const manifest = await response.json();
                    testFileList = manifest.files || [];
                } else {
                    // Fall back to the parent implementation
                    return super.loadAllTestData();
                }
            } catch (error) {
                console.warn('Error loading teil_2 manifest directly:', error);
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
        
        // Set up additional elements specific to Lesen Teil 2
        this.elements.thema = document.getElementById('thema');
        this.elements.textContent = document.getElementById('text-content');
        this.elements.questionsContainer = document.getElementById('questions-container');
    }
    
    /**
     * Validate that test data has the required structure for Lesen Teil 2
     * @override
     * @param {Object} data - Test data to validate
     * @returns {boolean} - Whether the data is valid
     */
    validateTestData(data) {
        return (
            data && 
            data.thema && 
            data.text && 
            Array.isArray(data.Aufgaben) && 
            data.Aufgaben.length > 0
        );
    }
    
    /**
     * Display the Lesen Teil 2 test
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
        
        // Display thema
        if (this.elements.thema) {
            this.elements.thema.textContent = test.thema;
        }
        
        // Display text content
        if (this.elements.textContent) {
            this.elements.textContent.innerHTML = this.formatText(test.text);
        }
        
        // Display questions
        this.displayQuestions(test.Aufgaben);
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
     * Display the questions
     * @param {Array} questions - Questions data
     */
    displayQuestions(questions) {
        const questionsContainer = this.elements.questionsContainer;
        questionsContainer.innerHTML = '';
        
        questions.forEach((question, index) => {
            const questionElement = Utils.createElement('div', {
                className: 'question',
                dataset: {
                    index: index,
                    type: question.type
                }
            });
            
            // Question text
            const questionText = Utils.createElement('div', {
                className: 'question-text'
            }, `${index + 1}. ${question.frage}`);
            
            questionElement.appendChild(questionText);
            
            // Question options
            const optionsContainer = Utils.createElement('div', {
                className: 'options'
            });
            
            if (question.type === 'richtig/falsch') {
                // Create true/false options
                this.createTrueFalseOptions(optionsContainer, index);
            } else if (question.type === 'multiple-choice') {
                // Create multiple-choice options
                this.createMultipleChoiceOptions(optionsContainer, question.optionen, index);
            }
            
            questionElement.appendChild(optionsContainer);
            questionsContainer.appendChild(questionElement);
        });
    }
    
    /**
     * Create true/false options
     * @param {Element} container - Container to add options to
     * @param {number} questionIndex - Index of the question
     */
    createTrueFalseOptions(container, questionIndex) {
        const options = [
            { value: 'richtig', label: 'Richtig' },
            { value: 'falsch', label: 'Falsch' }
        ];
        
        options.forEach(option => {
            const optionElement = Utils.createElement('div', {
                className: 'option',
                dataset: {
                    questionIndex: questionIndex,
                    value: option.value
                },
                onClick: this.handleOptionClick.bind(this)
            });
            
            const radio = Utils.createElement('input', {
                type: 'radio',
                name: `question-${questionIndex}`,
                value: option.value
            });
            
            const optionText = Utils.createElement('div', {
                className: 'option-text'
            }, option.label);
            
            optionElement.appendChild(radio);
            optionElement.appendChild(optionText);
            container.appendChild(optionElement);
        });
    }
    
    /**
     * Create multiple-choice options
     * @param {Element} container - Container to add options to
     * @param {Array} options - Options data
     * @param {number} questionIndex - Index of the question
     */
    createMultipleChoiceOptions(container, options, questionIndex) {
        options.forEach(option => {
            const optionElement = Utils.createElement('div', {
                className: 'option',
                dataset: {
                    questionIndex: questionIndex,
                    value: option.key
                },
                onClick: this.handleOptionClick.bind(this)
            });
            
            const radio = Utils.createElement('input', {
                type: 'radio',
                name: `question-${questionIndex}`,
                value: option.key
            });
            
            const optionText = Utils.createElement('div', {
                className: 'option-text'
            }, `${option.key}) ${option.text}`);
            
            optionElement.appendChild(radio);
            optionElement.appendChild(optionText);
            container.appendChild(optionElement);
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
        
        const questionIndex = optionElement.dataset.questionIndex;
        const value = optionElement.dataset.value;
        
        // Select the radio button
        const radio = optionElement.querySelector('input[type="radio"]');
        if (radio) {
            radio.checked = true;
        }
        
        // Store the answer
        this.userAnswers[questionIndex] = value;
    }
    
    /**
     * Check answers and show results
     * @override
     */
    checkAnswers() {
        let correct = 0;
        const aufgaben = this.currentTest.Aufgaben;
        
        // Check each answer
        aufgaben.forEach((aufgabe, index) => {
            const userAnswer = this.userAnswers[index];
            const correctAnswer = aufgabe.loesung;
            
            // Find all options for this question
            const optionElements = document.querySelectorAll(`.option[data-question-index="${index}"]`);
            
            // Find the selected option and correct option
            let selectedOption = null;
            let correctOption = null;
            
            optionElements.forEach(option => {
                const value = option.dataset.value;
                
                if (value === userAnswer) {
                    selectedOption = option;
                }
                
                if (value === correctAnswer) {
                    correctOption = option;
                }
            });
            
            // Mark selected option as correct or incorrect
            if (selectedOption) {
                if (userAnswer === correctAnswer) {
                    // Correct answer
                    selectedOption.classList.add('correct');
                    correct++;
                } else {
                    // Incorrect answer
                    selectedOption.classList.add('incorrect');
                }
            }
            
            // Highlight the correct answer if user was wrong or didn't answer
            if (userAnswer !== correctAnswer && correctOption) {
                correctOption.classList.add('correct');
            }
        });
        
        // Show score
        const total = aufgaben.length;
        if (this.elements.score) {
            this.elements.score.textContent = `${correct} von ${total} Punkten (${Math.round((correct / total) * 100)}%)`;
        }
        
        // Call the parent method to update UI
        super.checkAnswers();
    }
    
    /**
     * Get hardcoded fallback file list for Lesen Teil 2
     * @returns {Array} - List of file names
     */
    static getFallbackFileList() {
        return [
            'mock_1.json', 
            'mock_2.json', 
            'mock_3.json', 
            'mock_4.json',
            'mock_5.json', 
            'mock_6.json',
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
            // Use absolute path from root
            const filePath = `/data_mocktest/lesen/teil_2/${filename}`;
            
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
            console.error(`Error loading ${filename}:`, error);
            return null; // Return null for failed fetches
        }
    }
}

export default LesenTeil2; 