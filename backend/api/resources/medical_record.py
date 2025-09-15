"""
Medical Record API resources for Web3 HMS
"""

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.medical_record import MedicalRecord
from models.patient import Patient
from models.doctor import Doctor
from extensions import db
import uuid

class MedicalRecordListResource(Resource):
    """Medical Record list resource"""
    
    def get(self):
        """Get all medical records"""
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=20)
        parser.add_argument('patient_id', type=str)
        parser.add_argument('doctor_id', type=str)
        parser.add_argument('record_type', type=str)
        parser.add_argument('search', type=str)
        args = parser.parse_args()
        
        query = MedicalRecord.query.filter_by(is_active=True)
        
        if args['patient_id']:
            try:
                patient_uuid = uuid.UUID(args['patient_id'])
                query = query.filter_by(patient_id=patient_uuid)
            except ValueError:
                return {'error': 'Invalid patient ID'}, 400
        
        if args['doctor_id']:
            try:
                doctor_uuid = uuid.UUID(args['doctor_id'])
                query = query.filter_by(doctor_id=doctor_uuid)
            except ValueError:
                return {'error': 'Invalid doctor ID'}, 400
        
        if args['record_type']:
            query = query.filter_by(record_type=args['record_type'])
        
        if args['search']:
            query = query.filter(
                MedicalRecord.title.ilike(f"%{args['search']}%") |
                MedicalRecord.content.ilike(f"%{args['search']}%") |
                MedicalRecord.diagnosis.ilike(f"%{args['search']}%")
            )
        
        records = query.paginate(
            page=args['page'],
            per_page=args['per_page'],
            error_out=False
        )
        
        return {
            'records': [record.to_dict() for record in records.items],
            'total': records.total,
            'pages': records.pages,
            'current_page': records.page
        }
    
    @jwt_required()
    def post(self):
        """Create new medical record"""
        parser = reqparse.RequestParser()
        parser.add_argument('patient_id', required=True, help='Patient ID is required')
        parser.add_argument('doctor_id', required=True, help='Doctor ID is required')
        parser.add_argument('record_type', required=True, help='Record type is required')
        parser.add_argument('title', required=True, help='Title is required')
        parser.add_argument('content', required=True, help='Content is required')
        parser.add_argument('diagnosis')
        parser.add_argument('treatment')
        parser.add_argument('prescription')
        parser.add_argument('notes')
        parser.add_argument('ipfs_cid')
        parser.add_argument('blockchain_tx_hash')
        parser.add_argument('is_confidential', type=bool, default=False)
        args = parser.parse_args()
        
        # Validate patient exists
        try:
            patient_uuid = uuid.UUID(args['patient_id'])
            patient = Patient.query.get_or_404(patient_uuid)
        except ValueError:
            return {'error': 'Invalid patient ID'}, 400
        
        # Validate doctor exists
        try:
            doctor_uuid = uuid.UUID(args['doctor_id'])
            doctor = Doctor.query.get_or_404(doctor_uuid)
        except ValueError:
            return {'error': 'Invalid doctor ID'}, 400
        
        record = MedicalRecord(
            patient_id=patient_uuid,
            doctor_id=doctor_uuid,
            record_type=args['record_type'],
            title=args['title'],
            content=args['content'],
            diagnosis=args['diagnosis'],
            treatment=args['treatment'],
            prescription=args['prescription'],
            notes=args['notes'],
            ipfs_cid=args['ipfs_cid'],
            blockchain_tx_hash=args['blockchain_tx_hash'],
            is_confidential=args['is_confidential']
        )
        
        # Calculate blockchain hash
        record.blockchain_hash = record.calculate_hash()
        
        db.session.add(record)
        db.session.commit()
        
        return record.to_dict(), 201

class MedicalRecordResource(Resource):
    """Individual medical record resource"""
    
    def get(self, record_id):
        """Get medical record by ID"""
        try:
            record_uuid = uuid.UUID(record_id)
        except ValueError:
            return {'error': 'Invalid record ID'}, 400
        
        record = MedicalRecord.query.get_or_404(record_uuid)
        return record.to_dict()
    
    @jwt_required()
    def put(self, record_id):
        """Update medical record"""
        try:
            record_uuid = uuid.UUID(record_id)
        except ValueError:
            return {'error': 'Invalid record ID'}, 400
        
        record = MedicalRecord.query.get_or_404(record_uuid)
        
        parser = reqparse.RequestParser()
        parser.add_argument('record_type')
        parser.add_argument('title')
        parser.add_argument('content')
        parser.add_argument('diagnosis')
        parser.add_argument('treatment')
        parser.add_argument('prescription')
        parser.add_argument('notes')
        parser.add_argument('ipfs_cid')
        parser.add_argument('blockchain_tx_hash')
        parser.add_argument('block_number', type=int)
        parser.add_argument('is_confidential', type=bool)
        args = parser.parse_args()
        
        # Update fields
        for key, value in args.items():
            if value is not None:
                setattr(record, key, value)
        
        # Recalculate blockchain hash if content changed
        if any(args[key] is not None for key in ['title', 'content', 'diagnosis', 'treatment', 'prescription']):
            record.blockchain_hash = record.calculate_hash()
        
        db.session.commit()
        return record.to_dict()
    
    @jwt_required()
    def delete(self, record_id):
        """Deactivate medical record"""
        try:
            record_uuid = uuid.UUID(record_id)
        except ValueError:
            return {'error': 'Invalid record ID'}, 400
        
        record = MedicalRecord.query.get_or_404(record_uuid)
        record.is_active = False
        db.session.commit()
        
        return {'message': 'Medical record deactivated successfully'}
