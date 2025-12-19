"""
Listings tests
"""
import pytest


class TestListings:
    """Test listings endpoints"""
    
    def test_create_listing(self, client, auth_headers):
        """Test creating a listing"""
        response = client.post('/api/listings', 
            headers=auth_headers,
            json={
                'title': 'Solar Panel 400W',
                'price': '299.99',
                'condition': 'New',
                'description': 'Premium solar panel',
                'category': 'Electronics',
                'offer_shipping': 'Yes'
            }
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['listing']['title'] == 'Solar Panel 400W'
        assert float(data['listing']['price']) == 299.99
    
    def test_create_listing_invalid_condition(self, client, auth_headers):
        """Test creating listing with invalid condition"""
        response = client.post('/api/listings',
            headers=auth_headers,
            json={
                'title': 'Test Item',
                'price': '99.99',
                'condition': 'Invalid Condition',
                'description': 'Test'
            }
        )
        
        assert response.status_code == 400
    
    def test_create_listing_negative_price(self, client, auth_headers):
        """Test creating listing with negative price"""
        response = client.post('/api/listings',
            headers=auth_headers,
            json={
                'title': 'Test Item',
                'price': '-99.99',
                'condition': 'New'
            }
        )
        
        assert response.status_code == 400
    
    def test_get_listings(self, client, auth_headers, test_listing):
        """Test getting all listings"""
        response = client.get('/api/listings', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'listings' in data
        assert len(data['listings']) > 0
    
    def test_get_listing_by_id(self, client, auth_headers, test_listing):
        """Test getting listing by ID"""
        response = client.get(f'/api/listings/{test_listing.id}', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == test_listing.id
        assert data['title'] == test_listing.title
    
    def test_get_nonexistent_listing(self, client, auth_headers):
        """Test getting nonexistent listing"""
        response = client.get('/api/listings/nonexistent-id', headers=auth_headers)
        
        assert response.status_code == 404
    
    def test_update_listing(self, client, auth_headers, test_listing):
        """Test updating a listing"""
        response = client.put(f'/api/listings/{test_listing.id}',
            headers=auth_headers,
            json={
                'title': 'Updated Solar Panel 300W',
                'price': '249.99'
            }
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['listing']['title'] == 'Updated Solar Panel 300W'
        assert float(data['listing']['price']) == 249.99
    
    def test_delete_listing(self, client, auth_headers, test_listing):
        """Test deleting a listing"""
        response = client.delete(f'/api/listings/{test_listing.id}', headers=auth_headers)
        
        assert response.status_code == 200
        
        # Verify deletion
        get_response = client.get(f'/api/listings/{test_listing.id}', headers=auth_headers)
        assert get_response.status_code == 404
    
    def test_bulk_create_listings(self, client, auth_headers):
        """Test bulk creating listings"""
        response = client.post('/api/listings/bulk',
            headers=auth_headers,
            json={
                'listings': [
                    {
                        'title': 'Item 1',
                        'price': '99.99',
                        'condition': 'New'
                    },
                    {
                        'title': 'Item 2',
                        'price': '149.99',
                        'condition': 'Used - Like New'
                    }
                ]
            }
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert len(data['listings']) == 2
    
    def test_pagination(self, client, auth_headers, test_listing):
        """Test listings pagination"""
        response = client.get('/api/listings?page=1&per_page=10', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'page' in data
        assert 'per_page' in data
        assert 'total' in data

