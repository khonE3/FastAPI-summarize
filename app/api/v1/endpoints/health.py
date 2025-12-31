"""
Health Check Endpoints
"""
from fastapi import APIRouter
from app.models.schemas import HealthResponse
from app.services.summarizer import summarizer_service
from app.core.config import settings

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="ตรวจสอบสถานะ API",
    description="ตรวจสอบว่า API และ Model พร้อมใช้งานหรือไม่"
)
async def health_check() -> HealthResponse:
    """
    ตรวจสอบสถานะของ API
    
    Returns:
        - status: สถานะของ API
        - model_loaded: สถานะการโหลดโมเดล
        - version: เวอร์ชันของ API
    """
    return HealthResponse(
        status="healthy",
        model_loaded=summarizer_service.is_loaded,
        version=settings.APP_VERSION
    )


@router.get(
    "/",
    summary="Root endpoint",
    description="ข้อมูลพื้นฐานของ API"
)
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to FastAPI Summarize API",
        "docs": "/docs",
        "version": settings.APP_VERSION
    }
