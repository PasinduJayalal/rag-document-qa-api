from sklearn.feature_extraction.text import TfidfVectorizer


def embed_chunks(chunks: list[str]) -> tuple[TfidfVectorizer | None, list[list[float]]]:
    if not chunks:
        return None, []

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(chunks)
    return vectorizer, matrix.toarray().tolist()


def embed_query(query: str, vectorizer: TfidfVectorizer | None) -> list[float]:
    if not query or not query.strip() or vectorizer is None:
        return []

    matrix = vectorizer.transform([query])
    return matrix.toarray()[0].tolist()
