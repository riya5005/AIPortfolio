"""
A small LangGraph agent for the portfolio chatbot.

Flow:
  classify_intent -> retrieve -> generate -> END

classify_intent decides which "topic" of the knowledge base is most relevant
(links / projects / skills / education / general) so retrieval can be biased
toward the right documents. This is intentionally simple — it's meant to
demonstrate an agentic graph, not a huge production system.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END

from app.rag.vectorstore import get_vectorstore
from app.rag.chain import get_llm, SYSTEM_PROMPT


class ChatState(TypedDict):
    question: str
    intent: str
    context: str
    answer: str


INTENT_KEYWORDS = {
    "links": ["linkedin", "github", "link", "contact", "profile"],
    "projects": ["project", "built", "fraud", "house price", "portfolio project"],
    "skills": ["skill", "tech stack", "technology", "language", "framework", "library", "tool"],
    "education": ["education", "degree", "college", "university", "b.tech", "btech"],
}


def classify_intent(state: ChatState) -> ChatState:
    q = state["question"].lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(kw in q for kw in keywords):
            state["intent"] = intent
            return state
    state["intent"] = "general"
    return state


def retrieve(state: ChatState) -> ChatState:
    vectorstore = get_vectorstore()
    # Bias the search query slightly using the detected intent
    search_query = state["question"]
    if state["intent"] != "general":
        search_query = f"{state['intent']}: {state['question']}"

    docs = vectorstore.similarity_search(search_query, k=3)
    state["context"] = "\n\n".join(d.page_content for d in docs)
    return state


def generate(state: ChatState) -> ChatState:
    llm = get_llm()  # open-source model via Hugging Face's router API
    system = SYSTEM_PROMPT.format(context=state["context"])
    response = llm.invoke(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": state["question"]},
        ]
    )
    state["answer"] = response.content.strip()
    return state


def build_graph():
    graph = StateGraph(ChatState)
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("retrieve", retrieve)
    graph.add_node("generate", generate)

    graph.set_entry_point("classify_intent")
    graph.add_edge("classify_intent", "retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)

    return graph.compile()


_compiled_graph = None


def get_agent():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph


def run_agent(question: str) -> str:
    agent = get_agent()
    result = agent.invoke({"question": question, "intent": "", "context": "", "answer": ""})
    return result["answer"]
