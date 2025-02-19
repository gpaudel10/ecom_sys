# app/workers/email_worker.py

from celery import Celery
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings
from app.models.orders import Order

# Celery setup
celery_app = Celery(
    'email_worker',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True
)

# @celery_app.task
# async def send_order_confirmation(order: Order):
#     message = MessageSchema(
#         subject=f"Order Confirmation - Order #{order.id}",
#         recipients=[settings.MAIL_FROM],
#         body=f"""
#         Thank you for your order!
        
#         Order Details:
#         Order ID: {order.id}
#         Total Price: ${order.total_price}
#         Quantity: {order.quantity}
#         Status: {order.status}
        
#         We will notify you when your order ships.
#         """,
#     )
    
#     fm = FastMail(conf)
#     await fm.send_message(message)

@celery_app.task
def send_order_confirmation(order_dict):
    # Convert dict to order if needed
    
    # Create message
    message = MessageSchema(
        subject=f"Order Confirmation - Order #{order_dict['id']}",
        recipients=[settings.MAIL_FROM],
        body=f"""
        Thank you for your order!
        
        Order Details:
        Order ID: {order_dict['id']}
        Total Price: ${order_dict['total_price']}
        Quantity: {order_dict['quantity']}
        Status: {order_dict['status']}
        
        We will notify you when your order ships.
        """,
    )
    
    # Use synchronous email sending or run async in a sync context
    # This depends on how FastMail can be used synchronously
    fm = FastMail(conf)
    import asyncio
    asyncio.run(fm.send_message(message))