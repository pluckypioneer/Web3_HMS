"""
User model for Web3 HMS authentication
"""

from datetime import datetime
from extensions import mongo_db
import hashlib
import uuid

class User:
    """User model for authentication"""
    
    def __init__(self, username, email, password=None, role='patient', 
                 blockchain_addr=None, profile_id=None, is_active=True):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.role = role
        self.is_active = is_active
        self.blockchain_addr = blockchain_addr
        self.profile_id = profile_id
        self.last_login = None
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
        if password:
            self.set_password(password)
        else:
            self.password_hash = None
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        self.updated_at = datetime.utcnow()
    
    def check_password(self, password):
        """Check password"""
        return self.password_hash == hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'blockchain_addr': self.blockchain_addr,
            'profile_id': self.profile_id,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @staticmethod
    def get_collection():
        """Get users collection"""
        return mongo_db.users if mongo_db else None
    
    @classmethod
    def find_by_id(cls, user_id):
        """Find user by ID"""
        collection = cls.get_collection()
        if not collection:
            return None
            
        data = collection.find_one({'id': user_id})
        if not data:
            return None
            
        user = cls(data['username'], data['email'], role=data['role'])
        user.id = data['id']
        user.password_hash = data['password_hash']
        user.is_active = data.get('is_active', True)
        user.blockchain_addr = data.get('blockchain_addr')
        user.profile_id = data.get('profile_id')
        user.last_login = data.get('last_login')
        user.created_at = data['created_at']
        user.updated_at = data['updated_at']
        return user
    
    @classmethod
    def find_by_email(cls, email):
        """Find user by email"""
        collection = cls.get_collection()
        if not collection:
            return None
            
        data = collection.find_one({'email': email})
        if not data:
            return None
            
        user = cls(data['username'], data['email'], role=data['role'])
        user.id = data['id']
        user.password_hash = data['password_hash']
        user.is_active = data.get('is_active', True)
        user.blockchain_addr = data.get('blockchain_addr')
        user.profile_id = data.get('profile_id')
        user.last_login = data.get('last_login')
        user.created_at = data['created_at']
        user.updated_at = data['updated_at']
        return user
    
    def save(self):
        """Save user to database"""
        collection = self.get_collection()
        if not collection:
            return False
            
        data = self.to_dict()
        collection.replace_one({'id': self.id}, data, upsert=True)
        return True
    
    def delete(self):
        """Delete user from database"""
        collection = self.get_collection()
        if not collection:
            return False
            
        collection.delete_one({'id': self.id})
        return True
