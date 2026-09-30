import streamlit as st

from patterns.tools_using.graph import build_graph as build_tools_using_graph
from patterns.planner_executor.graph import build_graph as build_planner_executor_graph

st.set_page_config(page_title="Agentic AI Workflow Demo", layout="wide")

patterns = {
    "Tools-Using": {
        "description": "Math questions use the calculator tool. General questions fall back to a normal LLM answer.",
        "label": "Ask a question",
        "default": "What is the square of the average of 10 and 5?",
        "placeholder": "Try: Define AI. or What is 8 + 6?",
    },
    "Planner-Executor": {
        "description": "A planner breaks a task into steps, then an executor completes each step.",
        "label": "Describe a task",
        "default": "Create a simple 3-step plan for launching an AI chatbot product.",
        "placeholder": "For example: Plan a weekend trip to Boston.",
    },
}

pattern_name = st.sidebar.selectbox("Agentic design pattern", list(patterns))
pattern = patterns[pattern_name]

st.title(f"{pattern_name} Agent Demo")
st.caption(pattern["description"])

if pattern_name == "Tools-Using":
    app = build_tools_using_graph()
else:
    app = build_planner_executor_graph()

task = st.text_area(
    pattern["label"],
    value=pattern["default"],
    height=120,
    placeholder=pattern["placeholder"],
    key=f"task_{pattern_name}",
)

if st.button("Run agent", use_container_width=True, type="primary"):
    with st.spinner("Thinking..."):
        if pattern_name == "Tools-Using":
            result = app.invoke({"question": task})
        else:
            result = app.invoke({"task": task})

    if pattern_name == "Planner-Executor":
        st.subheader("Plan")
        plan = [step.strip().lstrip("- ").strip() for step in result.get("plan", []) if step.strip()]
        if plan:
            st.markdown("\n".join(f"{index}. {step}" for index, step in enumerate(plan, start=1)))
        else:
            st.info("The planner did not return any steps.")

        st.subheader("Execution")
        st.markdown(result.get("output", "No execution output was returned."))
    else:
        st.subheader("Response")

        if "result" in result:
            st.success(f"Calculated result: {result['result']}")
        elif "answer" in result:
            st.write(result["answer"])
        else:
            st.info(result)