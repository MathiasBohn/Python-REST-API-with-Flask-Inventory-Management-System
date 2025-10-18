import pytest
from unittest.mock import patch
from app import app, inventory

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def reset_inventory():
    original = inventory.copy()
    yield
    inventory.clear()
    inventory.extend(original)

# Test GET /inventory
def test_get_all(client):
    response = client.get('/inventory')
    assert response.status_code == 200
    assert len(response.json) >= 5

# Test GET /inventory/<id> - success
def test_get_one_success(client):
    response = client.get('/inventory/1')
    assert response.status_code == 200
    assert response.json['id'] == 1

# Test GET /inventory/<id> - not found
def test_get_one_not_found(client):
    response = client.get('/inventory/9999')
    assert response.status_code == 404

# Test POST /inventory - success
def test_add_success(client, reset_inventory):
    new_item = {"product_name": "Test Product", "brands": "Test", "quantity": 10}
    response = client.post('/inventory', json=new_item)
    assert response.status_code == 201
    assert response.json['product_name'] == "Test Product"

# Test POST /inventory - validation error
def test_add_validation_error(client):
    response = client.post('/inventory', json={"brands": "Test"})
    assert response.status_code == 400

# Test PATCH /inventory/<id> - success
def test_update_success(client, reset_inventory):
    response = client.patch('/inventory/1', json={"quantity": 100})
    assert response.status_code == 200
    assert response.json['quantity'] == 100

# Test PATCH /inventory/<id> - not found
def test_update_not_found(client):
    response = client.patch('/inventory/9999', json={"quantity": 100})
    assert response.status_code == 404

# Test PATCH with no data
def test_update_no_data(client):
    response = client.patch('/inventory/1', json={})
    assert response.status_code == 400

# Test DELETE /inventory/<id> - success
def test_delete_success(client, reset_inventory):
    response = client.delete('/inventory/1')
    assert response.status_code == 200
    verify = client.get('/inventory/1')
    assert verify.status_code == 404

# Test DELETE /inventory/<id> - not found
def test_delete_not_found(client):
    response = client.delete('/inventory/9999')
    assert response.status_code == 404

# Test GET /inventory/search/barcode/<barcode> - mocked success
@patch('app.fetch_openfoodfacts')
def test_search_success(mock_fetch, client):
    mock_fetch.return_value = {"product_name": "Test", "brands": "Brand"}
    response = client.get('/inventory/search/barcode/123')
    assert response.status_code == 200

# Test GET /inventory/search/barcode/<barcode> - not found
@patch('app.fetch_openfoodfacts')
def test_search_not_found(mock_fetch, client):
    mock_fetch.return_value = None
    response = client.get('/inventory/search/barcode/000')
    assert response.status_code == 404

# Test POST /inventory/import/<barcode> - success
@patch('app.fetch_openfoodfacts')
def test_import_success(mock_fetch, client, reset_inventory):
    mock_fetch.return_value = {
        "code": "123", "product_name": "Imported", "brands": "Brand"
    }
    response = client.post('/inventory/import/123', json={"quantity": 25})
    assert response.status_code == 201
    assert response.json['product_name'] == "Imported"

# Test POST /inventory/import/<barcode> - not found
@patch('app.fetch_openfoodfacts')
def test_import_not_found(mock_fetch, client):
    mock_fetch.return_value = None
    response = client.post('/inventory/import/000')
    assert response.status_code == 404

# Test health check
def test_health(client):
    response = client.get('/')
    assert response.status_code == 200