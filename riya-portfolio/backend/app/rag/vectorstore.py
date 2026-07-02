import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from app.rag.knowledge_base import load_documents
from app.config import VECTORSTORE_DIR, EMBEDDING_MODEL

# A small, free, fully open-source local embedding model — runs on your own
# machine, no API key or internet call needed after the first download.
_embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

_vectorstore: FAISS | None = None


def get_vectorstore() -> FAISS:
    """Load the FAISS index from disk if it exists, otherwise build it."""
    global _vectorstore
    if _vectorstore is not None:
        return _vectorstore

    if os.path.exists(VECTORSTORE_DIR):
        _vectorstore = FAISS.load_local(
            VECTORSTORE_DIR, _embeddings, allow_dangerous_deserialization=True
        )
    else:
        docs = load_documents()
        _vectorstore = FAISS.from_documents(docs, _embeddings)
        _vectorstore.save_local(VECTORSTORE_DIR)

    return _vectorstore


def rebuild_vectorstore() -> FAISS:
    """Force a rebuild — call this after editing knowledge_base.py."""
    global _vectorstore
    docs = load_documents()
    _vectorstore = FAISS.from_documents(docs, _embeddings)
    _vectorstore.save_local(VECTORSTORE_DIR)
    return _vectorstore
