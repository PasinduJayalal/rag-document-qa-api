import { FileText, LoaderCircle, Send, UploadCloud } from 'lucide-react';
import { useState } from 'react';

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || 'https://rag-document-qa-api.onrender.com'
).replace(/\/$/, '');

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState('');
  const [ingestResult, setIngestResult] = useState(null);
  const [answerResult, setAnswerResult] = useState(null);
  const [error, setError] = useState('');
  const [isIngesting, setIsIngesting] = useState(false);
  const [isAsking, setIsAsking] = useState(false);

  const handleIngest = async (event) => {
    event.preventDefault();

    if (!file) {
      setError('Choose a .txt or .pdf file first.');
      return;
    }

    setError('');
    setIsIngesting(true);
    setIngestResult(null);
    setAnswerResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_BASE_URL}/ingest`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to ingest document.');
      }

      setIngestResult(data);
    } catch (caughtError) {
      setError(caughtError.message);
    } finally {
      setIsIngesting(false);
    }
  };

  const handleAsk = async (event) => {
    event.preventDefault();

    if (!question.trim()) {
      setError('Ask a question about the uploaded document.');
      return;
    }

    setError('');
    setIsAsking(true);
    setAnswerResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to answer question.');
      }

      setAnswerResult(data);
    } catch (caughtError) {
      setError(caughtError.message);
    } finally {
      setIsAsking(false);
    }
  };

  return (
    <main className="app-shell">
      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">Document Q&A</p>
            <h1>Ask a document, not the internet.</h1>
          </div>
          <a className="api-link" href={`${API_BASE_URL}/docs`} target="_blank" rel="noreferrer">
            API Docs
          </a>
        </header>

        <div className="panels">
          <form className="panel upload-panel" onSubmit={handleIngest}>
            <div className="panel-heading">
              <FileText size={22} aria-hidden="true" />
              <div>
                <h2>Upload</h2>
                <p>Latest file replaces the previous one.</p>
              </div>
            </div>

            <label className="drop-zone">
              <input
                type="file"
                accept=".txt,.pdf"
                onChange={(event) => setFile(event.target.files?.[0] || null)}
              />
              <span className="file-name">{file ? file.name : 'Choose a TXT or PDF file'}</span>
            </label>

            <button className="primary-button" type="submit" disabled={isIngesting}>
              {isIngesting ? <LoaderCircle className="spin" size={18} /> : <UploadCloud size={18} />}
              {isIngesting ? 'Processing' : 'Ingest Document'}
            </button>

            {ingestResult && (
              <div className="status-box success">
                <strong>{ingestResult.filename}</strong>
                <span>{ingestResult.chunks_stored} chunks stored</span>
              </div>
            )}
          </form>

          <form className="panel ask-panel" onSubmit={handleAsk}>
            <div className="panel-heading">
              <Send size={22} aria-hidden="true" />
              <div>
                <h2>Ask</h2>
                <p>Answers stay grounded in the uploaded file.</p>
              </div>
            </div>

            <textarea
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="What is the task in this assessment?"
              rows={7}
            />

            <button className="primary-button" type="submit" disabled={isAsking}>
              {isAsking ? <LoaderCircle className="spin" size={18} /> : <Send size={18} />}
              {isAsking ? 'Thinking' : 'Ask Question'}
            </button>
          </form>
        </div>

        {error && <div className="status-box error">{error}</div>}

        <section className="answer-section">
          <h2>Answer</h2>
          <article className="answer-card">
            {answerResult ? answerResult.answer : 'Upload a document and ask a question to see the answer here.'}
          </article>

          {answerResult?.context_chunks?.length > 0 && (
            <div className="context-list">
              <h3>Retrieved Context</h3>
              {answerResult.context_chunks.map((chunk, index) => (
                <details key={`${chunk}-${index}`}>
                  <summary>Chunk {index + 1}</summary>
                  <p>{chunk}</p>
                </details>
              ))}
            </div>
          )}
        </section>
      </section>
    </main>
  );
}

export default App;
