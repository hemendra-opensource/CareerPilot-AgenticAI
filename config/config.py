import os
from pathlib import Path
from dotenv import load_dotenv

# Get the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

class Config:
    """Manages system configurations and environment variables."""
    
    # Base paths
    BASE_DIR = BASE_DIR
    REPORTS_DIR = BASE_DIR / "reports"
    DATA_DIR = BASE_DIR / "data"
    CONFIG_DIR = BASE_DIR / "config"
    
    # API configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    @classmethod
    def validate(cls) -> tuple[bool, str]:
        """
        Validates the configuration status.
        Returns:
            A tuple of (is_valid, error_message).
        """
        if not cls.GROQ_API_KEY:
            return False, "GROQ_API_KEY is not set. Please check your .env file."
        return True, "Configuration is valid."

# Create directories if they do not exist
Config.REPORTS_DIR.mkdir(exist_ok=True)
Config.DATA_DIR.mkdir(exist_ok=True)
