# app/api/v1/endpoints/orders.py

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.orders import OrderCreate, OrderResponse, OrderUpdate
from app.services.orders import OrderService
from fastapi_pagination import Page, paginate
from app.core.security import verify_token
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/", response_model=OrderResponse)

async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return await OrderService(db).create_order(order)

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    order = await OrderService(db).get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/", response_model=Page[OrderResponse])
async def list_orders(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    orders = await OrderService(db).list_orders()
    return paginate(orders)

@router.get("/search/", response_model=Page[OrderResponse])
async def search_orders(
    user_id: Optional[int] = None,
    status: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    orders = await OrderService(db).search_orders(
        user_id=user_id,
        status=status,
        start_date=start_date,
        end_date=end_date
    )
    return paginate(orders)

@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    updated_order = await OrderService(db).update_order(order_id, order_update)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@router.delete("/{order_id}")
async def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    success = await OrderService(db).delete_order(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order cancelled successfully"}