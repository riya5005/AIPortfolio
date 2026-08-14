import os
from dotenv import load_dotenv

load_dotenv()


AZURE_KEY_VAULT_URL = os.getenv("AZURE_KEY_VAULT_URL", "")

_kv_client = None
if AZURE_KEY_VAULT_URL:
    try:
        from azure.identity import DefaultAzureCredential
        from azure.keyvault.secrets import SecretClient
        _kv_client = SecretClient(
            vault_url=AZURE_KEY_VAULT_URL,
            credential=DefaultAzureCredential(),
        )
    except Exception as e:
        print(f"[warning] Could not connect to Azure Key Vault, falling back to env vars: {e}")
        _kv_client = None


def get_secret(name: str, env_var_name: str, default: str = "") -> str:
    """
    Fetches a secret from Azure Key Vault if configured, otherwise falls
    back to a plain environment variable. Key Vault secret names can't
    contain underscores, so e.g. HF_TOKEN becomes "hf-token" in the vault.
    """
    if _kv_client:
        try:
            return _kv_client.get_secret(name).value
        except Exception as e:
            print(f"[warning] Could not fetch '{name}' from Key Vault, falling back to env var: {e}")
    return os.getenv(env_var_name, default)


# LLM — fully open-source via Hugging Face's Inference Providers router.
HF_TOKEN = get_secret("hf-token", "HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL", "openai/gpt-oss-120b")
HF_PROVIDER = os.getenv("HF_PROVIDER", "auto")
HF_ROUTER_URL = "https://router.huggingface.co/v1"

# Embedding model
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-large")

# PostgreSQL - used only to log chat messages 
DATABASE_URL = get_secret("database-url", "DATABASE_URL")

# Vector store persistence
VECTORSTORE_DIR = os.getenv("VECTORSTORE_DIR", "vectorstore_data")

# Allowed frontend origin(s) for CORS
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
