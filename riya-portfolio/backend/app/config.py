import os
from dotenv import load_dotenv

load_dotenv()

# LLM — fully open-source via Hugging Face's Inference Providers router.
# Free HF account + free access token is enough (no paid tier required).
HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_MODEL = os.getenv("HF_MODEL", "meta-llama/Llama-3.2-3B-Instruct")
# "hf-inference" is Hugging Face's own free serverless provider.
HF_PROVIDER = os.getenv("HF_PROVIDER", "hf-inference")
HF_ROUTER_URL = "https://router.huggingface.co/v1"

# Embedding model (already open-source / local, unchanged)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-large")
# PostgreSQL - used only to log chat messages (optional, app still works without it)
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Vector store persistence
VECTORSTORE_DIR = os.getenv("VECTORSTORE_DIR", "vectorstore_data")

# Allowed frontend origin(s) for CORS
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
