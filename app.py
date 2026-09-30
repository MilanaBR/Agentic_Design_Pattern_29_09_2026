import streamlit as st

from patterns.tools_using.graph import build_graph as build_tools_using_graph
from patterns.planner_executor.graph import build_graph as build_planner_executor_graph
from patterns.supervisor_worker.graph import build_graph as build_supervisor_worker_graph
from patterns.reflection.graph import build_graph as build_reflection_graph

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
    "Supervisor-Worker": {
        "description": "A supervisor routes each request to a math or leave-balance worker.",
        "label": "Ask a question",
        "default": "What is the leave balance for Alice?",
        "placeholder": "Try: What is 18% of 250? or How much leave does Alice have?",
    },
    "Reflection": {
        "description": "A generator drafts an answer, then a critic reviews it and requests revisions when needed.",
        "label": "Describe a task",
        "default": "Explain why Python is a good language for beginners in exactly 2 sentences. Mention simple syntax, strong community support, and the availability of libraries.",
        "placeholder": "For example: Explain a technical concept in two clear sentences.",
    },
}

pattern_name = st.sidebar.selectbox("Agentic design pattern", list(patterns))
pattern = patterns[pattern_name]

st.title(f"{pattern_name} Agent Demo")
st.caption(pattern["description"])

if pattern_name == "Tools-Using":
    app = build_tools_using_graph()
elif pattern_name == "Planner-Executor":
    app = build_planner_executor_graph()
elif pattern_name == "Supervisor-Worker":
    app = build_supervisor_worker_graph()
else:
    app = build_reflection_graph()

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
        elif pattern_name == "Planner-Executor":
            result = app.invoke({"task": task})
        elif pattern_name == "Supervisor-Worker":
            result = app.invoke({"query": task})
        else:
            result = app.invoke({
                "task": task,
                "attempts": 0,
                "needs_revision": True,
                "status": "pending",
            })

    if pattern_name == "Planner-Executor":
        st.subheader("Plan")
        plan = [step.strip().lstrip("- ").strip() for step in result.get("plan", []) if step.strip()]
        if plan:
            st.markdown("\n".join(f"{index}. {step}" for index, step in enumerate(plan, start=1)))
        else:
            st.info("The planner did not return any steps.")

        st.subheader("Execution")
        st.markdown(result.get("output", "No execution output was returned."))
    elif pattern_name == "Reflection":
        st.subheader("Critic Review")
        status = result.get("status", "unknown")
        attempts = result.get("attempts", 0)
        if status == "approved":
            st.success(f"Approved after {attempts} draft(s).")
        else:
            st.warning(f"Status: {status.replace('_', ' ').title()} after {attempts} draft(s).")

        st.subheader("Final Answer")
        st.write(result.get("final_answer", result.get("draft", "No answer was returned.")))

        feedback = result.get("feedback")
        if feedback:
            st.caption("Latest critic feedback")
            st.write(feedback)
    elif pattern_name == "Supervisor-Worker":
        st.subheader("Supervisor Routing")
        worker = result.get("worker")
        worker_label = {
            "math": "Math Agent",
            "leave": "Leave Balance Agent",
        }.get(worker, "Unknown worker")
        st.write(f"Selected worker: **{worker_label}**")

        if worker == "math":
            st.caption("Generated arithmetic expression")
            st.code(result.get("expression", "No expression was returned."), language="python")
            st.success(f"Result: {result.get('result', 'No result was returned.')}")
        elif worker == "leave":
            st.write(f"Employee: {result.get('employee_name', 'Unknown')}")
            st.success(result.get("leave_balance", "No leave balance was returned."))
        else:
            st.info(result)
    else:
        st.subheader("Response")

        if "result" in result:
            st.success(f"Calculated result: {result['result']}")
        elif "answer" in result:
            st.write(result["answer"])
        else:
            st.info(result)