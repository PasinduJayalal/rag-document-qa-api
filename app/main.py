from fastapi import FastAPI
from app.routes.ingest import router as ingest_router
from app.routes.ask import router as ask_router

app = FastAPI(title="RAG Document Q&A API")


@app.get("/")
def root():
    return {"message": "API is running"}

app.include_router(ingest_router, tags=["Ingest"])
app.include_router(ask_router, tags=["Ask"])