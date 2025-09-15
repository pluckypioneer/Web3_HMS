"""
Appointment API resources for Web3 HMS
"""

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.appointment import Appointment
from models.patient import Patient
from models.doctor import Doctor
from extensions import db
import uuid
from datetime import datetime

class AppointmentListResource(Resource):
    """Appointment list resource"""
    
    def get(self):
        """Get all appointments"""
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=20)
        parser.add_argument('patient_id', type=str)
        parser.add_argument('doctor_id', type=str)
        parser.add_argument('status', type=str)
        parser.add_argument('date_from', type=str)
        parser.add_argument('date_to', type=str)
        args = parser.parse_args()
        
        query = Appointment.query
        
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
        
        if args['status']:
            query = query.filter_by(status=args['status'])
        
        if args['date_from']:
            try:
                date_from = datetime.fromisoformat(args['date_from'])
                query = query.filter(Appointment.schedule_time >= date_from)
            except ValueError:
                return {'error': 'Invalid date_from format'}, 400
        
        if args['date_to']:
            try:
                date_to = datetime.fromisoformat(args['date_to'])
                query = query.filter(Appointment.schedule_time <= date_to)
            except ValueError:
                return {'error': 'Invalid date_to format'}, 400
        
        appointments = query.paginate(
            page=args['page'],
            per_page=args['per_page'],
            error_out=False
        )
        
        return {
            'appointments': [appointment.to_dict() for appointment in appointments.items],
            'total': appointments.total,
            'pages': appointments.pages,
            'current_page': appointments.page
        }
    
    @jwt_required()
    def post(self):
        """Create new appointment"""
        parser = reqparse.RequestParser()
        parser.add_argument('patient_id', required=True, help='Patient ID is required')
        parser.add_argument('doctor_id', required=True, help='Doctor ID is required')
        parser.add_argument('dept_id', required=True, help='Department ID is required')
        parser.add_argument('dept_name', required=True, help='Department name is required')
        parser.add_argument('schedule_time', required=True, help='Schedule time is required')
        parser.add_argument('appointment_type', default='OUTPATIENT')
        parser.add_argument('reason')
        parser.add_argument('notes')
        parser.add_argument('fee', type=float, default=0)
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
        
        # Parse schedule time
        try:
            schedule_time = datetime.fromisoformat(args['schedule_time'])
        except ValueError:
            return {'error': 'Invalid schedule_time format'}, 400
        
        appointment = Appointment(
            patient_id=patient_uuid,
            doctor_id=doctor_uuid,
            dept_id=args['dept_id'],
            dept_name=args['dept_name'],
            schedule_time=schedule_time,
            appointment_type=args['appointment_type'],
            reason=args['reason'],
            notes=args['notes'],
            fee=args['fee']
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        return appointment.to_dict(), 201

class AppointmentResource(Resource):
    """Individual appointment resource"""
    
    def get(self, appointment_id):
        """Get appointment by ID"""
        try:
            appointment_uuid = uuid.UUID(appointment_id)
        except ValueError:
            return {'error': 'Invalid appointment ID'}, 400
        
        appointment = Appointment.query.get_or_404(appointment_uuid)
        return appointment.to_dict()
    
    @jwt_required()
    def put(self, appointment_id):
        """Update appointment"""
        try:
            appointment_uuid = uuid.UUID(appointment_id)
        except ValueError:
            return {'error': 'Invalid appointment ID'}, 400
        
        appointment = Appointment.query.get_or_404(appointment_uuid)
        
        parser = reqparse.RequestParser()
        parser.add_argument('schedule_time')
        parser.add_argument('appointment_type')
        parser.add_argument('status')
        parser.add_argument('reason')
        parser.add_argument('notes')
        parser.add_argument('fee', type=float)
        parser.add_argument('is_paid', type=bool)
        parser.add_argument('payment_method')
        parser.add_argument('payment_tx_hash')
        args = parser.parse_args()
        
        # Parse schedule time if provided
        if args['schedule_time']:
            try:
                schedule_time = datetime.fromisoformat(args['schedule_time'])
                appointment.schedule_time = schedule_time
            except ValueError:
                return {'error': 'Invalid schedule_time format'}, 400
        
        # Update fields
        for key, value in args.items():
            if value is not None and key != 'schedule_time':
                setattr(appointment, key, value)
        
        db.session.commit()
        return appointment.to_dict()
    
    @jwt_required()
    def delete(self, appointment_id):
        """Cancel appointment"""
        try:
            appointment_uuid = uuid.UUID(appointment_id)
        except ValueError:
            return {'error': 'Invalid appointment ID'}, 400
        
        appointment = Appointment.query.get_or_404(appointment_uuid)
        appointment.status = 'CANCELLED'
        db.session.commit()
        
        return {'message': 'Appointment cancelled successfully'}
