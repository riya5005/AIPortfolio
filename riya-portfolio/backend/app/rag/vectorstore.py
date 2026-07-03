import os
import requests
import numpy as np
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS

from app.rag.knowledge_base import load_documents
from app.config import VECTORSTORE_DIR, EMBEDDING_MODEL, HF_TOKEN

# Hugging Face's current hosted-inference domain (the old
# api-inference.huggingface.co was retired — same fix we applied to the
# chat model earlier, now applied here too).
HF_EMBED_URL = f"https://router.huggingface.co/hf-inference/models/{EMBEDDING_MODEL}"


class HFRouterEmbeddings(Embeddings):
    """
    Calls Hugging Face's hosted embedding API directly instead of loading
    the model locally. Loading it locally requires PyTorch, which alone
    can exceed free-tier hosting memory limits (e.g. Render's 512MB).
    """

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    def _embed_one(self, text: str):
        response = requests.post(
            HF_EMBED_URL,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"inputs": text, "options": {"wait_for_model": True}},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        arr = np.array(data)
        if arr.ndim == 2:
            arr = arr.mean(axis=0)  # mean-pool token embeddings into one vector
        return arr.tolist()

    def embed_documents(self, texts):
        return [self._embed_one(t) for t in texts]

    def embed_query(self, text):
        return self._embed_one(text)


_embeddings = HFRouterEmbeddings(api_key=HF_TOKEN, model=EMBEDDING_MODEL)

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
