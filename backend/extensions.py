"""
Flask extensions initialization
"""

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import redis

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
redis_client = None

def init_extensions(app):
    """Initialize extensions with app context"""
    global redis_client
    
    db.init_app(app)
    jwt.init_app(app)
    
    # Configure Redis with proper connection parameters
    redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/0')
    redis_client = redis.from_url(redis_url, decode_responses=True)
