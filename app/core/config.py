
import os

from dotenv import load_dotenv


load_dotenv()

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

TOP_K_RESULTS = 3

UPLOAD_DIR = "app/data/uploads"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
LLM_MODEL = "gemini-3-flash-preview"
MAX_TOKENS = 500

DEFAULT_FALLBACK_ANSWER = "I don't know"
