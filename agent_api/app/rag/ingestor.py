from pathlib import Path

from app.config.app_config import settings
from app.dependencies.chromadb_dependency import get_chroma_client, get_collection


def chunking():
    pass

def ingest_txt_files(data_path: str = None) -> int:
    """Reads all the txt files from data and indexes them in the collection
    returns the numbers of indexed chunks"""

    path = Path(data_path or settings.data_path)
    client = get_chroma_client()
    collection = get_collection(client)

    documents, ids, metadatas = [], [], []
    chunk_size = 80

    doc_id = 0

    for txt_file in path.glob("*.txt"):
        text = txt_file.read_text(encoding="utf-8")
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        for chunk in chunks:
            if chunk.strip():
                documents.append(chunk)
                ids.append(f"doc_{doc_id}")
                metadatas.append({"source": txt_file.name})
                doc_id += 1

        existing = collection.get()
        if existing["ids"]:
            collection.delete(ids=existing["ids"])

        if documents:
            collection.upsert(documents=documents, ids=ids, metadatas=metadatas)

        return len(documents)