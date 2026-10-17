from app.schemas.mcp import ToolDefinition

TOOL_DEFINITIONS = [
    ToolDefinition(
        name="get_current_time",
        description="Returns current day and time",
        input_schema={"type": "object", "proterties": {}}
    )
]