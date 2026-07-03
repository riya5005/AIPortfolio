import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings

from app.rag.knowledge_base import load_documents
from app.config import VECTORSTORE_DIR, EMBEDDING_MODEL, HF_TOKEN

# IMPORTANT: this calls Hugging Face's hosted embedding API instead of
# loading the model locally. Loading it locally requires PyTorch, which
# alone can use 500MB+ of RAM — too much for free-tier hosting (Render's
# free plan gives only 512MB total). Calling the API keeps this backend
# lightweight while still using the same open-source embedding model.
_embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=HF_TOKEN,
    model_name=EMBEDDING_MODEL,
)

_vectorstore = None


def get_vectorstore():
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


def rebuild_vectorstore():
    """Force a rebuild — call this after editing knowledge_base.py."""
    global _vectorstore
    docs = load_documents()
    _vectorstore = FAISS.from_documents(docs, _embeddings)
    _vectorstore.save_local(VECTORSTORE_DIR)
    return _vectorstore
