/**
 * Teil1Part - Implementation for Teil 1 of the Lesen exam
 */

import BasePart from './BasePart.js';
import Utils from '../../core/utils.js';
import LesenTeil1 from '../../test-types/lesen-teil-1.js';

class Teil1Part extends BasePart {
    /**
     * Constructor for Teil1Part
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
            this.engine = new LesenTeil1({
                testDataDir: '/data_mocktest/lesen/teil_1'
            });
            
            // Override DOM references to use our custom elements
            this.engine.elements = {
                ...this.engine.elements,
                instructions: this.elements.instructions,
                peopleContainer: this.elements.peopleContainer,
                articlesContainer: this.elements.articlesContainer,
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
            console.error('Error initializing Teil 1:', error);
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
                const correctArticleId = this.solutions[personId];
                const correctCell = this.elements.answerGrid.querySelector(`.grid-cell[data-person="${personId}"][data-article="${correctArticleId}"]`);
                
                if (correctCell) {
                    correctCell.classList.add('correct');
                }
            }
        }
        
        // Then mark user answers (which may override correct marking with incorrect marking)
        for (const personId in this.userAnswers) {
            if (this.userAnswers.hasOwnProperty(personId)) {
                const articleId = this.userAnswers[personId];
                const correctArticleId = this.solutions[personId];
                
                // If user made a selection for this person
                if (articleId) {
                    const selectedCell = this.elements.answerGrid.querySelector(`.grid-cell[data-person="${personId}"][data-article="${articleId}"]`);
                    
                    if (selectedCell) {
                        // Check if the answer is correct
                        const isCorrect = correctArticleId === articleId;
                        
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

export default Teil1Part; 