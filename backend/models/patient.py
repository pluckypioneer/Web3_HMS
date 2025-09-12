"""
Patient model for Web3 HMS
"""

from datetime import datetime
from extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Patient(db.Model):
    """Patient model"""
    __tablename__ = 'patients'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    id_card = db.Column(db.String(18), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(10))
    emergency_contact = db.Column(db.String(100))
    emergency_phone = db.Column(db.String(20))
    medical_card_id = db.Column(db.String(50), unique=True)
    blockchain_addr = db.Column(db.String(42))  # Ethereum address
    insurance_type = db.Column(db.String(50))
    insurance_number = db.Column(db.String(50))
    allergies = db.Column(db.Text)
    medical_history = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='patient', lazy='dynamic')
    medical_records = db.relationship('MedicalRecord', backref='patient', lazy='dynamic')
    inpatients = db.relationship('Inpatient', backref='patient', lazy='dynamic')
    
    def __repr__(self):
        return f'<Patient {self.name}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self.id),
            'name': self.name,
            'id_card': self.id_card,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'gender': self.gender,
            'emergency_contact': self.emergency_contact,
            'emergency_phone': self.emergency_phone,
            'medical_card_id': self.medical_card_id,
            'blockchain_addr': self.blockchain_addr,
            'insurance_type': self.insurance_type,
            'insurance_number': self.insurance_number,
            'allergies': self.allergies,
            'medical_history': self.medical_history,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
