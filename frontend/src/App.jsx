import { useState } from 'react'
import './App.css'

export default function App() {
  const [mode, setMode] = useState('search') // 'search' or 'rag'
  const [input, setInput] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [indexName, setIndexName] = useState('documents')
  const [isIndexing, setIsIndexing] = useState(false)

  const handleSemanticSearch = async (e) => {
    e.preventDefault()
    if (!input.trim()) return

    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`/api/v1/search/semantic?index_name=${indexName}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: input, top_k: 5 }),
      })

      if (!response.ok) throw new Error('Search failed')
      const data = await response.json()
      setResults(data.results || [])
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleRAGQuery = async (e) => {
    e.preventDefault()
    if (!input.trim()) return

    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`/api/v1/rag/query?index_name=${indexName}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: input, top_k: 5 }),
      })

      if (!response.ok) throw new Error('RAG query failed')
      const data = await response.json()
      setResults(data.sources || [])
      // Display answer separately
      alert(`Answer: ${data.answer}`)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return

    setIsIndexing(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch(
        `/api/v1/documents/upload?index_name=${indexName}`,
        {
          method: 'POST',
          body: formData,
        }
      )

      if (!response.ok) throw new Error('Upload failed')
      const data = await response.json()
      alert(`✅ Indexed ${data.chunks_indexed} chunks from ${file.name}`)
      e.target.value = ''
    } catch (err) {
      setError(err.message)
    } finally {
      setIsIndexing(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🔍 Endee RAG & Semantic Search</h1>
        <p>Vector-powered document retrieval and intelligent Q&A</p>
      </header>

      <div className="container">
        {/* Sidebar */}
        <aside className="sidebar">
          <div className="section">
            <h3>Mode</h3>
            <div className="modes">
              <button
                className={`btn-mode ${mode === 'search' ? 'active' : ''}`}
                onClick={() => setMode('search')}
              >
                🔎 Semantic Search
              </button>
              <button
                className={`btn-mode ${mode === 'rag' ? 'active' : ''}`}
                onClick={() => setMode('rag')}
              >
                💡 RAG Q&A
              </button>
            </div>
          </div>

          <div className="section">
            <h3>Index Name</h3>
            <input
              type="text"
              value={indexName}
              onChange={(e) => setIndexName(e.target.value)}
              placeholder="e.g., documents"
              className="input"
            />
          </div>

          <div className="section">
            <h3>Upload Document</h3>
            <label className="file-upload">
              <input
                type="file"
                accept=".txt"
                onChange={handleFileUpload}
                disabled={isIndexing}
              />
              <span>{isIndexing ? '📤 Indexing...' : '📁 Choose File'}</span>
            </label>
          </div>

          <div className="section">
            <h3>Mode Description</h3>
            {mode === 'search' ? (
              <p className="description">
                Finds similar documents using vector embeddings. Great for finding related content.
              </p>
            ) : (
              <p className="description">
                Combines search + LLM to answer questions based on your documents with source citations.
              </p>
            )}
          </div>
        </aside>

        {/* Main content */}
        <main className="main">
          <div className="search-box">
            <form
              onSubmit={mode === 'search' ? handleSemanticSearch : handleRAGQuery}
            >
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder={
                  mode === 'search'
                    ? 'Search documents...'
                    : 'Ask a question...'
                }
                className="search-input"
              />
              <button
                type="submit"
                disabled={loading || !input.trim()}
                className="btn-search"
              >
                {loading ? '⏳ Processing...' : '🚀 Search'}
              </button>
            </form>
          </div>

          {error && (
            <div className="error">
              ⚠️ {error}
            </div>
          )}

          <div className="results">
            {results.length > 0 && (
              <>
                <h2>
                  {mode === 'search' ? 'Search Results' : 'Sources Retrieved'}
                </h2>
                <div className="result-list">
                  {results.map((result, idx) => (
                    <div key={idx} className="result-card">
                      <div className="result-header">
                        <h4>Document {idx + 1}</h4>
                        {result.similarity && (
                          <span className="similarity">
                            Similarity: {(result.similarity * 100).toFixed(1)}%
                          </span>
                        )}
                      </div>
                      <p className="result-content">
                        {typeof result.content === 'string'
                          ? result.content.slice(0, 200)
                          : result.id}
                      </p>
                      {result.metadata && Object.keys(result.metadata).length > 0 && (
                        <div className="result-metadata">
                          <small>
                            {Object.entries(result.metadata)
                              .map(([k, v]) => `${k}: ${v}`)
                              .join(' | ')}
                          </small>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </>
            )}

            {!loading && results.length === 0 && input && (
              <div className="no-results">
                📭 No results found. Try uploading documents first!
              </div>
            )}

            {!loading && results.length === 0 && !input && (
              <div className="empty-state">
                {mode === 'search' ? (
                  <>
                    <h2>🔍 Semantic Search</h2>
                    <p>
                      Upload a document and search for similar content using vector embeddings.
                    </p>
                  </>
                ) : (
                  <>
                    <h2>💡 RAG Q&A</h2>
                    <p>
                      Ask questions about your documents. The system retrieves relevant content
                      and generates answers with source citations.
                    </p>
                  </>
                )}
              </div>
            )}
          </div>
        </main>
      </div>

      <footer className="footer">
        <p>
          Built with ❤️ using Endee vector database, FastAPI, and React
        </p>
      </footer>
    </div>
  )
}
