"""
Drug API resources for Web3 HMS
"""

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.drug import Drug
from extensions import db
import uuid

class DrugListResource(Resource):
    """Drug list resource"""
    
    def get(self):
        """Get all drugs"""
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=20)
        parser.add_argument('keyword', type=str)
        args = parser.parse_args()
        
        query = Drug.query.filter_by(is_active=True)
        
        if args['keyword']:
            keyword = f"%{args['keyword']}%"
            query = query.filter(
                Drug.name.ilike(keyword) |
                Drug.generic_name.ilike(keyword) |
                Drug.manufacturer.ilike(keyword) |
                Drug.category.ilike(keyword)
            )
        
        drugs = query.paginate(
            page=args['page'],
            per_page=args['per_page'],
            error_out=False
        )
        
        return {
            'items': [drug.to_dict() for drug in drugs.items],
            'total': drugs.total,
            'pages': drugs.pages,
            'current_page': drugs.page
        }
    
    @jwt_required()
    def post(self):
        """Create new drug"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='Name is required')
        parser.add_argument('generic_name')
        parser.add_argument('specification')
        parser.add_argument('manufacturer')
        parser.add_argument('batch_number')
        parser.add_argument('production_date')
        parser.add_argument('expiry_date')
        parser.add_argument('category')
        parser.add_argument('unit')
        parser.add_argument('unit_price', type=float)
        parser.add_argument('stock', type=int)
        parser.add_argument('min_stock', type=int)
        parser.add_argument('max_stock', type=int)
        parser.add_argument('supplier')
        parser.add_argument('blockchain_trace_id')
        args = parser.parse_args()
        
        drug = Drug(
            name=args['name'],
            generic_name=args['generic_name'],
            specification=args['specification'],
            manufacturer=args['manufacturer'],
            batch_number=args['batch_number'],
            production_date=args['production_date'],
            expiry_date=args['expiry_date'],
            category=args['category'],
            unit=args['unit'],
            unit_price=args['unit_price'],
            stock=args['stock'] if args['stock'] is not None else 0,
            min_stock=args['min_stock'] if args['min_stock'] is not None else 10,
            max_stock=args['max_stock'] if args['max_stock'] is not None else 1000,
            supplier=args['supplier'],
            blockchain_trace_id=args['blockchain_trace_id']
        )
        
        db.session.add(drug)
        db.session.commit()
        
        return drug.to_dict(), 201

class DrugResource(Resource):
    """Individual drug resource"""
    
    def get(self, drug_id):
        """Get drug by ID"""
        try:
            drug_uuid = uuid.UUID(drug_id)
        except ValueError:
            return {'error': 'Invalid drug ID'}, 400
        
        drug = Drug.query.get_or_404(drug_uuid)
        return drug.to_dict()
    
    @jwt_required()
    def put(self, drug_id):
        """Update drug"""
        try:
            drug_uuid = uuid.UUID(drug_id)
        except ValueError:
            return {'error': 'Invalid drug ID'}, 400
        
        drug = Drug.query.get_or_404(drug_uuid)
        
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('generic_name')
        parser.add_argument('specification')
        parser.add_argument('manufacturer')
        parser.add_argument('batch_number')
        parser.add_argument('production_date')
        parser.add_argument('expiry_date')
        parser.add_argument('category')
        parser.add_argument('unit')
        parser.add_argument('unit_price', type=float)
        parser.add_argument('stock', type=int)
        parser.add_argument('min_stock', type=int)
        parser.add_argument('max_stock', type=int)
        parser.add_argument('supplier')
        parser.add_argument('blockchain_trace_id')
        parser.add_argument('is_active', type=bool)
        args = parser.parse_args()
        
        # Update fields
        for key, value in args.items():
            if value is not None:
                setattr(drug, key, value)
        
        db.session.commit()
        return drug.to_dict()
    
    @jwt_required()
    def delete(self, drug_id):
        """Delete drug"""
        try:
            drug_uuid = uuid.UUID(drug_id)
        except ValueError:
            return {'error': 'Invalid drug ID'}, 400
        
        drug = Drug.query.get_or_404(drug_uuid)
        drug.is_active = False
        db.session.commit()
        
        return {'message': 'Drug deleted successfully'}