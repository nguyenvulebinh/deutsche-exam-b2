/**
 * Utility functions for TELC B2 Test Platform
 */

const Utils = {
    /**
     * Shuffles an array using Fisher-Yates algorithm
     * @param {Array} array - The array to shuffle
     * @returns {Array} - A new shuffled array
     */
    shuffleArray(array) {
        const newArray = [...array]; // Create a copy to avoid modifying the original
        for (let i = newArray.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [newArray[i], newArray[j]] = [newArray[j], newArray[i]]; // Swap elements
        }
        return newArray;
    },

    /**
     * Shows an element by removing the 'hidden' class
     * @param {string|Element} element - Element or element ID
     */
    showElement(element) {
        const el = typeof element === 'string' ? document.getElementById(element) : element;
        if (el) el.classList.remove('hidden');
    },

    /**
     * Hides an element by adding the 'hidden' class
     * @param {string|Element} element - Element or element ID
     */
    hideElement(element) {
        const el = typeof element === 'string' ? document.getElementById(element) : element;
        if (el) el.classList.add('hidden');
    },

    /**
     * Creates a DOM element with specified properties
     * @param {string} tag - Element tag name
     * @param {Object} props - Element properties
     * @param {string|Node} children - Child content (string or Node)
     * @returns {Element} - The created element
     */
    createElement(tag, props = {}, children = null) {
        const element = document.createElement(tag);
        
        // Set properties
        Object.keys(props).forEach(key => {
            if (key === 'className') {
                element.className = props[key];
            } else if (key === 'dataset') {
                Object.keys(props.dataset).forEach(dataKey => {
                    element.dataset[dataKey] = props.dataset[dataKey];
                });
            } else if (key.startsWith('on') && typeof props[key] === 'function') {
                element.addEventListener(key.slice(2).toLowerCase(), props[key]);
            } else {
                element[key] = props[key];
            }
        });
        
        // Add children
        if (children) {
            if (typeof children === 'string') {
                element.innerHTML = children;
            } else if (children instanceof Node) {
                element.appendChild(children);
            } else if (Array.isArray(children)) {
                children.forEach(child => {
                    if (typeof child === 'string') {
                        element.appendChild(document.createTextNode(child));
                    } else if (child instanceof Node) {
                        element.appendChild(child);
                    }
                });
            }
        }
        
        return element;
    },

    /**
     * Get a list of test files in a directory
     * Attempts to get a directory listing (works on some servers but not on GitHub Pages)
     * @param {string} directory - Directory path
     * @returns {Promise<Array>} - List of files or empty array if failed
     */
    async getTestFileList(directory) {
        try {
            // Try to fetch a directory listing
            const response = await fetch(directory);
            
            // If we got a successful response, try to parse it for JSON files
            if (response.ok) {
                const html = await response.text();
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const links = Array.from(doc.querySelectorAll('a'));
                
                // Extract filenames that end with .json
                const jsonFiles = links
                    .map(link => link.href)
                    .filter(href => href.endsWith('.json'))
                    .map(href => href.split('/').pop());
                
                if (jsonFiles.length > 0) {
                    console.log(`Found ${jsonFiles.length} JSON files in directory listing`);
                    return jsonFiles;
                }
            }
        } catch (error) {
            console.warn('Error getting directory listing:', error);
        }
        
        // Return empty array if failed
        return [];
    },

    /**
     * Get a fallback list of files from a manifest
     * @param {string} directory - Directory path
     * @returns {Promise<Array>} - List of files
     */
    async getFallbackFileList(directory) {
        let fileList = [];
        
        // 1. First try to use the new manifest format (preferred method for GitHub Pages)
        try {
            // Extract test type from directory (e.g., "data_mocktest/lesen/teil_1" -> "lesen/teil_1")
            const testPathParts = directory.split('/');
            const manifestBasePath = testPathParts.slice(0, testPathParts.length - 1).join('/');
            const testType = testPathParts[testPathParts.length - 1];
            
            // Try the new manifest location
            const manifestUrl = `${manifestBasePath}/${testType}_manifest.json`;
            console.log(`Loading manifest from: ${manifestUrl}`);
            
            const response = await fetch(manifestUrl);
            if (response.ok) {
                const manifest = await response.json();
                fileList = manifest.files || [];
                console.log(`Loaded ${fileList.length} files from manifest at ${manifestUrl}`);
                return fileList;
            } else {
                console.log(`Manifest not found at ${manifestUrl}, trying old location...`);
            }
        } catch (error) {
            console.warn('Error loading from new manifest format:', error);
        }
        
        // 2. If that fails, try the old manifest location
        try {
            const response = await fetch(`${directory}/file_manifest.json`);
            if (response.ok) {
                const manifest = await response.json();
                fileList = manifest.files || [];
                console.log(`Loaded ${fileList.length} files from old manifest location`);
                return fileList;
            }
        } catch (error) {
            console.warn('Error loading from old manifest location:', error);
        }
        
        // Default empty list if all else fails
        console.warn('No manifest found, falling back to empty list');
        return [];
    }
};

// Export the Utils object
export default Utils; 