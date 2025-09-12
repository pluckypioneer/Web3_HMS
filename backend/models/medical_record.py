"""
Medical Record model for Web3 HMS
"""

from datetime import datetime
from extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class MedicalRecord(db.Model):
    """Medical Record model"""
    __tablename__ = 'emr_records'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = db.Column(UUID(as_uuid=True), db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('doctors.id'), nullable=False)
    record_type = db.Column(db.String(50), nullable=False)  # EMR, PRESCRIPTION, SURGERY, REPORT
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    diagnosis = db.Column(db.Text)
    treatment = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)
    ipfs_cid = db.Column(db.String(100))  # IPFS Content Identifier
    blockchain_tx_hash = db.Column(db.String(66))  # Blockchain transaction hash
    blockchain_hash = db.Column(db.String(64))  # Data hash stored on blockchain
    block_number = db.Column(db.BigInteger)  # Block number where transaction was mined
    is_confidential = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<MedicalRecord {self.title}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self.id),
            'patient_id': str(self.patient_id),
            'doctor_id': str(self.doctor_id),
            'record_type': self.record_type,
            'title': self.title,
            'content': self.content,
            'diagnosis': self.diagnosis,
            'treatment': self.treatment,
            'prescription': self.prescription,
            'notes': self.notes,
            'ipfs_cid': self.ipfs_cid,
            'blockchain_tx_hash': self.blockchain_tx_hash,
            'blockchain_hash': self.blockchain_hash,
            'block_number': self.block_number,
            'is_confidential': self.is_confidential,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def calculate_hash(self):
        """Calculate SHA-256 hash of the record content"""
        import hashlib
        content_to_hash = f"{self.title}{self.content}{self.diagnosis}{self.treatment}{self.prescription}"
        return hashlib.sha256(content_to_hash.encode('utf-8')).hexdigest()
