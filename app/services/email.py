# app/services/email.py

from app.workers.email_worker import send_order_confirmation
from app.models.orders import Order

# async def send_order_email(order: Order):
#     """
#     Queue order confirmation email to be sent
#     """
#     send_order_confirmation.delay(order)
    
async def send_order_email(order: Order):
    # Convert order to dict
    order_dict = {
        "id": order.id,
        "total_price": float(order.total_price),
        "quantity": order.quantity,
        "status": order.status
    }
    send_order_confirmation.delay(order_dict)