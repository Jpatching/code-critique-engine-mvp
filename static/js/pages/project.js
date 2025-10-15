/**
 * Project Detail Page
 * Shows project details and analysis history
 */

export async function renderProjectPage(projectId) {
    const app = document.getElementById('app');
    showLoading('Loading project...');

    try {
        const [project, analyses, stats] = await Promise.all([
            apiClient.getProject(projectId),
            apiClient.getAnalyses(projectId),
            apiClient.getAnalysisStats(projectId)
        ]);

        app.innerHTML = `
            <div class="project-container">
                <header class="project-header">
                    <div>
                        <h1>${escapeHtml(project.name)}</h1>
                        <p class="project-meta">${escapeHtml(project.description || 'No description')}</p>
                    </div>
                    <div class="project-actions">
                        <a href="/analyze?project=${project.id}" data-route class="btn-primary">Analyze Code</a>
                        <a href="/dashboard" data-route class="btn-secondary">Back to Dashboard</a>
                    </div>
                </header>

                <!-- Project Info -->
                <div class="project-info-grid">
                    <div class="info-card">
                        <h3>Architecture</h3>
                        <p>${project.architecture_type || 'Not specified'}</p>
                    </div>
                    <div class="info-card">
                        <h3>Tech Stack</h3>
                        <p>${project.stack && project.stack.length > 0 ? project.stack.join(', ') : 'Not specified'}</p>
                    </div>
                    <div class="info-card">
                        <h3>Analyses</h3>
                        <p>${stats.total_analyses}</p>
                    </div>
                    <div class="info-card">
                        <h3>Avg Score</h3>
                        <p>${stats.average_total_score.toFixed(1)} / 25</p>
                    </div>
                </div>

                <!-- Analysis History -->
                <section class="analysis-history">
                    <h2>Analysis History</h2>
                    ${analyses.items.length === 0 ? renderEmptyAnalyses() : renderAnalysesList(analyses.items)}
                </section>
            </div>
        `;
        
        // Setup comparison checkboxes if analyses exist
        if (analyses.items.length > 1) {
            setupComparisonCheckboxes();
        }
        
    } catch (error) {
        showError(`Failed to load project: ${error.message}`);
    }
}

function renderEmptyAnalyses() {
    return `
        <div class="empty-state">
            <p>No analyses yet. Start analyzing code for this project!</p>
        </div>
    `;
}

function renderAnalysesList(analyses) {
    return `
        <div class="analyses-list">
            ${analyses.length > 1 ? `
                <div class="analysis-list-actions">
                    <button id="compareSelectedBtn" class="btn-secondary" style="display: none;">
                        🔄 Compare Selected
                    </button>
                    <span id="selectionHint" class="hint-text">Select 2 analyses to compare</span>
                </div>
            ` : ''}
            ${analyses.map(analysis => `
                <div class="analysis-item" data-analysis-id="${analysis.id}">
                    ${analyses.length > 1 ? `
                        <input type="checkbox" class="analysis-checkbox" data-id="${analysis.id}" />
                    ` : ''}
                    <div class="analysis-content">
                        <h4>Analysis from ${new Date(analysis.created).toLocaleString()}</h4>
                        <p class="analysis-preview">${escapeHtml(analysis.code_preview)}</p>
                        <div class="analysis-scores">
                            <span class="score-badge">Total: ${analysis.scores.total_score}/25</span>
                            <span class="score-badge">Reliability: ${analysis.scores.reliability_score}/10</span>
                            <span class="score-badge">Mastery: ${analysis.scores.mastery_score}/15</span>
                        </div>
                    </div>
                    <div class="analysis-actions">
                        <button onclick="viewAnalysisDetail('${analysis.id}')" class="btn-secondary">📊 View Details</button>
                        <button onclick="deleteAnalysis('${analysis.id}')" class="btn-icon" title="Delete">🗑️</button>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Global functions for analysis actions
window.viewAnalysisDetail = async function(analysisId) {
    window.router.navigate(`/analysis/${analysisId}`);
};

// Setup comparison checkboxes (called after rendering)
function setupComparisonCheckboxes() {
    const checkboxes = document.querySelectorAll('.analysis-checkbox');
    const compareBtn = document.getElementById('compareSelectedBtn');
    const hint = document.getElementById('selectionHint');
    
    if (!checkboxes.length) return;
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const selected = Array.from(checkboxes).filter(cb => cb.checked);
            
            if (selected.length === 2) {
                compareBtn.style.display = 'inline-block';
                hint.style.display = 'none';
            } else {
                compareBtn.style.display = 'none';
                hint.style.display = 'inline';
            }
            
            // Disable other checkboxes if 2 are selected
            if (selected.length === 2) {
                checkboxes.forEach(cb => {
                    if (!cb.checked) cb.disabled = true;
                });
            } else {
                checkboxes.forEach(cb => cb.disabled = false);
            }
        });
    });
    
    if (compareBtn) {
        compareBtn.addEventListener('click', () => {
            const selected = Array.from(checkboxes).filter(cb => cb.checked);
            const ids = selected.map(cb => cb.dataset.id);
            window.router.navigate(`/compare?id1=${ids[0]}&id2=${ids[1]}`);
        });
    }
}

window.deleteAnalysis = async function(analysisId) {
    if (confirm('Delete this analysis?')) {
        try {
            await apiClient.deleteAnalysis(analysisId);
            location.reload(); // Reload page
        } catch (error) {
            alert(`Failed to delete: ${error.message}`);
        }
    }
};
