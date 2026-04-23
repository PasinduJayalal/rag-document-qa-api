from app.core.config import TOP_K_RESULTS
from app.services.embedder import embed_query
from app.services.vector_store import get_collection


def retrieve_relevant_chunks(question: str, top_k: int = TOP_K_RESULTS) -> list[str]:
    if not question or not question.strip():
        return []

    query_embedding = embed_query(question)

    if not query_embedding:
        return []

    collection = get_collection()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "distances"]
    )

    documents = results.get("documents", [])

    if not documents or not documents[0]:
        return []

    return documents[0]