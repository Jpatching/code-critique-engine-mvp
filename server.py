#!/usr/bin/env python3
"""
Development server runner for Code Critique Engine.

Imports the modular Flask app factory and starts the server.
For production deployments, use the wsgi.py entrypoint with Gunicorn or similar.
"""
import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.config import config

# Instantiate the application
app = create_app()

if __name__ == '__main__':
    print("🚀 Starting Code Critique Engine (Development)")
    print(f"• Config: {type(config).__name__}")
    print(f"• Debug: {config.DEBUG}")
    print(f"• AI Model: {config.GEMINI_MODEL}")
    print(f"• PocketBase URL: {config.POCKETBASE_URL}")
    print(f"• GEMINI_API_KEY: {'✅ Set' if config.GEMINI_API_KEY else '❌ Missing'}")
    print("----------------------------------------")
    app.run(debug=config.DEBUG, host='127.0.0.1', port=5000)