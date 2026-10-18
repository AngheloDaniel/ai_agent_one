import chromadb

from app.config.app_config import settings

def get_chroma_client() -> chromadb.ClientAPI:
    return chromadb.PersistentClient(path=settings.CHROMA_DATABASE_PATH)