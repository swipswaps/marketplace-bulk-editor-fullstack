"""
Pytest configuration and fixtures
"""
import pytest
from app import create_app
from models.user import db
from models import User, Listing, Template, OCRScan, AuditLog


@pytest.fixture(scope='session')
def app():
    """Create application for testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture(scope='function')
def db_session(app):
    """Create database session for testing"""
    with app.app_context():
        # Clear all tables
        db.session.query(AuditLog).delete()
        db.session.query(Listing).delete()
        db.session.query(Template).delete()
        db.session.query(OCRScan).delete()
        db.session.query(User).delete()
        db.session.commit()
        
        yield db.session
        
        # Cleanup
        db.session.rollback()


@pytest.fixture
def test_user(db_session):
    """Create test user"""
    user = User(
        email='test@example.com',
        first_name='Test',
        last_name='User'
    )
    user.set_password('Test123!@#')
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers"""
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'Test123!@#'
    })
    
    data = response.get_json()
    access_token = data['access_token']
    
    return {'Authorization': f'Bearer {access_token}'}


@pytest.fixture
def test_listing(db_session, test_user):
    """Create test listing"""
    listing = Listing(
        user_id=test_user.id,
        title='Test Solar Panel 300W',
        price=199.99,
        condition='New',
        description='High-efficiency solar panel',
        category='Electronics',
        offer_shipping='Yes'
    )
    db_session.add(listing)
    db_session.commit()
    return listing

