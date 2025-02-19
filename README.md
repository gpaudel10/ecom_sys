# Order Management API

This is the project structure:

```bash

order_management/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py      # Configuration settings
│   │   ├── security.py    # JWT authentication
│   │   └── database.py    # Database connection
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   └── orders.py
│   │   │   └── router.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── orders.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── orders.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── orders.py
│   │   └── email.py
│   └── workers/
│       ├── __init__.py
│       └── email_worker.py
├── tests/
│   ├── __init__.py
│   └── test_orders.py
├── requirements.txt
└── alembic
└── README.md
```

## Objective
Create a RESTFUL API for managing orders in an e-commerce system.

## Overview
This project is a RESTful Order Management API built with FastAPI and PostgreSQL. It provides a solution for managing e-commerce orders with features like pagination, authentication, email notifications.

## Key Components

1. **API Endpoints**:
   - `POST /orders` - Create a new order
   - `GET /orders/:id` - Retrieve a specific order
   - `GET /orders` - List all orders with pagination
   - `GET /orders/search` - Search orders with filters
   - `PUT /orders/:id` - Update an order
   - `DELETE /orders/:id` - Soft delete (cancel) an order

2. **Database Models**:
   - `Order` - Stores order information with status tracking
   - `Product` - Stores product information for price calculation

3. **Authentication**:
   - JWT-based authentication for API security

4. **Background Processing**:
   - Celery worker  is used for sending order confirmation emails

5. **Caching**:
   - Redis is used for improved order retrieval performance

6. **Testing**:
   - Pytest-based test framework with database transaction management

## Setup instruction

To run this project locally:


1. Clone the repository
```bash
git clone https://github.com/gpaudel10/ecom_sys.git
cd ecom_sys
```

1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  
```

1. Install dependencies
```bash
pip install -r requirements.txt
```

1. Create PostgreSQL databases
```bash
# Connect to PostgreSQL
psql -U postgres

# Create main and test databases
CREATE DATABASE order_db;
CREATE DATABASE test_order_db;
```

5. Set up environment variables by creating a `.env` file:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/order_db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MAIL_USERNAME= your_email
MAIL_PASSWORD=your_password
MAIL_FROM=yor_email
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_FROM_NAME=Order Management System
```

6. Run database migrations
```bash
alembic upgrade head
```

## Running the application

1. Start the main application
```bash
uvicorn app.main:app --reload
```

2. Start Celery worker (in a separate terminal)
```bash
celery -A app.workers.email_worker worker --loglevel=info
```
if permission error the use this:

```bash
celery -A app.workers.email_worker:celery_app worker --loglevel=info --pool=solo
```
3. To check whether mail server is running, try sending an email to yourself from the FastMail app. In shell run ```python``` (after activating env)
```bash

from app.workers.email_worker import send_order_confirmation
result = send_order_confirmation.delay(email="your_mail@gmail.com")
print(f"Task ID: {result.id}")
```
You see the task ID in the output.

## Running tests
```bash
pytest -v
```

## API Documentation

Once the application is running, access the swagger documentation at:
```
http://localhost:8000/docs
