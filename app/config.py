"""
Application Configuration Management

This module provides centralized configuration management for the Code Critique Engine.
Supports environment-based configuration with validation and defaults.
"""
import os
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Config:
    """Base configuration class with common settings"""
    
    # Flask Configuration
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG: bool = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
    
    # AI Service Configuration
    GEMINI_API_KEY: str = os.getenv('GEMINI_API_KEY', '')
    GEMINI_MODEL: str = os.getenv('GEMINI_MODEL', 'models/gemini-1.5-flash')
    AI_REQUEST_TIMEOUT: int = int(os.getenv('AI_REQUEST_TIMEOUT', '30'))
    MAX_CONCURRENT_AI_REQUESTS: int = int(os.getenv('MAX_CONCURRENT_AI_REQUESTS', '3'))
    
    # PocketBase Configuration
    POCKETBASE_URL: str = os.getenv('POCKETBASE_URL', 'http://127.0.0.1:8090')
    POCKETBASE_ADMIN_EMAIL: str = os.getenv('POCKETBASE_ADMIN_EMAIL', '')
    POCKETBASE_ADMIN_PASSWORD: str = os.getenv('POCKETBASE_ADMIN_PASSWORD', '')
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = int(os.getenv('RATE_LIMIT_REQUESTS', '10'))
    RATE_LIMIT_WINDOW: str = os.getenv('RATE_LIMIT_WINDOW', '1 minute')
    
    # Security
    CORS_ORIGINS: List[str] = field(default_factory=lambda: os.getenv('CORS_ORIGINS', 'http://127.0.0.1:5500').split(','))
    MAX_CODE_LENGTH: int = int(os.getenv('MAX_CODE_LENGTH', '10000'))
    MAX_PROMPT_LENGTH: int = int(os.getenv('MAX_PROMPT_LENGTH', '1000'))
    
    def validate(self) -> bool:
        """Validate configuration settings"""
        errors = []
        
        if not self.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY is required")
            
        if self.AI_REQUEST_TIMEOUT < 1:
            errors.append("AI_REQUEST_TIMEOUT must be >= 1")
            
        if self.MAX_CONCURRENT_AI_REQUESTS < 1:
            errors.append("MAX_CONCURRENT_AI_REQUESTS must be >= 1")
            
        if errors:
            print("Configuration validation errors:")
            for error in errors:
                print(f"  - {error}")
            return False
            
        return True


@dataclass
class DevelopmentConfig(Config):
    """Development-specific configuration"""
    DEBUG: bool = True
    FORCE_FREE_TIER: bool = True


@dataclass
class ProductionConfig(Config):
    """Production-specific configuration"""
    DEBUG: bool = False
    FORCE_FREE_TIER: bool = False
    SECRET_KEY: str = os.getenv('SECRET_KEY')  # Must be set in production
    
    def validate(self) -> bool:
        """Additional production validations"""
        if not super().validate():
            return False
            
        errors = []
        
        if self.SECRET_KEY == 'dev-secret-key-change-in-production':
            errors.append("SECRET_KEY must be changed in production")
            
        if self.DEBUG:
            errors.append("DEBUG must be False in production")
            
        if errors:
            print("Production configuration validation errors:")
            for error in errors:
                print(f"  - {error}")
            return False
            
        return True


def get_config() -> Config:
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development').lower()
    
    if env == 'production':
        return ProductionConfig()
    else:
        return DevelopmentConfig()


# Global configuration instance
config = get_config()