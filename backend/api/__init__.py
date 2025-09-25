"""
API Blueprint for Web3 HMS
"""

from flask import Blueprint
from flask_restful import Api

# Create API blueprint
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Import resources
from .resources.patient import PatientResource, PatientListResource
from .resources.doctor import DoctorResource, DoctorListResource
from .resources.appointment import AppointmentResource, AppointmentListResource
from .resources.medical_record import MedicalRecordResource, MedicalRecordListResource
from .resources.blockchain import BlockchainResource
from .resources.auth import LoginResource, UserProfileResource

# Register resources
api.add_resource(PatientListResource, '/patients')
api.add_resource(PatientResource, '/patients/<string:patient_id>')
api.add_resource(DoctorListResource, '/doctors')
api.add_resource(DoctorResource, '/doctors/<string:doctor_id>')
api.add_resource(AppointmentListResource, '/appointments')
api.add_resource(AppointmentResource, '/appointments/<string:appointment_id>')
api.add_resource(MedicalRecordListResource, '/medical-records')
api.add_resource(MedicalRecordResource, '/medical-records/<string:record_id>')
api.add_resource(BlockchainResource, '/blockchain/<string:action>')
api.add_resource(LoginResource, '/auth/login')
api.add_resource(UserProfileResource, '/auth/me')
