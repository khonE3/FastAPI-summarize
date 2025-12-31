"""
Text Summarization Service using Transformers
"""
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class SummarizerService:
    """Service class for text summarization"""
    
    _instance = None
    _model = None
    _tokenizer = None
    _pipeline = None
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the summarizer service"""
        if self._pipeline is None:
            self._load_model()
    
    def _load_model(self):
        """Load the summarization model"""
        try:
            logger.info(f"Loading model: {settings.MODEL_NAME}")
            self._pipeline = pipeline(
                "summarization",
                model=settings.MODEL_NAME,
                tokenizer=settings.MODEL_NAME
            )
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def summarize(
        self,
        text: str,
        max_length: int = 150,
        min_length: int = 30
    ) -> str:
        """
        Summarize the given text
        
        Args:
            text: Input text to summarize
            max_length: Maximum length of summary
            min_length: Minimum length of summary
            
        Returns:
            Summarized text
        """
        if self._pipeline is None:
            self._load_model()
        
        # Truncate input if too long
        if len(text) > settings.MAX_INPUT_LENGTH * 4:  # Approximate character limit
            text = text[:settings.MAX_INPUT_LENGTH * 4]
        
        result = self._pipeline(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
            truncation=True
        )
        
        return result[0]["summary_text"]
    
    @property
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self._pipeline is not None


# Global instance
summarizer_service = SummarizerService()
