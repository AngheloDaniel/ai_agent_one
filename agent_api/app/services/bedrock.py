import boto3

from app.config.app_config import settings


class BedrockClient:
    def __init__(self):
        self._client = boto3.client(
            "bedrock_runtime",
            endpoint_url=settings.bedrock_endpoint_url,
            region_name=settings.aws_region
        )

    def invoke(self,
               messages: list[dict],
               system_prompt: str = "",
               tools: list[dict] = None) -> dict:
        """Calls AWS Bedrock model and returns the raw response for the
        orchestrator to process it"""
        kwars = {
            "modelId": settings.model_id,
            "messages": messages
        }

        if system_prompt:
            kwars["system"] = []
        if tools:
            kwars["toolConfig"] = {"tools": tools}

        return self._client.converse(**kwars)

    def _format_tools_for_bedrock(self, mcp_tools: list[dict]) -> list[dict]:
        """Converts the MCP format to the required Bedrock format"""
        return [
            {
                "toolSpec": {
                    "name": t["name"],
                    "description": t["description"],
                    "input_schema": {"json": t["input_schema"]},
                }
            }
            for t in mcp_tools
        ]