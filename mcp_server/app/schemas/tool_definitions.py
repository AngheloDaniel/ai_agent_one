from app.schemas.mcp import ToolDefinition

TOOL_DEFINITIONS = [
    ToolDefinition(
        name="get_current_time",
        description="Returns current day and time",
        input_schema={"type": "object", "proterties": {}}
    ),
    ToolDefinition(
        name="execute_web_search",
        description="Search the internet for current information about a topic",
        input_schema={
            "type": "object",
            "proterties": {
                "query": {"type": "string", "description": "Search query"},
            },
            "required": ["query"]
        }
    )
]