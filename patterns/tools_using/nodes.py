import re

from config.llm import get_llm
from tools.calculator import calculator
from .state import AgentState

llm = get_llm()

def _looks_like_math_question(question: str) -> bool:
    text = question.lower().strip()
    if not text:
        return False

    math_keywords = [
        "sum", "difference", "product", "average", "square", "cube",
        "plus", "minus", "multiply", "divide", "percentage", "percent",
        "calculate", "what is", "how much", "total", "area", "volume"
    ]

    if any(keyword in text for keyword in math_keywords):
        return True

    if re.search(r"\d", text) and re.search(r"[+\-*/%^()]", text):
        return True

    return False

def _is_valid_python_expression(expression: str) -> bool:
    cleaned = expression.strip()
    if not cleaned:
        return False

    try:
        compile(cleaned, "<expression>", "eval")
        return True
    except Exception:
        return False

def reasoning_agent(state: AgentState):
    question = state["question"]

    if not _looks_like_math_question(question):
        return {"mode": "fallback"}

    prompt = f"""
                You are a math reasoning agent.

                Convert the question into a valid Python math expression.
                Return ONLY the expression.

                Examples:
                Question: What is the sum of 5 and 3?
                Expression: 5 + 3

                Question: What is the average of 100 and 200?
                Expression: (100 + 200) / 2

                Question: What is the square of the average of 100 and 200?
                Expression: ((100 + 200) / 2) ** 2

                Question: {question}
                Expression:
                """
    expression = llm.invoke(prompt).content.strip()

    if not _is_valid_python_expression(expression):
        return {"mode": "fallback"}

    return {"mode": "math", "expression": expression}

def fallback_agent(state: AgentState):
    prompt = f"""
            You are a helpful assistant.

            Answer the user's question clearly and directly.
            Do not use code blocks unless the user asks for code.
            Keep the answer concise but useful.

            Question: {state['question']}
            Answer:
            """
    answer = llm.invoke(prompt).content.strip()
    return {"answer": answer, "mode": "fallback"}

def tool_executor(state: AgentState):
    result = calculator(state["expression"])
    return {"result": result, "mode": "math"}