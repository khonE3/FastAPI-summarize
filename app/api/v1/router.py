"""
API v1 Router - รวม routes ทั้งหมด
"""
from fastapi import APIRouter
from app.api.v1.endpoints import summarize, health

api_router = APIRouter()

# Include routers
api_router.include_router(health.router)
api_router.include_router(summarize.router)
