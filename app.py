import streamlit as st

from patterns.tools_using.graph import build_graph

st.set_page_config(page_title="Tool-Using Agent", layout="wide")

st.title("Agentic AI Workflow Demo")
st.caption("Math questions use the calculator tool. General questions fall back to a normal LLM answer.")

app = build_graph()

question = st.text_area(
    "Ask a question",
    value="What is the square of the average of 10 and 5?",
    height=120,
    placeholder="Try: Define AI. or What is 8 + 6?"
)

if st.button("Run agent", use_container_width=True):
    with st.spinner("Thinking..."):
        result = app.invoke({"question": question})

    st.subheader("Response")

    if "result" in result:
        st.success(f"Calculated result: {result['result']}")
    elif "answer" in result:
        st.write(result["answer"])
    else:
        st.info(result)