from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DB_PATH = "vector_db"

def retrieve_info(query):
    print(f"Searching for: '{query}'")
    
    # 1. Prepare the embedding model
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 2. Load the existing database from disk
    vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embedding_function)
    
    # 3. Search for the 3 most relevant chunks
    results = vector_db.similarity_search(query, k=3)
    
    return results

if __name__ == "__main__":
    # Feel free to change this question to something relevant to your specific PDF!
    user_query = "Can you tell me something about thoughtful mind" 
    
    results = retrieve_info(user_query)
    
    print("\n--- Found these relevant snippets ---")
    for doc in results:
        print(f"\n[Snippet]: {doc.page_content[:200]}...") # Print first 200 chars