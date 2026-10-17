from pydantic import BaseModel

class ToolDefinition(BaseModel):
    name: str
    description: str
    input_schema: dict[str, object]

class ToolCall(BaseModel):
    name: str
    arguments: dict[str, object]

class ToolResult(BaseModel):
    tool_name: str
    result: str
    is_error: bool = False