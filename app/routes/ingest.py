from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.config import UPLOAD_DIR
from app.models.schemas import IngestResponse
from app.services.chunker import chunk_text
from app.services.embedder import embed_chunks
from app.services.parser import extract_text_from_file
from app.services.vector_store import store_document

router = APIRouter()

upload_dir = Path(UPLOAD_DIR)
upload_dir.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".txt", ".pdf"}


@router.post("/ingest", response_model=IngestResponse, status_code=status.HTTP_200_OK)
async def ingest_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file name provided."
        )

    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .txt and .pdf files are supported."
        )

    file_path = upload_dir / file.filename

    try:
        file_bytes = await file.read()

        with open(file_path, "wb") as f:
            f.write(file_bytes)

        text = extract_text_from_file(file_path)

        if not text or not text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract any text from the uploaded file."
            )

        chunks = chunk_text(text)

        if not chunks:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text was extracted but no chunks were created."
            )

        vectorizer, embeddings = embed_chunks(chunks)

        if vectorizer is None or not embeddings:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create embeddings from the document."
            )

        store_document(chunks, vectorizer, embeddings)

        return IngestResponse(
            message="File processed and stored successfully.",
            filename=file.filename,
            chunks_stored=len(chunks)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to ingest document: {str(e)}"
        )
