/**
 * Analysis Comparison Page - Week 3-4 Enhancement
 * 
 * Features:
 * - Side-by-side analysis comparison
 * - Score delta visualization
 * - Code diff display
 * - Improvement metrics
 */

import { apiClient } from '../api.js';

export async function renderComparison(analysisId1, analysisId2) {
    const app = document.getElementById('app');
    
    // Show loading state
    app.innerHTML = `
        <div class="loading-container">
            <div class="spinner"></div>
            <p>Comparing analyses...</p>
        </div>
    `;
    
    try {
        // Fetch comparison data
        const data = await apiClient.get(`/analyses/compare?ids=${analysisId1},${analysisId2}`);
        
        // Render the comparison
        app.innerHTML = createComparisonHTML(data);
        
        // Attach event listeners
        attachComparisonListeners();
        
    } catch (error) {
        console.error('Error loading comparison:', error);
        app.innerHTML = `
            <div class="error-container">
                <h2>Failed to Load Comparison</h2>
                <p>${error.message}</p>
                <button onclick="window.router.navigate('/dashboard')" class="btn btn-primary">
                    Back to Dashboard
                </button>
            </div>
        `;
    }
}

function createComparisonHTML(data) {
    const { analysis1, analysis2, comparison } = data;
    const scores1 = analysis1.scores || {};
    const scores2 = analysis2.scores || {};
    
    return `
        <div class="comparison-page">
            <!-- Header -->
            <div class="page-header">
                <button onclick="window.router.navigate('/dashboard')" class="btn-back">
                    ← Back to Dashboard
                </button>
                <div class="header-content">
                    <h1>Analysis Comparison</h1>
                    <p class="comparison-subtitle">Comparing two code analyses</p>
                </div>
            </div>
            
            <!-- Comparison Summary -->
            <div class="comparison-summary-card">
                <div class="trend-indicator trend-${comparison.trend}">
                    ${comparison.trend === 'improved' ? '📈' : comparison.trend === 'declined' ? '📉' : '➡️'}
                    <strong>${comparison.trend.toUpperCase()}</strong>
                </div>
                <p class="comparison-message">${comparison.summary}</p>
                
                <div class="score-deltas">
                    ${createScoreDelta('Total Score', comparison.score_deltas.total, comparison.percentage_improvements.total)}
                    ${createScoreDelta('Reliability', comparison.score_deltas.reliability, comparison.percentage_improvements.reliability)}
                    ${createScoreDelta('Mastery', comparison.score_deltas.mastery, comparison.percentage_improvements.mastery)}
                </div>
            </div>
            
            <!-- Side-by-Side Comparison -->
            <div class="side-by-side-comparison">
                <!-- Analysis 1 -->
                <div class="analysis-column">
                    <div class="column-header">
                        <h3>Analysis 1</h3>
                        <span class="analysis-date">${new Date(analysis1.created).toLocaleDateString()}</span>
                    </div>
                    
                    <div class="score-cards">
                        <div class="score-card">
                            <div class="score-label">Total</div>
                            <div class="score-value">${scores1.total_score || 0}/25</div>
                        </div>
                        <div class="score-card">
                            <div class="score-label">Reliability</div>
                            <div class="score-value">${scores1.reliability_score || 0}/10</div>
                        </div>
                        <div class="score-card">
                            <div class="score-label">Mastery</div>
                            <div class="score-value">${scores1.mastery_score || 0}/15</div>
                        </div>
                    </div>
                    
                    <div class="code-section">
                        <h4>Code</h4>
                        <div class="code-block">
                            <pre><code class="language-python">${escapeHtml(analysis1.code)}</code></pre>
                        </div>
                    </div>
                    
                    <button class="btn btn-secondary" onclick="window.router.navigate('/analysis/${analysis1.id}')">
                        View Full Analysis
                    </button>
                </div>
                
                <!-- Analysis 2 -->
                <div class="analysis-column">
                    <div class="column-header">
                        <h3>Analysis 2</h3>
                        <span class="analysis-date">${new Date(analysis2.created).toLocaleDateString()}</span>
                    </div>
                    
                    <div class="score-cards">
                        <div class="score-card">
                            <div class="score-label">Total</div>
                            <div class="score-value">${scores2.total_score || 0}/25</div>
                        </div>
                        <div class="score-card">
                            <div class="score-label">Reliability</div>
                            <div class="score-value">${scores2.reliability_score || 0}/10</div>
                        </div>
                        <div class="score-card">
                            <div class="score-label">Mastery</div>
                            <div class="score-value">${scores2.mastery_score || 0}/15</div>
                        </div>
                    </div>
                    
                    <div class="code-section">
                        <h4>Code</h4>
                        <div class="code-block">
                            <pre><code class="language-python">${escapeHtml(analysis2.code)}</code></pre>
                        </div>
                    </div>
                    
                    <button class="btn btn-secondary" onclick="window.router.navigate('/analysis/${analysis2.id}')">
                        View Full Analysis
                    </button>
                </div>
            </div>
            
            <!-- Key Improvements Section -->
            <div class="improvements-section">
                <h3>Key Insights</h3>
                <div class="insights-grid">
                    ${createInsightCard('Security', analysis1.reports?.security, analysis2.reports?.security)}
                    ${createInsightCard('Performance', analysis1.reports?.efficiency, analysis2.reports?.efficiency)}
                    ${createInsightCard('Architecture', analysis1.reports?.modularity, analysis2.reports?.modularity)}
                </div>
            </div>
        </div>
    `;
}

function createScoreDelta(label, delta, percentage) {
    const isPositive = delta > 0;
    const isNegative = delta < 0;
    const deltaClass = isPositive ? 'positive' : isNegative ? 'negative' : 'neutral';
    const arrow = isPositive ? '↑' : isNegative ? '↓' : '→';
    
    return `
        <div class="delta-item ${deltaClass}">
            <div class="delta-label">${label}</div>
            <div class="delta-value">
                <span class="delta-arrow">${arrow}</span>
                <span class="delta-number">${Math.abs(delta)}</span>
                <span class="delta-percentage">(${percentage > 0 ? '+' : ''}${percentage}%)</span>
            </div>
        </div>
    `;
}

function createInsightCard(title, report1, report2) {
    // Simplified insight - in real implementation, could do text diff/analysis
    const hasImprovement = report2 && report2.length > report1?.length;
    
    return `
        <div class="insight-card">
            <h4>${title}</h4>
            <p class="insight-status">
                ${hasImprovement ? '✅ Analysis expanded in version 2' : '📝 Similar depth in both versions'}
            </p>
        </div>
    `;
}

function attachComparisonListeners() {
    // Add any interactive features here
    console.log('Comparison view loaded');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
