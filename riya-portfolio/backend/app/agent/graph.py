from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END

from app.rag.vectorstore import get_vectorstore
from app.rag.chain import get_llm, SYSTEM_PROMPT
from app.security.guardrails import (
    detect_prompt_injection,
    check_grounding,
    SAFE_REFUSAL,
    UNGROUNDED_FALLBACK,
)

VALID_INTENTS = {"links", "projects", "skills", "education", "general"}


class ChatState(TypedDict):
    question: str
    history: List[Dict[str, str]]
    intent: str
    context: str
    answer: str
    flagged: bool
    flag_reason: str


def guard_input(state: ChatState) -> ChatState:
    is_suspicious, pattern = detect_prompt_injection(state["question"])
    if is_suspicious:
        state["flagged"] = True
        state["flag_reason"] = f"input_guard:{pattern}"
        state["answer"] = SAFE_REFUSAL
    else:
        state["flagged"] = False
        state["flag_reason"] = ""
    return state


def classify_intent(state: ChatState) -> ChatState:
    if state.get("flagged"):
        return state

    llm = get_llm()
    prompt = (
        "Classify the visitor's question into exactly ONE of these categories: "
        "links, projects, skills, education, general.\n"
        "Reply with only the single category word — nothing else, no punctuation.\n\n"
        f"Question: {state['question']}"
    )
    try:
        response = llm.invoke([{"role": "user", "content": prompt}])
        intent = response.content.strip().lower()
        state["intent"] = intent if intent in VALID_INTENTS else "general"
    except Exception:
        state["intent"] = "general"
    return state


def retrieve(state: ChatState) -> ChatState:
    if state.get("flagged"):
        return state

    vectorstore = get_vectorstore()
    search_query = state["question"]
    if state["intent"] != "general":
        search_query = f"{state['intent']}: {state['question']}"

    docs = vectorstore.similarity_search(search_query, k=3)
    state["context"] = "\n\n".join(d.page_content for d in docs)
    return state


def generate(state: ChatState) -> ChatState:
    if state.get("flagged"):
        return state

    llm = get_llm()
    system = SYSTEM_PROMPT.format(context=state["context"])
    messages = [{"role": "system", "content": system}]
    messages.extend(state.get("history", []))
    messages.append({"role": "user", "content": state["question"]})

    try:
        response = llm.invoke(messages)
        state["answer"] = response.content.strip()
    except Exception as e:
        state["answer"] = (
            "I'm temporarily unable to answer — the AI service is at its "
            "usage limit right now. Please try again in a bit!"
        )
        state["flagged"] = True
        state["flag_reason"] = f"llm_error:{type(e).__name__}"
    return state


def guard_output(state: ChatState) -> ChatState:
    if state.get("flagged"):
        return state  # already handled by input guard


    if state["intent"] != "general":
        return state

    llm = get_llm()
    try:
        grounded = check_grounding(llm, state["answer"], state["context"])
        if not grounded:
            state["flagged"] = True
            state["flag_reason"] = "output_guard:ungrounded"
            state["answer"] = UNGROUNDED_FALLBACK
    except Exception:
       
        pass
    return state


def build_graph():
    graph = StateGraph(ChatState)
    graph.add_node("guard_input", guard_input)
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("retrieve", retrieve)
    graph.add_node("generate", generate)
    graph.add_node("guard_output", guard_output)

    graph.set_entry_point("guard_input")
    graph.add_edge("guard_input", "classify_intent")
    graph.add_edge("classify_intent", "retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", "guard_output")
    graph.add_edge("guard_output", END)

    return graph.compile()


_compiled_graph = None


def get_agent():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph


def run_agent(question: str, history: List[Dict[str, str]] = None) -> dict:
    agent = get_agent()
    result = agent.invoke({
        "question": question,
        "history": history or [],
        "intent": "",
        "context": "",
        "answer": "",
        "flagged": False,
        "flag_reason": "",
    })
    return result
