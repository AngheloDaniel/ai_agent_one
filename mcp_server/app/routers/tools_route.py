from fastapi import APIRouter

from app.schemas.mcp import ToolResult, ToolCall, ToolDefinition
from app.schemas.tool_definitions import TOOL_DEFINITIONS
from app.services.tool_service import ToolService

tools_router = APIRouter(prefix="/mcp", tags=["Tools"])


@tools_router.get("/tools", response_model=list[ToolDefinition])
async def tools():
    """MCP tool discovery endpoint"""
    return TOOL_DEFINITIONS

@tools_router.post("/excute", response_model=ToolResult)
async def tool_excute(call: ToolCall):
    """Execute MCP tool by name"""
    tool_service = ToolService()

    match call.name:
        case "get_current_time":
            return ToolResult(
                tool_name=call.name,
                result=tool_service.get_current_time()
            )
        case "web_search":
            query: str = str(call.arguments.get("query",""))
            return ToolResult(
                tool_name=call.name,
                result=tool_service.execute_web_search(query)
            )
        case _:
            return ToolResult(
                tool_name="tool_not_found",
                result="tool_not_found",
                is_error=True
            )