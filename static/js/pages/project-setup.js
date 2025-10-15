/**
 * Project Setup Page (Placeholder)
 */

export async function renderProjectSetupPage(projectId) {
    const app = document.getElementById('app');
    app.innerHTML = `
        <div class="container">
            <h1>Project Setup</h1>
            <p>Project ID: ${projectId}</p>
            <p>This feature is coming soon!</p>
            <a href="/dashboard" data-route class="btn-primary">Back to Dashboard</a>
        </div>
    `;
}
