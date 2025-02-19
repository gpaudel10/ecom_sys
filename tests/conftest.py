
# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from decimal import Decimal
from app.core.database import Base, get_db
from app.models.orders import Order, Product
from app.main import app
from fastapi.testclient import TestClient
from app.core.security import create_access_token

@pytest.fixture(scope="session")
def engine():
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    return create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

@pytest.fixture(scope="function")
def db_session(engine):
    Base.metadata.drop_all(bind=engine)  # Clear existing tables
    Base.metadata.create_all(bind=engine)  # Create new tables
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    # Create test product
    test_product = Product(
        id=1,
        name="Test Product",
        price=Decimal("100.00")
    )
    db.add(test_product)
    db.commit()
    
    yield db
    
    db.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def test_order():
    return {
        "product_id": 1,
        "quantity": 2,
        "user_id": 1
    }

# Mock email sending
@pytest.fixture(autouse=True)
def mock_email_worker(monkeypatch):
    async def mock_send(*args, **kwargs):
        return True
    monkeypatch.setattr("app.workers.email_worker.send_order_confirmation", mock_send)