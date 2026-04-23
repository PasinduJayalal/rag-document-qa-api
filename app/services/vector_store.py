import chromadb

from app.core.config import CHROMA_COLLECTION_NAME, CHROMA_PATH


client = chromadb.PersistentClient(path=CHROMA_PATH)


def _reset_collection():
    try:
        client.delete_collection(name=CHROMA_COLLECTION_NAME)
    except Exception:
        pass

    return client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)


def store_embeddings(chunks: list[str], embeddings: list[list[float]]) -> None:
    if len(chunks) != len(embeddings):
        raise ValueError("Number of chunks and embeddings must match.")

    collection = _reset_collection()

    ids = [f"chunk-{index}" for index in range(len(chunks))]
    metadatas = [{"chunk_index": index} for index in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def get_collection():
    return client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)