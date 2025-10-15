/**
 * Authentication Module
 * Handles user authentication state, token management, and auth-related operations
 */

const API_BASE = 'http://127.0.0.1:5000';

class AuthService {
    constructor() {
        this.token = localStorage.getItem('auth_token');
        this.user = null;
        this.initUser();
    }

    async initUser() {
        if (this.token) {
            try {
                const response = await fetch(`${API_BASE}/auth/me`, {
                    headers: {
                        'Authorization': `Bearer ${this.token}`
                    }
                });
                if (response.ok) {
                    this.user = await response.json();
                    this.updateUI();
                } else {
                    this.clearAuth();
                }
            } catch (error) {
                console.error('Failed to fetch user:', error);
                this.clearAuth();
            }
        }
    }

    async login(email, password) {
        try {
            const response = await fetch(`${API_BASE}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const data = await response.json();
                this.token = data.token;
                this.user = data.user;
                localStorage.setItem('auth_token', this.token);
                this.updateUI();
                return { success: true };
            } else {
                const error = await response.json();
                return { success: false, error: error.error || 'Login failed' };
            }
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }

    async signup(name, email, password, passwordConfirm) {
        try {
            const response = await fetch(`${API_BASE}/auth/signup`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name, email, password, passwordConfirm })
            });

            if (response.ok) {
                const data = await response.json();
                this.token = data.token;
                this.user = data.user;
                localStorage.setItem('auth_token', this.token);
                this.updateUI();
                return { success: true };
            } else {
                const error = await response.json();
                return { success: false, error: error.error || 'Signup failed' };
            }
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }

    async logout() {
        try {
            if (this.token) {
                await fetch(`${API_BASE}/auth/logout`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${this.token}`
                    }
                });
            }
        } catch (error) {
            console.error('Logout request failed:', error);
        } finally {
            this.clearAuth();
            window.location.href = '/auth';
        }
    }

    clearAuth() {
        this.token = null;
        this.user = null;
        localStorage.removeItem('auth_token');
        this.updateUI();
    }

    updateUI() {
        const userInfo = document.getElementById('userInfo');
        const logoutBtn = document.getElementById('logoutBtn');
        
        if (this.user && userInfo) {
            userInfo.textContent = `Hello, ${this.user.name}`;
            userInfo.style.display = 'inline';
            if (logoutBtn) logoutBtn.style.display = 'inline-block';
        } else {
            if (userInfo) userInfo.style.display = 'none';
            if (logoutBtn) logoutBtn.style.display = 'none';
        }
    }

    isAuthenticated() {
        return this.token !== null && this.user !== null;
    }

    getToken() {
        return this.token;
    }

    getUser() {
        return this.user;
    }
}

// Export singleton instance
const authService = new AuthService();

// Setup logout button
document.addEventListener('DOMContentLoaded', () => {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            if (confirm('Are you sure you want to logout?')) {
                authService.logout();
            }
        });
    }
});
