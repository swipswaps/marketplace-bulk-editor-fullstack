"""
API testing script
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_register():
    """Test user registration"""
    print("\n=== Testing User Registration ===")
    data = {
        "email": "test@example.com",
        "password": "Test123!@#",
        "first_name": "Test",
        "last_name": "User"
    }
    response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        return response.json()
    return None

def test_login():
    """Test user login"""
    print("\n=== Testing User Login ===")
    data = {
        "email": "test@example.com",
        "password": "Test123!@#"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        return response.json()
    return None

def test_create_listing(access_token):
    """Test listing creation"""
    print("\n=== Testing Listing Creation ===")
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "title": "Test Solar Panel 300W",
        "price": "199.99",
        "condition": "New",
        "description": "High-efficiency solar panel",
        "category": "Electronics",
        "offer_shipping": "Yes"
    }
    response = requests.post(f"{BASE_URL}/api/listings", json=data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        return response.json()
    return None

def test_get_listings(access_token):
    """Test get listings"""
    print("\n=== Testing Get Listings ===")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/api/listings", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_export_xlsx(access_token):
    """Test XLSX export"""
    print("\n=== Testing XLSX Export ===")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(f"{BASE_URL}/api/export/xlsx", json={}, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        with open("test_export.xlsx", "wb") as f:
            f.write(response.content)
        print("✓ XLSX file saved as test_export.xlsx")
        return True
    else:
        print(f"Error: {response.json()}")
    return False

def run_tests():
    """Run all tests"""
    print("=" * 60)
    print("MARKETPLACE BULK EDITOR - API TESTS")
    print("=" * 60)
    
    # Test health
    if not test_health():
        print("\n✗ Health check failed. Is the server running?")
        return
    
    # Test registration
    register_result = test_register()
    if not register_result:
        print("\n✗ Registration failed")
        return
    
    access_token = register_result.get('access_token')
    
    # Test login
    login_result = test_login()
    if login_result:
        access_token = login_result.get('access_token')
    
    # Test listing creation
    listing_result = test_create_listing(access_token)
    if not listing_result:
        print("\n✗ Listing creation failed")
        return
    
    # Test get listings
    test_get_listings(access_token)
    
    # Test export
    test_export_xlsx(access_token)
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS COMPLETED")
    print("=" * 60)

if __name__ == '__main__':
    run_tests()

