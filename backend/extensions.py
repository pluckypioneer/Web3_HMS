"""
Flask extensions initialization
"""

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import redis

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
redis_client = redis.Redis()

def init_extensions(app):
    """Initialize extensions with app context"""
    db.init_app(app)
    jwt.init_app(app)
    
    # Configure Redis
    redis_client.connection_pool = redis.ConnectionPool.from_url(app.config['REDIS_URL'])
