from fastapi import APIRouter, HTTPException, status

from app.core.config import DEFAULT_FALLBACK_ANSWER
from app.models.schemas import AskRequest, AskResponse
from app.services.retriever import retrieve_relevant_chunks
from app.services.llm_service import generate_answer

router = APIRouter()


@router.post("/ask", response_model=AskResponse, status_code=status.HTTP_200_OK)
def ask_question(payload: AskRequest):
    question = payload.question.strip()

    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question cannot be empty."
        )

    try:
        context_chunks = retrieve_relevant_chunks(question)

        if not context_chunks:
            return AskResponse(
                answer=DEFAULT_FALLBACK_ANSWER,
                context_chunks=[]
            )

        answer = generate_answer(question=question, context_chunks=context_chunks)

        if not answer or not answer.strip():
            answer = DEFAULT_FALLBACK_ANSWER

        return AskResponse(
            answer=answer,
            context_chunks=context_chunks
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to answer question: {str(e)}"
        )