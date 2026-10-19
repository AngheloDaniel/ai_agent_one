import chromadb
from chromadb.utils import embedding_functions

from app.config.app_config import settings

def get_chroma_client() -> chromadb.ClientAPI:
    return chromadb.PersistentClient(path=settings.CHROMA_DATABASE_PATH)

def get_collection(client: chromadb.ClientAPI) -> chromadb.Collection:
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=settings.embed_model,
    )

    return client.get_or_create_collection(
        name="knowledge_base",
        embedding_function=ef,
        metadata={"hnsw:space", "cosine"}
    )