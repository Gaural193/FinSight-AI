import { useState } from 'react'

function App() {
  const [file, setFile] = useState(null)
  const [uploadStatus, setUploadStatus] = useState('idle') // idle, loading, success, error
  const [uploadMessage, setUploadMessage] = useState('')
  
  const [query, setQuery] = useState('')
  const [messages, setMessages] = useState([])
  const [isSearching, setIsSearching] = useState(false)

  // -- 1. UPLOAD LOGIC --
  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
    }
  }

  const handleUpload = async () => {
    if (!file) return
    
    setUploadStatus('loading')
    setUploadMessage('Extracting and embedding PDF...')
    
    const formData = new FormData()
    formData.append('file', file)
    
    try {
      // Send it to FastAPI
      const res = await fetch('http://127.0.0.1:8000/api/upload/', {
        method: 'POST',
        body: formData
      })
      
      const data = await res.json()
      
      if (res.ok) {
        setUploadStatus('success')
        setUploadMessage(`Success! Indexed ${data.total_chunks_created} chunks into Vector DB.`)
      } else {
        setUploadStatus('error')
        setUploadMessage(data.detail || 'Upload failed.')
      }
    } catch (err) {
      setUploadStatus('error')
      setUploadMessage('Could not connect to the server. Is Uvicorn running?')
    }
  }

  // -- 2. SEARCH / CHAT LOGIC --
  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query.trim()) return
    
    // Add user message to UI immediately
    const userMsg = { role: 'user', content: query }
    setMessages(prev => [...prev, userMsg])
    setQuery('')
    setIsSearching(true)
    
    try {
      const res = await fetch('http://127.0.0.1:8000/api/search/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: userMsg.content, top_k: 3 })
      })
      
      const data = await res.json()
      
      if (res.ok) {
        // Add AI response to UI
        const aiMsg = { 
          role: 'ai', 
          content: data.answer,
          citations: data.citations 
        }
        setMessages(prev => [...prev, aiMsg])
      } else {
        setMessages(prev => [...prev, { role: 'ai', content: `Error: ${data.detail}` }])
      }
    } catch (err) {
      setMessages(prev => [...prev, { role: 'ai', content: 'Could not connect to the server.' }])
    } finally {
      setIsSearching(false)
    }
  }

  return (
    <div className="app-container">
      
      {/* LEFT SIDEBAR: Upload Zone */}
      <div className="glass-panel sidebar">
        <h1>FinSight AI</h1>
        <p>Premium Document Intelligence</p>
        
        <div className="upload-zone">
          <input type="file" accept=".pdf" onChange={handleFileChange} />
          <span className="upload-icon">📄</span>
          <h3>{file ? file.name : "Drag & Drop PDF"}</h3>
          <p style={{ marginTop: '8px' }}>or click to browse</p>
        </div>
        
        <button 
          className="btn-upload" 
          onClick={handleUpload}
          disabled={!file || uploadStatus === 'loading'}
        >
          {uploadStatus === 'loading' ? 'Processing...' : 'Ingest to Database'}
        </button>
        
        {uploadMessage && (
          <div style={{ marginTop: '24px', fontSize: '14px', color: uploadStatus === 'error' ? '#ef4444' : '#10b981' }}>
            {uploadMessage}
          </div>
        )}
      </div>

      {/* RIGHT CHAT AREA */}
      <div className="glass-panel chat-container">
        
        <div className="chat-history">
          {messages.length === 0 ? (
            <div style={{ margin: 'auto', color: 'var(--text-secondary)', textAlign: 'center' }}>
              <h2>Upload a PDF and ask me anything.</h2>
            </div>
          ) : (
            messages.map((msg, i) => (
              <div key={i} className={`message ${msg.role}`}>
                <div className="msg-bubble">
                  {msg.content}
                </div>
                
                {/* Display Citations if it's an AI message */}
                {msg.role === 'ai' && msg.citations && msg.citations.length > 0 && (
                  <div className="citations-box">
                    <h4>Citations Found:</h4>
                    {msg.citations.map((cite, j) => (
                      <div key={j} style={{ marginBottom: '8px' }}>
                        <strong>File:</strong> {cite.filename} <br/>
                        <span style={{ fontStyle: 'italic' }}>"...{cite.text.substring(0, 100)}..."</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))
          )}
          {isSearching && (
            <div className="message ai">
              <div className="msg-bubble"><div className="spinner"></div></div>
            </div>
          )}
        </div>
        
        <form className="input-area" onSubmit={handleSearch}>
          <input 
            type="text" 
            placeholder="Ask a question about your documents..." 
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isSearching}
          />
          <button type="submit" className="btn-send" disabled={isSearching || !query.trim()}>
            {/* SVG Send Icon */}
            <svg viewBox="0 0 24 24">
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
            </svg>
          </button>
        </form>
        
      </div>
    </div>
  )
}

export default App
