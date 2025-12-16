from pathlib import Path
from config.config import Config
import shutil
import time
import os

def setup_directories():
    """Create necessary directories for the application"""
    Config.setup_directories()

def clean_old_files(days:  int = 1):
    """
    Clean old files from upload and video directories
    
    Args: 
        days: Remove files older than this many days
    """
    try:
        current_time = time.time()
        max_age = days * 24 * 60 * 60  # Convert days to seconds
        
        # Clean uploads
        for file_path in Config.UPLOAD_DIR.glob("*"):
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                if file_age > max_age: 
                    file_path.unlink()
        
        # Clean videos
        for file_path in Config.VIDEO_DIR.glob("*"):
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                if file_age > max_age:
                    file_path.unlink()
                    
    except Exception as e: 
        print(f"Error cleaning old files: {str(e)}")

def format_timestamp(seconds: float) -> str:
    """
    Format seconds into MM:SS format
    
    Args:
        seconds: Time in seconds
        
    Returns: 
        Formatted timestamp
    """
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes: 02d}:{secs:02d}"

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to maximum length
    
    Args: 
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def estimate_reading_time(text: str, words_per_minute: int = 150) -> float:
    """
    Estimate reading/speaking time for text
    
    Args: 
        text: Text content
        words_per_minute:  Speaking pace
        
    Returns:
        Estimated time in minutes
    """
    word_count = len(text.split())
    return word_count / words_per_minute