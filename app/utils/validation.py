"""
Input Validation Utilities

This module provides validation functions for user inputs to ensure
security and data integrity throughout the application.
"""
import re
import ast
import json
from typing import Dict, Any, List, Optional, Union


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


def validate_code_input(code: str, max_length: int = 10000) -> str:
    """
    Validate and sanitize code input
    
    Args:
        code: The code string to validate
        max_length: Maximum allowed length
        
    Returns:
        Cleaned code string
        
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(code, str):
        raise ValidationError("Code must be a string")
    
    if not code.strip():
        raise ValidationError("Code cannot be empty")
    
    if len(code) > max_length:
        raise ValidationError(f"Code exceeds maximum length of {max_length} characters")
    
    # Check for potentially dangerous patterns
    dangerous_patterns = [
        r'import\s+os',
        r'import\s+subprocess',
        r'import\s+sys',
        r'__import__',
        r'eval\s*\(',
        r'exec\s*\(',
        r'compile\s*\(',
        r'open\s*\(',
        r'file\s*\(',
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, code, re.IGNORECASE):
            print(f"Warning: Potentially dangerous code pattern detected: {pattern}")
            # Log but don't block - let AI analysis proceed with warnings
    
    # Validate Python syntax (basic check)
    try:
        ast.parse(code)
    except SyntaxError:
        # Don't block invalid syntax - AI can analyze broken code too
        print("Note: Code has syntax errors, but proceeding with analysis")
    
    return code.strip()


def validate_prompt_input(prompt: str, max_length: int = 1000) -> str:
    """
    Validate and sanitize AI prompt input
    
    Args:
        prompt: The prompt string to validate
        max_length: Maximum allowed length
        
    Returns:
        Cleaned prompt string
        
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(prompt, str):
        raise ValidationError("Prompt must be a string")
    
    if not prompt.strip():
        raise ValidationError("Prompt cannot be empty")
    
    if len(prompt) > max_length:
        raise ValidationError(f"Prompt exceeds maximum length of {max_length} characters")
    
    # Check for potential prompt injection attempts
    suspicious_patterns = [
        r'ignore\s+previous\s+instructions',
        r'forget\s+everything',
        r'system\s*:',
        r'assistant\s*:',
        r'user\s*:',
        r'```\s*system',
        r'jailbreak',
        r'sudo\s+mode',
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, prompt, re.IGNORECASE):
            print(f"Warning: Potential prompt injection detected: {pattern}")
            # Log suspicious activity but don't block
    
    return prompt.strip()


def validate_project_idea_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate project idea creation/update data
    
    Args:
        data: Project idea data dictionary
        
    Returns:
        Validated and cleaned data
        
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(data, dict):
        raise ValidationError("Project idea data must be a dictionary")
    
    validated = {}
    
    # Title validation
    title = data.get('title', '').strip()
    if not title:
        raise ValidationError("Title is required")
    if len(title) > 200:
        raise ValidationError("Title too long (max 200 characters)")
    validated['title'] = title
    
    # Description validation
    description = data.get('description', '').strip()
    if not description:
        raise ValidationError("Description is required")
    if len(description) > 5000:
        raise ValidationError("Description too long (max 5000 characters)")
    validated['description'] = description
    
    # Purpose statement validation (optional)
    purpose_statement = data.get('purpose_statement', '').strip()
    if len(purpose_statement) > 2000:
        raise ValidationError("Purpose statement too long (max 2000 characters)")
    validated['purpose_statement'] = purpose_statement
    
    # Status validation
    valid_statuses = ['draft', 'in_review', 'approved']
    status = data.get('status', 'draft').lower()
    if status not in valid_statuses:
        raise ValidationError(f"Invalid status. Must be one of: {valid_statuses}")
    validated['status'] = status
    
    # Architecture JSON validation
    architecture_json = data.get('architecture_json', {})
    if architecture_json:
        if isinstance(architecture_json, str):
            try:
                architecture_json = json.loads(architecture_json)
            except json.JSONDecodeError:
                raise ValidationError("Invalid JSON in architecture_json field")
        
        if not isinstance(architecture_json, dict):
            raise ValidationError("architecture_json must be a JSON object")
        
        # Validate size of JSON
        json_str = json.dumps(architecture_json)
        if len(json_str) > 10000:
            raise ValidationError("Architecture JSON too large (max 10KB)")
    
    validated['architecture_json'] = architecture_json
    
    return validated


def validate_id_parameter(id_param: str, field_name: str = "ID") -> str:
    """
    Validate ID parameters (UUIDs, etc.)
    
    Args:
        id_param: The ID string to validate
        field_name: Name of the field for error messages
        
    Returns:
        Validated ID string
        
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(id_param, str):
        raise ValidationError(f"{field_name} must be a string")
    
    if not id_param.strip():
        raise ValidationError(f"{field_name} cannot be empty")
    
    # Basic alphanumeric check (PocketBase IDs are typically 15 chars alphanumeric)
    if not re.match(r'^[a-zA-Z0-9_-]+$', id_param):
        raise ValidationError(f"Invalid {field_name} format")
    
    if len(id_param) > 50:  # Reasonable upper bound
        raise ValidationError(f"{field_name} too long")
    
    return id_param.strip()


def sanitize_html(text: str) -> str:
    """
    Basic HTML sanitization to prevent XSS
    
    Args:
        text: Text that may contain HTML
        
    Returns:
        Sanitized text
    """
    if not isinstance(text, str):
        return str(text)
    
    # Basic HTML entity encoding
    replacements = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#x27;',
        '/': '&#x2F;',
    }
    
    for char, entity in replacements.items():
        text = text.replace(char, entity)
    
    return text


def validate_pagination(page: Union[str, int], per_page: Union[str, int]) -> tuple[int, int]:
    """
    Validate pagination parameters
    
    Args:
        page: Page number
        per_page: Items per page
        
    Returns:
        Tuple of (validated_page, validated_per_page)
        
    Raises:
        ValidationError: If validation fails
    """
    try:
        page_num = int(page) if isinstance(page, str) else page
        per_page_num = int(per_page) if isinstance(per_page, str) else per_page
    except (ValueError, TypeError):
        raise ValidationError("Page and per_page must be integers")
    
    if page_num < 1:
        raise ValidationError("Page must be >= 1")
    
    if per_page_num < 1:
        raise ValidationError("Per page must be >= 1")
    
    if per_page_num > 100:
        raise ValidationError("Per page cannot exceed 100")
    
    return page_num, per_page_num


def validate_search_query(query: str) -> str:
    """
    Validate search query
    
    Args:
        query: Search query string
        
    Returns:
        Validated query string
        
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(query, str):
        raise ValidationError("Search query must be a string")
    
    query = query.strip()
    
    if not query:
        raise ValidationError("Search query cannot be empty")
    
    if len(query) > 200:
        raise ValidationError("Search query too long (max 200 characters)")
    
    # Remove potentially dangerous SQL injection patterns
    dangerous_sql = ['--', ';', 'DROP', 'DELETE', 'INSERT', 'UPDATE', 'UNION']
    query_upper = query.upper()
    
    for pattern in dangerous_sql:
        if pattern in query_upper:
            raise ValidationError(f"Invalid search query: contains '{pattern}'")
    
    return query


def validate_auth_input(data: Dict[str, Any], is_signup: bool = False) -> Optional[str]:
    """
    Validate authentication input (login/signup)
    
    Args:
        data: Authentication data dictionary
        is_signup: Whether this is a signup (requires password confirmation)
        
    Returns:
        Error message if validation fails, None otherwise
    """
    if not isinstance(data, dict):
        return "Invalid request data"
    
    # Email validation
    email = data.get('email', '').strip()
    if not email:
        return "Email is required"
    
    # Basic email format validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return "Invalid email format"
    
    if len(email) > 255:
        return "Email too long"
    
    # Password validation
    password = data.get('password', '')
    if not password:
        return "Password is required"
    
    if len(password) < 8:
        return "Password must be at least 8 characters"
    
    if len(password) > 100:
        return "Password too long (max 100 characters)"
    
    # For signup, validate password confirmation
    if is_signup:
        password_confirm = data.get('passwordConfirm', '')
        if not password_confirm:
            return "Password confirmation is required"
        
        if password != password_confirm:
            return "Passwords do not match"
        
        # Optional name validation
        name = data.get('name', '').strip()
        if name and len(name) > 100:
            return "Name too long (max 100 characters)"
    
    return None