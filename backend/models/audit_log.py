"""
Audit Log model for tracking user actions
"""
import uuid
from datetime import datetime
from models.user import db


class AuditLog(db.Model):
    """Audit log model for compliance and security"""
    
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True, index=True)
    
    # Action details
    action = db.Column(db.String(100), nullable=False, index=True)  # login, create_listing, delete_listing, etc.
    resource_type = db.Column(db.String(50), nullable=True)  # listing, template, user, etc.
    resource_id = db.Column(db.String(36), nullable=True)
    
    # Request details
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    request_method = db.Column(db.String(10), nullable=True)
    request_path = db.Column(db.String(500), nullable=True)
    
    # Response details
    status_code = db.Column(db.Integer, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    
    # Additional data
    extra_data = db.Column(db.JSON, nullable=True)  # Renamed from metadata to avoid SQLAlchemy conflict
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def to_dict(self):
        """Convert audit log to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'request_method': self.request_method,
            'request_path': self.request_path,
            'status_code': self.status_code,
            'error_message': self.error_message,
            'extra_data': self.extra_data,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<AuditLog {self.action} by {self.user_id}>'

