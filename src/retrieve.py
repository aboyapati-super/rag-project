from typing import List
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from config import Config
from logger import setup_logger

# Initialize Logger
logger = setup_logger("retrieve")

def retrieve_info(query: str) -> List[Document]:
    """
    Retrieves relevant documents from the vector database based on the query.
    
    Args:
        query (str): The search query.
        
    Returns:
        List[Document]: A list of relevant documents.
        
    Raises:
        Exception: If retrieval fails.
    """
    try:
        logger.info(f"Searching for: '{query}'")
        
        # 1. Prepare the embedding model
        # Note: In a real production app, you might want to load this once (singleton) or pass it in.
        embeddings = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL_NAME)
        
        # 2. Load the existing database from disk
        vector_db = Chroma(
            persist_directory=Config.DB_PATH, 
            embedding_function=embeddings
        )
        
        # 3. Search for the most relevant chunks
        results = vector_db.similarity_search(query, k=Config.SEARCH_K)
        
        logger.info(f"Found {len(results)} relevant documents.")
        return results
        
    except Exception as e:
        logger.error(f"Error during information retrieval: {e}")
        raise

if __name__ == "__main__":
    try:
        # Example usage
        user_query = "Can you tell me something about thoughtful mind" 
        
        results = retrieve_info(user_query)
        
        print("\n--- Found these relevant snippets ---")
        for i, doc in enumerate(results, 1):
            print(f"\n[Snippet {i}]: {doc.page_content[:200]}...") # Print first 200 chars
            
    except Exception as e:
        logger.critical(f"Main execution failed: {e}")