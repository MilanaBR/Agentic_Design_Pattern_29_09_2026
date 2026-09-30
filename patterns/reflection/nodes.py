import json

from config.llm import get_llm
from .state import ReflectionState

llm = get_llm()


def _count_sentences(text: str) -> int:
    cleaned = text.strip()
    if not cleaned:
        return 0
    return len([part for part in cleaned.replace("!", ".").replace("?", ".").split(".") if part.strip()])


def generator_agent(state: ReflectionState):
    previous = state.get("draft", "")
    feedback = state.get("feedback", "")
    attempts = state.get("attempts", 0)

    if attempts == 0:
        draft = (
            "Python is a great language for beginners because it is easy to use. "
            "Many people like it and there are many tutorials online."
        )
    else:
        prompt = f"""
        You are the generator agent.
        Write a short answer for the task.

        If feedback is provided, use it to improve the previous answer.
        The answer must satisfy all requirements exactly.
        Keep it concise and direct.

        Task: {state['task']}
        Previous answer: {previous}
        Feedback: {feedback}

        Final answer:
        """
        draft = llm.invoke(prompt).content.strip()

    return {
        "draft": draft,
        "final_answer": draft,
        "attempts": attempts + 1,
        "status": "drafted",
    }


def critic_agent(state: ReflectionState):
    prompt = f"""
    You are the critic agent.
    Review this answer strictly.

    Rules:
    - The answer must directly answer the task.
    - It must be concise and clear.
    - It must not be vague or generic.
    - If the task requires exact structure, follow it exactly.
    - Do not approve weak answers.

    Return ONLY valid JSON in this exact shape:
    {{"needs_revision": true, "feedback": "short reason"}}

    Task: {state['task']}
    Answer: {state['draft']}
    """

    response = llm.invoke(prompt).content.strip()
    payload = json.loads(response)
    print(f"[Critic Agent] LLM response: {payload}")

    needs_revision = bool(payload.get("needs_revision", False))
    feedback = str(payload.get("feedback", "Looks good.")).strip()

    text = state.get("draft", "")
    sentence_count = _count_sentences(text)
    lower_text = text.lower()

    # strict local validation to prevent weak approval
    if sentence_count != 2:
        needs_revision = True
        feedback = "Answer must be exactly 2 sentences."
    elif "syntax" not in lower_text and "readable" not in lower_text and "simple" not in lower_text:
        needs_revision = True
        feedback = "Answer should mention why Python is beginner-friendly." \
            " Include simplicity/readability or easy syntax."
    elif "community" not in lower_text and "library" not in lower_text and "libraries" not in lower_text:
        needs_revision = True
        feedback = "Answer should mention community, libraries, or available resources."

    if not needs_revision:
        return {
            "needs_revision": False,
            "feedback": "Looks good.",
            "status": "approved",
            "final_answer": state["draft"],
        }

    return {
        "needs_revision": True,
        "feedback": feedback,
        "status": "needs_improvement",
        "attempts": state.get("attempts", 0),
    }