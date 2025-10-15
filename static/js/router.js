/**
 * Client-side Router
 * Handles SPA navigation without page reloads
 */

class Router {
    constructor() {
        this.routes = {};
        this.currentPath = '';
        this.init();
    }

    init() {
        // Handle initial page load
        window.addEventListener('load', () => {
            this.handleRoute(window.location.pathname);
        });

        // Handle browser back/forward
        window.addEventListener('popstate', () => {
            this.handleRoute(window.location.pathname);
        });

        // Handle link clicks
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-route]')) {
                e.preventDefault();
                const path = e.target.getAttribute('href');
                this.navigate(path);
            }
        });
    }

    addRoute(path, handler) {
        this.routes[path] = handler;
    }

    navigate(path) {
        window.history.pushState({}, '', path);
        this.handleRoute(path);
    }

    async handleRoute(path) {
        this.currentPath = path;

        // Extract query parameters
        const [pathname, queryString] = path.split('?');
        const queryParams = new URLSearchParams(queryString || '');

        // Check authentication
        if (pathname !== '/auth' && pathname !== '/' && !authService.isAuthenticated()) {
            this.navigate('/auth');
            return;
        }

        // Default route
        if (pathname === '/' && authService.isAuthenticated()) {
            this.navigate('/dashboard');
            return;
        } else if (pathname === '/') {
            this.navigate('/auth');
            return;
        }

        // Find and execute route handler
        const handler = this.routes[pathname];
        if (handler) {
            await handler(queryParams);
        } else {
            // Check for dynamic routes (e.g., /projects/:id, /analysis/:id)
            for (const [route, routeHandler] of Object.entries(this.routes)) {
                const match = this.matchRoute(route, pathname);
                if (match) {
                    await routeHandler(match.params, queryParams);
                    return;
                }
            }
            // 404
            this.show404();
        }
    }

    matchRoute(route, path) {
        const routeParts = route.split('/');
        const pathParts = path.split('/');

        if (routeParts.length !== pathParts.length) {
            return null;
        }

        const params = {};
        for (let i = 0; i < routeParts.length; i++) {
            if (routeParts[i].startsWith(':')) {
                const paramName = routeParts[i].slice(1);
                params[paramName] = pathParts[i];
            } else if (routeParts[i] !== pathParts[i]) {
                return null;
            }
        }

        return { params };
    }

    show404() {
        const app = document.getElementById('app');
        app.innerHTML = `
            <div class="error-page">
                <h1>404</h1>
                <p>Page not found</p>
                <a href="/dashboard" data-route class="btn-primary">Go to Dashboard</a>
            </div>
        `;
    }
}

// Export singleton instance
const router = new Router();
