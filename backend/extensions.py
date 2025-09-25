"""
Flask extensions initialization
"""

from flask_jwt_extended import JWTManager
import redis
from pymongo import MongoClient

# Initialize extensions
jwt = JWTManager()
redis_client = None
mongo_client = None
mongo_db = None

def init_extensions(app):
    """Initialize extensions with app context"""
    global redis_client, mongo_client, mongo_db
    
    jwt.init_app(app)
    
    # Configure Redis with proper connection parameters
    redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/0')
    redis_client = redis.from_url(redis_url, decode_responses=True)
    
    # Configure MongoDB
    mongo_uri = app.config.get('MONGO_URI', 'mongodb://localhost:27017/hms_db')
    mongo_client = MongoClient(mongo_uri)
    mongo_db = mongo_client.get_database()
