/**
 * TestEngine - Core class for TELC B2 Test Platform
 * This is the base class that all specific test types will extend
 */

import Utils from './utils.js';

class TestEngine {
    /**
     * Constructor for the TestEngine
     * @param {Object} options - Configuration options
     */
    constructor(options = {}) {
        // Default configuration
        this.config = {
            testDataDir: '',
            testType: '',
            defaultTestData: null,
            ...options
        };
        
        // State variables
        this.allTestData = [];
        this.currentTest = null;
        this.userAnswers = {};
        
        // DOM elements - to be set by subclasses
        this.elements = {};
        
        // Event listeners - to be bound by subclasses
        this.eventListeners = {};
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
                console.warn('No tests could be loaded, using default test');
                this.loadDefaultTest();
            }
            
            // Set up event listeners
            this.setupEventListeners();
            
            // Hide loading screen
            Utils.hideElement(this.elements.loading);
            Utils.showElement(this.elements.testContent);
        } catch (error) {
            console.error('Error initializing test engine:', error);
            this.loadDefaultTest();
        }
    }
    
    /**
     * Set up references to DOM elements
     * To be overridden by subclasses
     */
    setupDOMReferences() {
        this.elements = {
            loading: document.getElementById('loading'),
            testContent: document.getElementById('test-content'),
            instructions: document.getElementById('instructions'),
            finishButton: document.getElementById('finish-btn'),
            newTestButton: document.getElementById('new-test-btn'),
            results: document.getElementById('results'),
            score: document.getElementById('score')
        };
    }
    
    /**
     * Set up event listeners
     * To be overridden by subclasses
     */
    setupEventListeners() {
        // Set up the finish button
        if (this.elements.finishButton) {
            this.elements.finishButton.addEventListener('click', () => this.checkAnswers());
        }
        
        // Set up the new test button
        if (this.elements.newTestButton) {
            this.elements.newTestButton.addEventListener('click', () => this.loadRandomTest());
        }
    }
    
    /**
     * Load all test data from a directory
     * @returns {Promise<void>}
     */
    async loadAllTestData() {
        try {
            let testFileList = [];
            
            // Try to get test files in three ways (with fallbacks)
            // 1. First try to use the new manifest format (preferred method for GitHub Pages)
            try {
                // Extract test type from directory (e.g., "data_mocktest/lesen/teil_1" -> "lesen/teil_1")
                const testPathParts = this.config.testDataDir.split('/');
                const manifestBasePath = testPathParts.slice(0, testPathParts.length - 1).join('/');
                const testType = testPathParts[testPathParts.length - 1];
                
                // Try the new manifest location
                const manifestUrl = `${manifestBasePath}/${testType}_manifest.json`;
                console.log(`Loading manifest from: ${manifestUrl}`);
                
                const response = await fetch(manifestUrl);
                
                if (response.ok) {
                    const manifest = await response.json();
                    testFileList = manifest.files || [];
                    console.log(`Loaded ${testFileList.length} files from manifest at ${manifestUrl}`);
                } else {
                    console.log(`Manifest not found at ${manifestUrl}, trying old location...`);
                }
            } catch (error) {
                console.warn('Error loading from new manifest format:', error);
            }
            
            // 2. If that fails, try the old manifest location
            if (!testFileList || testFileList.length === 0) {
                try {
                    const response = await fetch(`${this.config.testDataDir}/file_manifest.json`);
                    if (response.ok) {
                        const manifest = await response.json();
                        testFileList = manifest.files || [];
                        console.log(`Loaded ${testFileList.length} files from old manifest location`);
                    }
                } catch (error) {
                    console.warn('Error loading from old manifest location:', error);
                }
            }
            
            // 3. As a last resort, try direct directory listing (works on some servers)
            if (!testFileList || testFileList.length === 0) {
                testFileList = await Utils.getTestFileList(this.config.testDataDir);
                if (testFileList && testFileList.length > 0) {
                    console.log(`Loaded ${testFileList.length} files from directory listing`);
                }
            }
            
            // 4. If everything else fails, try to use hardcoded fallback list
            if (!testFileList || testFileList.length === 0) {
                // Try to use the static method if the class has it
                if (this.constructor.getFallbackFileList) {
                    testFileList = this.constructor.getFallbackFileList();
                    console.log(`Using hardcoded list with ${testFileList.length} files`);
                }
            }
            
            if (!testFileList || testFileList.length === 0) {
                console.warn('No test files could be found');
                return;
            }
            
            // Fetch each test file and add to the allTestData array
            const fetchPromises = testFileList.map(file => this.fetchTestData(file));
            const testsData = await Promise.all(fetchPromises);
            
            // Filter out any null results (failed fetches)
            this.allTestData = testsData.filter(test => test !== null);
            
            // Log a summary of loaded tests
            console.log(`📚 Loaded ${this.allTestData.length}/${testFileList.length} tests for ${this.config.testType}`);
            
            // If no tests were loaded successfully, use the default test
            if (this.allTestData.length === 0) {
                console.warn('No tests could be loaded from external files');
            }
        } catch (error) {
            console.error('Error loading test data:', error);
            throw error;
        }
    }
    
    /**
     * Fetch a single test file
     * @param {string} filename - Name of the file to fetch
     * @returns {Promise<Object|null>} - Test data or null if fetch failed
     */
    async fetchTestData(filename) {
        try {
            const response = await fetch(`${this.config.testDataDir}/${filename}`);
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
            console.error(`Error loading ${filename}:`, error);
            return null; // Return null for failed fetches
        }
    }
    
    /**
     * Validate that test data has the required structure
     * To be overridden by subclasses
     * @param {Object} data - Test data to validate
     * @returns {boolean} - Whether the data is valid
     */
    validateTestData(data) {
        return (
            data && 
            typeof data === 'object'
        );
    }
    
    /**
     * Load a random test
     */
    loadRandomTest() {
        Utils.showElement(this.elements.loading);
        Utils.hideElement(this.elements.testContent);
        
        try {
            // Shuffle the tests and pick the first one
            const shuffledTests = Utils.shuffleArray(this.allTestData);
            this.currentTest = shuffledTests[0];
            
            // Display the test
            this.displayTest(this.currentTest);
            
            Utils.hideElement(this.elements.loading);
            Utils.showElement(this.elements.testContent);
        } catch (error) {
            console.error('Error loading test:', error);
            alert('Fehler beim Laden des Tests!');
        }
    }
    
    /**
     * Load the default test when no tests are available
     */
    loadDefaultTest() {
        if (this.config.defaultTestData) {
            this.currentTest = this.config.defaultTestData;
            
            // Set a filename identifier for the default test
            this.currentTest._sourceFilename = 'default_test_data';
            
            this.displayTest(this.currentTest);
            
            Utils.hideElement(this.elements.loading);
            Utils.showElement(this.elements.testContent);
        } else {
            console.error('No default test data available');
            alert('Fehler: Keine Testdaten verfügbar!');
        }
    }
    
    /**
     * Display a test
     * This method should be overridden by subclasses to handle test-specific display
     * @param {Object} test - Test data to display
     */
    displayTest(test) {
        // Reset the results display
        Utils.hideElement(this.elements.results);
        Utils.showElement(this.elements.finishButton);
        Utils.hideElement(this.elements.newTestButton);
        
        // Clear the score display
        if (this.elements.score) {
            this.elements.score.innerHTML = '';
        }
        
        // Store a reference to the current test
        this.currentTest = test;
        
        if (test._sourceFilename) {
            console.log(`📄 Task file: ${test._sourceFilename}`);
        }
        
        // Reset user answers
        this.userAnswers = {};
    }
    
    /**
     * Check answers and show results
     * To be overridden by subclasses
     */
    checkAnswers() {
        // To be implemented by subclasses
        console.log('Checking answers...');
        
        // Show results section
        if (this.elements.results) {
            Utils.showElement(this.elements.results);
        }
        
        // Hide finish button and show new test button
        if (this.elements.finishButton) {
            Utils.hideElement(this.elements.finishButton);
        }
        if (this.elements.newTestButton) {
            Utils.showElement(this.elements.newTestButton);
        }
    }
}

export default TestEngine; 