/**
 * ExamController - Main controller for the complete Lesen exam
 * Handles part navigation, scoring, and result display
 */

import Utils from '../../core/utils.js';
import Teil1Part from '../parts/Teil1Part.js';
import Teil2Part from '../parts/Teil2Part.js';
import Teil3Part from '../parts/Teil3Part.js';
import Teil4Part from '../parts/Teil4Part.js';

class ExamController {
    /**
     * Constructor for ExamController
     * @param {Object} options - Configuration options
     */
    constructor(options = {}) {
        this.elements = options.elements || {};
        this.currentPart = 1;
        this.parts = {};
        this.userAnswers = {};
        this.solutions = {};
        this.partCompleted = {
            1: false,
            2: false,
            3: false,
            4: false
        };
        this.isReviewMode = false;
    }

    /**
     * Initialize the exam
     * @returns {Promise<void>}
     */
    async initialize() {
        try {
            // Initialize parts
            await this.initializeParts();
            
            // Setup navigation event listeners
            this.setupNavigationListeners();
            
            // Set the first part as active
            this.setActivePart(1);
            
            // Update navigation buttons
            this.updateNavigation();
        } catch (error) {
            console.error('Error initializing exam:', error);
            throw error;
        }
    }

    /**
     * Initialize all parts of the exam
     * @returns {Promise<void>}
     */
    async initializeParts() {
        try {
            // Initialize Teil 1
            console.log('Loading Teil 1...');
            this.parts[1] = new Teil1Part({
                elements: this.elements.part1,
                isReviewMode: this.isReviewMode
            });
            
            const teil1Data = await this.parts[1].initialize();
            console.log('Teil 1 loaded successfully. Task file:', teil1Data.testData._sourceFilename || 'default');
            this.solutions[1] = teil1Data.solutions;
            this.parts[1].render();
            this.parts[1].setupEventListeners();
            
            // Initialize Teil 2
            console.log('Loading Teil 2...');
            this.parts[2] = new Teil2Part({
                elements: this.elements.part2,
                isReviewMode: this.isReviewMode
            });
            
            const teil2Data = await this.parts[2].initialize();
            console.log('Teil 2 loaded successfully. Task file:', teil2Data.testData._sourceFilename || 'default');
            this.solutions[2] = teil2Data.solutions;
            this.parts[2].render();
            this.parts[2].setupEventListeners();
            
            // Initialize Teil 3
            console.log('Loading Teil 3...');
            this.parts[3] = new Teil3Part({
                elements: this.elements.part3,
                isReviewMode: this.isReviewMode
            });
            
            const teil3Data = await this.parts[3].initialize();
            console.log('Teil 3 loaded successfully. Task file:', teil3Data.testData._sourceFilename || 'default');
            this.solutions[3] = teil3Data.solutions;
            this.parts[3].render();
            this.parts[3].setupEventListeners();
            
            // Initialize Teil 4
            console.log('Loading Teil 4...');
            this.parts[4] = new Teil4Part({
                elements: this.elements.part4,
                isReviewMode: this.isReviewMode
            });
            
            const teil4Data = await this.parts[4].initialize();
            console.log('Teil 4 loaded successfully. Task file:', teil4Data.testData._sourceFilename || 'default');
            this.solutions[4] = teil4Data.solutions;
            this.parts[4].render();
            this.parts[4].setupEventListeners();
        } catch (error) {
            console.error('Error initializing parts:', error);
            throw error;
        }
    }

    /**
     * Setup navigation event listeners
     */
    setupNavigationListeners() {
        // Previous button
        if (this.elements.prevButton) {
            this.elements.prevButton.addEventListener('click', () => {
                this.navigateToPreviousPart();
            });
        }
        
        // Next button
        if (this.elements.nextButton) {
            this.elements.nextButton.addEventListener('click', () => {
                this.navigateToNextPart();
            });
        }
        
        // Finish button
        if (this.elements.finishButton) {
            this.elements.finishButton.addEventListener('click', () => {
                this.finishExam();
            });
        }
        
        // New test button
        if (this.elements.newTestButton) {
            this.elements.newTestButton.addEventListener('click', () => {
                this.startNewExam();
            });
        }
    }

    /**
     * Navigate to the previous part
     */
    navigateToPreviousPart() {
        if (this.currentPart > 1) {
            this.saveCurrentPartAnswers();
            this.setActivePart(this.currentPart - 1);
            this.updateNavigation();
        }
    }

    /**
     * Navigate to the next part
     */
    navigateToNextPart() {
        if (this.currentPart < 4) {
            this.saveCurrentPartAnswers();
            this.setActivePart(this.currentPart + 1);
            this.updateNavigation();
        }
    }

    /**
     * Set the active part
     * @param {number} partNumber - Part number (1-4)
     */
    setActivePart(partNumber) {
        // Hide all parts
        for (let i = 1; i <= 4; i++) {
            if (this.elements.testParts[i]) {
                this.elements.testParts[i].classList.remove('active');
            }
        }
        
        // Show the selected part
        if (this.elements.testParts[partNumber]) {
            this.elements.testParts[partNumber].classList.add('active');
        }
        
        // Update current part
        this.currentPart = partNumber;
        
        // Update progress indicator
        this.updateProgressIndicator();
    }

    /**
     * Update the progress indicator
     */
    updateProgressIndicator() {
        // Update label
        if (this.elements.currentPartLabel) {
            this.elements.currentPartLabel.textContent = `Teil ${this.currentPart}/4`;
        }
        
        // Update steps
        for (let i = 1; i <= 4; i++) {
            if (this.elements.progressSteps[i]) {
                this.elements.progressSteps[i].classList.remove('active', 'completed');
                
                if (i === this.currentPart) {
                    this.elements.progressSteps[i].classList.add('active');
                } else if (i < this.currentPart || this.partCompleted[i]) {
                    this.elements.progressSteps[i].classList.add('completed');
                }
            }
        }
    }

    /**
     * Update navigation buttons
     */
    updateNavigation() {
        // Disable/enable previous button
        if (this.elements.prevButton) {
            this.elements.prevButton.disabled = (this.currentPart === 1);
        }
        
        // Update next button based on current part
        if (this.elements.nextButton) {
            this.elements.nextButton.disabled = (this.currentPart === 4);
        }
        
        // Always keep the finish button visible
        Utils.showElement(this.elements.finishButton);
    }

    /**
     * Save the answers for the current part
     */
    saveCurrentPartAnswers() {
        const part = this.parts[this.currentPart];
        
        if (part) {
            this.userAnswers[this.currentPart] = part.getUserAnswers();
        }
        
        // Mark the part as completed
        this.partCompleted[this.currentPart] = true;
    }

    /**
     * Finish the exam and calculate the score
     */
    finishExam() {
        // Save answers from the last part
        this.saveCurrentPartAnswers();
        
        // Switch to review mode
        this.isReviewMode = true;
        
        // Mark all parts as being in review mode
        for (let i = 1; i <= 4; i++) {
            if (this.parts[i]) {
                this.parts[i].setReviewMode(true);
            }
        }
        
        // Calculate score
        const score = this.calculateScore();
        
        // Show results
        this.showResults(score);
        
        // Mark all answers
        this.markAllAnswers();
        
        // Set the first part as active for review
        this.setActivePart(1);
        
        // Hide finish button
        Utils.hideElement(this.elements.finishButton);
        
        // Enable both navigation buttons for review
        if (this.elements.prevButton) {
            this.elements.prevButton.disabled = false;
        }
        
        if (this.elements.nextButton) {
            this.elements.nextButton.disabled = false;
        }
        
        // Show new test button
        Utils.showElement(this.elements.newTestButton);
    }

    /**
     * Mark all answers as correct or incorrect
     */
    markAllAnswers() {
        for (let partNumber = 1; partNumber <= 4; partNumber++) {
            const part = this.parts[partNumber];
            if (part) {
                part.markAnswers();
            }
        }
    }

    /**
     * Calculate the score for the exam
     * @returns {Object} - Score information
     */
    calculateScore() {
        // TELC scoring rules:
        // Teil 1: 5 Items × 3 Punkte = 15
        // Teil 2: 4 Items × 3 Punkte = 12
        // Teil 3: 4 Items × 3 Punkte = 12
        // Teil 4: 5 Items × 3 Punkte = 15
        const pointsPerItem = 3;
        const partMaxItems = {
            1: 5, // Teil 1: 5 Items × 3 Punkte = 15
            2: 4, // Teil 2: 4 Items × 3 Punkte = 12
            3: 4, // Teil 3: 4 Items × 3 Punkte = 12
            4: 5  // Teil 4: 5 Items × 3 Punkte = 15
        };

        const score = {
            total: 0,
            correct: 0,
            possiblePoints: 0,
            earnedPoints: 0,
            byPart: {
                1: { total: 0, correct: 0, possiblePoints: 0, earnedPoints: 0 },
                2: { total: 0, correct: 0, possiblePoints: 0, earnedPoints: 0 },
                3: { total: 0, correct: 0, possiblePoints: 0, earnedPoints: 0 },
                4: { total: 0, correct: 0, possiblePoints: 0, earnedPoints: 0 }
            }
        };
        
        // Check answers for each part
        for (let part = 1; part <= 4; part++) {
            const partAnswers = this.userAnswers[part] || {};
            const partSolutions = this.solutions[part] || {};
            
            // Count total questions
            const totalQuestions = Object.keys(partSolutions).length;
            score.byPart[part].total = totalQuestions;
            score.total += totalQuestions;
            
            // Calculate possible points based on TELC rules
            score.byPart[part].possiblePoints = partMaxItems[part] * pointsPerItem;
            score.possiblePoints += score.byPart[part].possiblePoints;
            
            // Count correct answers
            let correctAnswers = 0;
            
            Object.keys(partSolutions).forEach(questionId => {
                const userAnswer = partAnswers[questionId];
                const correctAnswer = partSolutions[questionId];
                
                if (userAnswer && userAnswer === correctAnswer) {
                    correctAnswers++;
                    score.correct++;
                }
            });
            
            score.byPart[part].correct = correctAnswers;
            
            // Calculate earned points based on correct answers and TELC scoring
            // If there are more items than the TELC specifies, we still limit the max points
            const validItems = Math.min(totalQuestions, partMaxItems[part]);
            const earnedItemCount = Math.min(correctAnswers, validItems);
            score.byPart[part].earnedPoints = earnedItemCount * pointsPerItem;
            score.earnedPoints += score.byPart[part].earnedPoints;
        }
        
        return score;
    }

    /**
     * Show the exam results
     * @param {Object} score - Score information
     */
    showResults(score) {
        // Show results container
        if (this.elements.results) {
            Utils.showElement(this.elements.results);
        }
        
        // Show the overall score
        if (this.elements.score) {
            const percentage = Math.round((score.earnedPoints / score.possiblePoints) * 100);
            this.elements.score.innerHTML = `
                <p>${score.earnedPoints} von ${score.possiblePoints} Punkten (${percentage}%)</p>
            `;
        }
        
        // Show detailed results in a compact table format
        if (this.elements.detailedResults) {
            let detailedHtml = '';
            
            // Create a table for more compact display
            detailedHtml += `
                <table class="results-table">
                    <thead>
                        <tr>
                            <th>Teil</th>
                            <th>Korrekt</th>
                            <th>Punkte</th>
                            <th>Prozent</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            
            for (let part = 1; part <= 4; part++) {
                const partScore = score.byPart[part];
                const partPercentage = partScore.possiblePoints > 0 
                    ? Math.round((partScore.earnedPoints / partScore.possiblePoints) * 100) 
                    : 0;
                
                detailedHtml += `
                    <tr>
                        <td>Teil ${part}</td>
                        <td>${partScore.correct}/${partScore.total}</td>
                        <td>${partScore.earnedPoints}/${partScore.possiblePoints}</td>
                        <td>${partPercentage}%</td>
                    </tr>
                `;
            }
            
            // Add a total row
            detailedHtml += `
                    <tr class="results-total">
                        <td><strong>Gesamt</strong></td>
                        <td><strong>${score.correct}/${score.total}</strong></td>
                        <td><strong>${score.earnedPoints}/${score.possiblePoints}</strong></td>
                        <td><strong>${Math.round((score.earnedPoints / score.possiblePoints) * 100)}%</strong></td>
                    </tr>
                </tbody>
            </table>
            `;
            
            this.elements.detailedResults.innerHTML = detailedHtml;
        }
    }

    /**
     * Start a new exam
     */
    startNewExam() {
        // Reload the page to start a new exam
        window.location.reload();
    }
}

export default ExamController; 