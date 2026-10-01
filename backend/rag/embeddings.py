"""Embedding configuration for ChromaDB.

ChromaDB owns embedding generation for this backend. Keeping this compatibility
module free of model imports avoids loading heavyweight ML dependencies.
"""


def get_embeddings(texts: list):
    return None


def get_single_embedding(text: str):
    return None