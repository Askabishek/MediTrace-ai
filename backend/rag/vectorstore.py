import os
from pinecone import Pinecone, ServerlessSpec
from rag.embeddings import get_embeddings, get_single_embedding
from dotenv import load_dotenv

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "meditrace-knowledge"

# Create cloud index if missing
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1024, # Dimension for bge-large-en-v1.5
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(index_name)

def add_documents(texts: list, ids: list, metadatas: list = None):
    embeddings = get_embeddings(texts)
    vectors = []
    for i in range(len(texts)):
        meta = metadatas[i] if metadatas else {}
        meta["text"] = texts[i]
        vectors.append({"id": ids[i], "values": embeddings[i], "metadata": meta})
    index.upsert(vectors=vectors)

def search_documents(query: str, n_results: int = 5):
    query_vector = get_single_embedding(query)
    results = index.query(vector=query_vector, top_k=n_results, include_metadata=True)
    return [match["metadata"]["text"] for match in results["matches"] if "text" in match["metadata"]]
