"""
Contract model for Web3 HMS
"""

from datetime import datetime
from extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Contract(db.Model):
    """Contract model for storing smart contract information"""
    __tablename__ = 'contracts'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(42), unique=True, nullable=False)  # Contract address
    abi = db.Column(db.Text)  # Contract ABI JSON
    network = db.Column(db.String(50), nullable=False)  # Network name
    deploy_time = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Contract {self.name}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self.id),
            'name': self.name,
            'address': self.address,
            'abi': self.abi,
            'network': self.network,
            'deploy_time': self.deploy_time.isoformat(),
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
