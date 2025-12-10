import os
import shutil
from typing import List, Optional
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from config import Config
from logger import setup_logger

# Initialize Logger
logger = setup_logger("ingest")

def create_vector_db() -> None:
    """
    Loads a specific PDF document, chunks it, creates embeddings,
    and saves the vector database locally.
    
    Raises:
        FileNotFoundError: If the source document doesn't exist.
        Exception: For any other errors during the ingestion process.
    """
    try:
        # Pre-check: Ensure data file exists
        if not os.path.exists(Config.DATA_PATH):
            logger.error(f"Data file not found at: {Config.DATA_PATH}")
            raise FileNotFoundError(f"Source file does not exist: {Config.DATA_PATH}")

        # 1. Load
        logger.info(f"Loading document from: {Config.DATA_PATH}")
        try:
            loader = PyPDFLoader(Config.DATA_PATH)
            documents: List[Document] = loader.load()
            logger.info(f"Successfully loaded {len(documents)} pages.")
        except Exception as e:
            logger.error(f"Failed to load document: {e}")
            raise

        # 2. Split
        logger.info("Chunking documents...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE, 
            chunk_overlap=Config.CHUNK_OVERLAP
        )
        chunks: List[Document] = text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks.")
        
        # 3. Embed & Store
        logger.info(f"Creating vector database at: {Config.DB_PATH}")
        
        # We use a standard, efficient model for creating embeddings
        embeddings = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL_NAME)
        
        # clear existing DB if needed to avoid duplicates or issues (optional strategy)
        # For this refactor, we will rely on Chroma's default behavior or we could wipe it.
        # Let's verify if directory exists and is valid. 
        
        # This does the heavy lifting: converts text -> numbers -> saves to DB folder
        try:
            vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                persist_directory=Config.DB_PATH
            )
            # Starting from somewhere in langchain 0.2/0.3 persist is automatic, 
            # but calling persist() is sometimes still good practice if version compatibility is unclear.
            # vector_store.persist() 
            logger.info(f"Vector database created successfully at '{Config.DB_PATH}'.")
        except Exception as e:
            logger.error(f"Failed to create vector database: {e}")
            raise

    except Exception as overall_e:
        logger.critical(f"Ingestion process failed: {overall_e}")
        raise

if __name__ == "__main__":
    create_vector_db()