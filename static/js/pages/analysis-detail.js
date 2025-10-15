/**
 * Analysis Detail Page - Week 3-4 Enhancement
 * 
 * Features:
 * - Tabbed report interface (Overview, Security, Performance, Architecture, Refactoring)
 * - Export functionality (Markdown, PDF)
 * - Code comparison view
 * - Project context display
 */

import { apiClient } from '../api.js';

export async function renderAnalysisDetail(analysisId) {
    const app = document.getElementById('app');
    
    // Show loading state
    app.innerHTML = `
        <div class="loading-container">
            <div class="spinner"></div>
            <p>Loading analysis...</p>
        </div>
    `;
    
    try {
        // Fetch analysis detail
        const response = await apiClient.get(`/analyses/${analysisId}`);
        const analysis = response;
        
        // Render the page
        app.innerHTML = createAnalysisDetailHTML(analysis);
        
        // Attach event listeners
        attachAnalysisDetailListeners(analysis);
        
    } catch (error) {
        console.error('Error loading analysis:', error);
        app.innerHTML = `
            <div class="error-container">
                <h2>Failed to Load Analysis</h2>
                <p>${error.message}</p>
                <button onclick="window.router.navigate('/dashboard')" class="btn btn-primary">
                    Back to Dashboard
                </button>
            </div>
        `;
    }
}

function createAnalysisDetailHTML(analysis) {
    const scores = analysis.scores || {};
    const reports = analysis.reports || {};
    const project = analysis.project;
    
    return `
        <div class="analysis-detail-page">
            <!-- Header -->
            <div class="page-header">
                <button onclick="window.router.navigate('/dashboard')" class="btn-back">
                    ← Back to Dashboard
                </button>
                <div class="header-content">
                    <h1>Analysis Detail</h1>
                    <div class="header-meta">
                        <span class="date">${new Date(analysis.created).toLocaleDateString()}</span>
                        ${project ? `<span class="project-badge">${project.name}</span>` : ''}
                    </div>
                </div>
                <div class="header-actions">
                    <button class="btn btn-secondary" id="export-markdown-btn">
                        📄 Export Markdown
                    </button>
                    <button class="btn btn-secondary" id="export-pdf-btn" disabled title="Coming soon!">
                        📑 Export PDF
                    </button>
                    <button class="btn btn-secondary" id="compare-btn" title="Select another analysis to compare">
                        🔄 Compare
                    </button>
                </div>
            </div>
            
            <!-- Score Summary Card -->
            <div class="score-summary-card">
                <div class="score-item">
                    <div class="score-circle total-score">
                        <span class="score-value">${scores.total_score || 0}</span>
                        <span class="score-max">/25</span>
                    </div>
                    <div class="score-label">Total Score</div>
                </div>
                <div class="score-item">
                    <div class="score-circle reliability-score">
                        <span class="score-value">${scores.reliability_score || 0}</span>
                        <span class="score-max">/10</span>
                    </div>
                    <div class="score-label">Reliability</div>
                </div>
                <div class="score-item">
                    <div class="score-circle mastery-score">
                        <span class="score-value">${scores.mastery_score || 0}</span>
                        <span class="score-max">/15</span>
                    </div>
                    <div class="score-label">Mastery</div>
                </div>
            </div>
            
            ${project ? `
            <!-- Project Context -->
            <div class="project-context-card">
                <h3>📦 Project Context</h3>
                <div class="context-details">
                    <div class="context-item">
                        <strong>Stack:</strong>
                        <div class="stack-tags">
                            ${project.stack.map(tech => `<span class="tag">${tech}</span>`).join('')}
                        </div>
                    </div>
                    <div class="context-item">
                        <strong>Architecture:</strong>
                        <span class="architecture-badge">${project.architecture_type}</span>
                    </div>
                    ${project.description ? `
                    <div class="context-item">
                        <strong>Description:</strong>
                        <p>${project.description}</p>
                    </div>
                    ` : ''}
                </div>
            </div>
            ` : ''}
            
            <!-- Tabbed Reports -->
            <div class="tabbed-reports">
                <div class="tab-navigation">
                    <button class="tab-btn active" data-tab="overview">Overview</button>
                    <button class="tab-btn" data-tab="security">Security</button>
                    <button class="tab-btn" data-tab="performance">Performance</button>
                    <button class="tab-btn" data-tab="architecture">Architecture</button>
                    <button class="tab-btn" data-tab="refactoring">Refactoring</button>
                </div>
                
                <div class="tab-content">
                    <!-- Overview Tab -->
                    <div class="tab-pane active" data-tab-content="overview">
                        <h3>Analysis Summary</h3>
                        <div class="overview-section">
                            ${scores.explanation_summary ? `
                            <div class="info-box">
                                <h4>📊 Explanation</h4>
                                <p>${scores.explanation_summary}</p>
                            </div>
                            ` : ''}
                            
                            ${scores.debug_prognosis ? `
                            <div class="warning-box">
                                <h4>⚠️ Debug Prognosis</h4>
                                <p>${scores.debug_prognosis}</p>
                            </div>
                            ` : ''}
                        </div>
                        
                        <h3>Original Prompt</h3>
                        <div class="code-block">
                            <pre><code>${escapeHtml(analysis.prompt)}</code></pre>
                        </div>
                        
                        <h3>Original Code</h3>
                        <div class="code-block">
                            <pre><code class="language-python">${escapeHtml(analysis.code)}</code></pre>
                        </div>
                    </div>
                    
                    <!-- Security Tab -->
                    <div class="tab-pane" data-tab-content="security">
                        <h3>🔒 Security Analysis</h3>
                        <div class="report-content">
                            ${reports.security ? `<p>${reports.security}</p>` : '<p>No security analysis available.</p>'}
                        </div>
                    </div>
                    
                    <!-- Performance Tab -->
                    <div class="tab-pane" data-tab-content="performance">
                        <h3>⚡ Performance & Efficiency</h3>
                        <div class="report-content">
                            ${reports.efficiency ? `<p>${reports.efficiency}</p>` : '<p>No efficiency analysis available.</p>'}
                        </div>
                    </div>
                    
                    <!-- Architecture Tab -->
                    <div class="tab-pane" data-tab-content="architecture">
                        <h3>🏗️ Architecture & Modularity</h3>
                        <div class="report-content">
                            <h4>Clarity</h4>
                            ${reports.clarity ? `<p>${reports.clarity}</p>` : '<p>No clarity analysis available.</p>'}
                            
                            <h4>Modularity</h4>
                            ${reports.modularity ? `<p>${reports.modularity}</p>` : '<p>No modularity analysis available.</p>'}
                            
                            <h4>Documentation</h4>
                            ${reports.documentation ? `<p>${reports.documentation}</p>` : '<p>No documentation analysis available.</p>'}
                        </div>
                    </div>
                    
                    <!-- Refactoring Tab -->
                    <div class="tab-pane" data-tab-content="refactoring">
                        <h3>🔧 Refactored Code</h3>
                        <div class="code-block">
                            <pre><code class="language-python">${escapeHtml(analysis.refactored_code || 'No refactored code available.')}</code></pre>
                        </div>
                        
                        ${analysis.roadmap ? `
                        <h3>📋 Project Roadmap</h3>
                        <div class="roadmap-list">
                            <ul>
                                ${(Array.isArray(analysis.roadmap) ? analysis.roadmap : [analysis.roadmap]).map(step => 
                                    `<li>${step}</li>`
                                ).join('')}
                            </ul>
                        </div>
                        ` : ''}
                    </div>
                </div>
            </div>
        </div>
    `;
}

function attachAnalysisDetailListeners(analysis) {
    // Tab switching
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.dataset.tab;
            
            // Update button states
            tabButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Update pane visibility
            tabPanes.forEach(pane => {
                if (pane.dataset.tabContent === targetTab) {
                    pane.classList.add('active');
                } else {
                    pane.classList.remove('active');
                }
            });
        });
    });
    
    // Export Markdown
    document.getElementById('export-markdown-btn').addEventListener('click', async () => {
        try {
            const btn = document.getElementById('export-markdown-btn');
            btn.disabled = true;
            btn.textContent = '⏳ Generating...';
            
            const response = await apiClient.post(`/analyses/${analysis.id}/export`, {
                format: 'markdown'
            });
            
            // Create download link
            const blob = new Blob([response.content], { type: 'text/markdown' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = response.filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            btn.disabled = false;
            btn.textContent = '✅ Downloaded!';
            setTimeout(() => {
                btn.textContent = '📄 Export Markdown';
            }, 2000);
            
        } catch (error) {
            console.error('Export failed:', error);
            alert('Failed to export analysis: ' + error.message);
            document.getElementById('export-markdown-btn').disabled = false;
            document.getElementById('export-markdown-btn').textContent = '📄 Export Markdown';
        }
    });
    
    // Compare button - navigate to comparison selector
    document.getElementById('compare-btn').addEventListener('click', () => {
        // Store current analysis ID for comparison
        sessionStorage.setItem('compareAnalysisId1', analysis.id);
        window.router.navigate(`/dashboard?selectForCompare=true`);
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
