/**
 * API Service for interacting with the backend
 */
class ApiService {
    constructor() {
        this.baseUrl = window.location.origin;
    }

    /**
     * Make a generic request to the API
     * @param {string} endpoint - API endpoint to call
     * @param {string} method - HTTP method (GET, POST, PUT, DELETE)
     * @param {object} data - Data to send (for POST and PUT)
     * @returns {Promise<object>} - Response data
     */
    async request(endpoint, method = 'GET', data = null) {
        // Make sure the URL is correctly formatted for Edge
        let url = `${this.baseUrl}${endpoint}`;
        
        // Edge sometimes has issues with URLs that don't start with /
        if (!endpoint.startsWith('/')) {
            url = `${this.baseUrl}/${endpoint}`;
        }
        
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            },
            // Add credentials for cross-origin requests (helps with Edge)
            credentials: 'same-origin',
            // Prevent caching in Edge
            cache: 'no-store'
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            console.log(`[${new Date().toISOString()}] Making API request: ${method} ${url}`);
            
            // Using try-catch with setTimeout to handle Edge connection issues
            const fetchPromise = fetch(url, options);
            
            // Create a timeout promise to handle hanging connections
            const timeoutPromise = new Promise((_, reject) => {
                setTimeout(() => reject(new Error('Request timeout')), 10000);
            });
            
            // Race between fetch and timeout
            const response = await Promise.race([fetchPromise, timeoutPromise]);
            
            if (!response.ok) {
                let errorMessage = `API request failed with status ${response.status}`;
                try {
                    const errorData = await response.json();
                    errorMessage = errorData.detail || errorMessage;
                } catch (e) {
                    // If we can't parse the error response, just use the status message
                }
                console.error(`API error: ${errorMessage}`);
                throw new Error(errorMessage);
            }
            
            // Handle empty response (like for DELETE)
            if (response.status === 204) {
                return { success: true };
            }
            
            // Parse the response - handle text responses (for Edge compatibility)
            let responseData;
            const contentType = response.headers.get("content-type");
            if (contentType && contentType.indexOf("application/json") !== -1) {
                responseData = await response.json();
            } else {
                // Handle non-JSON responses
                const text = await response.text();
                try {
                    // Try to parse it as JSON anyway
                    responseData = JSON.parse(text);
                } catch (e) {
                    // If parsing fails, return as text
                    responseData = { text, success: true };
                }
            }
            
            console.log(`API response:`, responseData);
            return responseData;
        } catch (error) {
            console.error('API request error:', error);
            throw error;
        }
    }

    // Owner endpoints
    async getOwners(search = null, skip = 0, limit = 100) {
        let endpoint = `/api/owners/?skip=${skip}&limit=${limit}`;
        if (search) {
            endpoint += `&search=${encodeURIComponent(search)}`;
        }
        return this.request(endpoint);
    }

    async getOwner(id) {
        return this.request(`/api/owners/${id}`);
    }

    async createOwner(data) {
        return this.request('/api/owners/', 'POST', data);
    }

    async updateOwner(id, data) {
        return this.request(`/api/owners/${id}`, 'PUT', data);
    }

    async deleteOwner(id) {
        return this.request(`/api/owners/${id}`, 'DELETE');
    }

    // Pet endpoints
    async getPets(ownerId = null, search = null, skip = 0, limit = 100) {
        let endpoint = `/api/pets/?skip=${skip}&limit=${limit}`;
        if (ownerId) {
            endpoint += `&owner_id=${ownerId}`;
        }
        if (search) {
            endpoint += `&search=${encodeURIComponent(search)}`;
        }
        return this.request(endpoint);
    }

    async getPet(id) {
        return this.request(`/api/pets/${id}`);
    }

    async createPet(data) {
        return this.request('/api/pets/', 'POST', data);
    }

    async updatePet(id, data) {
        return this.request(`/api/pets/${id}`, 'PUT', data);
    }

    async deletePet(id) {
        return this.request(`/api/pets/${id}`, 'DELETE');
    }

    // Visit endpoints
    async getVisits(petId = null, skip = 0, limit = 100) {
        let endpoint = `/api/visits/?skip=${skip}&limit=${limit}`;
        if (petId) {
            endpoint += `&pet_id=${petId}`;
        }
        return this.request(endpoint);
    }

    async getVisit(id) {
        return this.request(`/api/visits/${id}`);
    }

    async createVisit(data) {
        return this.request('/api/visits/', 'POST', data);
    }

    async updateVisit(id, data) {
        return this.request(`/api/visits/${id}`, 'PUT', data);
    }

    async deleteVisit(id) {
        return this.request(`/api/visits/${id}`, 'DELETE');
    }

    async saveCompleteVisit(data) {
        return this.request('/api/visits/complete', 'POST', data);
    }

    async getVisitPdf(id) {
        return this.request(`/api/visits/${id}/pdf`);
    }

    // Medication endpoints
    async getMedications(search = null, skip = 0, limit = 100) {
        let endpoint = `/api/medications/?skip=${skip}&limit=${limit}`;
        if (search) {
            endpoint += `&search=${encodeURIComponent(search)}`;
        }
        return this.request(endpoint);
    }

    async incrementMedicationUsage(name) {
        return this.request(`/api/medications/${encodeURIComponent(name)}/use`, 'POST');
    }

    // Species endpoints
    async getAllSpecies() {
        return this.request('/api/species/');
    }

    // Health check
    async healthCheck() {
        return this.request('/health');
    }

    // Configuration endpoints
    async getConfig() {
        return this.request('/api/config');
    }

    async updateConfig(configData) {
        return this.request('/api/config', 'POST', configData);
    }

    // Test PDF generation
    async testPdfGeneration() {
        return this.request('/api/test-pdf');
    }
}

// Create a singleton instance
const apiService = new ApiService(); 