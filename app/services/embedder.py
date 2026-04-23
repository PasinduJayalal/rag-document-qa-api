from sklearn.feature_extraction.text import TfidfVectorizer


VECTORIZER = TfidfVectorizer()


def embed_chunks(chunks: list[str]) -> list[list[float]]:
    if not chunks:
        return []

    matrix = VECTORIZER.fit_transform(chunks)
    return matrix.toarray().tolist()


def embed_query(query: str) -> list[float]:
    if not query or not query.strip():
        return []

    matrix = VECTORIZER.transform([query])
    return matrix.toarray()[0].tolist()