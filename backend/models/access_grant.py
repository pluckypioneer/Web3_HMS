"""
Access Grant model for Web3 HMS
"""

from datetime import datetime
from extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class AccessGrant(db.Model):
    """Access Grant model for data access permissions"""
    __tablename__ = 'access_grants'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    grantor_addr = db.Column(db.String(42), nullable=False)  # Patient blockchain address
    grantee_addr = db.Column(db.String(42), nullable=False)  # Healthcare provider address
    data_id = db.Column(UUID(as_uuid=True), nullable=False)  # Data record ID
    data_type = db.Column(db.String(50), nullable=False)  # Data type
    grant_time = db.Column(db.DateTime, default=datetime.utcnow)
    expire_time = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    blockchain_tx_hash = db.Column(db.String(66))  # Blockchain transaction hash
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<AccessGrant {self.grantor_addr}->{self.grantee_addr}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self.id),
            'grantor_addr': self.grantor_addr,
            'grantee_addr': self.grantee_addr,
            'data_id': str(self.data_id),
            'data_type': self.data_type,
            'grant_time': self.grant_time.isoformat(),
            'expire_time': self.expire_time.isoformat(),
            'is_active': self.is_active,
            'blockchain_tx_hash': self.blockchain_tx_hash,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
