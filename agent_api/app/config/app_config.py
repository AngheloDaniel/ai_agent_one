from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    aws_region: str = "us-east-1"
    bedrock_model_id: str = "amazon.nova-micro-v1:0"
    bedrock_endpoint_url: str = "https://bedrock-runtime.us-east-1.amazonaws.com"
    mcp_server_url: str = "http://localhost:8001"
    chroma_persist_path: str = "./chroma_store"
    data_path: str = "./data"
    embed_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    rerank_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"


settings = Settings()