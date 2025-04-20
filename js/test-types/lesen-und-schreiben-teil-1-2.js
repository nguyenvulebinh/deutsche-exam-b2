/**
 * LesenUndSchreibenTeil1_2 - Implementation for Lesen und Schreiben Teil 1 & 2 test type
 * This extends the base TestEngine class
 */

import TestEngine from '../core/test-engine.js';
import Utils from '../core/utils.js';

class LesenUndSchreibenTeil1_2 extends TestEngine {
    /**
     * Constructor for LesenUndSchreibenTeil1_2
     * @param {Object} options - Configuration options
     */
    constructor(options = {}) {
        // Set default options specific to Lesen und Schreiben Teil 1 & 2
        const defaultOptions = {
            testDataDir: '/data_mocktest/lesen_und_schreiben/teil_1_2',
            testType: 'Lesen und Schreiben Teil 1&2',
            defaultInstructions: 'Ihre Teamleitung leitet Ihnen die E-Mail von einem Kunden weiter und bittet Sie zu antworten.',
            defaultTestData: {
                "beschwerde_teamleiterin": {
                    "typ": "E-Mail von Teamleiterin",
                    "text": "```markdown\n**Von:** Marisa Leon\n**Erhalten:** heute, 8:23 Uhr\n**An:** ...\n\n**Betreff:** FW: Beschwerde Verschlechterung des Services\n\nHallo,\n\nunten stehende E-Mail erreichte mich gestern. Bitte kümmern Sie sich darum und antworten Sie dem Kunden höflich. Herr Stemmler ist seit Jahren Kunde bei uns und ich möchte ihn ungern verlieren. Sie können ihm ruhig den Grund für unsere aktuellen Probleme nennen. Ganz wichtig: Bitte schreiben Sie Herrn Stemmler auch, wie wir diese Probleme zukünftig lösen werden.\n\nVielen Dank und beste Grüße\n\nMarisa Leon\nTeamleiterin\n```"
                },
                "beschwerde_kunde": {
                    "typ": "E-Mail von Kunde",
                    "text": "```markdown\n**Gesendet:** gestern, 12:54 Uhr\n**Von:** Frank Stemmler\n**An:** Marisa Leon\n\n**Betreff:** Beschwerde Verschlechterung des Services\n\nSehr geehrte Frau Leon,\n\nleider bin ich mit Ihrem Service gar nicht mehr zufrieden. Sie führen bei uns die tägliche Reinigung aller Büroräume aus. Dazu gehört auch, in den Küchen aufzuräumen und die Konferenzräume für den nächsten Tag vorzubereiten. Bisher waren wir mit Ihrem Personal sehr zufrieden.\n\nIn den letzten drei Wochen kam es immer wieder vor, dass vor allem die Konferenzräume nicht ordentlich waren. Das führt zu Problemen, wenn dort am nächsten Tag bereits am Vormittag eine Besprechung stattfindet. Wir können uns nicht auf die Qualität Ihrer Arbeit verlassen und müssen selbst aufräumen. Auch die Reinigung der Büros und Küchen war in letzter Zeit oft nicht zufriedenstellend.\n\nBitte sorgen Sie wieder für einen einwandfreien Service in gewohnter Qualität.\nIch erwarte Ihre Antwort bis kommenden Freitag.\n\nMit freundlichen Grüßen\nFrank Stemmler\n```"
                },
                "aufgaben_list": [
                    {
                        "frage": "Herr Stemmler",
                        "optionen": [
                            {
                                "key": "a",
                                "text": "beschwert sich über Probleme während einer Konferenz."
                            },
                            {
                                "key": "b",
                                "text": "ist mit der Reinigung der Konferenzräume unzufrieden."
                            },
                            {
                                "key": "c",
                                "text": "möchte für den Reinigungsservice anderes Personal."
                            }
                        ],
                        "loesung": "b"
                    },
                    {
                        "frage": "Die Probleme",
                        "optionen": [
                            {
                                "key": "a",
                                "text": "bestehen schon länger."
                            },
                            {
                                "key": "b",
                                "text": "sind seit einigen Wochen zu beobachten."
                            },
                            {
                                "key": "c",
                                "text": "treten seit drei Monaten auf."
                            }
                        ],
                        "loesung": "b"
                    }
                ],
                "schreibaufgabe": {
                    "aufgaben_text": "Schreiben Sie eine E-Mail an den Kunden. Setzen Sie dabei alle Punkte Ihrer Teamleitung um.\nAchten Sie darauf, dass Sie dem Kunden gegenüber eine angemessene Sprache verwenden (Anrede, Höflichkeit, formelle Sprache etc.).",
                    "check_list": [
                        "Schreiben Sie eine formelle E-Mail an Herrn Stemmler.",
                        "Verwenden Sie eine passende Anrede (z.B. 'Sehr geehrter Herr Stemmler,').",
                        "Beziehen Sie sich auf seine Beschwerde-E-Mail.",
                        "Zeigen Sie Verständnis für seine Unzufriedenheit und entschuldigen Sie sich höflich für die Unannehmlichkeiten.",
                        "Nennen Sie (ggf. einen plausiblen) Grund für die aktuellen Probleme (gemäß Anweisung der Teamleiterin).",
                        "Erklären Sie, welche konkreten Maßnahmen ergriffen werden, um die Probleme zukünftig zu lösen und die gewohnte Qualität sicherzustellen.",
                        "Versichern Sie ihm, dass die Servicequalität wiederhergestellt wird.",
                        "Verwenden Sie eine höfliche und formelle Sprache.",
                        "Beenden Sie die E-Mail mit einer passenden Grußformel (z.B. 'Mit freundlichen Grüßen')."
                    ]
                }
            }
        };
        
        // Merge with provided options
        super({...defaultOptions, ...options});
        
        // Initialize checklist statuses
        this.checklistStatuses = {};
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
                const manifestUrl = '/data_mocktest/lesen_und_schreiben/teil_1_2_manifest.json';
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
                console.warn('Error loading teil_1_2 manifest directly:', error);
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
        
        // Set up additional elements specific to Lesen und Schreiben Teil 1 & 2
        this.elements.teamleiterEmailContent = document.getElementById('teamleiter-email-content');
        this.elements.kundeEmailContent = document.getElementById('kunde-email-content');
        this.elements.questionsContainer = document.getElementById('questions-container');
        this.elements.writingTask = document.getElementById('writing-task');
        this.elements.writingArea = document.getElementById('writing-area');
        this.elements.checklist = document.getElementById('checklist');
        this.elements.checklistItemsContainer = document.getElementById('checklist-items-container');
        this.elements.checklistScore = document.getElementById('checklist-score');
    }
    
    /**
     * Validate that test data has the required structure for Lesen und Schreiben Teil 1 & 2
     * @override
     * @param {Object} data - Test data to validate
     * @returns {boolean} - Whether the data is valid
     */
    validateTestData(data) {
        return (
            data && 
            (data.beschwerde_teamleiterin || data.beschwerde_teamleiter) && 
            (data.beschwerde_kunde || data.beschwerde_kundin) && 
            Array.isArray(data.aufgaben_list) && 
            data.aufgaben_list.length > 0 &&
            data.schreibaufgabe && 
            data.schreibaufgabe.aufgaben_text &&
            Array.isArray(data.schreibaufgabe.check_list)
        );
    }
    
    /**
     * Display the Lesen und Schreiben Teil 1 & 2 test
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
        
        // Clear previous answers
        this.userAnswers = {};
        
        // Clear writing area
        if (this.elements.writingArea) {
            this.elements.writingArea.value = '';
        }
        
        // Hide checklist
        if (this.elements.checklist) {
            this.elements.checklist.style.display = 'none';
        }
        
        // Set instructions if not already set in the HTML
        if (this.elements.instructions && (!this.elements.instructions.textContent || this.elements.instructions.textContent.trim() === '')) {
            this.elements.instructions.textContent = this.config.defaultInstructions;
        }
        
        // Display teamleiter email content
        if (this.elements.teamleiterEmailContent) {
            const teamleiterEmail = test.beschwerde_teamleiterin || test.beschwerde_teamleiter;
            if (teamleiterEmail && teamleiterEmail.text) {
                this.elements.teamleiterEmailContent.innerHTML = this.formatText(teamleiterEmail.text);
            }
        } else {
            console.error('Teamleiter email content element not found!');
        }
        
        // Display kunde email content
        if (this.elements.kundeEmailContent) {
            const kundeEmail = test.beschwerde_kunde || test.beschwerde_kundin;
            if (kundeEmail && kundeEmail.text) {
                this.elements.kundeEmailContent.innerHTML = this.formatText(kundeEmail.text);
            }
        } else {
            console.error('Kunde email content element not found!');
        }
        
        // Display questions
        this.displayQuestions(test.aufgaben_list);
        
        // Display writing task
        if (this.elements.writingTask && test.schreibaufgabe && test.schreibaufgabe.aufgaben_text) {
            this.elements.writingTask.innerHTML = `<h3>Schreibaufgabe:</h3><p>${test.schreibaufgabe.aufgaben_text}</p>`;
        }

        // Make sure the UI is properly updated
        if (this.elements.loading) {
            this.elements.loading.classList.add('loaded');
            Utils.hideElement(this.elements.loading);
        }
        
        if (this.elements.testContent) {
            this.elements.testContent.classList.remove('hidden');
            Utils.showElement(this.elements.testContent);
        }
    }
    
    /**
     * Format the text content with proper markdown-like parsing
     * @param {string} text - The text to format
     * @returns {string} - Formatted HTML
     */
    formatText(text) {
        // Check if marked library is available
        if (typeof marked !== 'undefined') {
            try {
                // Remove markdown code block markers if present
                let cleanText = text;
                if (text.startsWith('```markdown\n')) {
                    cleanText = text.substring('```markdown\n'.length);
                    if (cleanText.endsWith('\n```')) {
                        cleanText = cleanText.substring(0, cleanText.length - 4);
                    }
                }
                
                // Configure marked options
                marked.setOptions({
                    breaks: true,        // Convert \n to <br>
                    gfm: true,           // GitHub Flavored Markdown
                    headerIds: true,     // Add ids to headers for linking
                    mangle: false,       // Don't mangle header IDs
                    sanitize: false,     // Don't sanitize HTML
                    silent: false,       // Show errors
                    smartLists: true,    // Use smarter list behavior
                    smartypants: true,   // Use "smart" typographic punctuation
                    xhtml: false         // Don't close single tags with /
                });
                
                // Use marked to parse markdown
                return marked.parse(cleanText);
            } catch (error) {
                console.error('Error parsing markdown with marked:', error);
                // Fall back to the basic parsing if marked fails
                return this.basicMarkdownParse(text);
            }
        } else {
            console.warn('Marked library not available, using basic markdown parsing');
            return this.basicMarkdownParse(text);
        }
    }
    
    /**
     * Basic markdown parsing for fallback
     * @param {string} text - The markdown text to parse
     * @returns {string} - Simple HTML formatted text
     */
    basicMarkdownParse(text) {
        // Remove markdown code block markers if present
        let cleanText = text;
        if (text.startsWith('```markdown\n')) {
            cleanText = text.substring('```markdown\n'.length);
            if (cleanText.endsWith('\n```')) {
                cleanText = cleanText.substring(0, cleanText.length - 4);
            }
        }
        
        let html = cleanText
            // Convert bold (**text**)
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            // Convert italic (*text*)
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            // Convert lists
            .replace(/^- (.*)/gm, '<li>$1</li>')
            // Convert headers
            .replace(/^### (.*)/gm, '<h3>$1</h3>')
            .replace(/^## (.*)/gm, '<h2>$1</h2>')
            .replace(/^# (.*)/gm, '<h1>$1</h1>')
            // Convert line breaks
            .replace(/\n/g, '<br>');
        
        // Wrap lists in <ul> tags
        if (html.includes('<li>')) {
            html = html.replace(/(<li>.*?<\/li>)/g, '<ul>$1</ul>');
            // Fix nested lists
            html = html.replace(/<\/ul><ul>/g, '');
        }
        
        return html;
    }
    
    /**
     * Display multiple choice questions
     * @param {Array} questions - Array of question objects
     */
    displayQuestions(questions) {
        if (!this.elements.questionsContainer || !questions || !Array.isArray(questions)) return;
        
        // Clear previous questions
        this.elements.questionsContainer.innerHTML = '';
        
        // Add header for questions section
        const questionsHeader = document.createElement('h3');
        questionsHeader.textContent = 'Leseverstehen Aufgaben:';
        this.elements.questionsContainer.appendChild(questionsHeader);
        
        // Create and add each question
        questions.forEach((question, index) => {
            const questionDiv = document.createElement('div');
            questionDiv.className = 'question';
            questionDiv.dataset.index = index;
            
            const questionText = document.createElement('div');
            questionText.className = 'question-text';
            questionText.textContent = `${index + 1}. ${question.frage}`;
            questionDiv.appendChild(questionText);
            
            const optionsDiv = document.createElement('div');
            optionsDiv.className = 'options';
            
            // Create radio buttons for each option
            this.createMultipleChoiceOptions(optionsDiv, question.optionen, index);
            
            questionDiv.appendChild(optionsDiv);
            this.elements.questionsContainer.appendChild(questionDiv);
        });
    }
    
    /**
     * Create multiple choice options (radio buttons)
     * @param {HTMLElement} container - Container element for options
     * @param {Array} options - Array of option objects
     * @param {number} questionIndex - Index of the current question
     */
    createMultipleChoiceOptions(container, options, questionIndex) {
        if (!container || !options || !Array.isArray(options)) return;
        
        options.forEach(option => {
            const optionDiv = document.createElement('div');
            optionDiv.className = 'option';
            optionDiv.dataset.key = option.key;
            optionDiv.dataset.questionIndex = questionIndex;
            
            const radio = document.createElement('input');
            radio.type = 'radio';
            radio.name = `question-${questionIndex}`;
            radio.value = option.key;
            radio.id = `q${questionIndex}-${option.key}`;
            
            const label = document.createElement('label');
            label.className = 'option-text';
            label.htmlFor = `q${questionIndex}-${option.key}`;
            label.textContent = `${option.key}) ${option.text}`;
            
            optionDiv.appendChild(radio);
            optionDiv.appendChild(label);
            container.appendChild(optionDiv);
            
            // Add click handler
            optionDiv.addEventListener('click', this.handleOptionClick.bind(this));
        });
    }
    
    /**
     * Handle click on a multiple choice option
     * @param {Event} event - Click event
     */
    handleOptionClick(event) {
        const optionDiv = event.currentTarget;
        const radio = optionDiv.querySelector('input[type="radio"]');
        const questionIndex = parseInt(optionDiv.dataset.questionIndex, 10);
        const selectedKey = optionDiv.dataset.key;
        
        if (!radio || isNaN(questionIndex) || !selectedKey) return;
        
        // Select the radio button
        radio.checked = true;
        
        // Update user answer
        this.userAnswers[questionIndex] = selectedKey;
        
        // Update visual selection (optional)
        const questionDiv = optionDiv.closest('.question');
        if (questionDiv) {
            const allOptions = questionDiv.querySelectorAll('.option');
            allOptions.forEach(opt => opt.classList.remove('selected'));
            optionDiv.classList.add('selected');
        }
    }
    
    /**
     * Set up event listeners
     * @override
     */
    setupEventListeners() {
        // Call the parent method to set up basic event listeners
        super.setupEventListeners();
        
        // Additional event listeners for interactive checklist
        document.addEventListener('click', (event) => {
            // Check if the click was on a status button
            if (event.target.classList.contains('status-button')) {
                this.handleChecklistStatusChange(event);
            }
        });
    }
    
    /**
     * Handle clicks on checklist status buttons
     * @param {Event} event - Click event
     */
    handleChecklistStatusChange(event) {
        const button = event.target;
        const itemId = button.dataset.itemId;
        const status = button.dataset.status;
        
        if (!itemId || !status) return;
        
        // Get all status buttons for this item
        const itemButtons = document.querySelectorAll(`.status-button[data-item-id="${itemId}"]`);
        
        // Remove active class from all buttons
        itemButtons.forEach(btn => btn.classList.remove('active'));
        
        // Add active class to the clicked button
        button.classList.add('active');
        
        // Update status in our tracking object
        this.checklistStatuses[itemId] = status;
        
        // Update the checklist score
        this.updateChecklistScore();
    }
    
    /**
     * Update the checklist score based on current statuses
     */
    updateChecklistScore() {
        if (!this.elements.checklistScore || !this.currentTest?.schreibaufgabe?.check_list) return;
        
        const totalItems = this.currentTest.schreibaufgabe.check_list.length;
        let doneCount = 0;
        let notNecessaryCount = 0;
        let notDoneCount = 0;
        
        // Count statuses
        Object.values(this.checklistStatuses).forEach(status => {
            if (status === 'done') doneCount++;
            else if (status === 'not-necessary') notNecessaryCount++;
            else if (status === 'not-done') notDoneCount++;
        });
        
        // Calculate relevant items (total minus not necessary)
        const relevantItems = totalItems - notNecessaryCount;
        
        // Calculate percentage of done items out of relevant items
        let percentage = relevantItems > 0 ? Math.round((doneCount / relevantItems) * 100) : 0;
        
        // Update the score display
        this.elements.checklistScore.innerHTML = `
            <div>Erledigte Punkte: ${doneCount} / ${relevantItems} (${percentage}%)</div>
            <div>Nicht notwendige Punkte: ${notNecessaryCount}</div>
            <div>Nicht erledigte Punkte: ${notDoneCount}</div>
        `;
        
        console.log(`Checklist score updated: ${doneCount}/${relevantItems} done (${percentage}%), ${notNecessaryCount} not necessary, ${notDoneCount} not done`);
    }
    
    /**
     * Check user answers against correct answers
     * @override
     */
    checkAnswers() {
        if (!this.currentTest || !this.currentTest.aufgaben_list) {
            console.error('No current test loaded');
            return;
        }
        
        console.log(`Checking answers for test: ${this.currentTest._sourceFilename || 'unknown'}`);
        
        // Reset checklist statuses
        this.checklistStatuses = {};
        
        // Check multiple choice questions
        let correctCount = 0;
        const totalQuestions = this.currentTest.aufgaben_list.length;
        
        // Process each question
        this.currentTest.aufgaben_list.forEach((question, index) => {
            const userAnswer = this.userAnswers[index];
            const correctAnswer = question.loesung;
            
            console.log(`Question ${index + 1}: User answered "${userAnswer || 'none'}", correct answer is "${correctAnswer}"`);
            
            // Find the question div
            const questionDiv = this.elements.questionsContainer.querySelector(`.question[data-index="${index}"]`);
            if (!questionDiv) return;
            
            // Find all options for this question
            const options = questionDiv.querySelectorAll('.option');
            
            // Mark each option as correct or incorrect
            options.forEach(option => {
                const optionKey = option.dataset.key;
                if (optionKey === correctAnswer) {
                    option.classList.add('correct');
                } else if (optionKey === userAnswer && userAnswer !== correctAnswer) {
                    option.classList.add('incorrect');
                }
            });
            
            // Count correct answers
            if (userAnswer === correctAnswer) {
                correctCount++;
            }
        });
        
        // Calculate score
        const scorePercentage = totalQuestions > 0 ? Math.round((correctCount / totalQuestions) * 100) : 0;
        console.log(`Score: ${correctCount}/${totalQuestions} (${scorePercentage}%)`);
        
        // Display result
        if (this.elements.score) {
            this.elements.score.innerHTML = `
                <p>Leseverstehen: ${correctCount} von ${totalQuestions} Fragen richtig beantwortet (${scorePercentage}%)</p>
            `;
        }
        
        // Check if user has written anything in the writing area
        if (this.elements.writingArea) {
            const writingText = this.elements.writingArea.value.trim();
            console.log(`Writing task: User has ${writingText ? 'written' : 'not written'} a response (${writingText.length} characters)`);
        }
        
        // Show writing task checklist
        if (this.elements.checklist && this.elements.checklistItemsContainer && this.currentTest.schreibaufgabe && this.currentTest.schreibaufgabe.check_list) {
            console.log('Displaying interactive writing task checklist as table');
            this.elements.checklist.style.display = 'block';
            
            // Clear previous checklist
            this.elements.checklistItemsContainer.innerHTML = '';
            
            // Create table structure
            const table = document.createElement('table');
            table.className = 'checklist-table';
            
            // Create table header
            const thead = document.createElement('thead');
            thead.className = 'checklist-table-header';
            const headerRow = document.createElement('tr');
            
            const checkpointHeader = document.createElement('th');
            checkpointHeader.textContent = 'Prüfpunkt';
            headerRow.appendChild(checkpointHeader);
            
            const statusHeader = document.createElement('th');
            statusHeader.textContent = 'Status';
            headerRow.appendChild(statusHeader);
            
            thead.appendChild(headerRow);
            table.appendChild(thead);
            
            // Create table body
            const tbody = document.createElement('tbody');
            
            // Add interactive checklist items as table rows
            this.currentTest.schreibaufgabe.check_list.forEach((item, index) => {
                // Create row
                const row = document.createElement('tr');
                row.className = 'checklist-item';
                
                // Create text cell
                const textCell = document.createElement('td');
                textCell.className = 'checklist-item-text';
                textCell.textContent = item;
                row.appendChild(textCell);
                
                // Create status cell
                const statusCell = document.createElement('td');
                
                // Create status buttons container
                const statusDiv = document.createElement('div');
                statusDiv.className = 'checklist-status';
                
                // Add done button
                const doneBtn = document.createElement('button');
                doneBtn.className = 'status-button status-done';
                doneBtn.textContent = 'Erledigt';
                doneBtn.dataset.itemId = index;
                doneBtn.dataset.status = 'done';
                statusDiv.appendChild(doneBtn);
                
                // Add not necessary button
                const notNecessaryBtn = document.createElement('button');
                notNecessaryBtn.className = 'status-button status-not-necessary';
                notNecessaryBtn.textContent = 'Nicht notwendig';
                notNecessaryBtn.dataset.itemId = index;
                notNecessaryBtn.dataset.status = 'not-necessary';
                statusDiv.appendChild(notNecessaryBtn);
                
                // Add not done button
                const notDoneBtn = document.createElement('button');
                notDoneBtn.className = 'status-button status-not-done';
                notDoneBtn.textContent = 'Nicht erledigt';
                notDoneBtn.dataset.itemId = index;
                notDoneBtn.dataset.status = 'not-done';
                statusDiv.appendChild(notDoneBtn);
                
                // Add status buttons to cell
                statusCell.appendChild(statusDiv);
                
                // Add cell to row
                row.appendChild(statusCell);
                
                // Add row to table body
                tbody.appendChild(row);
            });
            
            // Add table body to table
            table.appendChild(tbody);
            
            // Add table to container
            this.elements.checklistItemsContainer.appendChild(table);
            
            // Initialize checklist score display
            this.updateChecklistScore();
        }
        
        // Show results and new test button
        if (this.elements.results) {
            this.elements.results.classList.remove('hidden');
        }
        
        if (this.elements.finishButton) {
            this.elements.finishButton.classList.add('hidden');
        }
        
        if (this.elements.newTestButton) {
            this.elements.newTestButton.classList.remove('hidden');
        }
        
        console.log('Check completed, results displayed');
    }
    
    /**
     * Return a static list of test files as a fallback
     * @returns {Array} - List of test file names
     */
    static getFallbackFileList() {
        return [
            "mock_1.json",
            "mock_2.json",
            "mock_3.json",
            "mock_4.json",
            "mock_5.json",
            "mock_6.json"
        ];
    }
    
    /**
     * Fetch a single test data file
     * @param {string} filename - Name of the file to fetch
     * @returns {Promise<Object|null>} - Test data or null if fetch failed
     */
    async fetchTestData(filename) {
        try {
            // console.log(`Fetching test file: ${filename}`);
            const response = await fetch(`${this.config.testDataDir}/${filename}`);
            
            if (!response.ok) {
                throw new Error(`Failed to fetch ${filename}: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            // Validate the data structure
            if (this.validateTestData(data)) {
                // Store the source filename in the test data for later reference
                data._sourceFilename = filename;
                // console.log(`Successfully loaded test: ${filename}`);
                return data;
            } else {
                console.warn(`Test data in ${filename} has invalid format`);
                return null;
            }
        } catch (error) {
            console.error(`Error fetching test data from ${filename}:`, error);
            return null;
        }
    }
    
    /**
     * Load the default test data
     */
    loadDefaultTest() {
        console.log('Loading default test data...');
        // If we have default test data in config, use that
        if (this.config.defaultTestData && this.validateTestData(this.config.defaultTestData)) {
            console.log('Loading default test data from config');
            this.currentTest = this.config.defaultTestData;
            
            // Set a filename identifier for the default test
            this.currentTest._sourceFilename = 'default_test_data';
            
            this.displayTest(this.currentTest);
        } else {
            // Otherwise show an error
            console.error('No valid default test data available');
            if (this.elements.loading) {
                this.elements.loading.innerHTML = `
                    <div class="error">
                        <p>Leider konnte kein Test geladen werden.</p>
                        <p>Bitte versuchen Sie es später noch einmal oder kontaktieren Sie den Administrator.</p>
                    </div>
                `;
                Utils.showElement(this.elements.loading);
            }
            Utils.hideElement(this.elements.testContent);
        }
    }
    
    /**
     * Initialize the test engine
     * @override
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
            
        } catch (error) {
            console.error('Error initializing test engine:', error);
            this.loadDefaultTest();
        }
    }
    
    /**
     * Load and display a random test
     */
    loadRandomTest() {
        console.log('Loading random test...');
        Utils.showElement(this.elements.loading);
        Utils.hideElement(this.elements.testContent);
        
        if (this.allTestData.length === 0) {
            console.warn('No test data available to load a random test');
            this.loadDefaultTest();
            return;
        }
        
        try {
            // Select a random test
            const randomIndex = Math.floor(Math.random() * this.allTestData.length);
            this.currentTest = this.allTestData[randomIndex];
            
            console.log(`Selected random test: ${this.currentTest._sourceFilename}`);
            
            // Display the test
            this.displayTest(this.currentTest);
            
            // Hide results and show finish button
            if (this.elements.results) {
                this.elements.results.classList.add('hidden');
            }
            
            if (this.elements.finishButton) {
                this.elements.finishButton.classList.remove('hidden');
            }
            
            if (this.elements.newTestButton) {
                this.elements.newTestButton.classList.add('hidden');
            }
        } catch (error) {
            console.error('Error loading random test:', error);
            
            // Make sure loading is always hidden even if there's an error
            if (this.elements.loading) {
                this.elements.loading.classList.add('loaded');
                Utils.hideElement(this.elements.loading);
            }
            
            alert('Fehler beim Laden des Tests!');
        }
    }
}

export default LesenUndSchreibenTeil1_2; 