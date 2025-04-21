/**
 * Schreiben - Implementation for Schreiben test type
 * This extends the base TestEngine class
 */

import TestEngine from '../core/test-engine.js';
import Utils from '../core/utils.js';

class Schreiben extends TestEngine {
    /**
     * Constructor for Schreiben
     * @param {Object} options - Configuration options
     */
    constructor(options = {}) {
        // Set default options specific to Schreiben
        const defaultOptions = {
            testDataDir: '/data_mocktest/schreiben/teil_1',
            testType: 'Schreiben',
            defaultInstructions: 'In Ihrer Firma können sich alle Mitarbeiterinnen und Mitarbeiter in einem Forum miteinander über Neuigkeiten austauschen. Begründen Sie Ihre Meinung und nennen Sie passende Beispiele. Gliedern Sie Ihren Text in sinnvolle Abschnitte.',
            defaultTestData: {
                "thema": "Beispiel-Thema",
                "aufgabe": "Dies ist ein Beispiel für eine Aufgabe im Schreiben-Test.",
                "solution": {
                    "level1": {
                        "title": "Level 1: Wichtige Punkte in der Aufgabe verstehen",
                        "guidance": "### Level 1: Wichtige Punkte verstehen\n\nHier finden Sie allgemeine Hinweise zur Aufgabe."
                    },
                    "level2": {
                        "title": "Level 2: Schritt-für-Schritt zum guten Forumsbeitrag",
                        "guidance": "### Level 2: Schritt-für-Schritt zum guten Forumsbeitrag\n\nHier finden Sie eine detaillierte Anleitung zum Schreiben eines Forumsbeitrags."
                    },
                    "level3": {
                        "title": "Level 3: Beispiel für einen vollständigen Forumsbeitrag (B2)",
                        "guidance": "### Level 3: Beispiel für einen vollständigen Forumsbeitrag (B2)\n\nHier finden Sie ein Beispiel für einen gut strukturierten Forumsbeitrag."
                    }
                }
            }
        };
        
        // Merge with provided options
        super({...defaultOptions, ...options});
    }
    
    /**
     * Load all test data - override the base method to handle the manifest file location
     * @returns {Promise<void>}
     */
    async loadAllTestData() {
        try {
            let testFileList = [];
            
            // Try to load from manifest file directly
            try {
                const manifestUrl = '/data_mocktest/schreiben/teil_1_manifest.json';
                console.log(`Attempting to load manifest from: ${manifestUrl}`);
                
                const response = await fetch(manifestUrl);
                
                if (response.ok) {
                    const manifest = await response.json();
                    testFileList = manifest.files || [];
                    console.log(`Loaded ${testFileList.length} files from manifest at ${manifestUrl}`);
                } else {
                    console.warn(`Manifest not found at ${manifestUrl}, falling back to parent implementation`);
                    // Fall back to the parent implementation
                    return super.loadAllTestData();
                }
            } catch (error) {
                console.warn('Error loading teil_1 manifest directly:', error);
                // Fall back to the parent implementation
                return super.loadAllTestData();
            }
            
            if (!testFileList || testFileList.length === 0) {
                console.warn('No test files found in manifest, falling back to default method');
                return super.loadAllTestData();
            }
            
            // Fetch each test file and add to the allTestData array
            console.log(`Starting to fetch ${testFileList.length} test files...`);
            const fetchPromises = testFileList.map(file => this.fetchTestData(file));
            const testsData = await Promise.all(fetchPromises);
            
            // Filter out any null results (failed fetches)
            this.allTestData = testsData.filter(test => test !== null);
            
            // Log a summary of loaded tests
            console.log(`📚 Successfully loaded ${this.allTestData.length}/${testFileList.length} tests for ${this.config.testType}`);
            
            // If no tests were loaded successfully, use the default test
            if (this.allTestData.length === 0) {
                console.warn('No tests could be loaded from external files');
            }
        } catch (error) {
            console.error('Error loading test data:', error);
            // Fall back to the parent implementation
            return super.loadAllTestData();
        }
    }
    
    /**
     * Set up references to DOM elements
     * @override
     */
    setupDOMReferences() {
        // Call the parent method to set up basic elements
        super.setupDOMReferences();
        
        // Set up additional elements specific to Schreiben
        this.elements.thema = document.getElementById('thema');
        this.elements.aufgabe = document.getElementById('aufgabe');
        this.elements.writingArea = document.getElementById('writing-area');
        this.elements.guidanceContainer = document.getElementById('guidance-container');
        this.elements.guidanceContent = document.getElementById('guidance-content');
        this.elements.guidanceLevelButtons = document.querySelectorAll('.guidance-level-btn');
    }
    
    /**
     * Validate that test data has the required structure
     * @override
     * @param {Object} data - Test data to validate
     * @returns {boolean} - Whether the data is valid
     */
    validateTestData(data) {
        return (
            data && 
            data.thema && 
            data.aufgabe && 
            data.solution &&
            data.solution.level1 &&
            data.solution.level2 &&
            data.solution.level3
        );
    }
    
    /**
     * Display the Schreiben test
     * @override
     * @param {Object} test - Test data to display
     */
    displayTest(test) {
        // Call the parent method to handle basic display
        super.displayTest(test);
        
        // Log which test file is being displayed
        if (test._sourceFilename) {
            console.log(`Displaying test from file: ${test._sourceFilename}`);
        }
        
        // Clear writing area
        if (this.elements.writingArea) {
            this.elements.writingArea.value = '';
        }
        
        // Display thema
        if (this.elements.thema && test.thema) {
            this.elements.thema.textContent = test.thema;
        }
        
        // Display aufgabe
        if (this.elements.aufgabe && test.aufgabe) {
            this.elements.aufgabe.textContent = test.aufgabe;
        }
        
        // Hide guidance content initially
        if (this.elements.guidanceContainer) {
            this.elements.guidanceContainer.style.display = 'none';
        }

        // Make sure the UI is properly updated
        if (this.elements.loading) {
            this.elements.loading.classList.add('loaded');
            Utils.hideElement(this.elements.loading);
        }
    }
    
    /**
     * Format text with markdown
     * @param {string} text - The text to format
     * @returns {string} - Formatted HTML
     */
    formatText(text) {
        if (!text) return '';
        
        // Use marked.js to convert markdown to HTML
        if (window.marked) {
            try {
                // Remove markdown code blocks indicators
                const cleanText = text.replace(/```markdown\n/g, '').replace(/```/g, '');
                
                // Fix bullet points for better display - ensure proper spacing
                const fixedText = cleanText
                    .replace(/\n\* /g, '\n\n* ') // Add extra line break before bullet points
                    .replace(/\n(\d+)\. /g, '\n\n$1. ') // Add extra line break before numbered lists
                    .replace(/>\n>/g, '>\n>\n>') // Fix blockquote spacing
                    .replace(/\n{3,}/g, '\n\n'); // Remove excessive line breaks
                    
                // Convert the markdown to HTML
                const html = window.marked.parse(fixedText);
                
                // Add a class to list items for better mobile styling
                return html.replace(/<li>/g, '<li class="guidance-list-item">');
            } catch (error) {
                console.error('Error parsing markdown:', error);
                return text;
            }
        } else {
            // Basic markdown parsing if marked.js is not available
            return this.basicMarkdownParse(text);
        }
    }
    
    /**
     * Very basic markdown parser for fallback
     * @param {string} text - The text to parse
     * @returns {string} - HTML formatted text
     */
    basicMarkdownParse(text) {
        if (!text) return '';
        
        // Remove markdown code blocks indicators
        let html = text.replace(/```markdown\n/g, '').replace(/```/g, '');
        
        // Convert headers
        html = html.replace(/^### (.*?)$/gm, '<h3>$1</h3>');
        html = html.replace(/^## (.*?)$/gm, '<h2>$1</h2>');
        html = html.replace(/^# (.*?)$/gm, '<h1>$1</h1>');
        
        // Convert bold and italic
        html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        // Convert links
        html = html.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>');
        
        // Convert bullet points (ensuring they're in a list structure)
        let inList = false;
        const lines = html.split('\n');
        html = lines.map(line => {
            if (line.trim().startsWith('* ')) {
                const content = line.trim().substring(2);
                if (!inList) {
                    inList = true;
                    return `<ul><li>${content}</li>`;
                } else {
                    return `<li>${content}</li>`;
                }
            } else if (inList && line.trim() !== '') {
                inList = false;
                return `</ul>${line}`;
            } else if (inList && line.trim() === '') {
                inList = false;
                return '</ul>';
            } else {
                return line;
            }
        }).join('\n');
        
        if (inList) {
            html += '</ul>';
        }
        
        // Convert blockquotes
        html = html.replace(/^> (.*?)$/gm, '<blockquote>$1</blockquote>');
        
        // Convert paragraphs (improved approach)
        html = html.replace(/\n\n+/g, '</p><p>');
        
        // Wrap in paragraph tags if not already
        if (!html.startsWith('<')) {
            html = '<p>' + html + '</p>';
        }
        
        return html;
    }
    
    /**
     * Handle guidance level button click
     * @param {number} level - Guidance level (1, 2, or 3)
     */
    showGuidanceLevel(level) {
        const test = this.currentTest;
        if (!test || !test.solution) return;
        
        const levelKey = `level${level}`;
        const levelData = test.solution[levelKey];
        
        if (!levelData) return;
        
        // Show the guidance container
        if (this.elements.guidanceContainer) {
            this.elements.guidanceContainer.style.display = 'block';
            
            // Add a subtle highlight animation to draw attention
            this.elements.guidanceContainer.style.animation = 'none';
            setTimeout(() => {
                this.elements.guidanceContainer.style.animation = 'highlight-guidance 1s ease-in-out';
            }, 10);
        }
        
        // Update the guidance content
        if (this.elements.guidanceContent) {
            // If the title isn't included in the guidance content, add it
            let contentWithTitle = levelData.guidance;
            if (!contentWithTitle.includes(levelData.title)) {
                contentWithTitle = `### ${levelData.title}\n\n${contentWithTitle}`;
            }
            
            this.elements.guidanceContent.innerHTML = this.formatText(contentWithTitle);
            
            // Scroll to the guidance container with a small delay for smoother experience
            setTimeout(() => {
                this.elements.guidanceContainer.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
            }, 50);
        }
        
        // Update active button state
        if (this.elements.guidanceLevelButtons) {
            this.elements.guidanceLevelButtons.forEach(btn => {
                const btnLevel = parseInt(btn.dataset.level);
                if (btnLevel === level) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });
        }
    }
    
    /**
     * Set up event listeners
     * @override
     */
    setupEventListeners() {
        // Call the parent method to set up basic listeners
        super.setupEventListeners();
        
        // Add guidance level button listeners
        this.elements.guidanceLevelButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const level = parseInt(btn.dataset.level);
                this.showGuidanceLevel(level);
            });
        });
        
        // Add finish button listener
        if (this.elements.finishButton) {
            this.elements.finishButton.addEventListener('click', () => {
                // Display the results section first so the guidance container is visible
                if (this.elements.results) {
                    Utils.showElement(this.elements.results);
                }
                
                // Show level 1 guidance (tips) when finish is clicked
                this.showGuidanceLevel(1);
                
                // Show the new test button
                if (this.elements.newTestButton) {
                    Utils.showElement(this.elements.newTestButton);
                }
            });
        }
    }
    
    /**
     * Static method to get a fallback file list
     * @returns {Array} - List of default test files
     */
    static getFallbackFileList() {
        return [
            'mocktest_generated_1.json',
            'mocktest_generated_2.json',
            'mocktest_generated_3.json',
            'mocktest_generated_4.json',
            'mocktest_generated_5.json'
        ];
    }
}

export default Schreiben; 