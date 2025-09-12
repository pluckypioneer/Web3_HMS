"""
Drug model for Web3 HMS
"""

from datetime import datetime
from extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Drug(db.Model):
    """Drug model"""
    __tablename__ = 'drugs'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(200), nullable=False)
    generic_name = db.Column(db.String(200))
    specification = db.Column(db.String(100))
    manufacturer = db.Column(db.String(200))
    batch_number = db.Column(db.String(100))
    production_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)
    category = db.Column(db.String(50))  # DRUG, MEDICAL_DEVICE, CONSUMABLE
    unit = db.Column(db.String(20))  # 片, 盒, 支, 瓶
    unit_price = db.Column(db.Numeric(10, 2))
    stock = db.Column(db.Integer, default=0)
    min_stock = db.Column(db.Integer, default=10)
    max_stock = db.Column(db.Integer, default=1000)
    supplier = db.Column(db.String(200))
    blockchain_trace_id = db.Column(db.String(100))  # Blockchain trace ID
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Drug {self.name}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self.id),
            'name': self.name,
            'generic_name': self.generic_name,
            'specification': self.specification,
            'manufacturer': self.manufacturer,
            'batch_number': self.batch_number,
            'production_date': self.production_date.isoformat() if self.production_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'category': self.category,
            'unit': self.unit,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'stock': self.stock,
            'min_stock': self.min_stock,
            'max_stock': self.max_stock,
            'supplier': self.supplier,
            'blockchain_trace_id': self.blockchain_trace_id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
