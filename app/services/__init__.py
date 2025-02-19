
# app/services/__init__.py
from app.services.orders import OrderService
from app.workers.email_worker import send_order_confirmation