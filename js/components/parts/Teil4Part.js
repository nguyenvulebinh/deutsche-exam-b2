/**
 * Teil4Part - Implementation for Teil 4 of the Lesen exam
 */

import BasePart from './BasePart.js';
import Utils from '../../core/utils.js';
import LesenTeil4 from '../../test-types/lesen-teil-4.js';

class Teil4Part extends BasePart {
    /**
     * Constructor for Teil4Part
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
            this.engine = new LesenTeil4({
                testDataDir: '/data_mocktest/lesen/teil_4'
            });
            
            // Override DOM references to use our custom elements
            this.engine.elements = {
                ...this.engine.elements,
                instructions: this.elements.instructions,
                meetingContent: this.elements.meetingContent,
                questionsContainer: this.elements.questionsContainer
            };
            
            // Load all test data
            await this.engine.loadAllTestData();
            
            // Select a random test
            const randomIndex = Math.floor(Math.random() * this.engine.allTestData.length);
            this.testData = this.engine.allTestData[randomIndex] || this.engine.config.defaultTestData;
            
            // Save the solutions
            this.solutions = {};
            
            return {
                testData: this.testData,
                solutions: this.solutions
            };
        } catch (error) {
            console.error('Error initializing Teil 4:', error);
            throw error;
        }
    }

    /**
     * Render the test content
     */
    render() {
        // Set instructions if not already set
        if (this.elements.instructions && (!this.elements.instructions.textContent || this.elements.instructions.textContent.trim() === '')) {
            this.elements.instructions.textContent = this.engine.config.defaultInstructions;
        }
        
        // Display meeting content with markdown formatting
        if (this.elements.meetingContent) {
            // Use the engine's formatText method to properly render markdown
            if (typeof this.engine.formatText === 'function') {
                this.elements.meetingContent.innerHTML = this.engine.formatText(this.testData.meeting_note || '');
            } else {
                this.elements.meetingContent.textContent = this.testData.meeting_note || '';
            }
        }
        
        // Display questions
        this.displayQuestions();
        
        // Setup solutions based on the displayed questions
        if (this.testData && Array.isArray(this.testData.aufgaben_list)) {
            this.testData.aufgaben_list.forEach((question, index) => {
                this.solutions[index] = question.loesung;
            });
        }
    }
    
    /**
     * Display the questions
     */
    displayQuestions() {
        // Clear the container
        if (this.elements.questionsContainer) {
            this.elements.questionsContainer.innerHTML = '';
            
            // Process the questions
            if (this.testData && Array.isArray(this.testData.aufgaben_list)) {
                this.testData.aufgaben_list.forEach((question, index) => {
                    // Create question container
                    const questionDiv = Utils.createElement('div', {
                        className: 'question',
                        dataset: { questionIndex: index.toString() }
                    });
                    
                    // Add question text
                    const questionText = Utils.createElement('div', {
                        className: 'question-text'
                    }, `${index + 1}. ${question.frage}`);
                    questionDiv.appendChild(questionText);
                    
                    // Add options
                    const optionsContainer = Utils.createElement('div', {
                        className: 'options'
                    });
                    
                    // Create multiple choice options
                    question.optionen.forEach(option => {
                        const optionContainer = Utils.createElement('div', {
                            className: 'option',
                            dataset: { value: option.key }
                        });
                        
                        const radio = Utils.createElement('input', {
                            type: 'radio',
                            name: `question-${index}`,
                            value: option.key,
                            disabled: this.isReviewMode
                        });
                        
                        const optionText = Utils.createElement('span', {
                            className: 'option-text'
                        }, `${option.key}) ${option.text}`);
                        
                        optionContainer.appendChild(radio);
                        optionContainer.appendChild(optionText);
                        optionsContainer.appendChild(optionContainer);
                    });
                    
                    questionDiv.appendChild(optionsContainer);
                    this.elements.questionsContainer.appendChild(questionDiv);
                });
            }
        }
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Set up event listeners for the multiple choice questions
        const options = this.elements.questionsContainer.querySelectorAll('.option');
        
        options.forEach(option => {
            option.addEventListener('click', () => {
                // If in review mode, don't allow changes
                if (this.isReviewMode) return;
                
                const questionIndex = option.closest('.question').dataset.questionIndex;
                const value = option.dataset.value;
                
                // Update the radio buttons
                const radio = option.querySelector('input[type="radio"]');
                if (radio) {
                    radio.checked = true;
                }
                
                // Update user answers
                this.userAnswers[questionIndex] = value;
            });
        });
    }

    /**
     * Mark answers as correct or incorrect
     */
    markAnswers() {
        // Find all questions
        const questions = this.elements.questionsContainer.querySelectorAll('.question');
        
        questions.forEach(question => {
            const questionIndex = question.dataset.questionIndex;
            const userAnswer = this.userAnswers[questionIndex];
            const correctAnswer = this.solutions[questionIndex];
            
            // Mark options as correct or incorrect
            const options = question.querySelectorAll('.option');
            
            // First remove any previous styling
            options.forEach(option => {
                option.classList.remove('correct', 'incorrect', 'selected');
            });
            
            // Always mark the correct option
            options.forEach(option => {
                const optionValue = option.dataset.value;
                
                if (optionValue === correctAnswer) {
                    option.classList.add('correct');
                }
            });
            
            // If user made a selection, mark it as selected and possibly incorrect
            if (userAnswer) {
                const selectedOption = question.querySelector(`.option[data-value="${userAnswer}"]`);
                
                if (selectedOption) {
                    selectedOption.classList.add('selected');
                    
                    // If it's incorrect, mark it as such
                    if (userAnswer !== correctAnswer) {
                        selectedOption.classList.add('incorrect');
                    }
                }
            }
        });
    }
}

export default Teil4Part; 