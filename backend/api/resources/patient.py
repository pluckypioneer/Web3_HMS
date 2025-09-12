"""
Patient API resources for Web3 HMS
"""

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.patient import Patient
from extensions import db
import uuid

class PatientListResource(Resource):
    """Patient list resource"""
    
    def get(self):
        """Get all patients"""
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=20)
        parser.add_argument('search', type=str)
        args = parser.parse_args()
        
        query = Patient.query.filter_by(is_active=True)
        
        if args['search']:
            query = query.filter(
                Patient.name.ilike(f"%{args['search']}%") |
                Patient.id_card.ilike(f"%{args['search']}%") |
                Patient.medical_card_id.ilike(f"%{args['search']}%")
            )
        
        patients = query.paginate(
            page=args['page'],
            per_page=args['per_page'],
            error_out=False
        )
        
        return {
            'patients': [patient.to_dict() for patient in patients.items],
            'total': patients.total,
            'pages': patients.pages,
            'current_page': patients.page
        }
    
    @jwt_required()
    def post(self):
        """Create new patient"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='Name is required')
        parser.add_argument('id_card', required=True, help='ID card is required')
        parser.add_argument('phone')
        parser.add_argument('email')
        parser.add_argument('address')
        parser.add_argument('birth_date')
        parser.add_argument('gender')
        parser.add_argument('emergency_contact')
        parser.add_argument('emergency_phone')
        parser.add_argument('medical_card_id')
        parser.add_argument('blockchain_addr')
        parser.add_argument('insurance_type')
        parser.add_argument('insurance_number')
        parser.add_argument('allergies')
        parser.add_argument('medical_history')
        args = parser.parse_args()
        
        # Check if patient already exists
        existing_patient = Patient.query.filter_by(id_card=args['id_card']).first()
        if existing_patient:
            return {'error': 'Patient with this ID card already exists'}, 400
        
        patient = Patient(
            name=args['name'],
            id_card=args['id_card'],
            phone=args['phone'],
            email=args['email'],
            address=args['address'],
            birth_date=args['birth_date'],
            gender=args['gender'],
            emergency_contact=args['emergency_contact'],
            emergency_phone=args['emergency_phone'],
            medical_card_id=args['medical_card_id'],
            blockchain_addr=args['blockchain_addr'],
            insurance_type=args['insurance_type'],
            insurance_number=args['insurance_number'],
            allergies=args['allergies'],
            medical_history=args['medical_history']
        )
        
        db.session.add(patient)
        db.session.commit()
        
        return patient.to_dict(), 201

class PatientResource(Resource):
    """Individual patient resource"""
    
    def get(self, patient_id):
        """Get patient by ID"""
        try:
            patient_uuid = uuid.UUID(patient_id)
        except ValueError:
            return {'error': 'Invalid patient ID'}, 400
        
        patient = Patient.query.get_or_404(patient_uuid)
        return patient.to_dict()
    
    @jwt_required()
    def put(self, patient_id):
        """Update patient"""
        try:
            patient_uuid = uuid.UUID(patient_id)
        except ValueError:
            return {'error': 'Invalid patient ID'}, 400
        
        patient = Patient.query.get_or_404(patient_uuid)
        
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('phone')
        parser.add_argument('email')
        parser.add_argument('address')
        parser.add_argument('birth_date')
        parser.add_argument('gender')
        parser.add_argument('emergency_contact')
        parser.add_argument('emergency_phone')
        parser.add_argument('medical_card_id')
        parser.add_argument('blockchain_addr')
        parser.add_argument('insurance_type')
        parser.add_argument('insurance_number')
        parser.add_argument('allergies')
        parser.add_argument('medical_history')
        args = parser.parse_args()
        
        # Update fields
        for key, value in args.items():
            if value is not None:
                setattr(patient, key, value)
        
        db.session.commit()
        return patient.to_dict()
    
    @jwt_required()
    def delete(self, patient_id):
        """Deactivate patient"""
        try:
            patient_uuid = uuid.UUID(patient_id)
        except ValueError:
            return {'error': 'Invalid patient ID'}, 400
        
        patient = Patient.query.get_or_404(patient_uuid)
        patient.is_active = False
        db.session.commit()
        
        return {'message': 'Patient deactivated successfully'}
