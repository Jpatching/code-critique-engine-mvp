/**
 * API Client
 * Handles all backend API calls
 */

const API_URL = 'http://127.0.0.1:5000';

class APIClient {
    constructor() {
        this.baseURL = API_URL;
    }

    async request(endpoint, options = {}) {
        const token = authService.getToken();
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                ...options,
                headers
            });

            if (response.status === 401) {
                // Unauthorized - clear auth and redirect to login
                authService.clearAuth();
                router.navigate('/auth');
                throw new Error('Session expired');
            }

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || data.details || 'API request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Projects API
    async getProjects(page = 1, perPage = 30) {
        return this.request(`/api/projects?page=${page}&per_page=${perPage}`);
    }

    async getProject(projectId) {
        return this.request(`/api/projects/${projectId}`);
    }

    async createProject(projectData) {
        return this.request('/api/projects', {
            method: 'POST',
            body: JSON.stringify(projectData)
        });
    }

    async updateProject(projectId, projectData) {
        return this.request(`/api/projects/${projectId}`, {
            method: 'PUT',
            body: JSON.stringify(projectData)
        });
    }

    async deleteProject(projectId) {
        return this.request(`/api/projects/${projectId}`, {
            method: 'DELETE'
        });
    }

    // Analysis API
    async analyzeCode(prompt, code, projectId = null) {
        const payload = { prompt, code };
        if (projectId) {
            payload.project_id = projectId;
        }
        return this.request('/analyze', {
            method: 'POST',
            body: JSON.stringify(payload)
        });
    }

    async getAnalyses(projectId = null, page = 1, perPage = 20) {
        let url = `/api/analyses?page=${page}&per_page=${perPage}`;
        if (projectId) {
            url += `&project_id=${projectId}`;
        }
        return this.request(url);
    }

    async getAnalysis(analysisId) {
        return this.request(`/api/analyses/${analysisId}`);
    }

    async deleteAnalysis(analysisId) {
        return this.request(`/api/analyses/${analysisId}`, {
            method: 'DELETE'
        });
    }

    async getAnalysisStats(projectId = null) {
        let url = '/api/analyses/stats';
        if (projectId) {
            url += `?project_id=${projectId}`;
        }
        return this.request(url);
    }
}

// Export singleton instance
const apiClient = new APIClient();
