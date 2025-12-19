"""
Templates routes
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from models.user import db
from models.template import Template
from schemas.template_schema import TemplateSchema, TemplateCreateSchema, TemplateUpdateSchema
from utils.auth import token_required
from utils.audit import log_action

templates_bp = Blueprint('templates', __name__)

template_schema = TemplateSchema()
templates_schema = TemplateSchema(many=True)
template_create_schema = TemplateCreateSchema()
template_update_schema = TemplateUpdateSchema()


@templates_bp.route('', methods=['GET'])
@token_required
def get_templates(current_user):
    """Get all templates for current user"""
    # Get user's own templates and public templates
    templates = Template.query.filter(
        db.or_(
            Template.user_id == current_user.id,
            Template.is_public == True
        )
    ).all()
    
    return jsonify({
        'templates': templates_schema.dump(templates)
    }), 200


@templates_bp.route('/<template_id>', methods=['GET'])
@token_required
def get_template(current_user, template_id):
    """Get template by ID"""
    template = Template.query.filter(
        Template.id == template_id,
        db.or_(
            Template.user_id == current_user.id,
            Template.is_public == True
        )
    ).first()
    
    if not template:
        return jsonify({'error': 'Template not found'}), 404
    
    return jsonify(template_schema.dump(template)), 200


@templates_bp.route('', methods=['POST'])
@token_required
def create_template(current_user):
    """Create new template"""
    try:
        data = template_create_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    
    # Create template
    template = Template(
        user_id=current_user.id,
        name=data['name'],
        description=data.get('description'),
        template_data=data['template_data'],
        is_public=data.get('is_public', False)
    )
    
    try:
        db.session.add(template)
        db.session.commit()
        
        log_action(current_user.id, 'create_template', 'template', template.id, 201)
        
        return jsonify({
            'message': 'Template created successfully',
            'template': template_schema.dump(template)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create template', 'details': str(e)}), 500


@templates_bp.route('/<template_id>', methods=['PUT'])
@token_required
def update_template(current_user, template_id):
    """Update template"""
    template = Template.query.filter_by(id=template_id, user_id=current_user.id).first()
    
    if not template:
        return jsonify({'error': 'Template not found'}), 404
    
    try:
        data = template_update_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    
    # Update fields
    for key, value in data.items():
        setattr(template, key, value)
    
    try:
        db.session.commit()
        
        log_action(current_user.id, 'update_template', 'template', template.id, 200)
        
        return jsonify({
            'message': 'Template updated successfully',
            'template': template_schema.dump(template)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update template', 'details': str(e)}), 500


@templates_bp.route('/<template_id>', methods=['DELETE'])
@token_required
def delete_template(current_user, template_id):
    """Delete template"""
    template = Template.query.filter_by(id=template_id, user_id=current_user.id).first()
    
    if not template:
        return jsonify({'error': 'Template not found'}), 404
    
    try:
        db.session.delete(template)
        db.session.commit()
        
        log_action(current_user.id, 'delete_template', 'template', template_id, 200)
        
        return jsonify({'message': 'Template deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete template', 'details': str(e)}), 500


@templates_bp.route('/<template_id>/use', methods=['POST'])
@token_required
def use_template(current_user, template_id):
    """Increment template use count"""
    template = Template.query.filter(
        Template.id == template_id,
        db.or_(
            Template.user_id == current_user.id,
            Template.is_public == True
        )
    ).first()
    
    if not template:
        return jsonify({'error': 'Template not found'}), 404
    
    try:
        template.use_count += 1
        db.session.commit()
        
        return jsonify({
            'message': 'Template use count updated',
            'template': template_schema.dump(template)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update template', 'details': str(e)}), 500

