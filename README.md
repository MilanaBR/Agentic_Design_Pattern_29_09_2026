# Agentic Design Pattern - Tool Using Workflow

This project demonstrates an agentic AI workflow that can:

- solve arithmetic and math questions using a calculator tool
- answer general questions using a backup LLM response
- expose the workflow through a simple Streamlit frontend

## Project structure

- `patterns/tools_using/nodes.py` - agent logic
- `patterns/tools_using/state.py` - shared state definition
- `patterns/tools_using/graph.py` - LangGraph workflow builder
- `patterns/tools_using/run.py` - backend demo script
- `app.py` - Streamlit frontend
- `config/` - LLM configuration
- `tools/` - utility tools such as the calculator

## How it works

1. The workflow receives a question.
2. `reasoning_agent` checks whether the question looks like a math problem.
3. If it is a math question:
   - it converts it into a Python expression
   - `tool_executor` evaluates it with the calculator
4. If it is not a math question:
   - the workflow routes to `fallback_agent`
   - the LLM answers the question normally

This prevents crashes for non-math prompts like:
- "Define AI."
- "Who is the president of France?"
- "Write a haiku about the ocean."

## Installation

From the project root:

```bash
pip install streamlit langgraph
