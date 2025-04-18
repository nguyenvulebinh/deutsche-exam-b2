/**
 * LesenExam - Implementation for the complete Lesen exam
 * This extends the base TestEngine class and integrates all 4 parts of the Lesen exam
 * Using a modular component architecture
 */

import TestEngine from '../core/test-engine.js';
import ExamController from '../components/exam/ExamController.js';
import Utils from '../core/utils.js';

class LesenExam extends TestEngine {
    /**
     * Constructor for LesenExam
     * @param {Object} options - Configuration options
     */
    constructor(options = {}) {
        // Set default options specific to Lesen Exam
        const defaultOptions = {
            testType: 'Lesen Exam',
        };
        
        // Merge with provided options
        super({...defaultOptions, ...options});
        
        // Exam controller
        this.examController = null;
    }
    
    /**
     * Initialize the exam
     * @returns {Promise<void>}
     */
    async initialize() {
        try {
            console.log('Initializing Lesen Exam...');
            
            // Get reference to key DOM elements
            this.setupDOMReferences();
            
            // Show loading screen
            Utils.showElement(this.elements.loading);
            Utils.hideElement(this.elements.testContent);
            
            // Create exam controller
            this.examController = new ExamController({
                elements: this.elements
            });
            
            // Initialize the exam controller
            console.log('Loading exam parts...');
            await this.examController.initialize();
            console.log('All parts loaded successfully');
            
            // Hide loading screen
            Utils.hideElement(this.elements.loading);
            Utils.showElement(this.elements.testContent);
        } catch (error) {
            console.error('LesenExam: Error initializing exam:', error);
            alert('Fehler beim Initialisieren der Prüfung. Bitte laden Sie die Seite neu.');
        }
    }
    
    /**
     * Set up references to DOM elements
     */
    setupDOMReferences() {
        // Call the parent method to set up basic elements
        super.setupDOMReferences();
        
        // Navigation buttons
        this.elements.prevButton = document.getElementById('prev-btn');
        this.elements.nextButton = document.getElementById('next-btn');
        this.elements.finishButton = document.getElementById('finish-btn');
        this.elements.newTestButton = document.getElementById('new-test-btn');
        
        // Progress indicators
        this.elements.currentPartLabel = document.getElementById('current-part-label');
        this.elements.progressSteps = {
            1: document.getElementById('progress-step-1'),
            2: document.getElementById('progress-step-2'),
            3: document.getElementById('progress-step-3'),
            4: document.getElementById('progress-step-4')
        };
        
        // Test part containers
        this.elements.testParts = {
            1: document.getElementById('test-part-1'),
            2: document.getElementById('test-part-2'),
            3: document.getElementById('test-part-3'),
            4: document.getElementById('test-part-4')
        };
        
        // Part 1 specific elements
        this.elements.part1 = {
            instructions: document.getElementById('instructions-part-1'),
            peopleContainer: document.getElementById('people-container-part-1'),
            articlesContainer: document.getElementById('articles-container-part-1'),
            answerGrid: document.getElementById('answer-grid-part-1')
        };
        
        // Part 2 specific elements
        this.elements.part2 = {
            instructions: document.getElementById('instructions-part-2'),
            textContainers: {
                1: {
                    container: document.getElementById('text-container-2-1'),
                    thema: document.getElementById('thema-2-1'),
                    textContent: document.getElementById('text-content-2-1'),
                    questionsContainer: document.getElementById('questions-container-2-1')
                },
                2: {
                    container: document.getElementById('text-container-2-2'),
                    thema: document.getElementById('thema-2-2'),
                    textContent: document.getElementById('text-content-2-2'),
                    questionsContainer: document.getElementById('questions-container-2-2')
                }
            }
        };
        
        // Part 3 specific elements
        this.elements.part3 = {
            instructions: document.getElementById('instructions-part-3'),
            peopleContainer: document.getElementById('people-container-part-3'),
            themaTitle: document.getElementById('thema-title-part-3'),
            postsContainer: document.getElementById('posts-container-part-3'),
            answerGrid: document.getElementById('answer-grid-part-3')
        };
        
        // Part 4 specific elements
        this.elements.part4 = {
            instructions: document.getElementById('instructions-part-4'),
            meetingContent: document.getElementById('meeting-content-part-4'),
            questionsContainer: document.getElementById('questions-container-part-4')
        };
        
        // Results elements
        this.elements.results = document.getElementById('results');
        this.elements.score = document.getElementById('score');
        this.elements.detailedResults = document.getElementById('detailed-results');
    }
}

// Export the LesenExam class
export default LesenExam; 