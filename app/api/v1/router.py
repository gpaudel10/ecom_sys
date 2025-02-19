# app/api/v1/router.py

from fastapi import APIRouter
from app.api.v1.endpoints import orders, auth, users

api_router = APIRouter()

api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])