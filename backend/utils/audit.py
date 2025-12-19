"""
Audit logging utilities
"""
from flask import request
from models.user import db
from models.audit_log import AuditLog


def log_action(user_id, action, resource_type=None, resource_id=None, status_code=200, error_message=None, metadata=None):
    """Log user action to audit log"""
    try:
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            request_method=request.method,
            request_path=request.path,
            status_code=status_code,
            error_message=error_message,
            metadata=metadata
        )
        db.session.add(audit_log)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        # Log error but don't fail the request
        print(f"Audit logging failed: {str(e)}")
        return False

