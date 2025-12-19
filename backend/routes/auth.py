"""
Authentication routes
"""
from datetime import datetime
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from models.user import db, User
from schemas.user_schema import RegisterSchema, LoginSchema, UserSchema
from utils.auth import generate_access_token, generate_refresh_token, verify_token, token_required
from utils.audit import log_action

auth_bp = Blueprint('auth', __name__)

register_schema = RegisterSchema()
login_schema = LoginSchema()
user_schema = UserSchema()


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user"""
    try:
        # Validate input
        data = register_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    
    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    # Create user
    user = User(
        email=data['email'],
        first_name=data.get('first_name'),
        last_name=data.get('last_name')
    )
    user.set_password(data['password'])
    
    try:
        db.session.add(user)
        db.session.commit()
        
        # Log action
        log_action(user.id, 'register', 'user', user.id, 201)
        
        # Generate tokens
        access_token = generate_access_token(user.id)
        refresh_token = generate_refresh_token(user.id)
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user_schema.dump(user),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed', 'details': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        # Validate input
        data = login_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    
    # Find user
    user = User.query.filter_by(email=data['email']).first()
    
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Check if account is locked
    if user.locked_until and user.locked_until > datetime.utcnow():
        return jsonify({'error': 'Account is locked. Please try again later.'}), 403
    
    # Check password
    if not user.check_password(data['password']):
        # Increment failed login attempts
        user.failed_login_attempts += 1
        if user.failed_login_attempts >= 5:
            from datetime import timedelta
            user.locked_until = datetime.utcnow() + timedelta(minutes=30)
        db.session.commit()
        
        log_action(user.id, 'login_failed', 'user', user.id, 401)
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Check if user is active
    if not user.is_active:
        return jsonify({'error': 'Account is inactive'}), 403
    
    # Reset failed login attempts
    user.failed_login_attempts = 0
    user.locked_until = None
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # Log action
    log_action(user.id, 'login', 'user', user.id, 200)
    
    # Generate tokens
    access_token = generate_access_token(user.id)
    refresh_token = generate_refresh_token(user.id)
    
    return jsonify({
        'message': 'Login successful',
        'user': user_schema.dump(user),
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """Refresh access token"""
    refresh_token = request.json.get('refresh_token')
    
    if not refresh_token:
        return jsonify({'error': 'Refresh token is missing'}), 401
    
    # Verify refresh token
    payload = verify_token(refresh_token, 'refresh')
    if not payload:
        return jsonify({'error': 'Invalid or expired refresh token'}), 401
    
    # Get user
    user = User.query.get(payload['user_id'])
    if not user or not user.is_active:
        return jsonify({'error': 'User not found or inactive'}), 401
    
    # Generate new access token
    access_token = generate_access_token(user.id)
    
    return jsonify({
        'access_token': access_token
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """Logout user"""
    # Log action
    log_action(current_user.id, 'logout', 'user', current_user.id, 200)
    
    # Note: With JWT, logout is handled client-side by removing tokens
    # For server-side logout, implement token blacklist with Redis
    
    return jsonify({'message': 'Logout successful'}), 200


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """Get current user info"""
    return jsonify(user_schema.dump(current_user)), 200

