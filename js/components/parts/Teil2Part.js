/**
 * Teil2Part - Implementation for Teil 2 of the Lesen exam
 */

import BasePart from './BasePart.js';
import Utils from '../../core/utils.js';
import LesenTeil2 from '../../test-types/lesen-teil-2.js';

class Teil2Part extends BasePart {
    /**
     * Constructor for Teil2Part
     * @param {Object} options - Configuration options
     */
    constructor(options = {}) {
        super(options);
        this.engine = null;
        this.testData = [];
    }

    /**
     * Initialize the part
     * @returns {Promise<Object>} - Test data and solutions
     */
    async initialize() {
        try {
            // Create test engine
            this.engine = new LesenTeil2({
                testDataDir: '/data_mocktest/lesen/teil_2'
            });
            
            // Load all test data
            await this.engine.loadAllTestData();
            
            // Select two random tests
            let randomTests = [];
            if (this.engine.allTestData.length >= 2) {
                // Shuffle the test data array
                const shuffledTests = Utils.shuffleArray([...this.engine.allTestData]);
                randomTests = shuffledTests.slice(0, 2);
            } else if (this.engine.allTestData.length === 1) {
                randomTests = [this.engine.allTestData[0], this.engine.config.defaultTestData];
            } else {
                randomTests = [this.engine.config.defaultTestData, this.engine.config.defaultTestData];
            }
            
            // Save the tests and initialize solutions
            this.testData = randomTests;
            this.solutions = {};
            
            return {
                testData: this.testData,
                solutions: this.solutions
            };
        } catch (error) {
            console.error('Error initializing Teil 2:', error);
            throw error;
        }
    }

    /**
     * Render the test content
     */
    render() {
        // Set instructions
        if (this.elements.instructions) {
            this.elements.instructions.textContent = this.engine.config.defaultInstructions;
        }
        
        // Display the first test
        this.displayTest(this.testData[0], 1);
        
        // Display the second test
        this.displayTest(this.testData[1], 2);
    }
    
    /**
     * Display a specific test
     * @param {Object} test - Test data
     * @param {number} testIndex - Index of the test (1 or 2)
     */
    displayTest(test, testIndex) {
        const container = this.elements.textContainers[testIndex];
        
        // Display thema
        if (container.thema) {
            container.thema.textContent = test.thema || '';
        }
        
        // Display text content
        if (container.textContent) {
            // Use the engine's formatText method to properly render markdown
            if (typeof this.engine.formatText === 'function') {
                container.textContent.innerHTML = this.engine.formatText(test.text || '');
            } else {
                container.textContent.textContent = test.text || '';
            }
        }
        
        // Display questions
        if (container.questionsContainer) {
            container.questionsContainer.innerHTML = '';
            
            // Process the questions
            if (Array.isArray(test.Aufgaben)) {
                test.Aufgaben.forEach((question, index) => {
                    // Save solution
                    this.solutions[`${testIndex}-${index}`] = question.loesung;
                    
                    // Create question container
                    const questionDiv = Utils.createElement('div', {
                        className: 'question',
                        dataset: { questionIndex: `${testIndex}-${index}` }
                    });
                    
                    // Add question text
                    const questionText = Utils.createElement('div', {
                        className: 'question-text'
                    }, `${index + 1}. ${question.frage}`);
                    questionDiv.appendChild(questionText);
                    
                    // Add options based on question type
                    const optionsContainer = Utils.createElement('div', {
                        className: 'options'
                    });
                    
                    if (question.type === 'richtig/falsch') {
                        // Create true/false options
                        ['richtig', 'falsch'].forEach(value => {
                            const optionContainer = Utils.createElement('div', {
                                className: 'option',
                                dataset: { value }
                            });
                            
                            const radio = Utils.createElement('input', {
                                type: 'radio',
                                name: `question-${testIndex}-${index}`,
                                value,
                                disabled: this.isReviewMode
                            });
                            
                            const optionText = Utils.createElement('span', {
                                className: 'option-text'
                            }, value);
                            
                            optionContainer.appendChild(radio);
                            optionContainer.appendChild(optionText);
                            optionsContainer.appendChild(optionContainer);
                        });
                    } else if (question.type === 'multiple-choice') {
                        // Create multiple choice options
                        question.optionen.forEach(option => {
                            const optionContainer = Utils.createElement('div', {
                                className: 'option',
                                dataset: { value: option.key }
                            });
                            
                            const radio = Utils.createElement('input', {
                                type: 'radio',
                                name: `question-${testIndex}-${index}`,
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
                    }
                    
                    questionDiv.appendChild(optionsContainer);
                    container.questionsContainer.appendChild(questionDiv);
                });
            }
        }
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Process each question container
        for (let testIndex = 1; testIndex <= 2; testIndex++) {
            const questionsContainer = this.elements.textContainers[testIndex].questionsContainer;
            const options = questionsContainer.querySelectorAll('.option');
            
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
    }

    /**
     * Mark answers as correct or incorrect
     */
    markAnswers() {
        // Process each question container
        for (let testIndex = 1; testIndex <= 2; testIndex++) {
            const questionsContainer = this.elements.textContainers[testIndex].questionsContainer;
            const questions = questionsContainer.querySelectorAll('.question');
            
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
}

export default Teil2Part; 