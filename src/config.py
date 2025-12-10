import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Centralized configuration for the RAG application.
    """
    # Base Paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = os.path.join(BASE_DIR, "data")
    DB_DIR = os.path.join(BASE_DIR, "vector_db")

    # Data Settings
    PDF_FILE_NAME = "sample.pdf"
    DATA_PATH = os.path.join(DATA_DIR, PDF_FILE_NAME)
    
    # Vector DB Settings
    DB_PATH = DB_DIR
    COLLECTION_NAME = "rag_collection"

    # Model Settings
    EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
    LLM_MODEL_NAME = "gpt-3.5-turbo"
    LLM_TEMPERATURE = 0

    # Chunking Settings
    CHUNK_SIZE = 1600
    CHUNK_OVERLAP = 200

    # Retrieval Settings
    SEARCH_K = 3

    @staticmethod
    def validate_env_vars():
        """
        Validate that required environment variables are set.
        """
        required_vars = ["OPENAI_API_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Ensure directories exist
os.makedirs(Config.DATA_DIR, exist_ok=True)
