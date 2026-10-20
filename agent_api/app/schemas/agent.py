from pydantic import BaseModel


class ToolResult(BaseModel):
    tool: str
    input: dict[str, object]
    result: str

class AgentResponse(BaseModel):
    answer: str
    tool_calls: list[ToolResult]
    rag_sources: list[str]

class AgentRequest(BaseModel):
    message: str
