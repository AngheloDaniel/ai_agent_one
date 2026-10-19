from sentence_transformers import CrossEncoder

from app.config.app_config import settings
from app.domain.retrieved_chunk import RetrievedChunk


def _load_reranker(maxsize=1) -> CrossEncoder:
    """Load the model one time (singleton)"""
    return CrossEncoder(settings.rerank_model)

def rerank(query: str, chunks: list[RetrievedChunk], top_k: int = 3) -> list[RetrievedChunk]:
    """
    Rerank chunks using a cross-encoder model, and returns the top-k most relevent
    Difference vs embeddings: the cross encoder evalutes query+chunks together
    """
    if not chunks:
        return []

    model = _load_reranker()
    pairs = [(query, chunk.text) for chunk in chunks]
    scores = model.predict(pairs)

    for chunk, score in zip(chunks, scores):
        chunk.score = float(score)

    return sorted(chunks, key=lambda c: c.score, reverse=True)[:top_k]
