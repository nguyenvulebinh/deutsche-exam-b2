/**
 * LesenTeil3 - Implementation for Lesen Teil 3 test type
 * This extends the base TestEngine class
 */

import TestEngine from '../core/test-engine.js';
import Utils from '../core/utils.js';

class LesenTeil3 extends TestEngine {
    /**
     * Constructor for LesenTeil3
     * @param {Object} options - Configuration options
     */
    constructor(options = {}) {
        // Set default options specific to Lesen Teil 3
        const defaultOptions = {
            testDataDir: '/data_mocktest/lesen/teil_3',  // Use absolute path from root
            testType: 'Lesen Teil 3',
            defaultTestData: {
                "thema": "Tipps für junge Auszubildende",
                "people_seeking_info": [
                    {
                        "id": 1,
                        "name": "Martha",
                        "situation": "Ich habe eine einfache Frage. Wie viele Tage Urlaub sollte ein Azubi unter 18 Jahren bekommen? Bei uns in der Firma haben fast alle Azubis unter 18 Jahren 24 Urlaubstage. Sie haben auch eine 40-Stunden-Woche, brauchen aber samstags nicht zu arbeiten. Wie ist das bei euch? Antwortet mal fleißig, wenn's geht, mit einem Link zum Gesetz."
                    },
                    {
                        "id": 2,
                        "name": "Tomas",
                        "situation": "Hallo Leute, unser Chef möchte, dass wir auch am Samstag arbeiten. Wir sind noch in der Ausbildung. Wir haben gehört, dass Auszubildende am Samstag nicht arbeiten dürfen. Kann jemand schnell Auskunft geben?"
                    },
                    {
                        "id": 3,
                        "name": "Egle",
                        "situation": "Eine Frage an alle. Hat jemand hier schon Erfahrungen gemacht? Ich hatte vor Monaten Urlaub beantragt, dann wurde ich zwei Tage vorher krank. Ich musste eine Woche zu Hause bleiben. Danach konnte ich dann zu meiner Familie nach Litauen in Urlaub fahren. Mein Chef sagt nun, dass ich Pech hatte, weil ich im Urlaub krank war. Die Krankentage hat er mir als Urlaubstage abgezogen. Eine Kollegin sagt, ich soll mich beschweren. Was soll ich tun?"
                    },
                    {
                        "id": 4,
                        "name": "Paul",
                        "situation": "Bei uns erhalten junge Leute unter 18 Jahren in der Ausbildung nur 25 Tage Urlaub. Wenn sie über 18 Jahre alt sind, kriegen sie sogar nur 24 Tage. Ich habe gehört, dass viele Betriebe einen Betriebsrat und eine Betriebsvereinbarung dazu haben. Was können wir hier machen, um mehr Informationen zu bekommen?"
                    }
                ],
                "posts": [
                    {
                        "id": "a",
                        "author": "Suszanna",
                        "timestamp": "vor 3 Stunden",
                        "content": "Ich finde es total ungerecht, dass minderjährige Azubis mehr Urlaub bekommen als volljährige. Man sagt doch immer, jüngere Menschen seien belastbarer als ältere. Bei uns ist das aber auch so."
                    },
                    {
                        "id": "b",
                        "author": "Hanna",
                        "timestamp": "vor 56 Minuten",
                        "content": "Also, grundsätzlich ist der Samstag ein ganz normaler Werktag, ihr dürft da also auch arbeiten. Geschützt sind allerdings minderjährige Auszubildende, die nur dann samstags arbeiten dürfen, wenn sie dafür in derselben oder der darauffolgenden Woche einen Tag frei machen dürfen."
                    },
                    {
                        "id": "c",
                        "author": "Veronica",
                        "timestamp": "vor 9 Stunden",
                        "content": "Krankheitszeiten haben keinen Einfluss auf den Urlaubsanspruch. Die Fehltage dürfen nicht auf den Urlaubsanspruch angerechnet werden. Im Gegenteil: Erkrankt der Azubi im Urlaub, werden die Krankentage nicht auf den Urlaub angerechnet, wenn er eine Krankmeldung vorlegt."
                    },
                    {
                        "id": "d",
                        "author": "Franziska",
                        "timestamp": "vor 42 Minuten",
                        "content": "Urlaub ist Urlaub und Krankheit ist Krankheit. Wenn du krank bist, musst du das in der Berufsschule melden. Am besten, du reichst das Attest vom Arzt dort ein. Mach das aber möglichst sofort, sonst fehlen dir eventuell einige Tage in deiner Berufsschule."
                    },
                    {
                        "id": "e",
                        "author": "Chiara",
                        "timestamp": "vor 3 Stunden",
                        "content": "Samstags arbeiten ist immer blöd. Ich mache das auch nicht gerne. Aber manchmal muss es eben sein. Viele ältere Kollegen müssen auf jeden Fall Samstag ran. Ich würde das auch unbedingt machen, das macht einen guten Eindruck!"
                    },
                    {
                        "id": "f",
                        "author": "Louis",
                        "timestamp": "vor 49 Minuten",
                        "content": "Das kann eigentlich nicht sein, denn das Gesetz schreibt vor, dass minderjährige Auszubildende mindestens 25 Werktage Urlaub haben müssen. Die wöchentliche Arbeitszeit beträgt für Minderjährige maximal 40 Stunden, Azubis über 18 dürfen sogar 48 Stunden pro Woche arbeiten, allerdings verteilt auf 6 Tage. Den Link dazu findest du unter www.azubi-azubine.de."
                    }
                ],
                "solutions": {
                    "1": "f",
                    "2": "b",
                    "3": "c",
                    "4": "x"
                }
            }
        };
        
        // Merge with provided options
        super({...defaultOptions, ...options});
        
        // Additional properties specific to Lesen Teil 3
        this.peopleContainer = null;
        this.postsContainer = null;
        this.answerGrid = null;
        this.originalPeopleOrder = []; // Store original order of people
        this.shuffledPeopleMap = {}; // Map original IDs to shuffled IDs
    }
    
    /**
     * Initialize the test engine
     * @returns {Promise<void>}
     */
    async initialize() {
        try {
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
                console.warn('LesenTeil3: No tests could be loaded, using default test');
                this.loadDefaultTest();
            }
            
            // Set up event listeners
            this.setupEventListeners();
            
            // Hide loading screen
            Utils.hideElement(this.elements.loading);
            Utils.showElement(this.elements.testContent);
        } catch (error) {
            console.error('LesenTeil3: Error initializing test engine:', error);
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
                const manifestUrl = '/data_mocktest/lesen/teil_3_manifest.json';  // Use absolute path from root
                
                const response = await fetch(manifestUrl);
                
                if (response.ok) {
                    const manifest = await response.json();
                    testFileList = manifest.files || [];
                } else {
                    // Fall back to the parent implementation
                    return super.loadAllTestData();
                }
            } catch (error) {
                console.warn('LesenTeil3: Error loading teil_3 manifest directly:', error);
                // Fall back to the parent implementation
                return super.loadAllTestData();
            }
            
            if (!testFileList || testFileList.length === 0) {
                console.warn('LesenTeil3: No test files found in manifest, falling back to default method');
                return super.loadAllTestData();
            }
            
            // Fetch each test file and add to the allTestData array
            const fetchPromises = testFileList.map(file => this.fetchTestData(file));
            const testsData = await Promise.all(fetchPromises);
            
            // Filter out any null results (failed fetches)
            this.allTestData = testsData.filter(test => test !== null);
            
            // If no tests were loaded successfully, use the default test
            if (this.allTestData.length === 0) {
                console.warn('LesenTeil3: No tests could be loaded from external files');
            }
        } catch (error) {
            console.error('LesenTeil3: Error loading test data:', error);
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
            const filePath = `/data_mocktest/lesen/teil_3/${filename}`;
            
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
            console.error(`LesenTeil3: Error loading ${filename}:`, error);
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
        
        // Set up additional elements specific to Lesen Teil 3
        this.elements.peopleContainer = document.getElementById('people-container');
        this.elements.postsContainer = document.getElementById('posts-container');
        this.elements.themaTitle = document.getElementById('thema-title');
        this.elements.answerGrid = document.querySelector('.answer-grid');
    }
    
    /**
     * Validate that test data has the required structure for Lesen Teil 3
     * @override
     * @param {Object} data - Test data to validate
     * @returns {boolean} - Whether the data is valid
     */
    validateTestData(data) {
        return (
            data && 
            data.thema && 
            Array.isArray(data.people_seeking_info) && 
            data.people_seeking_info.length > 0 &&
            Array.isArray(data.posts) && 
            data.posts.length > 0 &&
            data.solutions && 
            Object.keys(data.solutions).length > 0
        );
    }
    
    /**
     * Display the Lesen Teil 3 test
     * @override
     * @param {Object} test - Test data to display
     */
    displayTest(test) {
        // Create a deep copy of the test to avoid modifying the original
        const testCopy = JSON.parse(JSON.stringify(test));
                
        // Call the parent method to handle basic display
        super.displayTest(testCopy);
        
        // Clear previous answers
        this.userAnswers = {};
        
        // Display thema above posts container
        if (this.elements.themaTitle) {
            this.elements.themaTitle.textContent = `Thema: ${testCopy.thema}`;
        }
        
        // Create grid rows
        this.createAnswerGrid(testCopy);
        
        // Display people seeking info
        this.displayPeople(testCopy.people_seeking_info);
        
        // Display posts
        this.displayPosts(testCopy.posts);
    }
    
    /**
     * Create the answer grid for the test
     * @param {Object} test - Test data 
     */
    createAnswerGrid(test) {
        const answerGrid = this.elements.answerGrid;
        
        // Clear existing grid
        answerGrid.innerHTML = '';
        
        // Use the same grid layout as Teil 1 but with teil-3 variant for 7 columns
        answerGrid.className = 'answer-grid teil-3';
        
        // Column IDs (a, b, c, d, e, f, x)
        const columnIds = ['a', 'b', 'c', 'd', 'e', 'f', 'x'];
        
        // Add top-left empty cell
        answerGrid.appendChild(this.createGridCell('', 'grid-header'));
        
        // Add column headers (a-f, x)
        columnIds.forEach(id => {
            answerGrid.appendChild(this.createGridCell(id, 'grid-header'));
        });
        
        // Add rows for each person
        const people = test.people_seeking_info;
        people.forEach(person => {
            // Add row header with person ID
            answerGrid.appendChild(this.createGridCell(person.id, 'grid-header'));
            
            // Add selectable cells for each column
            columnIds.forEach(columnId => {
                const cell = this.createGridCell('', 'grid-cell');
                cell.dataset.person = person.id;
                cell.dataset.column = columnId;
                cell.addEventListener('click', (e) => this.handleCellClick(e));
                answerGrid.appendChild(cell);
            });
        });
    }
    
    /**
     * Create a grid cell element
     * @param {string} text - Text content of the cell
     * @param {string} className - CSS class for the cell
     * @returns {HTMLElement} - Grid cell element
     */
    createGridCell(text, className) {
        const cell = document.createElement('div');
        cell.className = className;
        cell.textContent = text;
        return cell;
    }
    
    /**
     * Display people seeking information
     * @param {Array} people - People data
     */
    displayPeople(people) {
        const container = this.elements.peopleContainer;
        container.innerHTML = '';
        
        people.forEach(person => {
            const personElement = document.createElement('div');
            personElement.className = 'person';
            
            const header = document.createElement('h3');
            header.textContent = `${person.id}. ${person.name}`;
            
            const content = document.createElement('p');
            content.textContent = person.situation;
            
            personElement.appendChild(header);
            personElement.appendChild(content);
            container.appendChild(personElement);
        });
    }
    
    /**
     * Display posts
     * @param {Array} posts - Posts data
     */
    displayPosts(posts) {
        const container = this.elements.postsContainer;
        container.innerHTML = '';
        
        posts.forEach(post => {
            const postElement = document.createElement('div');
            postElement.className = 'post';
            
            const header = document.createElement('h3');
            header.textContent = `${post.id}. ${post.author}`;
            
            const timestamp = document.createElement('div');
            timestamp.className = 'timestamp';
            timestamp.textContent = post.timestamp;
            
            const content = document.createElement('p');
            content.textContent = post.content;
            
            postElement.appendChild(header);
            postElement.appendChild(timestamp);
            postElement.appendChild(content);
            container.appendChild(postElement);
        });
    }
    
    /**
     * Handle click on answer grid cell
     * @param {Event} event - Click event
     */
    handleCellClick(event) {
        const cell = event.currentTarget;
        const person = cell.dataset.person;
        const column = cell.dataset.column;
        
        // Clear selection in this row
        const rowCells = document.querySelectorAll(`.grid-cell[data-person="${person}"]`);
        rowCells.forEach(cell => cell.classList.remove('selected'));
        
        // Select this cell
        cell.classList.add('selected');
        
        // Record the answer
        this.userAnswers[person] = column;
    }
    
    /**
     * Check user answers against solutions
     * @override
     */
    checkAnswers() {
        if (!this.currentTest || !this.currentTest.solutions) {
            console.error('LesenTeil3: No test loaded or no solutions available');
            return;
        }
        
        const solutions = this.currentTest.solutions;
        let correctCount = 0;
        const totalQuestions = Object.keys(solutions).length;
        
        // Check each answer
        Object.keys(solutions).forEach(person => {
            const correctAnswer = solutions[person];
            const userAnswer = this.userAnswers[person];
            
            // If the user answered correctly, increment count
            if (userAnswer === correctAnswer) {
                correctCount++;
            }
            
            // Find the cells
            const userCell = userAnswer ? document.querySelector(`.grid-cell[data-person="${person}"][data-column="${userAnswer}"]`) : null;
            const correctCell = document.querySelector(`.grid-cell[data-person="${person}"][data-column="${correctAnswer}"]`);
            
            // Mark user's answer
            if (userCell) {
                userCell.classList.remove('selected');
                if (userAnswer === correctAnswer) {
                    // Correct answer
                    userCell.classList.add('correct');
                } else {
                    // Incorrect answer
                    userCell.classList.add('incorrect');
                }
            }
            
            // Highlight correct answer if user was wrong or didn't answer
            if (!userAnswer || userAnswer !== correctAnswer) {
                if (correctCell) {
                    correctCell.classList.add('correct');
                }
            }
        });
        
        // Calculate and display score
        const score = Math.round((correctCount / totalQuestions) * 100);
        this.elements.score.textContent = `Sie haben ${correctCount} von ${totalQuestions} Fragen richtig beantwortet (${score}%).`;
        
        // Show results and new test button
        Utils.showElement(this.elements.results);
        Utils.hideElement(this.elements.finishButton);
        Utils.showElement(this.elements.newTestButton);
        
        // Log to console for debugging
        console.log('Check results:', {
            solutions,
            userAnswers: this.userAnswers,
            correctCount,
            totalQuestions,
            shuffledPeopleMap: this.shuffledPeopleMap,
            originalPeopleOrder: this.originalPeopleOrder
        });
    }
    
    /**
     * Provide a fallback list of files to use when directory listing fails
     * @static
     * @returns {Array} - List of filenames
     */
    static getFallbackFileList() {
        return [
            "mock_1.json",
            "mock_2.json",
            "mock_3.json",
            "mock_4.json",
            "mock_5.json",
            "mock_6.json"
        ];
    }
}

// Export the LesenTeil3 class
export default LesenTeil3; 