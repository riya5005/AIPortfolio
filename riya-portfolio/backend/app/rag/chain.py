from langchain_openai import ChatOpenAI
from app.config import HF_TOKEN, HF_MODEL, HF_PROVIDER, HF_ROUTER_URL
from app.rag.vectorstore import get_vectorstore

SYSTEM_PROMPT = """You are the assistant embedded in Riya Sharma's portfolio website.
You answer visitor questions ONLY using the context provided below, which comes from
Riya's resume and project details. Speak about Riya in the third person, be friendly,
concise (2-5 sentences), and confident. If the context does not contain the answer,
say you don't have that information rather than making something up. When relevant,
include GitHub/LinkedIn links or project links exactly as given in the context.

Context:
{context}
"""

_llm = None


def get_llm():
    """
    Open-source LLM served through Hugging Face's Inference Providers router
    (https://router.huggingface.co/v1) — this is HF's current, OpenAI-compatible
    API, replacing the old (now shut down) api-inference.huggingface.co domain.

    Swap HF_MODEL / HF_PROVIDER in .env for any other open model, e.g.:
      - meta-llama/Llama-3.2-3B-Instruct : hf-inference   (default, small & fast)
      - HuggingFaceH4/zephyr-7b-beta     : hf-inference
      - deepseek-ai/DeepSeek-V3-0324     : auto
    Browse huggingface.co/models and check the "Deploy > Inference Providers"
    tab on any model page to see which providers serve it.
    """
    global _llm
    if _llm is None:
        
        if HF_PROVIDER and HF_PROVIDER.lower() != "auto":
            model_id = f"{HF_MODEL}:{HF_PROVIDER}"
        else:
            model_id = HF_MODEL
        _llm = ChatOpenAI(
            model=model_id,
            api_key=HF_TOKEN,
            base_url=HF_ROUTER_URL,
            temperature=0.3,
            max_tokens=300,
        )
    return _llm


def retrieve_context(query: str, k: int = 3) -> str:
    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search(query, k=k)
    return "\n\n".join(d.page_content for d in docs)


def answer_question(query: str) -> str:
    context = retrieve_context(query)
    system = SYSTEM_PROMPT.format(context=context)
    llm = get_llm()
    response = llm.invoke(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": query},
        ]
    )
    return response.content.strip()
