import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
      setError(null);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('https://caseintel-u3yl.onrender.com/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to analyze document');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError('Error analyzing document: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const getDocumentIcon = () => {
    if (!file) return '📄';
    const name = file.name.toLowerCase();
    if (name.endsWith('.pdf')) return '📕';
    if (name.endsWith('.docx')) return '📗';
    if (name.endsWith('.txt')) return '📝';
    if (name.match(/\.(jpg|jpeg|png|gif)$/)) return '🖼️';
    return '📄';
  };

  const getAgentIcon = () => {
    if (!result) return null;
    const type = result.document_type?.toUpperCase() || '';
    if (type.includes('CONTRACT')) return '⚖️';
    if (type.includes('CASE')) return '🏛️';
    if (type.includes('COMPLIANCE')) return '✅';
    if (type.includes('NOTICE')) return '📋';
    return '🤖';
  };

  return (
    <div className="App">
      <div className="background-animation"></div>
      
      <div className="container">
        {/* Hero Section */}
        <div className="hero-section">
          <div className="hero-badge">AI-Powered Legal Analysis</div>
          <h1 className="hero-title">CaseIntel</h1>
          <p className="hero-subtitle">
            Professional legal document analysis powered by advanced AI. 
            Contract review, compliance checks, case management, and more.
          </p>
        </div>

        {/* Main Card */}
        <div className="main-card">
          {!result ? (
            <>
              {/* Upload Section */}
              <div className="upload-container">
                <div className="upload-header">
                  <h2>📤 Upload Your Document</h2>
                  <p className="upload-hint">Drag & drop or click to select</p>
                </div>

                <div
                  className={`upload-zone ${dragActive ? 'active' : ''} ${file ? 'has-file' : ''}`}
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                >
                  <input
                    type="file"
                    id="file-input"
                    onChange={handleFileChange}
                    accept=".txt,.pdf,.doc,.docx,.jpg,.jpeg,.png"
                    className="file-input"
                  />
                  <label htmlFor="file-input" className="upload-label">
                    <div className="upload-icon">
                      {file ? getDocumentIcon() : '📄'}
                    </div>
                    <div className="upload-text">
                      {file ? (
                        <>
                          <span className="file-selected">✓ File Selected</span>
                          <span className="file-name">{file.name}</span>
                        </>
                      ) : (
                        <>
                          <span className="upload-primary">Drag files here or click to browse</span>
                          <span className="upload-secondary">Supports: PDF, DOCX, TXT, Images</span>
                        </>
                      )}
                    </div>
                  </label>
                </div>

                {/* File Info */}
                {file && (
                  <div className="file-info">
                    <span className="file-info-item">
                      📋 {file.type || 'Document'}
                    </span>
                    <span className="file-info-item">
                      💾 {(file.size / 1024).toFixed(1)} KB
                    </span>
                  </div>
                )}

                {/* Error */}
                {error && <div className="error-message">❌ {error}</div>}

                {/* Analyze Button */}
                <button
                  onClick={handleAnalyze}
                  disabled={!file || loading}
                  className="analyze-button"
                >
                  {loading ? (
                    <>
                      <span className="spinner-small"></span>
                      Analyzing...
                    </>
                  ) : (
                    <>
                      🔍 Analyze Document
                    </>
                  )}
                </button>
              </div>

              {/* Features Grid */}
              <div className="features-grid">
                <div className="feature-item">
                  <span className="feature-icon">⚖️</span>
                  <span className="feature-name">Contract Analysis</span>
                </div>
                <div className="feature-item">
                  <span className="feature-icon">🏛️</span>
                  <span className="feature-name">Case Management</span>
                </div>
                <div className="feature-item">
                  <span className="feature-icon">✅</span>
                  <span className="feature-name">Compliance Check</span>
                </div>
                <div className="feature-item">
                  <span className="feature-icon">📋</span>
                  <span className="feature-name">Notice Analysis</span>
                </div>
              </div>
            </>
          ) : (
            <>
              {/* Results Section */}
              <div className="results-container">
                <div className="results-header">
                  <div className="results-title-section">
                    <span className="result-agent-icon">{getAgentIcon()}</span>
                    <div>
                      <h2>Analysis Complete</h2>
                      <p className="result-agent-type">{result.agent_used}</p>
                    </div>
                  </div>
                  <button 
                    className="new-analysis-btn"
                    onClick={() => {
                      setResult(null);
                      setFile(null);
                      setError(null);
                    }}
                  >
                    ➕ New Analysis
                  </button>
                </div>

                <div className="markdown-content analysis-result">
                  <ReactMarkdown>{result.analysis}</ReactMarkdown>
                </div>

                {/* Action Buttons */}
                <div className="result-actions">
                  <button 
                    className="action-btn copy-btn"
                    onClick={() => {
                      navigator.clipboard.writeText(result.analysis);
                      alert('Copied to clipboard!');
                    }}
                  >
                    📋 Copy Analysis
                  </button>
                  <button 
                    className="action-btn share-btn"
                    onClick={() => {
                      alert('Share feature coming soon! Use the copy button for now.');
                    }}
                  >
                    🔗 Share
                  </button>
                </div>
              </div>
            </>
          )}
        </div>

        {/* Footer */}
        <div className="footer">
          <p>CaseIntel © 2024 | AI-Powered Legal Analysis</p>
        </div>
      </div>
    </div>
  );
}

export default App;
