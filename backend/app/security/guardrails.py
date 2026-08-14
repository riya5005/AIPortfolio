import re

INJECTION_PATTERNS = [
    r"ignore (all |your )?(previous|prior|above) instructions",
    r"disregard (your |the )?(system|previous) (prompt|instructions)",
    r"reveal (your |the )?system prompt",
    r"you are now",
    r"act as (a |an )?(?!.*riya)",  # "act as X" role-override attempts
    r"jailbreak",
    r"bypass (your |the )?(rules|restrictions|guidelines|filters)",
    r"pretend (you|to) (are|be)",
    r"what (is|was) your (system |initial )?prompt",
    r"repeat (the words|everything) (above|before)",
]

_COMPILED = [re.compile(p, re.IGNORECASE) for p in INJECTION_PATTERNS]


def detect_prompt_injection(text: str) -> tuple[bool, str | None]:
    """Returns (is_suspicious, matched_pattern)."""
    for pattern in _COMPILED:
        if pattern.search(text):
            return True, pattern.pattern
    return False, None


def check_grounding(llm, answer: str, context: str) -> bool:
    """
    Lightweight output check: asks the LLM whether its own answer is
    actually supported by the retrieved context, or whether it invented
    information not present in the source data.
    """
    if not context.strip():
        # No context was retrieved at all — nothing to ground the answer in.
        return False

    prompt = (
        "You are a strict fact-checker. Given the CONTEXT and an ANSWER, "
        "reply with only YES if the answer's claims are all supported by "
        "the context, or NO if the answer includes information not "
        "present in the context.\n\n"
        f"CONTEXT:\n{context}\n\nANSWER:\n{answer}\n\nReply with only YES or NO."
    )
    result = llm.invoke([{"role": "user", "content": prompt}])
    verdict = result.content.strip().upper()
    return verdict.startswith("Y")


SAFE_REFUSAL = (
    "I can only answer questions about Riya's skills, projects, and "
    "background — I'm not able to help with that request."
)

UNGROUNDED_FALLBACK = (
    "I don't have enough information in my knowledge base to answer that "
    "accurately — feel free to ask about Riya's skills, projects, or education."
)