"""
Production WSGI Entry Point

This module provides the WSGI application for production deployment
with proper configuration and error handling.
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.config import config

# Create the WSGI application
application = create_app()

if __name__ == '__main__':
    print("Starting Code Critique Engine API (WSGI)...")
    print(f"Configuration: {type(config).__name__}")
    print(f"Debug mode: {config.DEBUG}")
    
    # For development, you can run this directly
    application.run(
        debug=config.DEBUG,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000))
    )