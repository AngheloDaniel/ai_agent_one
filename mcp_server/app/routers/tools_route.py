from fastapi import APIRouter

from app.schemas.mcp import ToolResult, ToolCall
from app.schemas.tool_definitions import TOOL_DEFINITIONS
from app.services import tool_service

tools_router = APIRouter(prefix="/mcp", tags=["Tools"])


@tools_router.get("/tools", response_model=TOOL_DEFINITIONS)
async def tools():
    """MCP tool discovery endpoint"""
    return TOOL_DEFINITIONS

@tools_router.post("/excute", response_model=ToolResult)
async def tool_excute(call: ToolCall):
    """Execute MCP tool by name"""
    match call.name:
        case "get_current_time":
            return ToolResult(
                tool_name=call.name,
                result=tool_service.get_current_time()
            )
        case _:
            return ToolResult(
                tool_name="tool_not_found",
                result={"error": "tool_not_found"}
            )