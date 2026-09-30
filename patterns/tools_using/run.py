from .graph import build_graph

app = build_graph()

questions = [
    "What is the square of the average of 10 and 5?",
    "Define AI.",
    "What is 12 * 7?"
]

for question in questions:
    result = app.invoke({"question": question})
    print("\n\nQuestion:")
    print(question)
    print("Result:")
    print(result)