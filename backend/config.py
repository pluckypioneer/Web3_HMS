"""
Configuration settings for Web3 HMS Backend
"""

import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/hms_db'
    
    # Redis configuration
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # CORS configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://localhost:8080').split(',')
    
    # Blockchain configuration
    WEB3_PROVIDER_URL = os.environ.get('WEB3_PROVIDER_URL') or 'http://localhost:8545'
    CONTRACT_ADDRESSES = {
        'MEDICAL_RECORD_HASH': os.environ.get('MEDICAL_RECORD_HASH_ADDRESS'),
        'ACCESS_CONTROL': os.environ.get('ACCESS_CONTROL_ADDRESS'),
        'DRUG_TRACE': os.environ.get('DRUG_TRACE_ADDRESS')
    }
    
    # IPFS configuration
    IPFS_URL = os.environ.get('IPFS_URL') or 'http://localhost:5001'
    
    # File upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Celery configuration
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/1'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    MONGO_URI = os.environ.get('DEV_MONGO_URI') or 'mongodb://localhost:27017/hms_dev'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    MONGO_URI = os.environ.get('MONGO_URI')
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    MONGO_URI = os.environ.get('TEST_MONGO_URI') or 'mongodb://localhost:27017/hms_test'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
