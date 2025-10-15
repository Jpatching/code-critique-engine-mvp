/**
 * Code Analysis Page
 * Main code analysis interface
 */

export async function renderAnalyzePage() {
    const app = document.getElementById('app');
    
    // Get project from URL query if present
    const urlParams = new URLSearchParams(window.location.search);
    const projectId = urlParams.get('project');

    showLoading('Loading...');

    try {
        // Fetch user's projects
        const projectsData = await apiClient.getProjects();
        
        app.innerHTML = `
            <div class="analyze-container">
                <header class="analyze-header">
                    <h1>Analyze Code</h1>
                    <a href="/dashboard" data-route class="btn-secondary">Back to Dashboard</a>
                </header>

                <form id="analyzeForm">
                    <div class="form-group">
                        <label for="projectSelect">Project (optional)</label>
                        <select id="projectSelect">
                            <option value="">None - Generic analysis</option>
                            ${projectsData.items.map(p => 
                                `<option value="${p.id}" ${p.id === projectId ? 'selected' : ''}>${escapeHtml(p.name)}</option>`
                            ).join('')}
                        </select>
                        <small>Select a project for context-aware analysis</small>
                    </div>

                    <div class="form-group">
                        <label for="promptInput">Original AI Prompt *</label>
                        <textarea id="promptInput" rows="3" required placeholder="Enter the prompt you gave to the AI..."></textarea>
                    </div>

                    <div class="form-group">
                        <label for="codeInput">AI-Generated Code *</label>
                        <textarea id="codeInput" rows="15" required placeholder="Paste the AI-generated code here..."></textarea>
                    </div>

                    <div class="form-error" id="analyzeError"></div>
                    <button type="submit" class="btn-primary">Analyze Code</button>
                </form>

                <div id="analysisResults" style="display: none;"></div>
            </div>
        `;

        setupAnalyzeForm();
    } catch (error) {
        showError(`Failed to load page: ${error.message}`);
    }
}

function setupAnalyzeForm() {
    const form = document.getElementById('analyzeForm');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const prompt = document.getElementById('promptInput').value.trim();
        const code = document.getElementById('codeInput').value.trim();
        const projectId = document.getElementById('projectSelect').value || null;
        const errorDiv = document.getElementById('analyzeError');
        const resultsDiv = document.getElementById('analysisResults');

        errorDiv.textContent = '';
        resultsDiv.style.display = 'none';

        const btn = form.querySelector('button[type="submit"]');
        btn.textContent = 'Analyzing...';
        btn.disabled = true;

        try {
            const results = await apiClient.analyzeCode(prompt, code, projectId);
            
            // Display results
            displayResults(results);
            resultsDiv.style.display = 'block';
            
            // Scroll to results
            resultsDiv.scrollIntoView({ behavior: 'smooth' });
            
        } catch (error) {
            errorDiv.textContent = `Analysis failed: ${error.message}`;
        } finally {
            btn.textContent = 'Analyze Code';
            btn.disabled = false;
        }
    });
}

function displayResults(results) {
    const resultsDiv = document.getElementById('analysisResults');
    
    resultsDiv.innerHTML = `
        <div class="results-container">
            <h2>Analysis Results</h2>
            
            <!-- Scores -->
            <div class="scores-grid">
                <div class="score-card">
                    <h3>${results.total_score}</h3>
                    <p>Total Score (out of 25)</p>
                </div>
                <div class="score-card">
                    <h3>${results.reliability_score}</h3>
                    <p>Reliability (out of 10)</p>
                </div>
                <div class="score-card">
                    <h3>${results.mastery_score}</h3>
                    <p>Mastery (out of 15)</p>
                </div>
            </div>

            <!-- Explanation -->
            <div class="result-section">
                <h3>Summary</h3>
                <p>${escapeHtml(results.explanation_summary)}</p>
            </div>

            <!-- Debug Prognosis -->
            ${results.debug_prognosis ? `
                <div class="result-section alert-warning">
                    <h3>⚠️ Debug Prognosis</h3>
                    <p>${escapeHtml(results.debug_prognosis)}</p>
                </div>
            ` : ''}

            <!-- Reports -->
            <div class="reports-grid">
                ${renderReport('Clarity', results.clarity)}
                ${renderReport('Modularity', results.modularity)}
                ${renderReport('Efficiency', results.efficiency)}
                ${renderReport('Security', results.security)}
                ${renderReport('Documentation', results.documentation)}
            </div>

            <!-- Refactored Code -->
            ${results.refactored_code ? `
                <div class="result-section">
                    <h3>Refactored Code</h3>
                    <pre><code>${escapeHtml(results.refactored_code)}</code></pre>
                </div>
            ` : ''}

            <!-- Roadmap -->
            ${results.project_roadmap && results.project_roadmap.length > 0 ? `
                <div class="result-section">
                    <h3>Architectural Roadmap</h3>
                    <ol class="roadmap-list">
                        ${results.project_roadmap.map(step => `<li>${escapeHtml(step)}</li>`).join('')}
                    </ol>
                </div>
            ` : ''}
        </div>
    `;
}

function renderReport(title, content) {
    return `
        <div class="report-card">
            <h4>${title}</h4>
            <p>${escapeHtml(content || 'No report available')}</p>
        </div>
    `;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
