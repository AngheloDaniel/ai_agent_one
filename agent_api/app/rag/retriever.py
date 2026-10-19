from app.dependencies.chromadb_dependency import get_chroma_client, get_collection
from app.domain.retrieved_chunk import RetrievedChunk


def retrieve(query: str, n_results: int = 10) -> list[RetrievedChunk]:
    """Retrieve the top-N result most similar to the given query."""
    client = get_chroma_client()
    collection = get_collection(client)

    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count(), 1),
        include=["documents", "metadatas", "distances"]
    )

    chunks = []

    for doc, meta, dist, in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        chunks.append(RetrievedChunk(
            text=doc,
            source=meta.get("source", "unknown"),
            score=1 - dist
        ))

    return chunks