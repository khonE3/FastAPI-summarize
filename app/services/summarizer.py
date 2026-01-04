"""
Text Summarization Service using Transformers
Supports English and Thai languages
"""
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from app.core.config import settings
from langdetect import detect, LangDetectException
import logging

logger = logging.getLogger(__name__)


class SummarizerService:
    """Service class for text summarization"""
    
    _instance = None
    _en_pipeline = None
    _th_pipeline = None
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the summarizer service"""
        if self._en_pipeline is None:
            self._load_models()
    
    def _load_models(self):
        """Load the summarization models for both languages"""
        try:
            # Load English model (BART)
            logger.info(f"Loading English model: {settings.MODEL_NAME_EN}")
            self._en_pipeline = pipeline(
                "summarization",
                model=settings.MODEL_NAME_EN,
                tokenizer=settings.MODEL_NAME_EN
            )
            logger.info("English model loaded successfully")
            
            # Load Thai model (mT5)
            logger.info(f"Loading Thai model: {settings.MODEL_NAME_TH}")
            self._th_pipeline = pipeline(
                "summarization",
                model=settings.MODEL_NAME_TH,
                tokenizer=settings.MODEL_NAME_TH
            )
            logger.info("Thai model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise
    
    def detect_language(self, text: str) -> str:
        """
        Detect language of the input text
        
        Args:
            text: Input text
            
        Returns:
            Language code ('en' or 'th')
        """
        try:
            lang = detect(text)
            if lang == 'th':
                return 'th'
            return 'en'
        except LangDetectException:
            # Default to English if detection fails
            logger.warning("Language detection failed, defaulting to English")
            return 'en'
    
    def summarize(
        self,
        text: str,
        max_length: int = 150,
        min_length: int = 30,
        language: str = None
    ) -> dict:
        """
        Summarize the given text
        
        Args:
            text: Input text to summarize
            max_length: Maximum length of summary
            min_length: Minimum length of summary
            language: Language code ('en', 'th', or None for auto-detect)
            
        Returns:
            Dictionary with summary and detected language
        """
        if self._en_pipeline is None or self._th_pipeline is None:
            self._load_models()
        
        # Auto-detect language if not specified
        if language is None:
            language = self.detect_language(text)
        
        # Select appropriate pipeline
        pipeline_to_use = self._th_pipeline if language == 'th' else self._en_pipeline
        
        # Truncate input if too long
        max_chars = settings.MAX_INPUT_LENGTH * 4
        if len(text) > max_chars:
            text = text[:max_chars]
        
        # Summarize with appropriate model
        result = pipeline_to_use(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
            truncation=True
        )
        
        return {
            "summary": result[0]["summary_text"],
            "language": language
        }
    
    @property
    def is_loaded(self) -> bool:
        """Check if models are loaded"""
        return self._en_pipeline is not None and self._th_pipeline is not None


# Global instance
summarizer_service = SummarizerService()
