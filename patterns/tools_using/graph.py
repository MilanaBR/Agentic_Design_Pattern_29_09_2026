from langgraph.graph import StateGraph, START, END

from .nodes import reasoning_agent, tool_executor, fallback_agent
from .state import AgentState

def route_after_reasoning(state: AgentState):
    return "math" if state.get("mode") == "math" else "fallback"

def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("reasoning_agent", reasoning_agent)
    workflow.add_node("tool_executor", tool_executor)
    workflow.add_node("fallback_agent", fallback_agent)

    workflow.add_edge(START, "reasoning_agent")
    workflow.add_conditional_edges(
        "reasoning_agent",
        route_after_reasoning,
        {
            "math": "tool_executor",
            "fallback": "fallback_agent"
        }
    )
    workflow.add_edge("tool_executor", END)
    workflow.add_edge("fallback_agent", END)

    return workflow.compile()