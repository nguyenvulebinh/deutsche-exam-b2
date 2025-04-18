/**
 * Teil3Part - Implementation for Teil 3 of the Lesen exam
 */

import BasePart from './BasePart.js';
import Utils from '../../core/utils.js';
import LesenTeil3 from '../../test-types/lesen-teil-3.js';

class Teil3Part extends BasePart {
    /**
     * Constructor for Teil3Part
     * @param {Object} options - Configuration options
     */
    constructor(options = {}) {
        super(options);
        this.engine = null;
    }

    /**
     * Initialize the part
     * @returns {Promise<Object>} - Test data and solutions
     */
    async initialize() {
        try {
            // Create test engine
            this.engine = new LesenTeil3({
                testDataDir: '/data_mocktest/lesen/teil_3'
            });
            
            // Override DOM references to use our custom elements
            this.engine.elements = {
                ...this.engine.elements,
                instructions: this.elements.instructions,
                peopleContainer: this.elements.peopleContainer,
                themaTitle: this.elements.themaTitle,
                postsContainer: this.elements.postsContainer,
                answerGrid: this.elements.answerGrid
            };
            
            // Load all test data
            await this.engine.loadAllTestData();
            
            // Select a random test
            const randomIndex = Math.floor(Math.random() * this.engine.allTestData.length);
            this.testData = this.engine.allTestData[randomIndex] || this.engine.config.defaultTestData;
            
            // Save the solutions
            this.solutions = this.testData.solutions || {};
            
            return {
                testData: this.testData,
                solutions: this.solutions
            };
        } catch (error) {
            console.error('Error initializing Teil 3:', error);
            throw error;
        }
    }

    /**
     * Render the test content
     */
    render() {
        // Create a deep copy of the test data to avoid modifying the original
        const testCopy = JSON.parse(JSON.stringify(this.testData));
                
        // Display the test using our direct methods
        this.engine.userAnswers = {};  // Reset user answers
        this.updateEngineWithShuffledData(testCopy);
    }
    
    /**
     * Update the engine with our shuffled data instead of letting it shuffle again
     * @param {Object} testData - The already shuffled test data
     */
    updateEngineWithShuffledData(testData) {
        // Update instructions if available
        if (this.elements.instructions && testData.instructions) {
            this.elements.instructions.textContent = testData.instructions;
        }
        
        // Update thema title if available
        if (this.elements.themaTitle && testData.thema) {
            this.elements.themaTitle.textContent = `Thema: ${testData.thema}`;
        }
        
        // Create the answer grid
        this.createAnswerGrid(testData);
        
        // Display people and posts
        this.displayPeople(testData.people_seeking_info);
        this.displayPosts(testData.posts);
        
        // Store the shuffled data in the engine
        this.engine.currentTest = testData;
    }
    
    /**
     * Create the answer grid for the test
     * @param {Object} test - Test data 
     */
    createAnswerGrid(test) {
        const answerGrid = this.elements.answerGrid;
        
        // Clear existing grid
        answerGrid.innerHTML = '';
        
        // Use the same grid layout as in LesenTeil3
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
        // If in review mode, don't allow changes
        if (this.isReviewMode) return;
        
        const cell = event.currentTarget;
        const person = cell.dataset.person;
        const column = cell.dataset.column;
        
        // Clear selection in this row
        const rowCells = document.querySelectorAll(`.grid-cell[data-person="${person}"]`);
        rowCells.forEach(cell => cell.classList.remove('selected'));
        
        // Select this cell
        cell.classList.add('selected');
        
        // Record the answer in both our local userAnswers and the engine's
        this.userAnswers[person] = column;
        if (this.engine) {
            this.engine.userAnswers = {...this.userAnswers};
        }
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Add click event listeners to answer grid cells
        const gridCells = this.elements.answerGrid.querySelectorAll('.grid-cell');
        gridCells.forEach(cell => {
            cell.addEventListener('click', (event) => {
                // If in review mode, don't allow changes
                if (this.isReviewMode) return;
                
                // Call handleCellClick from the engine if it exists
                if (typeof this.engine.handleCellClick === 'function') {
                    this.engine.handleCellClick(event);
                }
                
                // Save the answers
                this.userAnswers = {...this.engine.userAnswers};
            });
        });
    }

    /**
     * Mark answers as correct or incorrect
     */
    markAnswers() {
        // Find all grid cells
        const gridCells = this.elements.answerGrid.querySelectorAll('.grid-cell');
        
        // Remove previous styling
        gridCells.forEach(cell => {
            cell.classList.remove('selected', 'correct', 'incorrect');
        });
        
        // First, mark all correct answers (this ensures they're visible even if no answer provided)
        for (const personId in this.solutions) {
            if (this.solutions.hasOwnProperty(personId)) {
                const correctColumnId = this.solutions[personId];
                const correctCell = this.elements.answerGrid.querySelector(`.grid-cell[data-person="${personId}"][data-column="${correctColumnId}"]`);
                
                if (correctCell) {
                    correctCell.classList.add('correct');
                }
            }
        }
        
        // Then mark user answers (which may override correct marking with incorrect marking)
        for (const personId in this.userAnswers) {
            if (this.userAnswers.hasOwnProperty(personId)) {
                const columnId = this.userAnswers[personId];
                const correctColumnId = this.solutions[personId];
                
                // If user made a selection for this person
                if (columnId) {
                    const selectedCell = this.elements.answerGrid.querySelector(`.grid-cell[data-person="${personId}"][data-column="${columnId}"]`);
                    
                    if (selectedCell) {
                        // Check if the answer is correct
                        const isCorrect = correctColumnId === columnId;
                        
                        if (isCorrect) {
                            // Already marked as correct in the first loop
                        } else {
                            // Mark as incorrect (and make sure the correct answer is still marked)
                            selectedCell.classList.add('incorrect');
                        }
                    }
                }
            }
        }
    }
}

export default Teil3Part; 