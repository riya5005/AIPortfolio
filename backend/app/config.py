import os
from dotenv import load_dotenv

load_dotenv()


HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_MODEL = os.getenv("HF_MODEL", "meta-llama/Llama-3.2-3B-Instruct")
HF_PROVIDER = os.getenv("HF_PROVIDER", "hf-inference")
HF_ROUTER_URL = "https://router.huggingface.co/v1"

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-large")
DATABASE_URL = os.getenv("DATABASE_URL", "")

VECTORSTORE_DIR = os.getenv("VECTORSTORE_DIR", "vectorstore_data")

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
