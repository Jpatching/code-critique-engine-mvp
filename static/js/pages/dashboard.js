/**
 * Dashboard Page
 * Shows user's projects and recent analyses
 */

export async function renderDashboardPage() {
    const app = document.getElementById('app');
    showLoading('Loading dashboard...');

    try {
        // Fetch projects and stats in parallel
        const [projectsData, stats] = await Promise.all([
            apiClient.getProjects(),
            apiClient.getAnalysisStats()
        ]);

        app.innerHTML = `
            <div class="dashboard-container">
                <header class="dashboard-header">
                    <h1>Your Projects</h1>
                    <button id="createProjectBtn" class="btn-primary">+ New Project</button>
                </header>

                <!-- Stats Section -->
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>${stats.total_analyses}</h3>
                        <p>Total Analyses</p>
                    </div>
                    <div class="stat-card">
                        <h3>${stats.average_total_score.toFixed(1)}</h3>
                        <p>Average Score</p>
                    </div>
                    <div class="stat-card">
                        <h3>${stats.score_trend === 'improving' ? '📈' : stats.score_trend === 'declining' ? '📉' : '➡️'}</h3>
                        <p>Trend</p>
                    </div>
                </div>

                <!-- Projects Section -->
                <div class="projects-grid" id="projectsGrid">
                    ${projectsData.items.length === 0 ? renderEmptyState() : ''}
                </div>
            </div>
        `;

        // Render project cards
        if (projectsData.items.length > 0) {
            const grid = document.getElementById('projectsGrid');
            projectsData.items.forEach(project => {
                grid.appendChild(createProjectCard(project));
            });
        }

        // Setup create project button
        document.getElementById('createProjectBtn').addEventListener('click', () => {
            showCreateProjectModal();
        });

    } catch (error) {
        showError(`Failed to load dashboard: ${error.message}`, true, 'renderDashboardPage()');
    }
}

function renderEmptyState() {
    return `
        <div class="empty-state">
            <h3>No projects yet</h3>
            <p>Create your first project to start analyzing code with context-aware insights.</p>
        </div>
    `;
}

function createProjectCard(project) {
    const card = document.createElement('div');
    card.className = 'project-card';
    card.innerHTML = `
        <div class="project-card-header">
            <h3>${escapeHtml(project.name)}</h3>
            <button class="btn-icon" data-project-id="${project.id}" data-action="delete" title="Delete">
                🗑️
            </button>
        </div>
        <p class="project-description">${escapeHtml(project.description || 'No description')}</p>
        ${project.stack && project.stack.length > 0 ? `
            <div class="stack-badges">
                ${project.stack.slice(0, 5).map(tech => `<span class="badge">${escapeHtml(tech)}</span>`).join('')}
                ${project.stack.length > 5 ? `<span class="badge">+${project.stack.length - 5}</span>` : ''}
            </div>
        ` : ''}
        <div class="project-card-footer">
            <span class="project-meta">${project.architecture_type || 'No architecture'}</span>
            <a href="/projects/${project.id}" data-route class="btn-secondary">View</a>
        </div>
    `;

    // Handle delete
    const deleteBtn = card.querySelector('[data-action="delete"]');
    deleteBtn.addEventListener('click', async (e) => {
        e.stopPropagation();
        if (confirm(`Delete project "${project.name}"? This cannot be undone.`)) {
            try {
                await apiClient.deleteProject(project.id);
                card.remove();
                // Check if grid is now empty
                const grid = document.getElementById('projectsGrid');
                if (grid.children.length === 0) {
                    grid.innerHTML = renderEmptyState();
                }
            } catch (error) {
                alert(`Failed to delete project: ${error.message}`);
            }
        }
    });

    return card;
}

function showCreateProjectModal() {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h2>Create New Project</h2>
                <button class="modal-close" onclick="this.closest('.modal').remove()">&times;</button>
            </div>
            <form id="createProjectForm">
                <div class="form-group">
                    <label for="projectName">Project Name *</label>
                    <input type="text" id="projectName" required maxlength="200">
                </div>
                <div class="form-group">
                    <label for="projectDescription">Description</label>
                    <textarea id="projectDescription" maxlength="2000" rows="3"></textarea>
                </div>
                <div class="form-group">
                    <label for="projectStack">Tech Stack (comma-separated)</label>
                    <input type="text" id="projectStack" placeholder="e.g., Python, Flask, React">
                    <small>Separate multiple items with commas</small>
                </div>
                <div class="form-group">
                    <label for="architectureType">Architecture Type</label>
                    <select id="architectureType">
                        <option value="">Select...</option>
                        <option value="monolith">Monolith</option>
                        <option value="microservices">Microservices</option>
                        <option value="serverless">Serverless</option>
                        <option value="modular_monolith">Modular Monolith</option>
                        <option value="other">Other</option>
                    </select>
                </div>
                <div class="form-error" id="createProjectError"></div>
                <div class="modal-footer">
                    <button type="button" class="btn-secondary" onclick="this.closest('.modal').remove()">Cancel</button>
                    <button type="submit" class="btn-primary">Create Project</button>
                </div>
            </form>
        </div>
    `;

    document.body.appendChild(modal);

    // Handle form submission
    document.getElementById('createProjectForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const name = document.getElementById('projectName').value.trim();
        const description = document.getElementById('projectDescription').value.trim();
        const stackInput = document.getElementById('projectStack').value.trim();
        const architectureType = document.getElementById('architectureType').value;
        const errorDiv = document.getElementById('createProjectError');

        // Parse stack
        const stack = stackInput ? stackInput.split(',').map(s => s.trim()).filter(s => s) : [];

        const projectData = {
            name,
            description: description || null,
            stack: stack.length > 0 ? stack : null,
            architecture_type: architectureType || null
        };

        try {
            errorDiv.textContent = '';
            const btn = e.target.querySelector('button[type="submit"]');
            btn.textContent = 'Creating...';
            btn.disabled = true;

            await apiClient.createProject(projectData);
            modal.remove();
            // Reload dashboard
            renderDashboardPage();
        } catch (error) {
            errorDiv.textContent = error.message;
            const btn = e.target.querySelector('button[type="submit"]');
            btn.textContent = 'Create Project';
            btn.disabled = false;
        }
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
