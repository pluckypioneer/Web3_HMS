"""
Doctor API resources for Web3 HMS
"""

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.doctor import Doctor
from extensions import db
import uuid

class DoctorListResource(Resource):
    """Doctor list resource"""
    
    def get(self):
        """Get all doctors"""
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=20)
        parser.add_argument('search', type=str)
        parser.add_argument('dept_id', type=str)
        args = parser.parse_args()
        
        query = Doctor.query.filter_by(is_active=True)
        
        if args['search']:
            query = query.filter(
                Doctor.name.ilike(f"%{args['search']}%") |
                Doctor.license_no.ilike(f"%{args['search']}%") |
                Doctor.specialization.ilike(f"%{args['search']}%")
            )
        
        if args['dept_id']:
            query = query.filter_by(dept_id=args['dept_id'])
        
        doctors = query.paginate(
            page=args['page'],
            per_page=args['per_page'],
            error_out=False
        )
        
        return {
            'doctors': [doctor.to_dict() for doctor in doctors.items],
            'total': doctors.total,
            'pages': doctors.pages,
            'current_page': doctors.page
        }
    
    @jwt_required()
    def post(self):
        """Create new doctor"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='Name is required')
        parser.add_argument('title', required=True, help='Title is required')
        parser.add_argument('dept_id', required=True, help='Department ID is required')
        parser.add_argument('dept_name', required=True, help='Department name is required')
        parser.add_argument('license_no', required=True, help='License number is required')
        parser.add_argument('phone')
        parser.add_argument('email')
        parser.add_argument('specialization')
        parser.add_argument('education')
        parser.add_argument('experience')
        parser.add_argument('blockchain_addr')
        args = parser.parse_args()
        
        # Check if doctor already exists
        existing_doctor = Doctor.query.filter_by(license_no=args['license_no']).first()
        if existing_doctor:
            return {'error': 'Doctor with this license number already exists'}, 400
        
        doctor = Doctor(
            name=args['name'],
            title=args['title'],
            dept_id=args['dept_id'],
            dept_name=args['dept_name'],
            license_no=args['license_no'],
            phone=args['phone'],
            email=args['email'],
            specialization=args['specialization'],
            education=args['education'],
            experience=args['experience'],
            blockchain_addr=args['blockchain_addr']
        )
        
        db.session.add(doctor)
        db.session.commit()
        
        return doctor.to_dict(), 201

class DoctorResource(Resource):
    """Individual doctor resource"""
    
    def get(self, doctor_id):
        """Get doctor by ID"""
        try:
            doctor_uuid = uuid.UUID(doctor_id)
        except ValueError:
            return {'error': 'Invalid doctor ID'}, 400
        
        doctor = Doctor.query.get_or_404(doctor_uuid)
        return doctor.to_dict()
    
    @jwt_required()
    def put(self, doctor_id):
        """Update doctor"""
        try:
            doctor_uuid = uuid.UUID(doctor_id)
        except ValueError:
            return {'error': 'Invalid doctor ID'}, 400
        
        doctor = Doctor.query.get_or_404(doctor_uuid)
        
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('title')
        parser.add_argument('dept_id')
        parser.add_argument('dept_name')
        parser.add_argument('license_no')
        parser.add_argument('phone')
        parser.add_argument('email')
        parser.add_argument('specialization')
        parser.add_argument('education')
        parser.add_argument('experience')
        parser.add_argument('blockchain_addr')
        args = parser.parse_args()
        
        # Update fields
        for key, value in args.items():
            if value is not None:
                setattr(doctor, key, value)
        
        db.session.commit()
        return doctor.to_dict()
    
    @jwt_required()
    def delete(self, doctor_id):
        """Deactivate doctor"""
        try:
            doctor_uuid = uuid.UUID(doctor_id)
        except ValueError:
            return {'error': 'Invalid doctor ID'}, 400
        
        doctor = Doctor.query.get_or_404(doctor_uuid)
        doctor.is_active = False
        db.session.commit()
        
        return {'message': 'Doctor deactivated successfully'}
