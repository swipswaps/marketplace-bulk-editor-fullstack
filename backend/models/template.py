"""
Template model for saving listing templates
"""
import uuid
from datetime import datetime
from models.user import db


class Template(db.Model):
    """Template model for reusable listing configurations"""
    
    __tablename__ = 'templates'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Template data (JSON structure matching Listing fields)
    template_data = db.Column(db.JSON, nullable=False)
    
    # Sharing settings
    is_public = db.Column(db.Boolean, default=False, nullable=False)
    use_count = db.Column(db.Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert template to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'template_data': self.template_data,
            'is_public': self.is_public,
            'use_count': self.use_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Template {self.name}>'

