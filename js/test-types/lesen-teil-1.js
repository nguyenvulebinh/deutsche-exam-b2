/**
 * LesenTeil1 - Implementation for Lesen Teil 1 test type
 * This extends the base TestEngine class
 */

import TestEngine from '../core/test-engine.js';
import Utils from '../core/utils.js';

class LesenTeil1 extends TestEngine {
    /**
     * Constructor for LesenTeil1
     * @param {Object} options - Configuration options
     */
    constructor(options = {}) {
        // Set default options specific to Lesen Teil 1
        const defaultOptions = {
            testDataDir: '/data_mocktest/lesen/teil_1',  // Use absolute path from root
            testType: 'Lesen Teil 1',
            defaultTestData: {
                "exercise_type": "TELC B2",
                "skill": "Lesen",
                "part": "Teil 1",
                "instructions": "Sie lesen online in einer Wirtschaftszeitung und möchten Ihren Freunden einige Artikel schicken.\nEntscheiden Sie, welcher Artikel a–h zu welcher Person 1–5 passt.\nMarkieren Sie Ihre Lösungen auf dem Antwortbogen.",
                "people": [
                    { "id": 1, "description": "Karolina überlegt, sich selbständig zu machen." },
                    { "id": 2, "description": "Lena fragt sich, ob sie ihre Vorgesetzte duzen kann." },
                    { "id": 3, "description": "Andrey hat Probleme mit dem steigenden Arbeitsdruck." },
                    { "id": 4, "description": "Sarah interessiert sich für eine Tätigkeit im Ausland." },
                    { "id": 5, "description": "Lukas möchte Beruf und Familie besser verbinden." }
                ],
                "articles": [
                    { "id": "a", "title": "Es ist alles zu viel!", "description": "Ohne Pause durchgearbeitet, noch nichts gegessen und dann muss man auch noch ängstliche Patienten, besorgte Eltern oder unzufriedene Klienten beruhigen. Eine Krankenhausärztin, ein Lehrer und ein Sozialarbeiter berichten über den alltäglichen Wahnsinn und wie sie damit klarkommen." },
                    { "id": "b", "title": "Kinder oder Arbeit?", "description": "Immer mehr Arbeitnehmerinnen und Arbeitnehmer wollen mehr Zeit für ihre Kinder und ihren Partner / ihre Partnerin haben. Doch der Job lässt oft wenig Spielraum, die Arbeitsbelastung ist hoch. Neue Arbeitszeitmodelle helfen dabei, die richtige Balance zu finden." },
                    { "id": "c", "title": "Siezen oder duzen?", "description": "In der Korrespondenz mit Kundinnen und Kunden sollte man genau hinschauen. Ein saloppes Du kommt nicht bei allen Kundinnen und Kunden gut an, auch wenn Sie in einem modernen Start-up arbeiten. Fingerspitzengefühl ist gefragt." },
                    { "id": "d", "title": "Elternzeit", "description": "In Deutschland gibt es viele Förderungen für Familien. Die Elternzeit wird nicht nur von Frauen, sondern zunehmend auch von Männern gerne genutzt. Kinderwagen schieben statt am Computer sitzen: Wir zeigen Ihnen, wie Sie die Elternzeit richtig beantragen." },
                    { "id": "e", "title": "Das Problem mit der Anrede", "description": "In vielen Firmen sprechen sich die Mitarbeitenden mit Vornamen an und duzen sich. Aber kann man das auch mit dem Chef oder der Chefin machen? Das hat Vor- und Nachteile, die neue Mitarbeitende unbedingt beachten sollten." },
                    { "id": "f", "title": "Ein gutes Konzept ist wichtig", "description": "Wer sein eigener Chef werden will, muss sich gut vorbereiten. Man muss sich von Routinen verabschieden und mit finanzieller Unsicherheit leben können. Der Lohn ist ein selbstbestimmtes Arbeitsleben. Der Ratgeber \"Der große Schritt\" hilft Ihnen, Schwierigkeiten beim Weg in die Selbständigkeit zu meistern." },
                    { "id": "g", "title": "Das Internationale im Lebenslauf", "description": "Madrid, Paris, New York ... Viele Mitarbeitende wollen gerne mal für einen bestimmten Zeitraum in einem anderen Land arbeiten. Das ist nicht nur eine sehr wertvolle Berufserfahrung, sondern beeindruckt auch Arbeitgeber. Diese Tipps helfen bei der Suche nach einer geeigneten Stelle." },
                    { "id": "h", "title": "Ich muss mal raus aus Deutschland!", "description": "Der Urlaubsantrag sorgt immer wieder für Konflikte in Unternehmen. Wer darf wann gehen? Viele wollen den Frühbucherrabatt von Auslandsreisen nutzen und den Urlaub möglichst früh beantragen. Wie sieht das arbeitsrechtlich aus?" }
                ],
                "solutions": {
                    "1": "f",
                    "2": "e",
                    "3": "a",
                    "4": "g",
                    "5": "b"
                }
            }
        };
        
        // Merge with provided options
        super({...defaultOptions, ...options});
        
        // Additional properties specific to Lesen Teil 1
        this.peopleContainer = null;
        this.articlesContainer = null;
        this.answerGrid = null;
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
                console.warn('LesenTeil1: No tests could be loaded, using default test');
                this.loadDefaultTest();
            }
            
            // Set up event listeners
            this.setupEventListeners();
            
            // Hide loading screen
            Utils.hideElement(this.elements.loading);
            Utils.showElement(this.elements.testContent);
        } catch (error) {
            console.error('LesenTeil1: Error initializing test engine:', error);
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
                const manifestUrl = '/data_mocktest/lesen/teil_1_manifest.json';  // Use absolute path from root
                
                const response = await fetch(manifestUrl);
                
                if (response.ok) {
                    const manifest = await response.json();
                    testFileList = manifest.files || [];
                } else {
                    // Fall back to the parent implementation
                    return super.loadAllTestData();
                }
            } catch (error) {
                console.warn('LesenTeil1: Error loading teil_1 manifest directly:', error);
                // Fall back to the parent implementation
                return super.loadAllTestData();
            }
            
            if (!testFileList || testFileList.length === 0) {
                console.warn('LesenTeil1: No test files found in manifest, falling back to default method');
                return super.loadAllTestData();
            }
            
            // Fetch each test file and add to the allTestData array
            const fetchPromises = testFileList.map(file => this.fetchTestData(file));
            const testsData = await Promise.all(fetchPromises);
            
            // Filter out any null results (failed fetches)
            this.allTestData = testsData.filter(test => test !== null);
            
            // If no tests were loaded successfully, use the default test
            if (this.allTestData.length === 0) {
                console.warn('LesenTeil1: No tests could be loaded from external files');
            }
        } catch (error) {
            console.error('LesenTeil1: Error loading test data:', error);
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
            const filePath = `/data_mocktest/lesen/teil_1/${filename}`;
            
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
            console.error(`LesenTeil1: Error loading ${filename}:`, error);
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
        
        // Set up additional elements specific to Lesen Teil 1
        this.elements.peopleContainer = document.getElementById('people-container');
        this.elements.articlesContainer = document.getElementById('articles-container');
        this.elements.answerGrid = document.querySelector('.answer-grid');
    }
    
    /**
     * Validate that test data has the required structure for Lesen Teil 1
     * @override
     * @param {Object} data - Test data to validate
     * @returns {boolean} - Whether the data is valid
     */
    validateTestData(data) {
        return (
            data && 
            data.instructions && 
            Array.isArray(data.people) && 
            data.people.length > 0 &&
            Array.isArray(data.articles) && 
            data.articles.length > 0 &&
            data.solutions && 
            Object.keys(data.solutions).length > 0
        );
    }
    
    /**
     * Display the Lesen Teil 1 test
     * @override
     * @param {Object} test - Test data to display
     */
    displayTest(test) {
        // Call the parent method to handle basic display
        super.displayTest(test);
        
        // Clear previous answers
        this.userAnswers = {};
        
        // Display instructions
        if (this.elements.instructions) {
            this.elements.instructions.textContent = test.instructions;
        }
        
        // Create grid rows
        this.createAnswerGrid(test);
        
        // Display people
        this.displayPeople(test.people);
        
        // Display articles
        this.displayArticles(test.articles);
    }
    
    /**
     * Create the answer grid for the test
     * @param {Object} test - Test data 
     */
    createAnswerGrid(test) {
        const answerGrid = this.elements.answerGrid;
        
        // Clear existing grid
        answerGrid.innerHTML = '';
        
        // Ensure we're using the original grid layout, not the vertical one
        answerGrid.className = 'answer-grid';
        
        // Add headers
        answerGrid.appendChild(this.createGridCell('', 'grid-header'));
        for (let i = 0; i < 8; i++) {
            answerGrid.appendChild(this.createGridCell(String.fromCharCode(97 + i), 'grid-header'));
        }
        
        // Add rows for each person
        test.people.forEach(person => {
            answerGrid.appendChild(this.createGridCell(person.id, 'grid-header'));
            
            // Add cells for each article option
            for (let i = 0; i < 8; i++) {
                const cell = Utils.createElement('div', {
                    className: 'grid-cell',
                    dataset: {
                        person: person.id,
                        article: String.fromCharCode(97 + i) // a, b, c, etc.
                    },
                    onClick: this.handleCellClick.bind(this)
                });
                answerGrid.appendChild(cell);
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
     * Display the people section
     * @param {Array} people - People data
     */
    displayPeople(people) {
        const peopleContainer = this.elements.peopleContainer;
        peopleContainer.innerHTML = '';
        
        people.forEach(person => {
            const personElement = Utils.createElement('div', {
                className: 'person'
            }, `<strong>${person.id}.</strong> ${person.description}`);
            
            peopleContainer.appendChild(personElement);
        });
    }
    
    /**
     * Display the articles section
     * @param {Array} articles - Articles data
     */
    displayArticles(articles) {
        const articlesContainer = this.elements.articlesContainer;
        articlesContainer.innerHTML = '';
        
        // Sort articles by ID (a to h)
        const sortedArticles = [...articles].sort((a, b) => a.id.localeCompare(b.id));
        
        sortedArticles.forEach(article => {
            const articleElement = Utils.createElement('div', {
                className: 'article'
            }, `
                <div class="article-title">${article.id}) ${article.title}</div>
                <div>${article.description}</div>
            `);
            
            articlesContainer.appendChild(articleElement);
        });
    }
    
    /**
     * Handle click on a cell in the answer grid
     * @param {Event} event - Click event
     */
    handleCellClick(event) {
        const person = event.target.dataset.person;
        const article = event.target.dataset.article;
        
        // Clear previous selection for this person
        document.querySelectorAll(`.grid-cell[data-person="${person}"]`).forEach(cell => {
            cell.classList.remove('selected');
        });
        
        // Select this cell
        event.target.classList.add('selected');
        
        // Store the answer
        this.userAnswers[person] = article;
    }
    
    /**
     * Check answers and show results
     * @override
     */
    checkAnswers() {
        let correct = 0;
        const solutions = this.currentTest.solutions;
        
        // Check each answer
        Object.keys(solutions).forEach(person => {
            const correctArticle = solutions[person];
            const userArticle = this.userAnswers[person];
            
            // Find the corresponding cells
            const selectedCell = document.querySelector(`.grid-cell[data-person="${person}"][data-article="${userArticle}"]`);
            const correctCell = document.querySelector(`.grid-cell[data-person="${person}"][data-article="${correctArticle}"]`);
            
            if (selectedCell) {
                selectedCell.classList.remove('selected');
                
                if (userArticle === correctArticle) {
                    // Correct answer
                    selectedCell.classList.add('correct');
                    correct++;
                } else {
                    // Incorrect answer
                    selectedCell.classList.add('incorrect');
                }
            }
            
            // Highlight the correct answer if user was wrong
            if (userArticle !== correctArticle && correctCell) {
                correctCell.classList.add('correct');
            }
        });
        
        // Show score
        const total = Object.keys(solutions).length;
        if (this.elements.score) {
            this.elements.score.textContent = `${correct} von ${total} Punkten (${Math.round((correct / total) * 100)}%)`;
        }
        
        // Call the parent method to update UI
        super.checkAnswers();
    }
    
    /**
     * Get hardcoded fallback file list for Lesen Teil 1
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
            'mocktest_generated_10.json',
            'mocktest_generated_11.json',
            'mocktest_generated_12.json',
            'mocktest_generated_13.json',
            'mocktest_generated_14.json'
        ];
    }
}

export default LesenTeil1; 