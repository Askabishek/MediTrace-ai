from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(texts: list):
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings.tolist()

def get_single_embedding(text: str):
    embedding = model.encode([text], convert_to_numpy=True)
    return embedding[0].tolist()
