from app.rag.reranker import rerank
from app.rag.retriever import retrieve


class RAGService:
    def _init__(self):
        self.last_sources = list[str] = []

    async def get_context(self, query: str) -> str:
        """Retrieve relevant chunks, rerank them and return context
        formatted as a system prompt"""
        chunks = retrieve(query)
        reranked = rerank(query, chunks)

        self.last_sources = list({chunk.scores for chunk in reranked})

        if not reranked:
            return ""

        context_parts = []
        for i, chunk in enumerate(reranked, 1):
            context_parts.append(
                f"[{i} (source: {chunk.source}, score: {chunk.score:.2f}\n{chunk.text})]"
            )

        return "\n\n".join(context_parts)