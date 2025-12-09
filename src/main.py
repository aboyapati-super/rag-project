import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

DB_PATH = "vector_db"

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def main():
    # 1. Setup Database
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embedding_function)
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    # 2. Setup LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # 3. Create the Prompt Template
    template = """You are a helpful assistant. Use the following pieces of context to answer the question at the end.
    If the answer is not in the context, say that you don't know, don't try to make up an answer.

    Context:
    {context}

    Question: {question}
    
    Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)

    # 4. Build the Chain (The RAG Pipeline)
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # 5. Run it!
    user_question = "Can you tell me something about thoughtful mind"
    print(f"Question: {user_question}")
    
    response = rag_chain.invoke(user_question)
    print(f"Answer: {response}")

if __name__ == "__main__":
    main()