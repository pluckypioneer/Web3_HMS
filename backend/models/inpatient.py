"""
Inpatient model for Web3 HMS
"""

from datetime import datetime
from extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Inpatient(db.Model):
    """Inpatient model"""
    __tablename__ = 'inpatients'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = db.Column(UUID(as_uuid=True), db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('doctors.id'), nullable=False)
    bed_id = db.Column(db.String(50), nullable=False)
    ward_id = db.Column(db.String(50), nullable=False)
    ward_name = db.Column(db.String(100), nullable=False)
    admit_time = db.Column(db.DateTime, nullable=False)
    discharge_time = db.Column(db.DateTime)
    diagnosis = db.Column(db.Text, nullable=False)
    admission_reason = db.Column(db.Text)
    treatment_plan = db.Column(db.Text)
    status = db.Column(db.String(20), default='ADMITTED')  # ADMITTED, DISCHARGED, TRANSFERRED
    total_fee = db.Column(db.Numeric(12, 2), default=0)
    paid_amount = db.Column(db.Numeric(12, 2), default=0)
    insurance_covered = db.Column(db.Numeric(12, 2), default=0)
    is_settled = db.Column(db.Boolean, default=False)
    settlement_tx_hash = db.Column(db.String(66))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Inpatient {self.id}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self.id),
            'patient_id': str(self.patient_id),
            'doctor_id': str(self.doctor_id),
            'bed_id': self.bed_id,
            'ward_id': self.ward_id,
            'ward_name': self.ward_name,
            'admit_time': self.admit_time.isoformat(),
            'discharge_time': self.discharge_time.isoformat() if self.discharge_time else None,
            'diagnosis': self.diagnosis,
            'admission_reason': self.admission_reason,
            'treatment_plan': self.treatment_plan,
            'status': self.status,
            'total_fee': float(self.total_fee) if self.total_fee else 0,
            'paid_amount': float(self.paid_amount) if self.paid_amount else 0,
            'insurance_covered': float(self.insurance_covered) if self.insurance_covered else 0,
            'is_settled': self.is_settled,
            'settlement_tx_hash': self.settlement_tx_hash,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
