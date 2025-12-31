"""
Summarization Endpoints
"""
from fastapi import APIRouter, HTTPException, status
from app.models.schemas import SummarizeRequest, SummarizeResponse, ErrorResponse
from app.services.summarizer import summarizer_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/summarize", tags=["Summarization"])


@router.post(
    "/",
    response_model=SummarizeResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="สรุปข้อความ",
    description="รับข้อความและสรุปด้วย AI Model"
)
async def summarize_text(request: SummarizeRequest) -> SummarizeResponse:
    """
    สรุปข้อความด้วย AI
    
    - **text**: ข้อความที่ต้องการสรุป
    - **max_length**: ความยาวสูงสุดของข้อความสรุป (default: 150)
    - **min_length**: ความยาวต่ำสุดของข้อความสรุป (default: 30)
    """
    try:
        # Summarize the text
        summary = summarizer_service.summarize(
            text=request.text,
            max_length=request.max_length,
            min_length=request.min_length
        )
        
        # Calculate compression ratio
        original_length = len(request.text)
        summary_length = len(summary)
        compression_ratio = round(1 - (summary_length / original_length), 2)
        
        return SummarizeResponse(
            original_text=request.text,
            summary=summary,
            original_length=original_length,
            summary_length=summary_length,
            compression_ratio=compression_ratio
        )
        
    except Exception as e:
        logger.error(f"Error summarizing text: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error summarizing text: {str(e)}"
        )


@router.post(
    "/batch",
    response_model=list[SummarizeResponse],
    summary="สรุปข้อความหลายรายการ",
    description="รับข้อความหลายรายการและสรุปทั้งหมด"
)
async def summarize_batch(requests: list[SummarizeRequest]) -> list[SummarizeResponse]:
    """
    สรุปข้อความหลายรายการพร้อมกัน
    """
    results = []
    for req in requests:
        try:
            summary = summarizer_service.summarize(
                text=req.text,
                max_length=req.max_length,
                min_length=req.min_length
            )
            
            original_length = len(req.text)
            summary_length = len(summary)
            compression_ratio = round(1 - (summary_length / original_length), 2)
            
            results.append(SummarizeResponse(
                original_text=req.text,
                summary=summary,
                original_length=original_length,
                summary_length=summary_length,
                compression_ratio=compression_ratio
            ))
        except Exception as e:
            logger.error(f"Error in batch summarization: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error summarizing text: {str(e)}"
            )
    
    return results
