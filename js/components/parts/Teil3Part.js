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
        // Display the test using the engine
        this.engine.displayTest(this.testData);
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