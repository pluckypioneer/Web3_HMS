"""
Security utilities for Web3 HMS Backend
包含安全相关的工具函数和日志记录功能
"""

import logging
import functools
import traceback
from datetime import datetime
from flask import request, current_app, g
from flask_jwt_extended import get_jwt_identity
import uuid

# 配置安全日志记录器
security_logger = logging.getLogger('security')
audit_logger = logging.getLogger('audit')
error_logger = logging.getLogger('error')

def setup_security_logging():
    """配置安全日志记录"""
    # 安全日志处理器
    security_handler = logging.FileHandler('logs/security.log', encoding='utf-8')
    security_handler.setLevel(logging.WARNING)
    security_formatter = logging.Formatter(
        '%(asctime)s - SECURITY - %(levelname)s - %(message)s'
    )
    security_handler.setFormatter(security_formatter)
    security_logger.addHandler(security_handler)
    security_logger.setLevel(logging.WARNING)
    
    # 审计日志处理器
    audit_handler = logging.FileHandler('logs/audit.log', encoding='utf-8')
    audit_handler.setLevel(logging.INFO)
    audit_formatter = logging.Formatter(
        '%(asctime)s - AUDIT - %(levelname)s - %(message)s'
    )
    audit_handler.setFormatter(audit_formatter)
    audit_logger.addHandler(audit_handler)
    audit_logger.setLevel(logging.INFO)
    
    # 错误日志处理器
    error_handler = logging.FileHandler('logs/error.log', encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter(
        '%(asctime)s - ERROR - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s'
    )
    error_handler.setFormatter(error_formatter)
    error_logger.addHandler(error_handler)
    error_logger.setLevel(logging.ERROR)

def log_security_event(event_type, details, severity='WARNING'):
    """记录安全事件"""
    user_id = None
    try:
        user_id = get_jwt_identity()
    except:
        pass
    
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'event_type': event_type,
        'user_id': user_id,
        'ip_address': request.remote_addr if request else 'unknown',
        'user_agent': request.headers.get('User-Agent', 'unknown') if request else 'unknown',
        'details': details,
        'request_id': getattr(g, 'request_id', 'unknown')
    }
    
    message = f"Event: {event_type} | User: {user_id} | IP: {log_entry['ip_address']} | Details: {details}"
    
    if severity == 'CRITICAL':
        security_logger.critical(message, extra=log_entry)
    elif severity == 'ERROR':
        security_logger.error(message, extra=log_entry)
    else:
        security_logger.warning(message, extra=log_entry)

def log_audit_event(action, resource, resource_id=None, details=None):
    """记录审计事件"""
    user_id = None
    try:
        user_id = get_jwt_identity()
    except:
        pass
    
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'action': action,
        'resource': resource,
        'resource_id': resource_id,
        'user_id': user_id,
        'ip_address': request.remote_addr if request else 'unknown',
        'details': details,
        'request_id': getattr(g, 'request_id', 'unknown')
    }
    
    message = f"Action: {action} | Resource: {resource} | ID: {resource_id} | User: {user_id}"
    audit_logger.info(message, extra=log_entry)

def log_error(error, context=None):
    """记录错误事件"""
    error_id = str(uuid.uuid4())
    
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'error_id': error_id,
        'error_type': type(error).__name__,
        'error_message': str(error),
        'traceback': traceback.format_exc(),
        'context': context,
        'request_id': getattr(g, 'request_id', 'unknown')
    }
    
    if request:
        log_entry.update({
            'method': request.method,
            'url': request.url,
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', 'unknown')
        })
    
    message = f"Error ID: {error_id} | Type: {type(error).__name__} | Message: {str(error)}"
    error_logger.error(message, extra=log_entry)
    
    return error_id

def sanitize_input(input_data):
    """清理和验证输入数据"""
    if isinstance(input_data, str):
        # 移除潜在的危险字符
        dangerous_chars = ['<', '>', '"', "'", '&', '\x00']
        for char in dangerous_chars:
            input_data = input_data.replace(char, '')
        
        # 限制长度
        if len(input_data) > 1000:
            input_data = input_data[:1000]
            
        return input_data.strip()
    
    return input_data

def require_role(required_roles):
    """角色权限装饰器"""
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                current_user_id = get_jwt_identity()
                if not current_user_id:
                    log_security_event('UNAUTHORIZED_ACCESS', f'Attempted access to {f.__name__} without token')
                    return {'message': 'Authentication required'}, 401
                
                # 这里需要查询用户角色，暂时跳过具体实现
                # user = User.query.get(current_user_id)
                # if user.role not in required_roles:
                #     log_security_event('INSUFFICIENT_PRIVILEGES', 
                #                       f'User {current_user_id} attempted to access {f.__name__} without proper role')
                #     return {'message': 'Insufficient privileges'}, 403
                
                return f(*args, **kwargs)
            except Exception as e:
                error_id = log_error(e, f'Role check failed for function {f.__name__}')
                return {'message': 'Authorization error', 'error_id': error_id}, 500
        
        return decorated_function
    return decorator

class InputValidator:
    """输入验证器类"""
    
    @staticmethod
    def validate_email(email):
        """验证邮箱格式"""
        if not email or len(email) > 254:
            return False
        
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password):
        """验证密码强度"""
        if not password or len(password) < 8:
            return False, "密码长度至少8位"
        
        if len(password) > 128:
            return False, "密码长度不能超过128位"
        
        # 检查是否包含数字、字母
        import re
        if not re.search(r'[A-Za-z]', password):
            return False, "密码必须包含字母"
        
        if not re.search(r'\d', password):
            return False, "密码必须包含数字"
        
        return True, "密码符合要求"
    
    @staticmethod
    def validate_uuid(uuid_string):
        """验证UUID格式"""
        try:
            uuid.UUID(uuid_string)
            return True
        except ValueError:
            return False