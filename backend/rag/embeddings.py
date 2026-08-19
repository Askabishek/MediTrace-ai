import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_embeddings(texts: list):
    response = client.embeddings.create(
        model="bge-large-en-v1.5",  # Free on Groq
        input=texts
    )
    return [data.embedding for data in response.data]

def get_single_embedding(text: str):
    return get_embeddings([text])[0]
