"""
Authentication API resources for Web3 HMS
"""

from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import request
from models.user import User
from extensions import db
from utils.security import (
    log_security_event, log_audit_event, log_error, 
    sanitize_input, InputValidator
)
import uuid

class LoginResource(Resource):
    """User login resource with enhanced security"""
    
    def post(self):
        """Authenticate user and return JWT token"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', required=True, help='Email is required')
            parser.add_argument('password', required=True, help='Password is required')
            args = parser.parse_args()
            
            # Input validation and sanitization
            email = sanitize_input(args['email']).lower()
            password = args['password']  # Don't sanitize password to preserve exact input
            
            # Validate email format
            if not InputValidator.validate_email(email):
                log_security_event('INVALID_EMAIL_FORMAT', f'Invalid email format: {email[:20]}...')
                return {
                    'message': 'Invalid email format',
                    'error': 'INVALID_EMAIL'
                }, 400
            
            # Rate limiting check - log multiple failed attempts
            client_ip = request.remote_addr
            
            # Find user by email
            user = User.query.filter_by(email=email, is_active=True).first()
            
            if not user:
                log_security_event('LOGIN_FAILED', f'Login attempt with non-existent email: {email} from {client_ip}')
                return {
                    'message': 'Invalid email or password',
                    'error': 'AUTHENTICATION_FAILED'
                }, 401
            
            if not user.check_password(password):
                log_security_event('LOGIN_FAILED', f'Wrong password for user: {user.id} from {client_ip}', 'WARNING')
                return {
                    'message': 'Invalid email or password',
                    'error': 'AUTHENTICATION_FAILED'
                }, 401
            
            # Successful login
            access_token = create_access_token(identity=str(user.id))
            
            # Update last login time
            user.last_login = db.func.now()
            db.session.commit()
            
            # Log successful login
            log_audit_event('LOGIN_SUCCESS', 'user', str(user.id), {
                'email': email,
                'ip_address': client_ip
            })
            
            return {
                'token': access_token,
                'user': {
                    'id': str(user.id),
                    'email': user.email,
                    'username': user.username,
                    'role': user.role,
                    'blockchain_addr': user.blockchain_addr
                }
            }, 200
            
        except Exception as e:
            error_id = log_error(e, 'Login process failed')
            return {
                'message': 'Login failed due to server error',
                'error': 'SERVER_ERROR',
                'error_id': error_id
            }, 500

class UserProfileResource(Resource):
    """User profile resource with enhanced security"""
    
    @jwt_required()
    def get(self):
        """Get current user profile"""
        try:
            current_user_id = get_jwt_identity()
            
            # Validate UUID format
            if not InputValidator.validate_uuid(current_user_id):
                log_security_event('INVALID_USER_ID', f'Invalid user ID format: {current_user_id}')
                return {'message': 'Invalid user ID format'}, 400
            
            user_uuid = uuid.UUID(current_user_id)
            user = User.query.get(user_uuid)
            
            if not user:
                log_security_event('USER_NOT_FOUND', f'User not found: {current_user_id}')
                return {'message': 'User not found'}, 404
            
            if not user.is_active:
                log_security_event('INACTIVE_USER_ACCESS', f'Inactive user access attempt: {current_user_id}')
                return {'message': 'User account is inactive'}, 403
            
            # Log profile access
            log_audit_event('PROFILE_ACCESS', 'user', current_user_id)
            
            return {
                'id': str(user.id),
                'email': user.email,
                'username': user.username,
                'role': user.role,
                'blockchain_addr': user.blockchain_addr
            }, 200
            
        except ValueError:
            log_security_event('INVALID_USER_ID', f'Invalid user ID format: {current_user_id}')
            return {'message': 'Invalid user ID format'}, 400
        except Exception as e:
            error_id = log_error(e, 'Profile access failed')
            return {
                'message': 'Failed to get user profile',
                'error_id': error_id
            }, 500

    @jwt_required()
    def put(self):
        """Update current user profile with validation"""
        try:
            current_user_id = get_jwt_identity()
            
            # Validate UUID format
            if not InputValidator.validate_uuid(current_user_id):
                return {'message': 'Invalid user ID format'}, 400
                
            user_uuid = uuid.UUID(current_user_id)
            user = User.query.get(user_uuid)
            
            if not user:
                return {'message': 'User not found'}, 404
            
            if not user.is_active:
                return {'message': 'User account is inactive'}, 403
            
            parser = reqparse.RequestParser()
            parser.add_argument('username')
            parser.add_argument('email')
            parser.add_argument('blockchain_addr')
            args = parser.parse_args()
            
            # Track changes for audit
            changes = {}
            
            # Validate and sanitize inputs
            if args.get('username'):
                new_username = sanitize_input(args['username'])
                if len(new_username) < 3 or len(new_username) > 50:
                    return {'message': 'Username must be between 3 and 50 characters'}, 400
                if new_username != user.username:
                    changes['username'] = {'from': user.username, 'to': new_username}
                    user.username = new_username
            
            if args.get('email'):
                new_email = sanitize_input(args['email']).lower()
                if not InputValidator.validate_email(new_email):
                    return {'message': 'Invalid email format'}, 400
                
                # Check if email is already taken by another user
                existing_user = User.query.filter_by(email=new_email).first()
                if existing_user and existing_user.id != user.id:
                    return {'message': 'Email already in use'}, 409
                
                if new_email != user.email:
                    changes['email'] = {'from': user.email, 'to': new_email}
                    user.email = new_email
            
            if args.get('blockchain_addr'):
                new_addr = sanitize_input(args['blockchain_addr'])
                # Basic Ethereum address validation
                if new_addr and (len(new_addr) != 42 or not new_addr.startswith('0x')):
                    return {'message': 'Invalid blockchain address format'}, 400
                if new_addr != user.blockchain_addr:
                    changes['blockchain_addr'] = {'from': user.blockchain_addr, 'to': new_addr}
                    user.blockchain_addr = new_addr
            
            # Only commit if there are changes
            if changes:
                user.updated_at = db.func.now()
                db.session.commit()
                
                # Log profile update
                log_audit_event('PROFILE_UPDATE', 'user', current_user_id, changes)
            
            return {
                'id': str(user.id),
                'email': user.email,
                'username': user.username,
                'role': user.role,
                'blockchain_addr': user.blockchain_addr
            }, 200
            
        except ValueError:
            return {'message': 'Invalid user ID format'}, 400
        except Exception as e:
            db.session.rollback()
            error_id = log_error(e, 'Profile update failed')
            return {
                'message': 'Failed to update user profile',
                'error_id': error_id
            }, 500