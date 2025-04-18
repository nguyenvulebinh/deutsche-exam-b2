/**
 * BasePart - Base class for all test parts
 * Handles common functionality for part rendering and interaction
 */

import Utils from '../../core/utils.js';

class BasePart {
    /**
     * Constructor for BasePart
     * @param {Object} options - Configuration options
     */
    constructor(options = {}) {
        this.elements = options.elements || {};
        this.testEngine = options.testEngine || null;
        this.testData = options.testData || null;
        this.userAnswers = options.userAnswers || {};
        this.solutions = options.solutions || {};
        this.isReviewMode = options.isReviewMode || false;
    }

    /**
     * Initialize the part
     * @returns {Promise<void>}
     */
    async initialize() {
        throw new Error('Method not implemented: initialize()');
    }

    /**
     * Render the test content
     */
    render() {
        throw new Error('Method not implemented: render()');
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        throw new Error('Method not implemented: setupEventListeners()');
    }

    /**
     * Get user answers
     * @returns {Object} - User answers
     */
    getUserAnswers() {
        return this.userAnswers;
    }

    /**
     * Set user answers
     * @param {Object} answers - User answers
     */
    setUserAnswers(answers) {
        this.userAnswers = {...answers};
    }

    /**
     * Get solutions
     * @returns {Object} - Solutions
     */
    getSolutions() {
        return this.solutions;
    }

    /**
     * Mark answers as correct or incorrect
     * Should be implemented by subclasses
     */
    markAnswers() {
        throw new Error('Method not implemented: markAnswers()');
    }

    /**
     * Enable review mode (after test completion)
     * @param {boolean} isReviewMode - Whether the part is in review mode
     */
    setReviewMode(isReviewMode) {
        this.isReviewMode = isReviewMode;
    }
}

export default BasePart; 