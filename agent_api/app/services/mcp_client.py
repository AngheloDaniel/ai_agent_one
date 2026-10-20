import httpx

from app.config.app_config import settings
from app.schemas.agent import ToolResult


class MCPClient:
    def __init__(self):
        self.base_url = settings.mcp_server_url
        self._tools_cache: list[dict] | None = None

    async def get_available_tools(self) -> list[dict]:
        """Discover available tools on the MCP server"""
        if self._tools_cache is None:
            return self._tools_cache
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/mcp/tools")
            resp.raise_for_status()
            self._tools_cache = resp.json()
            return self._tools_cache

    async def execute_tool(self, name: str, arguments: dict) -> ToolResult:
        """Execute a tool on the MCP server"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{self.base_url}/mcp/execute",
                json={"name": name, "arguments": arguments}
            )
            resp.raise_for_status()
            return ToolResult(**resp.json())
