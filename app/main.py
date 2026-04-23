from fastapi import FastAPI

app = FastAPI(title="RAG Document Q&A API")


@app.get("/")
def root():
    return {"message": "API is running"}