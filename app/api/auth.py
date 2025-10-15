"""
Authentication API Endpoints

Handles user registration, login, logout, and profile management
using PocketBase authentication.
"""
from flask import Blueprint, request, jsonify
from app.services.pocketbase_service import PocketBaseService
from app.utils.validation import validate_auth_input
from functools import wraps
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
pb_service = PocketBaseService(os.getenv('POCKETBASE_URL', 'http://127.0.0.1:8090'))


def require_auth(f):
    """
    Decorator to protect routes that require authentication.
    Extracts and validates JWT token from Authorization header.
    Passes the authenticated user as the first argument (current_user) to the decorated function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Missing authorization header'}), 401
        
        # Extract token (format: "Bearer <token>")
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return jsonify({'error': 'Invalid authorization header format'}), 401
        
        # Verify token with PocketBase
        user = pb_service.verify_token(token)
        if not user:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Add user to request context for backward compatibility
        request.user = user
        request.token = token
        
        # Pass user as first argument to the decorated function
        return f(user, *args, **kwargs)
    
    return decorated_function


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    Register a new user
    
    Expected JSON body:
    {
        "email": "user@example.com",
        "password": "securepassword",
        "passwordConfirm": "securepassword",
        "name": "John Doe" (optional)
    }
    
    Returns:
    {
        "user": {...},
        "token": "jwt_token"
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        validation_error = validate_auth_input(data, is_signup=True)
        if validation_error:
            return jsonify({'error': validation_error}), 400
        
        # Create user in PocketBase
        result = pb_service.create_user(
            email=data['email'],
            password=data['password'],
            password_confirm=data['passwordConfirm'],
            name=data.get('name', '')
        )
        
        if 'error' in result:
            return jsonify({'error': result['error']}), 400
        
        return jsonify({
            'user': result['user'],
            'token': result['token']
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Signup failed: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT token
    
    Expected JSON body:
    {
        "email": "user@example.com",
        "password": "securepassword"
    }
    
    Returns:
    {
        "user": {...},
        "token": "jwt_token"
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        validation_error = validate_auth_input(data, is_signup=False)
        if validation_error:
            return jsonify({'error': validation_error}), 400
        
        # Authenticate with PocketBase
        result = pb_service.authenticate_user(
            email=data['email'],
            password=data['password']
        )
        
        if 'error' in result:
            return jsonify({'error': result['error']}), 401
        
        return jsonify({
            'user': result['user'],
            'token': result['token']
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500


@auth_bp.route('/logout', methods=['POST'])
@require_auth
def logout():
    """
    Logout user (client-side token removal primarily)
    
    Returns:
    {
        "message": "Logged out successfully"
    }
    """
    # Note: JWT tokens are stateless, so logout is primarily client-side
    # (removing token from localStorage). This endpoint confirms the action.
    return jsonify({'message': 'Logged out successfully'}), 200


@auth_bp.route('/me', methods=['GET'])
@require_auth
def get_current_user():
    """
    Get current authenticated user's profile
    
    Returns:
    {
        "user": {...}
    }
    """
    return jsonify({'user': request.user}), 200


@auth_bp.route('/me', methods=['PUT'])
@require_auth
def update_current_user():
    """
    Update current user's profile
    
    Expected JSON body:
    {
        "name": "New Name",
        "email": "newemail@example.com" (optional)
    }
    
    Returns:
    {
        "user": {...}
    }
    """
    try:
        data = request.get_json()
        
        # Update user in PocketBase
        result = pb_service.update_user(
            user_id=request.user['id'],
            token=request.token,
            data=data
        )
        
        if 'error' in result:
            return jsonify({'error': result['error']}), 400
        
        return jsonify({'user': result['user']}), 200
        
    except Exception as e:
        return jsonify({'error': f'Update failed: {str(e)}'}), 500


@auth_bp.route('/refresh', methods=['POST'])
@require_auth
def refresh_token():
    """
    Refresh JWT token
    
    Returns:
    {
        "token": "new_jwt_token"
    }
    """
    try:
        # Get new token from PocketBase
        result = pb_service.refresh_auth_token(request.token)
        
        if 'error' in result:
            return jsonify({'error': result['error']}), 401
        
        return jsonify({'token': result['token']}), 200
        
    except Exception as e:
        return jsonify({'error': f'Token refresh failed: {str(e)}'}), 500
