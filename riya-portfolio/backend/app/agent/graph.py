from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END

from app.rag.vectorstore import get_vectorstore
from app.rag.chain import get_llm, SYSTEM_PROMPT

VALID_INTENTS = {"links", "projects", "skills", "education", "general"}


class ChatState(TypedDict):
    question: str
    history: List[Dict[str, str]]  
    intent: str
    context: str
    answer: str


def classify_intent(state: ChatState) -> ChatState:
    """
    The LLM itself decides the intent — this is what makes it 'agentic'
    rather than a hardcoded if/else on keywords.
    """
    llm = get_llm()
    prompt = (
        "Classify the visitor's question into exactly ONE of these categories: "
        "links, projects, skills, education, general.\n"
        "Reply with only the single category word — nothing else, no punctuation.\n\n"
        f"Question: {state['question']}"
    )
    response = llm.invoke([{"role": "user", "content": prompt}])
    intent = response.content.strip().lower()

    state["intent"] = intent if intent in VALID_INTENTS else "general"
    return state


def retrieve(state: ChatState) -> ChatState:
    vectorstore = get_vectorstore()
    search_query = state["question"]
    if state["intent"] != "general":
        search_query = f"{state['intent']}: {state['question']}"

    docs = vectorstore.similarity_search(search_query, k=3)
    state["context"] = "\n\n".join(d.page_content for d in docs)
    return state


def generate(state: ChatState) -> ChatState:
    llm = get_llm()
    system = SYSTEM_PROMPT.format(context=state["context"])

   
    messages = [{"role": "system", "content": system}]
    messages.extend(state.get("history", []))
    messages.append({"role": "user", "content": state["question"]})

    response = llm.invoke(messages)
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


def run_agent(question: str, history: List[Dict[str, str]] = None) -> str:
    agent = get_agent()
    result = agent.invoke({
        "question": question,
        "history": history or [],
        "intent": "",
        "context": "",
        "answer": "",
    })
    return result["answer"]
