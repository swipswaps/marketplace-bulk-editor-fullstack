"""
Authentication tests
"""
import pytest
from models.user import User


class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_register_success(self, client, db_session):
        """Test successful user registration"""
        response = client.post('/api/auth/register', json={
            'email': 'newuser@example.com',
            'password': 'Test123!@#',
            'first_name': 'New',
            'last_name': 'User'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert data['user']['email'] == 'newuser@example.com'
    
    def test_register_weak_password(self, client, db_session):
        """Test registration with weak password"""
        response = client.post('/api/auth/register', json={
            'email': 'newuser@example.com',
            'password': 'weak',
            'first_name': 'New',
            'last_name': 'User'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_register_duplicate_email(self, client, test_user):
        """Test registration with duplicate email"""
        response = client.post('/api/auth/register', json={
            'email': 'test@example.com',
            'password': 'Test123!@#',
            'first_name': 'Test',
            'last_name': 'User'
        })
        
        assert response.status_code == 409
        data = response.get_json()
        assert 'already registered' in data['error'].lower()
    
    def test_login_success(self, client, test_user):
        """Test successful login"""
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'Test123!@#'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert data['user']['email'] == 'test@example.com'
    
    def test_login_invalid_credentials(self, client, test_user):
        """Test login with invalid credentials"""
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'WrongPassword123!@#'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'invalid credentials' in data['error'].lower()
    
    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user"""
        response = client.post('/api/auth/login', json={
            'email': 'nonexistent@example.com',
            'password': 'Test123!@#'
        })
        
        assert response.status_code == 401
    
    def test_get_current_user(self, client, auth_headers):
        """Test get current user endpoint"""
        response = client.get('/api/auth/me', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['email'] == 'test@example.com'
    
    def test_get_current_user_no_token(self, client):
        """Test get current user without token"""
        response = client.get('/api/auth/me')
        
        assert response.status_code == 401
    
    def test_refresh_token(self, client, test_user):
        """Test token refresh"""
        # Login to get refresh token
        login_response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'Test123!@#'
        })
        
        refresh_token = login_response.get_json()['refresh_token']
        
        # Refresh access token
        response = client.post('/api/auth/refresh', json={
            'refresh_token': refresh_token
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
    
    def test_logout(self, client, auth_headers):
        """Test logout"""
        response = client.post('/api/auth/logout', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'logout successful' in data['message'].lower()

