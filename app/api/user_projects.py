"""
User Projects API Endpoints

This module handles CRUD operations for user-owned projects with proper
validation, error handling, authentication, and project context management.
"""
from flask import Blueprint, request, jsonify
from app.services.pocketbase_service import PocketBaseService
from app.utils.validation import ValidationError
from app.api.auth import require_auth
from functools import wraps

user_projects_bp = Blueprint('user_projects', __name__)
pb_service = PocketBaseService()


def validate_project_data(data, is_update=False):
    """Validate project creation/update data"""
    if not isinstance(data, dict):
        raise ValidationError("Request data must be a JSON object")
    
    # Name validation (required for creation)
    if not is_update or 'name' in data:
        name = data.get('name', '').strip()
        if not is_update and not name:
            raise ValidationError("Project name is required")
        if name and (len(name) < 1 or len(name) > 200):
            raise ValidationError("Project name must be 1-200 characters")
        data['name'] = name
    
    # Description validation (optional)
    if 'description' in data:
        description = data.get('description', '').strip()
        if len(description) > 2000:
            raise ValidationError("Description must be less than 2000 characters")
        data['description'] = description
    
    # Stack validation (optional array of strings)
    if 'stack' in data:
        stack = data.get('stack')
        if stack is not None:
            if not isinstance(stack, list):
                raise ValidationError("Stack must be an array")
            if len(stack) > 50:
                raise ValidationError("Stack can have maximum 50 items")
            # Validate each stack item
            for item in stack:
                if not isinstance(item, str):
                    raise ValidationError("Stack items must be strings")
                if len(item) > 50:
                    raise ValidationError("Stack item must be less than 50 characters")
        data['stack'] = stack
    
    # Architecture type validation (optional)
    if 'architecture_type' in data:
        arch_type = data.get('architecture_type')
        valid_types = ['monolith', 'microservices', 'serverless', 'modular_monolith', 'other']
        if arch_type is not None and arch_type not in valid_types:
            raise ValidationError(f"Architecture type must be one of: {', '.join(valid_types)}")
        data['architecture_type'] = arch_type
    
    # Code style validation (optional JSON object)
    if 'code_style' in data:
        code_style = data.get('code_style')
        if code_style is not None and not isinstance(code_style, dict):
            raise ValidationError("Code style must be a JSON object")
        data['code_style'] = code_style
    
    return data


@user_projects_bp.route('/projects', methods=['GET'])
@require_auth
def list_projects(current_user):
    """
    List all projects for the authenticated user
    
    Query parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 30, max: 100)
    
    Returns:
        JSON response with paginated projects
    """
    try:
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 30)), 100)
        
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 30
        
        # Fetch projects for this user
        result = pb_service.pb.collection('projects').get_list(
            page=page,
            per_page=per_page,
            query_params={
                'filter': f'user_id = "{current_user["id"]}"',
                'sort': '-created'
            }
        )
        
        return jsonify({
            "items": result.items,
            "page": result.page,
            "per_page": result.per_page,
            "total_items": result.total_items,
            "total_pages": result.total_pages
        }), 200
        
    except Exception as e:
        print(f"Error listing projects: {str(e)}")
        return jsonify({
            "error": "Failed to list projects",
            "details": str(e)
        }), 500


@user_projects_bp.route('/projects', methods=['POST'])
@require_auth
def create_project(current_user):
    """
    Create a new project for the authenticated user
    
    Expected JSON payload:
    {
        "name": "My Project",
        "description": "Optional description",
        "stack": ["Python", "Flask", "React"],
        "architecture_type": "monolith",
        "code_style": {
            "indentation": "spaces",
            "naming_convention": "snake_case"
        }
    }
    
    Returns:
        JSON response with created project
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
        
        # Validate the data
        try:
            validated_data = validate_project_data(data, is_update=False)
        except ValidationError as e:
            return jsonify({"error": f"Validation error: {str(e)}"}), 400
        
        # Add user_id to the data
        validated_data['user_id'] = current_user['id']
        
        # Create the project
        result = pb_service.pb.collection('projects').create(validated_data)
        
        print(f"Created project: {result.id} - {validated_data['name']} for user {current_user['id']}")
        return jsonify(result.__dict__), 201
        
    except Exception as e:
        print(f"Error creating project: {str(e)}")
        return jsonify({
            "error": "Failed to create project",
            "details": str(e)
        }), 500


@user_projects_bp.route('/projects/<project_id>', methods=['GET'])
@require_auth
def get_project(current_user, project_id):
    """
    Get a specific project by ID (must belong to authenticated user)
    
    Returns:
        JSON response with project details
    """
    try:
        # Fetch the project
        result = pb_service.pb.collection('projects').get_one(project_id)
        
        # Verify ownership
        if result.user_id != current_user['id']:
            return jsonify({"error": "Unauthorized access to project"}), 403
        
        return jsonify(result.__dict__), 200
        
    except Exception as e:
        if '404' in str(e) or 'not found' in str(e).lower():
            return jsonify({"error": "Project not found"}), 404
        print(f"Error fetching project: {str(e)}")
        return jsonify({
            "error": "Failed to fetch project",
            "details": str(e)
        }), 500


@user_projects_bp.route('/projects/<project_id>', methods=['PUT'])
@require_auth
def update_project(current_user, project_id):
    """
    Update a project (must belong to authenticated user)
    
    Expected JSON payload (all fields optional):
    {
        "name": "Updated name",
        "description": "Updated description",
        "stack": ["Python", "Django"],
        "architecture_type": "microservices",
        "code_style": {...}
    }
    
    Returns:
        JSON response with updated project
    """
    try:
        # First verify the project exists and belongs to the user
        existing = pb_service.pb.collection('projects').get_one(project_id)
        if existing.user_id != current_user['id']:
            return jsonify({"error": "Unauthorized access to project"}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
        
        # Validate the data
        try:
            validated_data = validate_project_data(data, is_update=True)
        except ValidationError as e:
            return jsonify({"error": f"Validation error: {str(e)}"}), 400
        
        # Update the project
        result = pb_service.pb.collection('projects').update(project_id, validated_data)
        
        print(f"Updated project: {project_id} for user {current_user['id']}")
        return jsonify(result.__dict__), 200
        
    except Exception as e:
        if '404' in str(e) or 'not found' in str(e).lower():
            return jsonify({"error": "Project not found"}), 404
        print(f"Error updating project: {str(e)}")
        return jsonify({
            "error": "Failed to update project",
            "details": str(e)
        }), 500


@user_projects_bp.route('/projects/<project_id>', methods=['DELETE'])
@require_auth
def delete_project(current_user, project_id):
    """
    Delete a project (must belong to authenticated user)
    
    Returns:
        JSON response confirming deletion
    """
    try:
        # First verify the project exists and belongs to the user
        existing = pb_service.pb.collection('projects').get_one(project_id)
        if existing.user_id != current_user['id']:
            return jsonify({"error": "Unauthorized access to project"}), 403
        
        # Delete the project
        pb_service.pb.collection('projects').delete(project_id)
        
        print(f"Deleted project: {project_id} for user {current_user['id']}")
        return jsonify({"message": "Project deleted successfully"}), 200
        
    except Exception as e:
        if '404' in str(e) or 'not found' in str(e).lower():
            return jsonify({"error": "Project not found"}), 404
        print(f"Error deleting project: {str(e)}")
        return jsonify({
            "error": "Failed to delete project",
            "details": str(e)
        }), 500
