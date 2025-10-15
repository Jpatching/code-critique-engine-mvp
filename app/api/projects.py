"""
Project Ideas API Endpoints

This module handles CRUD operations for project ideas with proper
validation, error handling, and response formatting.
"""
from flask import Blueprint, request, jsonify
from app.services.pocketbase_service import PocketBaseService
from app.utils.validation import (
    validate_project_idea_data, validate_id_parameter, 
    validate_pagination, validate_search_query, ValidationError
)

projects_bp = Blueprint('projects', __name__)
pb_service = PocketBaseService()


@projects_bp.route('/ideas', methods=['GET'])
def list_project_ideas():
    """
    List project ideas with pagination and optional search
    
    Query parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 30, max: 100)
    - search: Search query (optional)
    
    Returns:
        JSON response with paginated project ideas
    """
    try:
        # Validate pagination parameters
        page = request.args.get('page', 1)
        per_page = request.args.get('per_page', 30)
        
        try:
            page, per_page = validate_pagination(page, per_page)
        except ValidationError as e:
            return jsonify({"error": f"Pagination error: {str(e)}"}), 400
        
        # Handle search if provided
        search_query = request.args.get('search')
        if search_query:
            try:
                search_query = validate_search_query(search_query)
                result = pb_service.search_project_ideas(search_query)
            except ValidationError as e:
                return jsonify({"error": f"Search error: {str(e)}"}), 400
        else:
            result = pb_service.list_project_ideas(page, per_page)
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error listing project ideas: {str(e)}")
        return jsonify({
            "error": "Failed to list project ideas",
            "details": str(e)
        }), 500


@projects_bp.route('/ideas', methods=['POST'])
def create_project_idea():
    """
    Create a new project idea
    
    Expected JSON payload:
    {
        "title": "Project title",
        "description": "Project description",
        "purpose_statement": "Optional purpose statement",
        "architecture_json": {...}, // Optional architecture object
        "status": "draft" // Optional: draft, in_review, approved
    }
    
    Returns:
        JSON response with created project idea
    """
    try:
        # Parse and validate request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
        
        try:
            validated_data = validate_project_idea_data(data)
        except ValidationError as e:
            return jsonify({"error": f"Validation error: {str(e)}"}), 400
        
        # Create the project idea
        try:
            result = pb_service.create_project_idea(validated_data)
            
            print(f"Created project idea: {result.get('id')} - {validated_data['title']}")
            return jsonify(result), 201
            
        except Exception as e:
            print(f"PocketBase creation error: {str(e)}")
            return jsonify({
                "error": "Failed to create project idea",
                "details": str(e)
            }), 500
        
    except Exception as e:
        print(f"Unexpected error creating project idea: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "details": "An unexpected error occurred"
        }), 500


@projects_bp.route('/ideas/<idea_id>', methods=['GET'])
def get_project_idea(idea_id):
    """
    Get a specific project idea by ID
    
    Args:
        idea_id: The ID of the project idea
        
    Returns:
        JSON response with project idea data
    """
    try:
        # Validate ID parameter
        try:
            idea_id = validate_id_parameter(idea_id, "Project idea ID")
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        
        # Get the project idea
        try:
            result = pb_service.get_project_idea(idea_id)
            return jsonify(result), 200
            
        except Exception as e:
            print(f"Error getting project idea {idea_id}: {str(e)}")
            if "404" in str(e):
                return jsonify({"error": "Project idea not found"}), 404
            return jsonify({
                "error": "Failed to get project idea",
                "details": str(e)
            }), 500
        
    except Exception as e:
        print(f"Unexpected error getting project idea: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "details": "An unexpected error occurred"
        }), 500


@projects_bp.route('/ideas/<idea_id>', methods=['PUT', 'PATCH'])
def update_project_idea(idea_id):
    """
    Update a project idea
    
    Args:
        idea_id: The ID of the project idea
        
    Expected JSON payload: Same as create, but all fields optional
    
    Returns:
        JSON response with updated project idea
    """
    try:
        # Validate ID parameter
        try:
            idea_id = validate_id_parameter(idea_id, "Project idea ID")
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        
        # Parse and validate request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
        
        # For updates, we allow partial data, so validate only provided fields
        validated_data = {}
        try:
            if 'title' in data or 'description' in data:
                # If updating core fields, validate the entire object
                validated_data = validate_project_idea_data(data)
            else:
                # For other fields, validate individually
                for field in ['purpose_statement', 'architecture_json', 'status']:
                    if field in data:
                        validated_data[field] = data[field]
        except ValidationError as e:
            return jsonify({"error": f"Validation error: {str(e)}"}), 400
        
        # Update the project idea
        try:
            result = pb_service.update_project_idea(idea_id, validated_data)
            
            print(f"Updated project idea: {idea_id}")
            return jsonify(result), 200
            
        except Exception as e:
            print(f"Error updating project idea {idea_id}: {str(e)}")
            if "404" in str(e):
                return jsonify({"error": "Project idea not found"}), 404
            return jsonify({
                "error": "Failed to update project idea",
                "details": str(e)
            }), 500
        
    except Exception as e:
        print(f"Unexpected error updating project idea: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "details": "An unexpected error occurred"
        }), 500


@projects_bp.route('/ideas/<idea_id>', methods=['DELETE'])
def delete_project_idea(idea_id):
    """
    Delete a project idea
    
    Args:
        idea_id: The ID of the project idea
        
    Returns:
        Empty response with 204 status code
    """
    try:
        # Validate ID parameter
        try:
            idea_id = validate_id_parameter(idea_id, "Project idea ID")
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        
        # Delete the project idea
        try:
            success = pb_service.delete_project_idea(idea_id)
            
            if success:
                print(f"Deleted project idea: {idea_id}")
                return '', 204
            else:
                return jsonify({"error": "Failed to delete project idea"}), 500
                
        except Exception as e:
            print(f"Error deleting project idea {idea_id}: {str(e)}")
            if "404" in str(e):
                return jsonify({"error": "Project idea not found"}), 404
            return jsonify({
                "error": "Failed to delete project idea",
                "details": str(e)
            }), 500
        
    except Exception as e:
        print(f"Unexpected error deleting project idea: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "details": "An unexpected error occurred"
        }), 500


@projects_bp.route('/ideas/search', methods=['GET'])
def search_project_ideas():
    """
    Search project ideas by text query
    
    Query parameters:
    - q: Search query (required)
    - fields: Comma-separated list of fields to search (optional)
    
    Returns:
        JSON response with search results
    """
    try:
        # Get and validate search query
        query = request.args.get('q')
        if not query:
            return jsonify({"error": "Search query 'q' parameter is required"}), 400
        
        try:
            query = validate_search_query(query)
        except ValidationError as e:
            return jsonify({"error": f"Search error: {str(e)}"}), 400
        
        # Get search fields (optional)
        fields_param = request.args.get('fields')
        fields = None
        if fields_param:
            fields = [f.strip() for f in fields_param.split(',') if f.strip()]
            # Validate field names
            valid_fields = ['title', 'description', 'purpose_statement']
            fields = [f for f in fields if f in valid_fields]
        
        # Perform search
        try:
            result = pb_service.search_project_ideas(query, fields)
            return jsonify(result), 200
            
        except Exception as e:
            print(f"Error searching project ideas: {str(e)}")
            return jsonify({
                "error": "Search failed",
                "details": str(e)
            }), 500
        
    except Exception as e:
        print(f"Unexpected error in search: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "details": "An unexpected error occurred"
        }), 500