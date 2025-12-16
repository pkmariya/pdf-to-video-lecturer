import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # OpenAI Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
    
    # TTS Settings
    TTS_SERVICE = os.getenv("TTS_SERVICE", "gtts")
    AZURE_TTS_KEY = os. getenv("AZURE_TTS_KEY", "")
    AZURE_TTS_REGION = os.getenv("AZURE_TTS_REGION", "eastus")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
    ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
    
    # Application Settings
    MAX_PDF_SIZE_MB = int(os.getenv("MAX_PDF_SIZE_MB", "50"))
    VIDEO_OUTPUT_FORMAT = os.getenv("VIDEO_OUTPUT_FORMAT", "mp4")
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os. getenv("CHUNK_OVERLAP", "200"))
    
    # Directory Settings
    BASE_DIR = Path(__file__).parent. parent
    DATA_DIR = BASE_DIR / "data"
    UPLOAD_DIR = DATA_DIR / "uploads"
    VIDEO_DIR = DATA_DIR / "videos"
    VECTORDB_DIR = DATA_DIR / "vectordb"
    
    # Create directories if they don't exist
    @classmethod
    def setup_directories(cls):
        """Create necessary directories"""
        for directory in [cls.DATA_DIR, cls.UPLOAD_DIR, cls.VIDEO_DIR, cls. VECTORDB_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def validate_config(cls):
        """Validate required configuration"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required.  Please set it in . env file")
        
        return True