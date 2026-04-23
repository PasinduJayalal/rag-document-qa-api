from google import genai

from app.core.config import DEFAULT_FALLBACK_ANSWER, LLM_MODEL
from app.core.prompt import build_prompt


client = genai.Client()


def generate_answer(question: str, context_chunks: list[str]) -> str:
    if not question or not question.strip():
        return DEFAULT_FALLBACK_ANSWER

    if not context_chunks:
        return DEFAULT_FALLBACK_ANSWER

    prompt = build_prompt(question=question, context_chunks=context_chunks)

    try:
        response = client.models.generate_content(
            model=LLM_MODEL,
            contents=prompt,
        )

        answer = getattr(response, "text", None)

        if not answer or not answer.strip():
            return DEFAULT_FALLBACK_ANSWER

        return answer.strip()

    except Exception:
        return DEFAULT_FALLBACK_ANSWER