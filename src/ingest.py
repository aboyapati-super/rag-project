import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DATA_PATH = os.path.join("data", "sample.pdf")
DB_PATH = "vector_db"  # Folder where the database will be saved

def create_vector_db():
    # 1. Load
    print("Loading document...")
    loader = PyPDFLoader(DATA_PATH)
    documents = loader.load()
    
    # 2. Split
    print("Chunking documents...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1600, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    
    # 3. Embed & Store
    print("Creating vector database...")
    # We use a standard, efficient model for creating embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # This does the heavy lifting: converts text -> numbers -> saves to DB folder
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    print(f"Vector database created at '{DB_PATH}' with {len(chunks)} chunks.")

if __name__ == "__main__":
    create_vector_db()