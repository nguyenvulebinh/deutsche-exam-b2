/**
 * SprachbausteineTeil1 - Implementation for Sprachbausteine Teil 1 test type
 * This extends the base TestEngine class
 */

import TestEngine from '../core/test-engine.js';
import Utils from '../core/utils.js';

class SprachbausteineTeil1 extends TestEngine {
    /**
     * Constructor for SprachbausteineTeil1
     * @param {Object} options - Configuration options
     */
    constructor(options = {}) {
        // Set default options specific to Sprachbausteine Teil 1
        const defaultOptions = {
            testDataDir: '/data_mocktest/sprachbausteine/teil_1',  // Use absolute path from root
            testType: 'Sprachbausteine Teil 1',
            defaultTestData: {
                "thema": "Muster-Thema",
                "textinhalt": "Dies ist ein Beispieltext mit Lücken __1__, __2__, __3__, __4__, __5__, __6__.",
                "options": [
                    { "id": "a", "content": "OPTION_A" },
                    { "id": "b", "content": "OPTION_B" },
                    { "id": "c", "content": "OPTION_C" },
                    { "id": "d", "content": "OPTION_D" },
                    { "id": "e", "content": "OPTION_E" },
                    { "id": "f", "content": "OPTION_F" },
                    { "id": "g", "content": "OPTION_G" },
                    { "id": "h", "content": "OPTION_H" },
                    { "id": "i", "content": "OPTION_I" },
                    { "id": "j", "content": "OPTION_J" }
                ],
                "loesung": [
                    { "blank": "1", "option_id": "a" },
                    { "blank": "2", "option_id": "b" },
                    { "blank": "3", "option_id": "c" },
                    { "blank": "4", "option_id": "d" },
                    { "blank": "5", "option_id": "e" },
                    { "blank": "6", "option_id": "f" }
                ]
            }
        };
        
        // Merge with provided options
        super({...defaultOptions, ...options});
        
        // Additional properties specific to Sprachbausteine Teil 1
        this.optionsTable = null;
        this.answerGrid = null;
        this.textContent = null;
        this.marked = null;
        
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
                console.warn('SprachbausteineTeil1: No tests could be loaded, using default test');
                this.loadDefaultTest();
            }
            
            // Set up event listeners
            this.setupEventListeners();
            
            // Hide loading screen
            Utils.hideElement(this.elements.loading);
            Utils.showElement(this.elements.testContent);
        } catch (error) {
            console.error('SprachbausteineTeil1: Error initializing test engine:', error);
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
                const manifestUrl = '/data_mocktest/sprachbausteine/teil_1_manifest.json';  // Use absolute path from root
                
                const response = await fetch(manifestUrl);
                
                if (response.ok) {
                    const manifest = await response.json();
                    testFileList = manifest.files || [];
                } else {
                    // Fall back to the parent implementation
                    return super.loadAllTestData();
                }
            } catch (error) {
                console.warn('SprachbausteineTeil1: Error loading teil_1 manifest directly:', error);
                // Fall back to the parent implementation
                return super.loadAllTestData();
            }
            
            if (!testFileList || testFileList.length === 0) {
                console.warn('SprachbausteineTeil1: No test files found in manifest, falling back to default method');
                return super.loadAllTestData();
            }
            
            // Fetch each test file and add to the allTestData array
            const fetchPromises = testFileList.map(file => this.fetchTestData(file));
            const testsData = await Promise.all(fetchPromises);
            
            // Filter out any null results (failed fetches)
            this.allTestData = testsData.filter(test => test !== null);
            
            // If no tests were loaded successfully, use the default test
            if (this.allTestData.length === 0) {
                console.warn('SprachbausteineTeil1: No tests could be loaded from external files');
            }
        } catch (error) {
            console.error('SprachbausteineTeil1: Error loading test data:', error);
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
            const filePath = `/data_mocktest/sprachbausteine/teil_1/${filename}`;
            
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
            console.error(`SprachbausteineTeil1: Error loading ${filename}:`, error);
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
        
        // Set up additional elements specific to Sprachbausteine Teil 1
        this.elements.thema = document.getElementById('thema');
        this.elements.textContent = document.getElementById('text-content');
        this.elements.optionsTable = document.getElementById('options-table');
        this.elements.answerGrid = document.getElementById('answer-grid');
        
        // Add references to buttons
        this.elements.finishBtn = document.getElementById('finish-btn');
        this.elements.newTestBtn = document.getElementById('new-test-btn');
        
        // Add reference to the results section
        this.elements.results = document.getElementById('results');
        this.elements.score = document.getElementById('score');
    }
    
    /**
     * Validate that test data has the required structure for Sprachbausteine Teil 1
     * @override
     * @param {Object} data - Test data to validate
     * @returns {boolean} - Whether the data is valid
     */
    validateTestData(data) {
        return (
            data && 
            typeof data.thema === 'string' &&
            typeof data.textinhalt === 'string' &&
            Array.isArray(data.options) &&
            data.options.length >= 10 &&
            Array.isArray(data.loesung) &&
            data.loesung.length >= 6
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
        
        // Display the thema
        this.elements.thema.textContent = test.thema;
        
        // Process and display the text with blanks
        this.displayText(test.textinhalt);
        
        // Display the options in a table
        this.displayOptions(test.options);
        
        // Create the answer grid for user input
        this.createAnswerGrid(test.loesung);
    }
    
    /**
     * Display the text with blanks, using markdown parsing
     * @param {string} text - Text content with placeholders for blanks
     */
    displayText(text) {
        // Convert multiple consecutive newlines to double newlines (markdown paragraph break)
        // Then remove any remaining single newlines that aren't part of paragraph breaks
        let cleanedText = text.replace(/\n{3,}/g, '\n\n')  // Convert 3+ newlines to 2
                             .replace(/([^\n])\n([^\n])/g, '$1 $2');  // Replace single newlines with spaces
                             
        // Process text to create uniform blanks that don't affect surrounding text
        const processedText = cleanedText.replace(/__(\d+)__/g, '<span class="blank" data-blank-id="$1">$1</span>');
        
        // Parse the processed text as markdown
        const htmlContent = this.marked.parse(processedText);
        
        // Set the HTML content
        this.elements.textContent.innerHTML = htmlContent;
    }
    
    /**
     * Display the options in a 3-column table
     * @param {Array<Object>} options - Array of option objects with id and content
     */
    displayOptions(options) {
        // Clear the options table
        this.elements.optionsTable.innerHTML = '';
        
        // Calculate how many rows we need (ceil of options.length / 3)
        const rowCount = Math.ceil(options.length / 3);
        
        // Create the table rows and cells
        for (let row = 0; row < rowCount; row++) {
            const tr = document.createElement('tr');
            
            for (let col = 0; col < 3; col++) {
                const optionIndex = row * 3 + col;
                const td = document.createElement('td');
                
                // Add option content if available
                if (optionIndex < options.length) {
                    const option = options[optionIndex];
                    
                    const optionId = document.createElement('span');
                    optionId.className = 'option-id';
                    optionId.textContent = option.id + ': ';
                    
                    td.appendChild(optionId);
                    td.appendChild(document.createTextNode(option.content));
                }
                
                tr.appendChild(td);
            }
            
            this.elements.optionsTable.appendChild(tr);
        }
    }
    
    /**
     * Create the answer grid for user input
     * @param {Array<Object>} solutions - Array of solution objects
     */
    createAnswerGrid(solutions) {
        // Clear the answer grid
        this.elements.answerGrid.innerHTML = '';
        
        // We don't need to set gridTemplateColumns here, it's set in CSS via the sprachbausteine-grid class
        
        // Add header row with options (a-j)
        this.elements.answerGrid.appendChild(this.createGridCell('', 'grid-header'));
        for (let i = 0; i < 10; i++) {
            const optionId = String.fromCharCode(97 + i); // a-j
            this.elements.answerGrid.appendChild(this.createGridCell(optionId, 'grid-header'));
        }
        
        // Create a row for each blank
        solutions.forEach(solution => {
            const blankId = solution.blank;
            
            // Add the row header (blank number)
            this.elements.answerGrid.appendChild(this.createGridCell(blankId, 'grid-header'));
            
            // Add cells for each option (a-j)
            for (let i = 0; i < 10; i++) {
                const optionId = String.fromCharCode(97 + i); // a-j
                const cell = Utils.createElement('div', {
                    className: 'grid-cell',
                    dataset: {
                        blank: blankId,
                        option: optionId
                    },
                    onClick: this.handleCellClick.bind(this)
                });
                this.elements.answerGrid.appendChild(cell);
            }
        });
    }
    
    /**
     * Helper function to create grid cells
     * @param {string} text - Text content
     * @param {string} className - CSS class
     * @returns {HTMLElement} - The created cell
     */
    createGridCell(text, className) {
        return Utils.createElement('div', {
            className: className,
            textContent: text
        });
    }
    
    /**
     * Handle click on a cell in the answer grid
     * @param {Event} event - Click event
     */
    handleCellClick(event) {
        const blank = event.target.dataset.blank;
        const option = event.target.dataset.option;
        
        // Clear previous selection for this blank
        document.querySelectorAll(`.grid-cell[data-blank="${blank}"]`).forEach(cell => {
            cell.classList.remove('selected');
        });
        
        // Select this cell
        event.target.classList.add('selected');
        
        // Store the answer
        this.userAnswers[blank] = option;
    }
    
    /**
     * Set up event listeners for the test
     * @override
     */
    setupEventListeners() {
        // Instead of calling the parent method, we'll set up our listeners directly
        // to avoid duplicate event listeners on the new test button
        
        // Add event listener for the finish button
        if (this.elements.finishBtn) {
            // Remove any existing listeners first
            const newFinishBtn = this.elements.finishBtn.cloneNode(true);
            this.elements.finishBtn.parentNode.replaceChild(newFinishBtn, this.elements.finishBtn);
            this.elements.finishBtn = newFinishBtn;
            
            // Add the event listener
            this.elements.finishBtn.addEventListener('click', () => this.checkAnswers());
        }
        
        // Add event listener for the new test button
        if (this.elements.newTestBtn) {
            // Remove any existing listeners first
            const newButton = this.elements.newTestBtn.cloneNode(true);
            this.elements.newTestBtn.parentNode.replaceChild(newButton, this.elements.newTestBtn);
            this.elements.newTestBtn = newButton;
            
            // Add the event listener
            this.elements.newTestBtn.addEventListener('click', () => this.loadRandomTest());
        }
    }
    
    /**
     * Check the user's answers against the correct answers
     * @override
     */
    checkAnswers() {
        let correctCount = 0;
        const totalCount = this.currentTest.loesung.length;
        
        // Create a solutions lookup for easy checking
        const solutionsMap = {};
        this.currentTest.loesung.forEach(solution => {
            solutionsMap[solution.blank] = solution.option_id;
        });
        
        // Check all blanks, whether answered or not
        this.currentTest.loesung.forEach(solution => {
            const blankId = solution.blank;
            const correctOption = solution.option_id;
            const userOption = this.userAnswers[blankId]; // May be undefined if no answer given
            
            // Find the corresponding cells
            const correctCell = document.querySelector(`.grid-cell[data-blank="${blankId}"][data-option="${correctOption}"]`);
            
            if (userOption) {
                // User provided an answer for this blank
                const selectedCell = document.querySelector(`.grid-cell[data-blank="${blankId}"][data-option="${userOption}"]`);
                
                if (selectedCell) {
                    selectedCell.classList.remove('selected');
                    
                    if (userOption === correctOption) {
                        // Correct answer
                        selectedCell.classList.add('correct');
                        correctCount++;
                    } else {
                        // Incorrect answer
                        selectedCell.classList.add('incorrect');
                        
                        // Always highlight the correct answer
                        if (correctCell) {
                            correctCell.classList.add('correct');
                        }
                    }
                }
            } else {
                // No answer provided - just highlight the correct answer
                if (correctCell) {
                    correctCell.classList.add('correct');
                }
            }
        });
        
        // Calculate percentage
        const percentage = Math.round((correctCount / totalCount) * 100);
        
        // Show score with format matching lesen_teil_1.html
        this.elements.score.textContent = `${correctCount} von ${totalCount} Punkten (${percentage}%)`;
        
        // Show results 
        if (this.elements.results) {
            Utils.showElement(this.elements.results);
        }
        
        // Hide finish button 
        if (this.elements.finishBtn) {
            Utils.hideElement(this.elements.finishBtn);
        }
        
        // Show new test button
        if (this.elements.newTestBtn) {
            Utils.showElement(this.elements.newTestBtn);
        }
        
        // Note: We're not calling super.checkAnswers() anymore since we're handling the UI changes ourselves
    }
    
    /**
     * Get fallback file list for testing
     * @returns {Array<string>} - List of fallback test files
     */
    static getFallbackFileList() {
        return [
            'mock_1.json',
            'mock_2.json',
            'mock_3.json',
            'mock_4.json',
            'mock_5.json'
        ];
    }

    /**
     * Load a random test from the available tests
     * @override
     */
    loadRandomTest() {
        // Select a random test
        const randomIndex = Math.floor(Math.random() * this.allTestData.length);
        const randomTest = this.allTestData[randomIndex];
        
        // Clear previous user answers
        this.userAnswers = {};
        
        // Display the selected test
        this.displayTest(randomTest);
        
        // Log which test file is being used
        if (randomTest._sourceFilename) {
            console.log(`📝 Loaded task: ${randomTest._sourceFilename} (Sprachbausteine Teil 1)`);
        }
        
        // Reset UI elements for a new test
        if (this.elements.finishBtn) {
            Utils.showElement(this.elements.finishBtn);
        }
        if (this.elements.newTestBtn) {
            Utils.hideElement(this.elements.newTestBtn);
        }
        if (this.elements.results) {
            Utils.hideElement(this.elements.results);
        }
    }

    /**
     * Load the default test data
     * @override
     */
    loadDefaultTest() {
        // Clear previous user answers
        this.userAnswers = {};
        
        // Display the default test
        this.displayTest(this.config.defaultTestData);
        
        // Log that we're using the default test
        console.log('📝 Loaded default task (Sprachbausteine Teil 1)');
        
        // Reset UI elements for a new test
        if (this.elements.finishBtn) {
            Utils.showElement(this.elements.finishBtn);
        }
        if (this.elements.newTestBtn) {
            Utils.hideElement(this.elements.newTestBtn);
        }
        if (this.elements.results) {
            Utils.hideElement(this.elements.results);
        }
    }
}

export default SprachbausteineTeil1; 