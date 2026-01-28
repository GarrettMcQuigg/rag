"""
Configuration management for the RAG application.
Loads environment variables and provides centralized config access.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration loaded from environment variables."""

    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "towering-fir")

    # Chunking settings
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50

    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY is required. Add it to your .env file.")
        return True


# Validate on import
Config.validate()
