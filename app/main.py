#app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.database import engine, Base
from fastapi_pagination import add_pagination

# Create database tables
Base.metadata.create_all(bind=engine)

# # app/main.py --> to debug
# # After Base.metadata.create_all(bind=engine)
# print("Database tables created:", Base.metadata.tables.keys())

app = FastAPI(
    title="Order Management API",
    description="This is a REST API for managing orders in an e-commerce system",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api/v1")

# Add pagination
add_pagination(app)

@app.get("/")
async def root():
    return {"message": "welcome to the  Order Management API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}