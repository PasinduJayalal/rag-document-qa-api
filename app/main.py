from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import CORS_ORIGINS
from app.routes.ingest import router as ingest_router
from app.routes.ask import router as ask_router

app = FastAPI(title="RAG Document Q&A API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "API is running"}

app.include_router(ingest_router, tags=["Ingest"])
app.include_router(ask_router, tags=["Ask"])
