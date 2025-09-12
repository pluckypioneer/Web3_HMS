"""
Doctor model for Web3 HMS
"""

from datetime import datetime
from extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Doctor(db.Model):
    """Doctor model"""
    __tablename__ = 'doctors'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(50))  # 主任医师, 副主任医师, 主治医师, 住院医师
    dept_id = db.Column(db.String(50), nullable=False)  # Department ID
    dept_name = db.Column(db.String(100), nullable=False)
    license_no = db.Column(db.String(50), unique=True, nullable=False)  # 执业证号
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    specialization = db.Column(db.Text)  # 专业特长
    education = db.Column(db.Text)  # 学历背景
    experience = db.Column(db.Text)  # 工作经历
    blockchain_addr = db.Column(db.String(42))  # Ethereum address
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='doctor', lazy='dynamic')
    medical_records = db.relationship('MedicalRecord', backref='doctor', lazy='dynamic')
    inpatients = db.relationship('Inpatient', backref='doctor', lazy='dynamic')
    
    def __repr__(self):
        return f'<Doctor {self.name}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self.id),
            'name': self.name,
            'title': self.title,
            'dept_id': self.dept_id,
            'dept_name': self.dept_name,
            'license_no': self.license_no,
            'phone': self.phone,
            'email': self.email,
            'specialization': self.specialization,
            'education': self.education,
            'experience': self.experience,
            'blockchain_addr': self.blockchain_addr,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
