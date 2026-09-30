from typing import TypedDict, Optional, Union

class AgentState(TypedDict):
    question: str
    expression: str
    result: Optional[Union[int, float, str]]
    answer: Optional[str]
    mode: str