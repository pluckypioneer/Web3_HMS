"""
Web3 HMS Backend Application
Main Flask application entry point
"""

from flask import Flask, request, g
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os
import uuid
import logging
from datetime import datetime
from dotenv import load_dotenv

from config import Config
from extensions import db, redis_client, init_extensions
from api import api_bp
# Import specific models for registration
from models import (
    User, Patient, Doctor, MedicalRecord, Appointment,
    Inpatient, Drug, Contract, DataHash, AccessGrant
)
from utils.security import setup_security_logging, log_security_event, log_error

# Load environment variables
load_dotenv()


def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 创建日志目录
    os.makedirs('logs', exist_ok=True)
    
    # 设置安全日志记录
    setup_security_logging()
    
    # Initialize extensions
    init_extensions(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    
    # Initialize CORS with more restrictive configuration
    CORS(app, 
         origins=app.config['CORS_ORIGINS'],
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    
    # Initialize rate limiter with stricter limits for medical system
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour", "10 per minute"],
        storage_uri=app.config.get('REDIS_URL', 'redis://localhost:6379/0')
    )
    limiter.init_app(app)
    
    # Request ID middleware for tracing
    @app.before_request
    def before_request():
        g.request_id = str(uuid.uuid4())
        g.request_start_time = datetime.utcnow()
        
        # Log suspicious requests
        if request.content_length and request.content_length > app.config.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024):
            log_security_event('LARGE_REQUEST', f'Large request detected: {request.content_length} bytes', 'ERROR')
    
    @app.after_request
    def after_request(response):
        # Log request completion
        duration = (datetime.utcnow() - g.request_start_time).total_seconds()
        if duration > 5.0:  # Log slow requests
            log_security_event('SLOW_REQUEST', f'Slow request: {duration:.2f}s for {request.endpoint}')
        return response
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Enhanced error handlers
    @app.errorhandler(400)
    def bad_request(error):
        error_id = log_error(error, 'Bad request')
        return {
            'error': 'Bad request',
            'message': '请求格式错误',
            'error_id': error_id
        }, 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        log_security_event('UNAUTHORIZED_ACCESS', f'Unauthorized access attempt from {request.remote_addr}')
        return {
            'error': 'Unauthorized',
            'message': '身份验证失败'
        }, 401
    
    @app.errorhandler(403)
    def forbidden(error):
        log_security_event('FORBIDDEN_ACCESS', f'Forbidden access attempt from {request.remote_addr}', 'ERROR')
        return {
            'error': 'Forbidden',
            'message': '权限不足'
        }, 403
    
    @app.errorhandler(404)
    def not_found(error):
        return {
            'error': 'Not found',
            'message': '资源不存在'
        }, 404
    
    @app.errorhandler(429)
    def ratelimit_handler(error):
        log_security_event('RATE_LIMIT_EXCEEDED', f'Rate limit exceeded from {request.remote_addr}', 'WARNING')
        return {
            'error': 'Rate limit exceeded',
            'message': '请求过于频繁，请稍后再试'
        }, 429
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        error_id = log_error(error, 'Internal server error')
        
        # 在生产环境中不暴露详细错误信息
        if app.config.get('DEBUG', False):
            return {
                'error': 'Internal server error',
                'message': '服务器内部错误',
                'error_id': error_id,
                'details': str(error)
            }, 500
        else:
            return {
                'error': 'Internal server error',
                'message': '服务器内部错误，请联系管理员',
                'error_id': error_id
            }, 500
    
    # Improved health check endpoint with minimal information exposure
    @app.route('/health')
    def health_check():
        try:
            # Simple database connectivity check without exposing details
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            db.session.commit()
            db_healthy = True
        except Exception as e:
            log_error(e, 'Database health check failed')
            db_healthy = False
        
        # Basic health status without sensitive information
        health_status = {
            'status': 'healthy' if db_healthy else 'unhealthy',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Only include version in development mode
        if app.config.get('DEBUG', False):
            health_status['version'] = '1.0.0'
            health_status['database'] = 'connected' if db_healthy else 'disconnected'
        
        return health_status, 200 if db_healthy else 503
    
    return app

# Create the app instance at module level for gunicorn
app = create_app()

if __name__ == '__main__':
    # Only enable debug mode in development environment
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
