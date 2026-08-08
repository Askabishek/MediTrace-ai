import chromadb

chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_or_create_collection(
    name="medical_knowledge",
    metadata={"hnsw:space": "cosine"}
)

def add_documents(texts: list, ids: list, metadatas: list = None):
    collection.add(
        documents=texts,
        ids=ids,
        metadatas=metadatas or [{}] * len(texts)
    )

def search_documents(query: str, n_results: int = 5):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results["documents"][0] if results["documents"] else []

def get_collection_count():
    return collection.count()
