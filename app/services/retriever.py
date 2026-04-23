from sklearn.metrics.pairwise import cosine_similarity

from app.core.config import TOP_K_RESULTS
from app.services.embedder import embed_query
from app.services.vector_store import get_store


def retrieve_relevant_chunks(question: str, top_k: int = TOP_K_RESULTS) -> list[str]:
    if not question or not question.strip():
        return []

    store = get_store()

    if store is None or not store.chunks or not store.embeddings:
        return []

    query_embedding = embed_query(question, store.vectorizer)

    if not query_embedding:
        return []

    similarity_scores = cosine_similarity([query_embedding], store.embeddings)[0]

    if len(similarity_scores) == 0:
        return []

    ranked_indices = sorted(
        range(len(similarity_scores)),
        key=lambda index: similarity_scores[index],
        reverse=True,
    )

    top_indices = ranked_indices[:top_k]
    return [store.chunks[index] for index in top_indices]
