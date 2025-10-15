"""
Analysis API Endpoints

This module handles code analysis requests with proper validation,
error handling, and response formatting with optional project context.
"""
from flask import Blueprint, request, jsonify
from app.services.ai_service import AIAnalysisService
from app.services.pocketbase_service import PocketBaseService
from app.utils.validation import validate_code_input, validate_prompt_input, ValidationError
from app.api.auth import require_auth

analysis_bp = Blueprint('analysis', __name__)
ai_service = None  # Lazy initialization
pb_service = PocketBaseService()


def get_ai_service():
    """Get or initialize the AI service"""
    global ai_service
    if ai_service is None:
        ai_service = AIAnalysisService()
    return ai_service


@analysis_bp.route('/analyze', methods=['POST'])
@require_auth
def analyze_code(current_user):
    """
    Analyze code using AI with comprehensive validation, error handling, and optional project context
    
    Expected JSON payload:
    {
        "prompt": "The original AI prompt",
        "code": "The AI-generated code to analyze",
        "project_id": "optional_project_id_for_context"
    }
    
    Returns:
        JSON response with analysis results or error information
    """
    try:
        # Parse and validate request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        # Extract and validate inputs
        try:
            prompt = validate_prompt_input(data.get('prompt', ''))
            code = validate_code_input(data.get('code', ''))
            project_id = data.get('project_id')
        except ValidationError as e:
            return jsonify({"error": f"Validation error: {str(e)}"}), 400

        # Fetch project context if project_id provided
        project_context = None
        if project_id:
            try:
                project = pb_service.pb.collection('projects').get_one(project_id)
                # Verify ownership
                if project.user_id != current_user['id']:
                    return jsonify({"error": "Unauthorized access to project"}), 403
                
                # Build context string
                project_context = f"""
Project Context:
- Name: {project.name}
- Description: {project.description or 'No description'}
- Stack: {', '.join(project.stack) if project.stack else 'Not specified'}
- Architecture: {project.architecture_type or 'Not specified'}
- Code Style Preferences: {project.code_style if project.code_style else 'Not specified'}

Given this project context, please provide analysis that aligns with the project's architecture and coding patterns.
"""
            except Exception as e:
                print(f"Failed to fetch project context: {str(e)}")
                # Continue without context rather than failing

        # Log the request (for monitoring)
        print("-" * 50)
        print(f"Analysis Request:")
        print(f"  User: {current_user['email']}")
        print(f"  Project ID: {project_id or 'None'}")
        print(f"  Prompt: {prompt[:100]}..." if len(prompt) > 100 else f"  Prompt: {prompt}")
        print(f"  Code length: {len(code)} characters")
        print("-" * 50)

        # Perform AI analysis with optional context
        try:
            service = get_ai_service()
            results = service.analyze_code(prompt, code, project_context=project_context)
            
            # Save analysis to database
            try:
                analysis_data = {
                    'user_id': current_user['id'],
                    'project_id': project_id,
                    'prompt': prompt,
                    'code': code,
                    'scores': {
                        'total_score': results.get('total_score'),
                        'reliability_score': results.get('reliability_score'),
                        'mastery_score': results.get('mastery_score'),
                        'explanation_summary': results.get('explanation_summary')
                    },
                    'reports': results.get('reports', {}),
                    'refactored_code': results.get('refactored_code'),
                    'roadmap': results.get('project_roadmap', [])
                }
                saved_analysis = pb_service.pb.collection('analyses').create(analysis_data)
                results['analysis_id'] = saved_analysis.id
                print(f"Saved analysis: {saved_analysis.id}")
            except Exception as e:
                print(f"Failed to save analysis: {str(e)}")
                # Continue without saving rather than failing
            
            # Log successful analysis
            print(f"Analysis completed successfully")
            print(f"  Total score: {results.get('total_score', 'N/A')}")
            print(f"  Reliability: {results.get('reliability_score', 'N/A')}")
            print(f"  Mastery: {results.get('mastery_score', 'N/A')}")
            
            return jsonify(results), 200
            
        except Exception as e:
            print(f"AI analysis failed: {str(e)}")
            return jsonify({
                "error": "Analysis failed",
                "details": str(e)
            }), 500

    except Exception as e:
        print(f"Unexpected error in analyze_code: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "details": "An unexpected error occurred during analysis"
        }), 500


@analysis_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring
    
    Returns:
        JSON response with service health status
    """
    try:
        # Basic health checks
        try:
            service = get_ai_service()
            ai_available = "available"
            model = service.model_name
        except Exception as e:
            ai_available = f"unavailable: {str(e)}"
            model = "none"
        
        health_status = {
            "status": "healthy",
            "service": "analysis",
            "ai_service": ai_available,
            "model": model
        }
        
        return jsonify(health_status), 200
        
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500