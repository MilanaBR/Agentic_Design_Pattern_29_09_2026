from patterns.planner_executor.graph import build_graph
import json

app = build_graph()

task = "Create a simple 3-step plan for launching an AI chatbot product."
result=app.invoke({"task": task})
print(json.dumps(result, indent=2, ensure_ascii=False))

"""
Create a simple 3-step plan for launching an AI chatbot product.
"""