#app/services/orders.py

from sqlalchemy.orm import Session
from app.models.orders import Order, Product
from app.schemas.orders import OrderCreate, OrderUpdate
from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException
from app.workers.email_worker import send_order_confirmation

class OrderService:
    def __init__(self, db: Session): 
        self.db = db

    async def create_order(self, order: OrderCreate):
        try:
            # Get product price
            product = self.db.query(Product).filter(Product.id == order.product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            
            # Calculate total price
            total_price = product.price * order.quantity
            
            # Create order
            db_order = Order(
                user_id=order.user_id,
                product_id=order.product_id,
                quantity=order.quantity,
                total_price=total_price,
                status="pending"
            )
            
            self.db.add(db_order)
            self.db.commit()
            self.db.refresh(db_order)
            
            return db_order
            
        except Exception as e:
            self.db.rollback()
            raise


