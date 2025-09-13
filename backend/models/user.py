"""
User model for Web3 HMS authentication
"""

from datetime import datetime
from extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
import hashlib

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='patient')  # patient, doctor, admin
    is_active = db.Column(db.Boolean, default=True)
    blockchain_addr = db.Column(db.String(42))  # Ethereum address
    profile_id = db.Column(UUID(as_uuid=True))  # Reference to patient or doctor profile
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def check_password(self, password):
        """Check password"""
        return self.password_hash == hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self.id),
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'blockchain_addr': self.blockchain_addr,
            'profile_id': str(self.profile_id) if self.profile_id else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
