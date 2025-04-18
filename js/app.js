/**
 * Main application file for TELC B2 Test Platform
 * Initializes the appropriate test type based on the page URL or parameters
 */

import LesenTeil1 from './test-types/lesen-teil-1.js';
import LesenTeil2 from './test-types/lesen-teil-2.js';

// Collection of available test types
const testTypes = {
    'lesen-teil-1': LesenTeil1,
    'lesen-teil-2': LesenTeil2
    // Add more test types here as they are implemented:
    // 'lesen-teil-3': LesenTeil3,
    // 'hoeren-teil-1': HoerenTeil1,
    // etc.
};

/**
 * Initialize the application when the DOM is loaded
 */
function initApp() {
    // Get the test type from: 
    // 1. window.testType (set directly in the HTML page)
    // 2. URL parameters
    // 3. Fall back to default
    const testType = window.testType || getTestTypeFromURL() || 'lesen-teil-1';
    
    // Get the TestEngine class for this test type
    const TestClass = testTypes[testType];
    
    if (TestClass) {
        // Create an instance of the test engine
        const testEngine = new TestClass();
        
        // Initialize the test engine
        testEngine.initialize()
            .catch(error => {
                console.error('Error initializing test engine:', error);
                showError('Fehler beim Initialisieren des Tests. Bitte laden Sie die Seite neu.');
            });
    } else {
        showError(`Unbekannter Testtyp: ${testType}`);
    }
}

/**
 * Get the test type from the URL parameters
 * @returns {string|null} - Test type or null if not specified
 */
function getTestTypeFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('testType');
}

/**
 * Show an error message
 * @param {string} message - Error message to show
 */
function showError(message) {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.innerHTML = `<div class="error">${message}</div>`;
        loading.classList.remove('hidden');
    } else {
        alert(message);
    }
}

// Start the application when the page loads
window.addEventListener('DOMContentLoaded', initApp); 