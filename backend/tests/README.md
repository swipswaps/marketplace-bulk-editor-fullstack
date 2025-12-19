# Backend Tests

Comprehensive test suite for the Marketplace Bulk Editor backend API.

---

## Running Tests

### All Tests

```bash
cd backend
pytest
```

### Specific Test File

```bash
pytest tests/test_auth.py
pytest tests/test_listings.py
pytest tests/test_export.py
```

### Specific Test

```bash
pytest tests/test_auth.py::TestAuthentication::test_login_success
```

### With Coverage

```bash
pytest --cov=. --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html
```

---

## Test Structure

### Test Files

- **test_auth.py** - Authentication endpoint tests (11 tests)
- **test_listings.py** - Listings CRUD and bulk operations (11 tests)
- **test_export.py** - Multi-format export tests (7 tests)

### Fixtures (conftest.py)

- `app` - Flask application instance
- `client` - Test client for making requests
- `db_session` - Database session with cleanup
- `test_user` - Pre-created test user
- `auth_headers` - Authentication headers with valid token
- `test_listing` - Pre-created test listing

---

## Test Coverage

### Authentication Tests

✅ User registration (success, weak password, duplicate email)  
✅ User login (success, invalid credentials, nonexistent user)  
✅ Get current user (with/without token)  
✅ Token refresh  
✅ Logout  

### Listings Tests

✅ Create listing (success, invalid condition, negative price)  
✅ Get all listings (with pagination)  
✅ Get listing by ID (success, nonexistent)  
✅ Update listing  
✅ Delete listing  
✅ Bulk create listings  

### Export Tests

✅ Export as text  
✅ Export as CSV  
✅ Export as JSON  
✅ Export as XLSX  
✅ Export as SQL  
✅ Export specific listings  
✅ Export with no listings  

---

## Writing New Tests

### Example Test

```python
def test_my_feature(client, auth_headers):
    """Test description"""
    response = client.post('/api/endpoint',
        headers=auth_headers,
        json={'key': 'value'}
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['key'] == 'expected_value'
```

### Using Fixtures

```python
def test_with_user(test_user):
    """Test with pre-created user"""
    assert test_user.email == 'test@example.com'

def test_with_listing(test_listing):
    """Test with pre-created listing"""
    assert test_listing.title == 'Test Solar Panel 300W'
```

---

## Continuous Integration

Tests are designed to run in CI/CD pipelines:

```yaml
# .github/workflows/test.yml
- name: Run tests
  run: |
    cd backend
    pytest --cov=. --cov-report=xml
```

---

## Test Database

Tests use SQLite in-memory database by default (configured in `config.py`):

```python
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
```

---

## Troubleshooting

### Import Errors

Make sure you're in the backend directory:
```bash
cd backend
pytest
```

### Database Errors

Tests automatically create and drop tables. If you see errors, try:
```bash
rm -f test.db
pytest
```

### Missing Dependencies

Install test dependencies:
```bash
pip install pytest pytest-cov
```

---

## Next Steps

- [ ] Add template tests
- [ ] Add OCR tests
- [ ] Add model unit tests
- [ ] Add integration tests
- [ ] Increase coverage to 90%+

