"""
Application Factory and Main Entry Point

This module creates and configures the Flask application with proper
blueprint registration, error handling, and middleware setup.
"""
import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from app.config import config
from app.api.analysis import analysis_bp
from app.api.projects import projects_bp
from app.api.auth import auth_bp
from app.api.user_projects import user_projects_bp
from app.api.analyses import analyses_bp


def create_app(config_override=None):
    """
    Application factory function
    
    Args:
        config_override: Optional configuration override
        
    Returns:
        Configured Flask application
    """
    # Create Flask app with static folder
    static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    app = Flask(__name__, static_folder=static_folder, static_url_path='/static')
    
    # Use provided config or global config
    app_config = config_override or config
    
    # Apply configuration
    app.config['SECRET_KEY'] = app_config.SECRET_KEY
    app.config['DEBUG'] = app_config.DEBUG
    
    # Setup CORS
    CORS(app, origins=app_config.CORS_ORIGINS)
    
    # Validate configuration
    if not app_config.validate():
        print("Configuration validation failed!")
        if not app_config.DEBUG:
            raise ValueError("Invalid configuration for production")
    
    # Register blueprints with /api prefix (except for compatibility)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(analysis_bp)  # Keep at root for now
    app.register_blueprint(projects_bp, url_prefix='/api')
    app.register_blueprint(user_projects_bp, url_prefix='/api')
    app.register_blueprint(analyses_bp, url_prefix='/api')
    
    # Register error handlers
    register_error_handlers(app)
    
    # Add global endpoints
    register_global_endpoints(app)
    
    return app


def register_error_handlers(app):
    """Register global error handlers"""
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Endpoint not found",
            "message": "The requested resource does not exist"
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "error": "Method not allowed",
            "message": "The method is not allowed for the requested URL"
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "error": "Internal server error",
            "message": "An unexpected error occurred"
        }), 500
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        print(f"Unexpected error: {str(error)}")
        return jsonify({
            "error": "Internal server error",
            "message": "An unexpected error occurred"
        }), 500


def register_global_endpoints(app):
    """Register global application endpoints"""
    
    @app.route('/')
    def root():
        """Serve the main SPA entry point"""
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.route('/<path:path>')
    def catch_all(path):
        """Catch all routes and serve index.html for client-side routing"""
        # If the path is a file that exists, serve it
        file_path = os.path.join(app.static_folder, path)
        if os.path.isfile(file_path):
            return send_from_directory(app.static_folder, path)
        # Otherwise serve the SPA entry point
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.route('/api/health')
    def health():
        """Global health check endpoint"""
        return jsonify({
            "status": "healthy",
            "service": "code-critique-engine",
            "version": "1.0.0"
        })


# Create the application instance
app = create_app()


if __name__ == '__main__':
    print(f"Starting Code Critique Engine API...")
    print(f"Debug mode: {config.DEBUG}")
    print(f"AI Model: {config.GEMINI_MODEL}")
    print(f"PocketBase URL: {config.POCKETBASE_URL}")
    
    app.run(
        debug=config.DEBUG,
        host='127.0.0.1',
        port=5000
    )