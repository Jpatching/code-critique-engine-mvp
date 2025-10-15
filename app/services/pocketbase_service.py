"""
PocketBase Service

This module handles all interactions with PocketBase for data persistence.
Provides CRUD operations for project ideas and user management.
"""
import requests
from typing import Dict, List, Any, Optional
from app.config import config


class PocketBaseService:
    """Service for PocketBase database operations"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or config.POCKETBASE_URL
        self.session = requests.Session()
        self._auth_token: Optional[str] = None
    
    def authenticate_admin(self, email: str = None, password: str = None) -> bool:
        """
        Authenticate as admin user
        
        Args:
            email: Admin email (optional, uses config if not provided)
            password: Admin password (optional, uses config if not provided)
            
        Returns:
            True if authentication successful
        """
        email = email or config.POCKETBASE_ADMIN_EMAIL
        password = password or config.POCKETBASE_ADMIN_PASSWORD
        
        if not email or not password:
            print("Admin credentials not configured")
            return False
        
        try:
            response = requests.post(
                f"{self.base_url}/api/admins/auth-with-password",
                json={"identity": email, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                self._auth_token = data.get("token")
                self.session.headers.update({"Authorization": f"Bearer {self._auth_token}"})
                return True
            else:
                print(f"Admin authentication failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"Admin authentication error: {e}")
            return False
    
    def list_project_ideas(self, page: int = 1, per_page: int = 30) -> Dict[str, Any]:
        """
        List all project ideas with pagination
        
        Args:
            page: Page number (1-based)
            per_page: Number of items per page
            
        Returns:
            Dictionary with items, page info, and total count
        """
        try:
            params = {"page": page, "perPage": per_page}
            response = requests.get(
                f"{self.base_url}/api/collections/project_ideas/records",
                params=params
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to list ideas: {response.text}")
                
        except Exception as e:
            raise Exception(f"PocketBase error: {str(e)}")
    
    def create_project_idea(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new project idea
        
        Args:
            data: Project idea data (title, description, etc.)
            
        Returns:
            Created project idea record
        """
        try:
            # Validate required fields
            if not data.get("title"):
                raise ValueError("Title is required")
            if not data.get("description"):
                raise ValueError("Description is required")
            
            # Prepare the record
            record = {
                "title": data["title"],
                "description": data["description"],
                "purpose_statement": data.get("purpose_statement", ""),
                "architecture_json": data.get("architecture_json", {}),
                "status": data.get("status", "draft")
            }
            
            response = requests.post(
                f"{self.base_url}/api/collections/project_ideas/records",
                json=record
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to create idea: {response.text}")
                
        except Exception as e:
            raise Exception(f"PocketBase error: {str(e)}")
    
    def get_project_idea(self, idea_id: str) -> Dict[str, Any]:
        """
        Get a specific project idea by ID
        
        Args:
            idea_id: The ID of the project idea
            
        Returns:
            Project idea record
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/collections/project_ideas/records/{idea_id}"
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to get idea: {response.text}")
                
        except Exception as e:
            raise Exception(f"PocketBase error: {str(e)}")
    
    def update_project_idea(self, idea_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a project idea
        
        Args:
            idea_id: The ID of the project idea
            data: Updated data
            
        Returns:
            Updated project idea record
        """
        try:
            response = requests.patch(
                f"{self.base_url}/api/collections/project_ideas/records/{idea_id}",
                json=data
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to update idea: {response.text}")
                
        except Exception as e:
            raise Exception(f"PocketBase error: {str(e)}")
    
    def delete_project_idea(self, idea_id: str) -> bool:
        """
        Delete a project idea
        
        Args:
            idea_id: The ID of the project idea
            
        Returns:
            True if deletion successful
        """
        try:
            response = requests.delete(
                f"{self.base_url}/api/collections/project_ideas/records/{idea_id}"
            )
            
            return response.status_code == 204
                
        except Exception as e:
            raise Exception(f"PocketBase error: {str(e)}")
    
    def search_project_ideas(self, query: str, fields: List[str] = None) -> Dict[str, Any]:
        """
        Search project ideas by text
        
        Args:
            query: Search query
            fields: Fields to search in (default: title, description)
            
        Returns:
            Search results
        """
        try:
            if fields is None:
                fields = ["title", "description", "purpose_statement"]
            
            # Build filter string for PocketBase
            filter_parts = [f'{field} ~ "{query}"' for field in fields]
            filter_string = " || ".join(filter_parts)
            
            params = {"filter": filter_string}
            response = requests.get(
                f"{self.base_url}/api/collections/project_ideas/records",
                params=params
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to search ideas: {response.text}")
                
        except Exception as e:
            raise Exception(f"PocketBase error: {str(e)}")
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Check PocketBase health status
        
        Returns:
            Health status information
        """
        try:
            response = requests.get(f"{self.base_url}/api/health")
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"status": "unhealthy", "error": response.text}
                
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    # Authentication Methods
    
    def create_user(self, email: str, password: str, password_confirm: str, name: str = "") -> Dict[str, Any]:
        """
        Create a new user account
        
        Args:
            email: User email
            password: User password
            password_confirm: Password confirmation
            name: User display name (optional)
            
        Returns:
            Dictionary with user data and token, or error
        """
        try:
            # Create user record
            user_data = {
                "email": email,
                "password": password,
                "passwordConfirm": password_confirm,
                "name": name,
                "emailVisibility": True
            }
            
            response = requests.post(
                f"{self.base_url}/api/collections/users/records",
                json=user_data
            )
            
            if response.status_code == 200:
                user = response.json()
                
                # Authenticate to get token
                auth_result = self.authenticate_user(email, password)
                
                if 'error' not in auth_result:
                    return {
                        'user': auth_result['user'],
                        'token': auth_result['token']
                    }
                else:
                    # User created but auth failed - return user data
                    return {
                        'user': user,
                        'token': '',
                        'warning': 'User created but initial authentication failed'
                    }
            else:
                error_data = response.json()
                error_message = error_data.get('message', 'Failed to create user')
                
                # Extract field-specific errors if available
                if 'data' in error_data:
                    field_errors = []
                    for field, errors in error_data['data'].items():
                        if isinstance(errors, dict) and 'message' in errors:
                            field_errors.append(f"{field}: {errors['message']}")
                    if field_errors:
                        error_message = "; ".join(field_errors)
                
                return {'error': error_message}
                
        except Exception as e:
            return {'error': f"User creation error: {str(e)}"}
    
    def authenticate_user(self, email: str, password: str) -> Dict[str, Any]:
        """
        Authenticate a user and get JWT token
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Dictionary with user data and token, or error
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/collections/users/auth-with-password",
                json={"identity": email, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'user': data.get('record', {}),
                    'token': data.get('token', '')
                }
            else:
                return {'error': 'Invalid email or password'}
                
        except Exception as e:
            return {'error': f"Authentication error: {str(e)}"}
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify JWT token and return user data
        
        Args:
            token: JWT token to verify
            
        Returns:
            User data if token is valid, None otherwise
        """
        try:
            # Use PocketBase auth-refresh endpoint to verify token
            response = requests.post(
                f"{self.base_url}/api/collections/users/auth-refresh",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('record', {})
            else:
                return None
                
        except Exception as e:
            print(f"Token verification error: {e}")
            return None
    
    def update_user(self, user_id: str, token: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user profile
        
        Args:
            user_id: User ID
            token: Authentication token
            data: Update data (name, email, etc.)
            
        Returns:
            Updated user data, or error
        """
        try:
            response = requests.patch(
                f"{self.base_url}/api/collections/users/records/{user_id}",
                json=data,
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                return {'user': response.json()}
            else:
                return {'error': 'Failed to update user profile'}
                
        except Exception as e:
            return {'error': f"Update error: {str(e)}"}
    
    def refresh_auth_token(self, token: str) -> Dict[str, Any]:
        """
        Refresh authentication token
        
        Args:
            token: Current token
            
        Returns:
            New token, or error
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/collections/users/auth-refresh",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                return {'token': data.get('token', '')}
            else:
                return {'error': 'Token refresh failed'}
                
        except Exception as e:
            return {'error': f"Refresh error: {str(e)}"}