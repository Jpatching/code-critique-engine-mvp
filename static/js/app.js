/**
 * Main Application Entry Point
 * Registers routes and initializes the application
 */

// Register routes
router.addRoute('/auth', async () => {
    const { renderAuthPage } = await import('./pages/auth.js');
    renderAuthPage();
});

router.addRoute('/dashboard', async () => {
    const { renderDashboardPage } = await import('./pages/dashboard.js');
    renderDashboardPage();
});

router.addRoute('/projects/:id', async (params) => {
    const { renderProjectPage } = await import('./pages/project.js');
    renderProjectPage(params.id);
});

router.addRoute('/projects/:id/setup', async (params) => {
    const { renderProjectSetupPage } = await import('./pages/project-setup.js');
    renderProjectSetupPage(params.id);
});

router.addRoute('/analyze', async () => {
    const { renderAnalyzePage } = await import('./pages/analyze.js');
    renderAnalyzePage();
});

// Week 3-4 Enhancement: Analysis detail view
router.addRoute('/analysis/:id', async (params) => {
    const { renderAnalysisDetail } = await import('./pages/analysis-detail.js');
    renderAnalysisDetail(params.id);
});

// Week 3-4 Enhancement: Analysis comparison
router.addRoute('/compare', async (params, queryParams) => {
    const id1 = queryParams.get('id1');
    const id2 = queryParams.get('id2');
    
    if (!id1 || !id2) {
        window.showError('Missing analysis IDs for comparison. Please select two analyses.');
        return;
    }
    
    const { renderComparison } = await import('./pages/comparison.js');
    renderComparison(id1, id2);
});

// Helper function to show loading state
window.showLoading = function(message = 'Loading...') {
    const app = document.getElementById('app');
    app.innerHTML = `
        <div class="loading-container">
            <div class="spinner"></div>
            <p>${message}</p>
        </div>
    `;
};

// Helper function to show error
window.showError = function(message, canRetry = false, retryCallback = null) {
    const app = document.getElementById('app');
    app.innerHTML = `
        <div class="error-container">
            <h2>Error</h2>
            <p>${message}</p>
            ${canRetry ? `<button onclick="${retryCallback}" class="btn-primary">Retry</button>` : ''}
            <a href="/dashboard" data-route class="btn-secondary">Go to Dashboard</a>
        </div>
    `;
};

console.log('Code Critique Engine initialized');
