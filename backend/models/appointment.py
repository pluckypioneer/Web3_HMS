"""
Appointment model for Web3 HMS
"""

from datetime import datetime
from extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Appointment(db.Model):
    """Appointment model"""
    __tablename__ = 'appointments'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = db.Column(UUID(as_uuid=True), db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('doctors.id'), nullable=False)
    dept_id = db.Column(db.String(50), nullable=False)
    dept_name = db.Column(db.String(100), nullable=False)
    schedule_time = db.Column(db.DateTime, nullable=False)
    appointment_type = db.Column(db.String(50), default='OUTPATIENT')  # OUTPATIENT, FOLLOW_UP, EMERGENCY
    status = db.Column(db.String(20), default='SCHEDULED')  # SCHEDULED, CONFIRMED, CANCELLED, COMPLETED
    reason = db.Column(db.Text)
    notes = db.Column(db.Text)
    fee = db.Column(db.Numeric(10, 2), default=0)
    is_paid = db.Column(db.Boolean, default=False)
    payment_method = db.Column(db.String(50))
    payment_tx_hash = db.Column(db.String(66))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Appointment {self.id}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self.id),
            'patient_id': str(self.patient_id),
            'doctor_id': str(self.doctor_id),
            'dept_id': self.dept_id,
            'dept_name': self.dept_name,
            'schedule_time': self.schedule_time.isoformat(),
            'appointment_type': self.appointment_type,
            'status': self.status,
            'reason': self.reason,
            'notes': self.notes,
            'fee': float(self.fee) if self.fee else 0,
            'is_paid': self.is_paid,
            'payment_method': self.payment_method,
            'payment_tx_hash': self.payment_tx_hash,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
