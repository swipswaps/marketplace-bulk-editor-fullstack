"""
Export tests
"""
import pytest
import io


class TestExport:
    """Test export endpoints"""
    
    def test_export_text(self, client, auth_headers, test_listing):
        """Test text export"""
        response = client.post('/api/export/text',
            headers=auth_headers,
            json={}
        )
        
        assert response.status_code == 200
        assert response.mimetype == 'text/plain'
        assert b'TITLE' in response.data
        assert b'Test Solar Panel 300W' in response.data
    
    def test_export_csv(self, client, auth_headers, test_listing):
        """Test CSV export"""
        response = client.post('/api/export/csv',
            headers=auth_headers,
            json={}
        )
        
        assert response.status_code == 200
        assert response.mimetype == 'text/csv'
        assert b'TITLE,PRICE,CONDITION' in response.data
    
    def test_export_json(self, client, auth_headers, test_listing):
        """Test JSON export"""
        response = client.post('/api/export/json',
            headers=auth_headers,
            json={}
        )
        
        assert response.status_code == 200
        assert response.mimetype == 'application/json'
        
        # Parse JSON
        import json
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) > 0
        assert 'TITLE' in data[0]
    
    def test_export_xlsx(self, client, auth_headers, test_listing):
        """Test XLSX export"""
        response = client.post('/api/export/xlsx',
            headers=auth_headers,
            json={}
        )
        
        assert response.status_code == 200
        assert 'spreadsheet' in response.mimetype
    
    def test_export_sql(self, client, auth_headers, test_listing):
        """Test SQL export"""
        response = client.post('/api/export/sql',
            headers=auth_headers,
            json={}
        )
        
        assert response.status_code == 200
        assert b'CREATE TABLE' in response.data
        assert b'INSERT INTO' in response.data
    
    def test_export_specific_listings(self, client, auth_headers, test_listing):
        """Test exporting specific listings"""
        response = client.post('/api/export/json',
            headers=auth_headers,
            json={'listing_ids': [test_listing.id]}
        )
        
        assert response.status_code == 200
        
        import json
        data = json.loads(response.data)
        assert len(data) == 1
    
    def test_export_no_listings(self, client, auth_headers):
        """Test export with no listings"""
        response = client.post('/api/export/json',
            headers=auth_headers,
            json={'listing_ids': ['nonexistent-id']}
        )
        
        assert response.status_code == 404

