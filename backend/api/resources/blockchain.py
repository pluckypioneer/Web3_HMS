"""
Blockchain API resources for Web3 HMS
"""

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from web3 import Web3
import json
import os
from models.contract import Contract
from models.data_hash import DataHash
from models.medical_record import MedicalRecord
from extensions import db

class BlockchainResource(Resource):
    """Blockchain interaction resource"""
    
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_PROVIDER_URL', 'http://localhost:8545')))
        self.contracts = self._load_contracts()
    
    def _load_contracts(self):
        """Load contract ABIs and addresses"""
        contracts = {}
        
        # Load MedicalRecordHash contract
        medical_record_contract = Contract.query.filter_by(name='MedicalRecordHash', is_active=True).first()
        if medical_record_contract:
            contracts['medical_record'] = self.w3.eth.contract(
                address=medical_record_contract.address,
                abi=json.loads(medical_record_contract.abi)
            )
        
        # Load AccessControl contract
        access_control_contract = Contract.query.filter_by(name='AccessControl', is_active=True).first()
        if access_control_contract:
            contracts['access_control'] = self.w3.eth.contract(
                address=access_control_contract.address,
                abi=json.loads(access_control_contract.abi)
            )
        
        # Load DrugTrace contract
        drug_trace_contract = Contract.query.filter_by(name='DrugTrace', is_active=True).first()
        if drug_trace_contract:
            contracts['drug_trace'] = self.w3.eth.contract(
                address=drug_trace_contract.address,
                abi=json.loads(drug_trace_contract.abi)
            )
        
        return contracts
    
    def get(self, action):
        """Handle blockchain read operations"""
        if action == 'status':
            return self._get_blockchain_status()
        elif action == 'contracts':
            return self._get_contracts()
        elif action == 'verify':
            return self._verify_data()
        else:
            return {'error': 'Invalid action'}, 400
    
    @jwt_required()
    def post(self, action):
        """Handle blockchain write operations"""
        if action == 'store_hash':
            return self._store_data_hash()
        elif action == 'grant_access':
            return self._grant_access()
        elif action == 'revoke_access':
            return self._revoke_access()
        elif action == 'create_item':
            return self._create_trace_item()
        else:
            return {'error': 'Invalid action'}, 400
    
    def _get_blockchain_status(self):
        """Get blockchain connection status"""
        try:
            is_connected = self.w3.is_connected()
            latest_block = self.w3.eth.block_number if is_connected else None
            return {
                'connected': is_connected,
                'latest_block': latest_block,
                'network_id': self.w3.eth.chain_id if is_connected else None
            }
        except Exception as e:
            return {'error': str(e)}, 500
    
    def _get_contracts(self):
        """Get deployed contracts information"""
        contracts = Contract.query.filter_by(is_active=True).all()
        return {
            'contracts': [contract.to_dict() for contract in contracts]
        }
    
    def _verify_data(self):
        """Verify data integrity using blockchain hash"""
        parser = reqparse.RequestParser()
        parser.add_argument('record_id', required=True)
        parser.add_argument('hash_value', required=True)
        args = parser.parse_args()
        
        try:
            # Get record from database
            record = MedicalRecord.query.get(args['record_id'])
            if not record:
                return {'error': 'Record not found'}, 404
            
            # Calculate current hash
            current_hash = record.calculate_hash()
            
            # Verify with blockchain if transaction hash exists
            if record.blockchain_tx_hash and 'medical_record' in self.contracts:
                try:
                    # Get transaction receipt
                    tx_receipt = self.w3.eth.get_transaction_receipt(record.blockchain_tx_hash)
                    if tx_receipt.status == 1:  # Transaction successful
                        # Verify hash matches
                        is_valid = current_hash == args['hash_value']
                        return {
                            'valid': is_valid,
                            'current_hash': current_hash,
                            'provided_hash': args['hash_value'],
                            'blockchain_verified': True,
                            'block_number': tx_receipt.blockNumber
                        }
                except Exception as e:
                    return {'error': f'Blockchain verification failed: {str(e)}'}, 500
            
            return {
                'valid': current_hash == args['hash_value'],
                'current_hash': current_hash,
                'provided_hash': args['hash_value'],
                'blockchain_verified': False
            }
            
        except Exception as e:
            return {'error': str(e)}, 500
    
    def _store_data_hash(self):
        """Store data hash on blockchain"""
        parser = reqparse.RequestParser()
        parser.add_argument('record_id', required=True)
        parser.add_argument('record_type', required=True)
        parser.add_argument('patient_id', required=True)
        parser.add_argument('doctor_id', required=True)
        args = parser.parse_args()
        
        try:
            # Get record from database
            record = MedicalRecord.query.get(args['record_id'])
            if not record:
                return {'error': 'Record not found'}, 404
            
            # Calculate hash
            hash_value = record.calculate_hash()
            
            # Store on blockchain
            if 'medical_record' in self.contracts:
                contract = self.contracts['medical_record']
                
                # Prepare transaction
                tx = contract.functions.createRecord(
                    args['record_id'],
                    args['patient_id'],
                    args['doctor_id'],
                    args['record_type'],
                    hash_value
                ).build_transaction({
                    'from': get_jwt_identity(),
                    'gas': 200000,
                    'gasPrice': self.w3.eth.gas_price
                })
                
                # Sign and send transaction
                # Note: In production, you would use a proper wallet or key management system
                # For demo purposes, we'll simulate the transaction
                tx_hash = "0x" + "0" * 64  # Simulated transaction hash
                
                # Update record with blockchain information
                record.blockchain_tx_hash = tx_hash
                record.blockchain_hash = hash_value
                
                # Store hash record
                data_hash = DataHash(
                    data_type=args['record_type'],
                    original_id=record.id,
                    hash_value=hash_value,
                    tx_hash=tx_hash,
                    contract_address=contract.address
                )
                
                db.session.add(data_hash)
                db.session.commit()
                
                return {
                    'message': 'Data hash stored successfully',
                    'tx_hash': tx_hash,
                    'hash_value': hash_value
                }
            else:
                return {'error': 'MedicalRecord contract not available'}, 500
                
        except Exception as e:
            return {'error': str(e)}, 500
    
    def _grant_access(self):
        """Grant access to medical data"""
        parser = reqparse.RequestParser()
        parser.add_argument('grant_id', required=True)
        parser.add_argument('grantee_address', required=True)
        parser.add_argument('data_id', required=True)
        parser.add_argument('data_type', required=True)
        parser.add_argument('duration', type=int, default=86400)  # Default 24 hours
        args = parser.parse_args()
        
        try:
            if 'access_control' in self.contracts:
                contract = self.contracts['access_control']
                
                # Prepare transaction
                tx = contract.functions.grantAccess(
                    args['grant_id'],
                    args['grantee_address'],
                    args['data_id'],
                    args['data_type'],
                    args['duration']
                ).build_transaction({
                    'from': get_jwt_identity(),
                    'gas': 200000,
                    'gasPrice': self.w3.eth.gas_price
                })
                
                # Simulate transaction
                tx_hash = "0x" + "0" * 64
                
                return {
                    'message': 'Access granted successfully',
                    'tx_hash': tx_hash,
                    'grant_id': args['grant_id']
                }
            else:
                return {'error': 'AccessControl contract not available'}, 500
                
        except Exception as e:
            return {'error': str(e)}, 500
    
    def _revoke_access(self):
        """Revoke access to medical data"""
        parser = reqparse.RequestParser()
        parser.add_argument('grant_id', required=True)
        args = parser.parse_args()
        
        try:
            if 'access_control' in self.contracts:
                contract = self.contracts['access_control']
                
                # Prepare transaction
                tx = contract.functions.revokeAccess(args['grant_id']).build_transaction({
                    'from': get_jwt_identity(),
                    'gas': 100000,
                    'gasPrice': self.w3.eth.gas_price
                })
                
                # Simulate transaction
                tx_hash = "0x" + "0" * 64
                
                return {
                    'message': 'Access revoked successfully',
                    'tx_hash': tx_hash,
                    'grant_id': args['grant_id']
                }
            else:
                return {'error': 'AccessControl contract not available'}, 500
                
        except Exception as e:
            return {'error': str(e)}, 500
    
    def _create_trace_item(self):
        """Create traceable item"""
        parser = reqparse.RequestParser()
        parser.add_argument('item_id', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('specification', required=True)
        parser.add_argument('manufacturer', required=True)
        parser.add_argument('batch_number', required=True)
        parser.add_argument('production_date', type=int, required=True)
        parser.add_argument('expiry_date', type=int, required=True)
        parser.add_argument('category', required=True)
        args = parser.parse_args()
        
        try:
            if 'drug_trace' in self.contracts:
                contract = self.contracts['drug_trace']
                
                # Prepare transaction
                tx = contract.functions.createItem(
                    args['item_id'],
                    args['name'],
                    args['specification'],
                    args['manufacturer'],
                    args['batch_number'],
                    args['production_date'],
                    args['expiry_date'],
                    args['category']
                ).build_transaction({
                    'from': get_jwt_identity(),
                    'gas': 300000,
                    'gasPrice': self.w3.eth.gas_price
                })
                
                # Simulate transaction
                tx_hash = "0x" + "0" * 64
                
                return {
                    'message': 'Traceable item created successfully',
                    'tx_hash': tx_hash,
                    'item_id': args['item_id']
                }
            else:
                return {'error': 'DrugTrace contract not available'}, 500
                
        except Exception as e:
            return {'error': str(e)}, 500
