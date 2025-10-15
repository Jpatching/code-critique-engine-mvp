"""
Analyses History API Endpoints

This module handles retrieval and management of saved code analyses.
"""
from flask import Blueprint, request, jsonify
from app.services.pocketbase_service import PocketBaseService
from app.api.auth import require_auth

analyses_bp = Blueprint('analyses', __name__)
pb_service = PocketBaseService()


@analyses_bp.route('/analyses', methods=['GET'])
@require_auth
def list_analyses(current_user):
    """
    List all analyses for the authenticated user with optional project filtering
    
    Query parameters:
    - project_id: Filter by project (optional)
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20, max: 100)
    
    Returns:
        JSON response with paginated analyses
    """
    try:
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)
        project_id = request.args.get('project_id')
        
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 20
        
        # Build filter
        filter_str = f'user_id = "{current_user["id"]}"'
        if project_id:
            filter_str += f' && project_id = "{project_id}"'
        
        # Fetch analyses
        result = pb_service.pb.collection('analyses').get_list(
            page=page,
            per_page=per_page,
            query_params={
                'filter': filter_str,
                'sort': '-created',
                'expand': 'project_id'
            }
        )
        
        # Format response
        items = []
        for item in result.items:
            analysis_data = {
                'id': item.id,
                'created': item.created,
                'updated': item.updated,
                'prompt': item.prompt[:200] + '...' if len(item.prompt) > 200 else item.prompt,
                'code_preview': item.code[:100] + '...' if len(item.code) > 100 else item.code,
                'scores': item.scores,
                'project_id': item.project_id
            }
            # Add project name if expanded
            if hasattr(item, 'expand') and item.expand and 'project_id' in item.expand:
                analysis_data['project_name'] = item.expand['project_id'].name
            items.append(analysis_data)
        
        return jsonify({
            "items": items,
            "page": result.page,
            "per_page": result.per_page,
            "total_items": result.total_items,
            "total_pages": result.total_pages
        }), 200
        
    except Exception as e:
        print(f"Error listing analyses: {str(e)}")
        return jsonify({
            "error": "Failed to list analyses",
            "details": str(e)
        }), 500


@analyses_bp.route('/analyses/<analysis_id>', methods=['GET'])
@require_auth
def get_analysis(current_user, analysis_id):
    """
    Get a specific analysis by ID (must belong to authenticated user)
    
    Returns:
        JSON response with full analysis details
    """
    try:
        # Fetch the analysis
        result = pb_service.pb.collection('analyses').get_one(
            analysis_id,
            query_params={'expand': 'project_id'}
        )
        
        # Verify ownership
        if result.user_id != current_user['id']:
            return jsonify({"error": "Unauthorized access to analysis"}), 403
        
        # Format full response
        analysis_data = {
            'id': result.id,
            'created': result.created,
            'updated': result.updated,
            'prompt': result.prompt,
            'code': result.code,
            'scores': result.scores,
            'reports': result.reports,
            'refactored_code': result.refactored_code,
            'roadmap': result.roadmap,
            'project_id': result.project_id
        }
        
        # Add project info if available
        if hasattr(result, 'expand') and result.expand and 'project_id' in result.expand:
            project = result.expand['project_id']
            analysis_data['project'] = {
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'stack': project.stack,
                'architecture_type': project.architecture_type
            }
        
        return jsonify(analysis_data), 200
        
    except Exception as e:
        if '404' in str(e) or 'not found' in str(e).lower():
            return jsonify({"error": "Analysis not found"}), 404
        print(f"Error fetching analysis: {str(e)}")
        return jsonify({
            "error": "Failed to fetch analysis",
            "details": str(e)
        }), 500


@analyses_bp.route('/analyses/<analysis_id>', methods=['DELETE'])
@require_auth
def delete_analysis(current_user, analysis_id):
    """
    Delete an analysis (must belong to authenticated user)
    
    Returns:
        JSON response confirming deletion
    """
    try:
        # First verify the analysis exists and belongs to the user
        existing = pb_service.pb.collection('analyses').get_one(analysis_id)
        if existing.user_id != current_user['id']:
            return jsonify({"error": "Unauthorized access to analysis"}), 403
        
        # Delete the analysis
        pb_service.pb.collection('analyses').delete(analysis_id)
        
        print(f"Deleted analysis: {analysis_id} for user {current_user['id']}")
        return jsonify({"message": "Analysis deleted successfully"}), 200
        
    except Exception as e:
        if '404' in str(e) or 'not found' in str(e).lower():
            return jsonify({"error": "Analysis not found"}), 404
        print(f"Error deleting analysis: {str(e)}")
        return jsonify({
            "error": "Failed to delete analysis",
            "details": str(e)
        }), 500


@analyses_bp.route('/analyses/stats', methods=['GET'])
@require_auth
def get_analysis_stats(current_user):
    """
    Get statistics about user's analyses
    
    Query parameters:
    - project_id: Filter by project (optional)
    
    Returns:
        JSON response with statistics
    """
    try:
        project_id = request.args.get('project_id')
        
        # Build filter
        filter_str = f'user_id = "{current_user["id"]}"'
        if project_id:
            filter_str += f' && project_id = "{project_id}"'
        
        # Fetch all analyses (with pagination)
        all_analyses = []
        page = 1
        while True:
            result = pb_service.pb.collection('analyses').get_list(
                page=page,
                per_page=100,
                query_params={'filter': filter_str}
            )
            all_analyses.extend(result.items)
            if page >= result.total_pages:
                break
            page += 1
        
        # Calculate statistics
        total_analyses = len(all_analyses)
        if total_analyses == 0:
            return jsonify({
                "total_analyses": 0,
                "average_total_score": 0,
                "average_reliability_score": 0,
                "average_mastery_score": 0,
                "score_trend": "no_data"
            }), 200
        
        # Extract scores
        total_scores = []
        reliability_scores = []
        mastery_scores = []
        
        for analysis in all_analyses:
            if hasattr(analysis, 'scores') and analysis.scores:
                scores = analysis.scores
                if 'total_score' in scores:
                    total_scores.append(scores['total_score'])
                if 'reliability_score' in scores:
                    reliability_scores.append(scores['reliability_score'])
                if 'mastery_score' in scores:
                    mastery_scores.append(scores['mastery_score'])
        
        # Calculate averages
        avg_total = sum(total_scores) / len(total_scores) if total_scores else 0
        avg_reliability = sum(reliability_scores) / len(reliability_scores) if reliability_scores else 0
        avg_mastery = sum(mastery_scores) / len(mastery_scores) if mastery_scores else 0
        
        # Determine trend (compare first half to second half)
        score_trend = "stable"
        if len(total_scores) >= 4:
            mid = len(total_scores) // 2
            first_half_avg = sum(total_scores[:mid]) / mid
            second_half_avg = sum(total_scores[mid:]) / (len(total_scores) - mid)
            if second_half_avg > first_half_avg + 2:
                score_trend = "improving"
            elif second_half_avg < first_half_avg - 2:
                score_trend = "declining"
        
        return jsonify({
            "total_analyses": total_analyses,
            "average_total_score": round(avg_total, 1),
            "average_reliability_score": round(avg_reliability, 1),
            "average_mastery_score": round(avg_mastery, 1),
            "score_trend": score_trend
        }), 200
        
    except Exception as e:
        print(f"Error calculating stats: {str(e)}")
        return jsonify({
            "error": "Failed to calculate statistics",
            "details": str(e)
        }), 500


@analyses_bp.route('/analyses/compare', methods=['GET'])
@require_auth
def compare_analyses(current_user):
    """
    Compare two analyses side-by-side
    
    Query params:
        ids: Comma-separated analysis IDs (e.g., ?ids=id1,id2)
    
    Returns:
        200: Comparison data with score deltas and improvements
        400: Invalid request
        404: One or more analyses not found
        500: Server error
    """
    try:
        ids_param = request.args.get('ids', '')
        
        if not ids_param:
            return jsonify({'error': 'Missing "ids" parameter'}), 400
        
        analysis_ids = [id.strip() for id in ids_param.split(',')]
        
        if len(analysis_ids) != 2:
            return jsonify({'error': 'Exactly 2 analysis IDs required'}), 400
        
        # Fetch both analyses
        analyses = []
        for analysis_id in analysis_ids:
            try:
                analysis = pb_service.pb.collection('analyses').get_one(analysis_id)
                
                # Verify ownership
                if analysis.user_id != current_user['id']:
                    return jsonify({'error': 'Unauthorized'}), 403
                
                # Format analysis data
                analysis_data = {
                    'id': analysis.id,
                    'created': analysis.created,
                    'prompt': analysis.prompt,
                    'code': analysis.code,
                    'scores': analysis.scores,
                    'reports': analysis.reports,
                    'refactored_code': analysis.refactored_code,
                    'project_id': analysis.project_id
                }
                analyses.append(analysis_data)
                
            except Exception as e:
                return jsonify({'error': f'Analysis {analysis_id} not found'}), 404
        
        # Calculate comparison metrics
        comparison = _calculate_comparison(analyses[0], analyses[1])
        
        return jsonify({
            'analysis1': analyses[0],
            'analysis2': analyses[1],
            'comparison': comparison
        }), 200
        
    except Exception as e:
        print(f"Error comparing analyses: {e}")
        return jsonify({'error': 'Failed to compare analyses'}), 500


@analyses_bp.route('/analyses/<analysis_id>/export', methods=['POST'])
@require_auth
def export_analysis(current_user, analysis_id):
    """
    Export analysis in specified format
    
    Body:
        format: 'markdown' or 'pdf'
    
    Returns:
        200: Export content or file URL
        400: Invalid format
        404: Analysis not found
        500: Server error
    """
    try:
        data = request.get_json() or {}
        export_format = data.get('format', 'markdown').lower()
        
        if export_format not in ['markdown', 'pdf']:
            return jsonify({'error': 'Invalid format. Use "markdown" or "pdf"'}), 400
        
        # Fetch analysis
        analysis = pb_service.pb.collection('analyses').get_one(
            analysis_id,
            query_params={'expand': 'project_id'}
        )
        
        # Verify ownership
        if analysis.user_id != current_user['id']:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Fetch project for context
        project = None
        if hasattr(analysis, 'expand') and analysis.expand and 'project_id' in analysis.expand:
            project = analysis.expand['project_id']
        
        # Generate export content
        if export_format == 'markdown':
            content = _generate_markdown_export(analysis, project)
            return jsonify({
                'format': 'markdown',
                'content': content,
                'filename': f"analysis_{analysis_id}.md"
            }), 200
        
        elif export_format == 'pdf':
            # PDF generation (placeholder - requires additional libraries)
            return jsonify({
                'error': 'PDF export coming soon! Use markdown export for now.'
            }), 501  # Not Implemented
        
    except Exception as e:
        if '404' in str(e) or 'not found' in str(e).lower():
            return jsonify({"error": "Analysis not found"}), 404
        print(f"Error exporting analysis: {e}")
        return jsonify({'error': 'Failed to export analysis'}), 500


def _calculate_comparison(analysis1: dict, analysis2: dict) -> dict:
    """
    Calculate comparison metrics between two analyses
    
    Args:
        analysis1: First analysis data
        analysis2: Second analysis data
    
    Returns:
        Dictionary with comparison metrics
    """
    # Extract scores safely
    scores1 = analysis1.get('scores', {})
    scores2 = analysis2.get('scores', {})
    
    a1_total = scores1.get('total_score', 0)
    a2_total = scores2.get('total_score', 0)
    a1_reliability = scores1.get('reliability_score', 0)
    a2_reliability = scores2.get('reliability_score', 0)
    a1_mastery = scores1.get('mastery_score', 0)
    a2_mastery = scores2.get('mastery_score', 0)
    
    # Calculate deltas
    total_delta = a2_total - a1_total
    reliability_delta = a2_reliability - a1_reliability
    mastery_delta = a2_mastery - a1_mastery
    
    # Calculate percentage improvements
    total_improvement = (total_delta / a1_total * 100) if a1_total > 0 else 0
    reliability_improvement = (reliability_delta / a1_reliability * 100) if a1_reliability > 0 else 0
    mastery_improvement = (mastery_delta / a1_mastery * 100) if a1_mastery > 0 else 0
    
    # Determine overall trend
    if total_delta > 0:
        trend = 'improved'
    elif total_delta < 0:
        trend = 'declined'
    else:
        trend = 'unchanged'
    
    return {
        'score_deltas': {
            'total': total_delta,
            'reliability': reliability_delta,
            'mastery': mastery_delta
        },
        'percentage_improvements': {
            'total': round(total_improvement, 1),
            'reliability': round(reliability_improvement, 1),
            'mastery': round(mastery_improvement, 1)
        },
        'trend': trend,
        'summary': _generate_comparison_summary(total_delta, reliability_delta, mastery_delta)
    }


def _generate_comparison_summary(total_delta: int, reliability_delta: int, mastery_delta: int) -> str:
    """Generate human-readable comparison summary"""
    
    if total_delta > 5:
        return "Significant improvement! Your code quality has increased substantially."
    elif total_delta > 0:
        return "Good progress! Your code shows measurable improvement."
    elif total_delta == 0:
        return "No change in overall score. Consider focusing on specific weak areas."
    elif total_delta > -5:
        return "Slight decline. Review the feedback to identify regression areas."
    else:
        return "Notable decline. This code may need significant revision."


def _generate_markdown_export(analysis, project=None) -> str:
    """
    Generate markdown-formatted export of analysis
    
    Args:
        analysis: Analysis record from PocketBase
        project: Optional project record for context
    
    Returns:
        Markdown-formatted string
    """
    scores = analysis.scores if hasattr(analysis, 'scores') else {}
    reports = analysis.reports if hasattr(analysis, 'reports') else {}
    
    md = f"""# Code Analysis Report

## Overview
**Date:** {analysis.created if hasattr(analysis, 'created') else 'N/A'}  
**Total Score:** {scores.get('total_score', 0)}/25  
**Reliability Score:** {scores.get('reliability_score', 0)}/10  
**Mastery Score:** {scores.get('mastery_score', 0)}/15  

"""
    
    # Add project context if available
    if project:
        project_stack = project.stack if hasattr(project, 'stack') else []
        project_arch = project.architecture_type if hasattr(project, 'architecture_type') else 'N/A'
        project_name = project.name if hasattr(project, 'name') else 'N/A'
        
        md += f"""## Project Context
**Project:** {project_name}  
**Stack:** {', '.join(project_stack) if project_stack else 'N/A'}  
**Architecture:** {project_arch}  

"""
    
    # Add original prompt
    if hasattr(analysis, 'prompt') and analysis.prompt:
        md += f"""## Original Prompt
```
{analysis.prompt}
```

"""
    
    # Add explanation summary
    if scores.get('explanation_summary'):
        md += f"""## Analysis Summary
{scores['explanation_summary']}

"""
    
    # Add debug prognosis
    if scores.get('debug_prognosis'):
        md += f"""## Debug Prognosis
{scores['debug_prognosis']}

"""
    
    # Add detailed reports
    md += """## Detailed Reports

"""
    
    report_sections = [
        ('clarity', 'Code Clarity'),
        ('modularity', 'Modularity'),
        ('efficiency', 'Efficiency'),
        ('security', 'Security'),
        ('documentation', 'Documentation')
    ]
    
    for key, title in report_sections:
        if reports.get(key):
            md += f"""### {title}
{reports[key]}

"""
    
    # Add refactored code
    if hasattr(analysis, 'refactored_code') and analysis.refactored_code:
        md += f"""## Refactored Code
```python
{analysis.refactored_code}
```

"""
    
    # Add project roadmap
    if hasattr(analysis, 'roadmap') and analysis.roadmap:
        md += """## Project Roadmap
"""
        roadmap = analysis.roadmap
        if isinstance(roadmap, list):
            for step in roadmap:
                md += f"- {step}\n"
        else:
            md += f"{roadmap}\n"
        md += "\n"
    
    # Add original code for reference
    if hasattr(analysis, 'code') and analysis.code:
        md += f"""## Original Code (For Reference)
```python
{analysis.code}
```

"""
    
    md += """---
*Generated by Code Critique Engine*
"""
    
    return md
