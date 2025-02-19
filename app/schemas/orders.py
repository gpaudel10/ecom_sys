# app/schemas/orders.py

from typing import Optional
from pydantic import BaseModel, Field, constr, Field, ConfigDict
from decimal import Decimal
from typing import Optional
from datetime import datetime


class OrderBase(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderCreate(OrderBase):
    user_id: int


class OrderUpdate(BaseModel):
    quantity: Optional[int] = Field(default=None, gt=0)
    status: Optional[str] = Field(default=None, pattern=r'^(pending|shipped|delivered|cancelled)$') 


class OrderResponse(OrderBase):
    id: int
    user_id: int
    total_price: Decimal
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductBase(BaseModel):
    name: str
    price: Decimal


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)