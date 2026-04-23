from google import genai

from app.core.config import DEFAULT_FALLBACK_ANSWER, GEMINI_API_KEY, LLM_MODEL
from app.core.prompt import build_prompt


def generate_answer(question: str, context_chunks: list[str]) -> str:
    if not question or not question.strip():
        return DEFAULT_FALLBACK_ANSWER

    if not context_chunks:
        return DEFAULT_FALLBACK_ANSWER

    prompt = build_prompt(question=question, context_chunks=context_chunks)

    try:
        if not GEMINI_API_KEY:
            return DEFAULT_FALLBACK_ANSWER

        client = genai.Client(api_key=GEMINI_API_KEY)
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
