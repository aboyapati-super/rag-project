import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 1. Load the secrets from the .env file
load_dotenv()

# 2. Initialize the model
llm = ChatOpenAI(model="gpt-3.5-turbo")

# 3. Test it
response = llm.invoke("Hello! Are you working?")
print(response.content)