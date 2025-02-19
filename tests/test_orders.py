
# tests/test_orders.py
import pytest
from app.core.security import create_access_token

def test_create_order(client, test_order, db_session):
    print("\n=== Testing Create Order ===")
    
    # Create access token
    access_token = create_access_token({"sub": "testuser"})
    headers = {"Authorization": f"Bearer {access_token}"}
    
    print(f"Access Token: {access_token}")
    print(f"Headers: {headers}")
    print(f"Test Order Data: {test_order}")
    
    # Verify product exists
    from app.models.orders import Product
    product = db_session.query(Product).filter(Product.id == test_order["product_id"]).first()
    print(f"Test Product in DB: {product.id if product else 'Not found'}")
    
    # Make request
    response = client.post("/api/v1/orders/", json=test_order, headers=headers)
    print(f"Response Status: {response.status_code}")
    print(f"Response Body: {response.text}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == test_order["product_id"]
    assert data["quantity"] == test_order["quantity"]
    assert data["user_id"] == test_order["user_id"]