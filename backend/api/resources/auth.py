"""
Authentication API resources for Web3 HMS
"""

from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User
from extensions import db
import uuid

class LoginResource(Resource):
    """User login resource"""
    
    def post(self):
        """Authenticate user and return JWT token"""
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help='Email is required')
        parser.add_argument('password', required=True, help='Password is required')
        args = parser.parse_args()
        
        # Find user by email
        user = User.query.filter_by(email=args['email'], is_active=True).first()
        
        if not user or not user.check_password(args['password']):
            return {'message': 'Invalid email or password'}, 401
        
        # Create access token
        access_token = create_access_token(identity=str(user.id))
        
        # Update last login time
        user.last_login = db.func.now()
        db.session.commit()
        
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

class UserProfileResource(Resource):
    """User profile resource"""
    
    @jwt_required()
    def get(self):
        """Get current user profile"""
        current_user_id = get_jwt_identity()
        try:
            user_uuid = uuid.UUID(current_user_id)
        except ValueError:
            return {'message': 'Invalid user ID'}, 400
        
        user = User.query.get_or_404(user_uuid)
        
        return {
            'id': str(user.id),
            'email': user.email,
            'username': user.username,
            'role': user.role,
            'blockchain_addr': user.blockchain_addr
        }, 200

    @jwt_required()
    def put(self):
        """Update current user profile"""
        current_user_id = get_jwt_identity()
        try:
            user_uuid = uuid.UUID(current_user_id)
        except ValueError:
            return {'message': 'Invalid user ID'}, 400
        
        user = User.query.get_or_404(user_uuid)
        
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('email')
        parser.add_argument('blockchain_addr')
        args = parser.parse_args()
        
        # Update fields
        for key, value in args.items():
            if value is not None:
                setattr(user, key, value)
        
        db.session.commit()
        
        return {
            'id': str(user.id),
            'email': user.email,
            'username': user.username,
            'role': user.role,
            'blockchain_addr': user.blockchain_addr
        }, 200