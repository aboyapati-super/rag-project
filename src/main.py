import os
import sys
from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

from config import Config
from logger import setup_logger

# Initialize Logger
logger = setup_logger("main")

def format_docs(docs: List[Document]) -> str:
    """
    Formats the list of documents into a single string.
    """
    return "\n\n".join(doc.page_content for doc in docs)

def main() -> None:
    """
    Main function to run the RAG pipeline.
    """
    try:
        # Validate environment variables first
        try:
            Config.validate_env_vars()
        except EnvironmentError as e:
            logger.critical(f"Environment Validation Failed: {e}")
            logger.critical("Please ensure .env file is correctly configured.")
            sys.exit(1)

        logger.info("Starting RAG Pipeline...")

        # 1. Setup Database
        logger.info("Initializing Vector Database and Retriever...")
        try:
            embedding_function = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL_NAME)
            vector_db = Chroma(
                persist_directory=Config.DB_PATH, 
                embedding_function=embedding_function
            )
            # Check if DB is empty or not created (basic check can be done by trying to peek or count)
            # For now, we assume if persist_directory exists, it's fine. 
            # If not, chroma might init empty which is fine until search fails or returns nothing.
            
            retriever = vector_db.as_retriever(search_kwargs={"k": Config.SEARCH_K})
        except Exception as e:
            logger.error(f"Failed to initialize Vector DB: {e}")
            raise

        # 2. Setup LLM
        logger.info(f"Initializing LLM: {Config.LLM_MODEL_NAME}")
        try:
            llm = ChatOpenAI(
                model=Config.LLM_MODEL_NAME, 
                temperature=Config.LLM_TEMPERATURE
            )
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise

        # 3. Create the Prompt Template
        template = """You are a helpful assistant. Use the following pieces of context to answer the question at the end.
        If the answer is not in the context, say that you don't know, don't try to make up an answer.

        Context:
        {context}

        Question: {question}
        
        Answer:"""
        
        prompt = ChatPromptTemplate.from_template(template)

        # 4. Build the Chain (The RAG Pipeline)
        logger.info("Building RAG Chain...")
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        # 5. Run it!
        user_question = "Can you tell me something about thoughtful mind"
        logger.info(f"Processing Question: {user_question}")
        
        try:
            response = rag_chain.invoke(user_question)
            logger.info("Successfully generated response.")
            print(f"Question: {user_question}")
            print(f"Answer: {response}")
        except Exception as e:
            logger.error(f"Failed to generate answer: {e}")
            raise

    except Exception as overall_e:
        logger.critical(f"Application failed: {overall_e}")
        sys.exit(1)

if __name__ == "__main__":
    main()