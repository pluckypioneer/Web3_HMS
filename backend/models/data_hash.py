"""
Data Hash model for Web3 HMS
"""

from datetime import datetime
from extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class DataHash(db.Model):
    """Data Hash model for blockchain data verification"""
    __tablename__ = 'data_hashes'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data_type = db.Column(db.String(50), nullable=False)  # EMR, PRESCRIPTION, SURGERY, REPORT
    original_id = db.Column(UUID(as_uuid=True), nullable=False)  # Original record ID
    hash_value = db.Column(db.String(64), nullable=False)  # SHA-256 hash
    tx_hash = db.Column(db.String(66))  # Blockchain transaction hash
    block_number = db.Column(db.BigInteger)  # Block number
    contract_address = db.Column(db.String(42))  # Contract address
    gas_used = db.Column(db.BigInteger)  # Gas used for transaction
    gas_price = db.Column(db.BigInteger)  # Gas price
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<DataHash {self.data_type}:{self.original_id}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self.id),
            'data_type': self.data_type,
            'original_id': str(self.original_id),
            'hash_value': self.hash_value,
            'tx_hash': self.tx_hash,
            'block_number': self.block_number,
            'contract_address': self.contract_address,
            'gas_used': self.gas_used,
            'gas_price': self.gas_price,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
