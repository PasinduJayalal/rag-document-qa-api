from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer


@dataclass
class InMemoryVectorStore:
    chunks: list[str]
    vectorizer: TfidfVectorizer
    embeddings: list[list[float]]


_current_store: InMemoryVectorStore | None = None


def store_document(
    chunks: list[str],
    vectorizer: TfidfVectorizer,
    embeddings: list[list[float]],
) -> None:
    global _current_store

    if len(chunks) != len(embeddings):
        raise ValueError("Number of chunks and embeddings must match.")

    _current_store = InMemoryVectorStore(
        chunks=chunks,
        vectorizer=vectorizer,
        embeddings=embeddings,
    )


def get_store() -> InMemoryVectorStore | None:
    return _current_store
