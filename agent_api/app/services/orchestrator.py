from app.schemas.agent import AgentResponse
from app.services.bedrock import BedrockClient
from app.services.mcp_client import MCPClient
from app.services.rag import RAGService

MAX_ITERATIONS = 5

SYSTEM_PROMPT = """You are a helpful AI assistant with access to tools and a knowledge base.

When answering:
1. First, check if the knowledge base has relevant information (it will be provided as context).
2. Use tools when you need current information not in the knowledge base.
3. Always cite your sources (knowledge base vs web search).
4. If you use a tool, wait for the result before answering.

Available context from knowledge base:
{rag_context}
"""

class AgentOrchestrator:
    def __init__(self):
        self.bedrock = BedrockClient()
        self.mcp = MCPClient()
        self.rag = RAGService()

    async def run(self, user_message: str) -> AgentResponse:
        rag_context = await self.rag.get_context(user_message)
        mcp_tools = await self.mcp.get_available_tools()
        bedrock_tools = self.bedrock._format_tools_for_bedrock(mcp_tools)

        # prepare message history
        messages = [{"role": "user", "content": [{"text": user_message}]}]
        system = SYSTEM_PROMPT.format(rag_context=rag_context or "No relevant context found")

        tool_calls_log = []
        for iteration in range(MAX_ITERATIONS):
            response = self.bedrock.invoke(
                messages=messages,
                system_prompt=system,
                tools=bedrock_tools,
            )

            stop_reason = response["stop_reason"]
            output_message = response["output"]["message"]
            messages.append(output_message)

            if stop_reason == "end_turn":
                final_text = self._extract_text(output_message)
                return AgentResponse(
                    answer=final_text,
                    tool_calls=tool_calls_log,
                    rag_sources=self.rag.last_sources
                )

            if stop_reason == "tool_use":
                tool_results = []
                for block in output_message["content"]:
                    if block.get("toolUse"):
                        tool_use = block["toolUse"]
                        tool_name = tool_use["name"]
                        tool_input = tool_use["input"]

                        result = await self.mcp.execute_tool(tool_name, tool_input)
                        tool_calls_log.append({"tool": tool_name, "input": tool_input, "result": result.result})

                        tool_results.append({
                            "toolResult": {
                                "toolUseId": tool_use["toolUseId"],
                                "content": [{"text": result.result}]
                            }
                        })

                messages.append({"role": "user", "content": tool_results})

        return AgentResponse()

    def _extract_text(self, message: dict) -> str:
        return " ".join(
            block["text"] for block in message.get("content", [])
            if "text" in block
        )
