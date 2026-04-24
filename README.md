# RAG Document Q&A API

A lightweight FastAPI RAG backend that accepts a `.txt` or `.pdf` file, stores the latest uploaded document in memory, retrieves relevant chunks with TF-IDF, and asks Gemini to answer strictly from that context.

## Features
- Upload `.txt` and `.pdf` documents
- Chunk document text and store the latest document in memory
- Retrieve the most relevant chunks for each question
- Generate answers with Gemini using context-only prompting
- Return `"I don't know"` when the answer is not supported by the document

## Tech Stack
- FastAPI
- scikit-learn TF-IDF retrieval
- Google Gemini API
- React + Vite frontend
- Docker

## Live API
```text
https://rag-document-qa-api.onrender.com
```

API docs:

```text
https://rag-document-qa-api.onrender.com/docs
```

## Live Frontend
```text
https://rag-document-qa-ui.onrender.com
```

## Notes About This Version
- This implementation keeps only one active document at a time.
- Uploading a new document replaces the previous one.
- Because storage is in memory, restarting the app clears the uploaded document.

## Environment Setup
Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_real_gemini_api_key_here
```

`.env` is already ignored by git, so your API key stays local.

## Run Locally Without Docker
From the project root:

```bash
./.venv/Scripts/uvicorn.exe app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Run With Docker
Build the image:

```bash
docker build -t rag-document-qa-api .
```

Run the container with your local `.env` file:

```bash
docker run --env-file .env -p 8000:8000 rag-document-qa-api
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Run Frontend Locally
From the `frontend` directory:

```bash
npm install
npm run dev
```

The frontend uses this API by default:

```text
https://rag-document-qa-api.onrender.com
```

To point it at another backend, create `frontend/.env.local`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## API Endpoints
### `POST /ingest`
Upload a `.txt` or `.pdf` file as `form-data` with key `file`.

Example response:

```json
{
  "message": "File processed and stored successfully.",
  "filename": "sample.pdf",
  "chunks_stored": 9
}
```

### `POST /ask`
Send a JSON body:

```json
{
  "question": "What is the task in this assessment?"
}
```

Example response:

```json
{
  "answer": "Build a RESTful API that allows a user to upload text and ask an LLM questions based on that context.",
  "context_chunks": [
    "Relevant chunk 1",
    "Relevant chunk 2"
  ]
}
```

## Suggested Postman Flow
1. Call `POST /ingest` with a `.txt` or `.pdf` file.
2. Call `POST /ask` with a question about that uploaded document.
3. Upload a different document to replace the previous one.
4. Ask again and confirm answers now come from the latest file only.

## Deployment
The app is container-ready for deployment to services such as Render, Koyeb, Azure App Service, or any platform that can run a Docker container. Configure `GEMINI_API_KEY` as an environment variable in the deployment platform.

### Render Deployment
This repository includes a `render.yaml` blueprint for deploying the Dockerized backend on Render.

Steps:
1. Push this repository to GitHub.
2. In Render, create a new Blueprint or Web Service from the GitHub repository.
3. When prompted, provide `GEMINI_API_KEY` as a secret environment variable.
4. Deploy the service.
5. Open the generated Render URL and check `/docs`.

Live API URL:

```text
https://rag-document-qa-api.onrender.com
```

Use these hosted endpoints:

```text
https://rag-document-qa-api.onrender.com/ingest
https://rag-document-qa-api.onrender.com/ask
https://rag-document-qa-api.onrender.com/docs
```

### Render Frontend Deployment
The same `render.yaml` also defines a static site named `rag-document-qa-ui`.

It builds from the `frontend` directory and uses:

```text
VITE_API_BASE_URL=https://rag-document-qa-api.onrender.com
```

## CI/CD
This repository includes a GitHub Actions workflow at `.github/workflows/docker-build.yml`.

The workflow builds the Docker image on pushes to `main` or `master` and on pull requests. This gives a quick check that the Dockerfile still builds before deployment.
