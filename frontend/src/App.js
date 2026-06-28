import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import Results from './Results';
import './App.css';

function Home() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
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
      navigate('/results', { state: { result: data } });
    } catch (err) {
      setError('Error analyzing document: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <nav className="navbar">
        <div className="nav-container">
          <div className="nav-logo">
            <span className="logo-icon">⚖️</span>
            <span className="logo-text">CaseIntel</span>
          </div>
          <p className="nav-tagline">AI-powered legal document analysis</p>
        </div>
      </nav>

      <div className="main-content">
        <div className="content-container">
          <div className="hero">
            <h1 className="hero-title">Upload your legal documents</h1>
            <p className="hero-subtitle">
              Get professional analysis in seconds. Contract review, compliance checks, case management, and more.
            </p>
          </div>

          <div className="upload-card">
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
                <div className="upload-content">
                  {file ? (
                    <>
                      <div className="upload-icon-success">✓</div>
                      <p className="upload-text-success">{file.name}</p>
                      <p className="upload-size">{(file.size / 1024).toFixed(1)} KB</p>
                    </>
                  ) : (
                    <>
                      <div className="upload-icon">📄</div>
                      <p className="upload-text">Drag and drop your file here</p>
                      <p className="upload-hint">or click to browse</p>
                      <p className="upload-formats">PDF, DOCX, TXT, or images</p>
                    </>
                  )}
                </div>
              </label>
            </div>

            {error && <div className="error-message">{error}</div>}

            <button
              onClick={handleAnalyze}
              disabled={!file || loading}
              className="analyze-button"
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Analyzing...
                </>
              ) : (
                <>
                  <span className="button-icon">↑</span>
                  Analyze Document
                </>
              )}
            </button>
          </div>

          <div className="features">
            <div className="feature">
              <span className="feature-icon">⚖️</span>
              <span className="feature-label">Contracts</span>
            </div>
            <div className="feature">
              <span className="feature-icon">🏛️</span>
              <span className="feature-label">Cases</span>
            </div>
            <div className="feature">
              <span className="feature-icon">✅</span>
              <span className="feature-label">Compliance</span>
            </div>
            <div className="feature">
              <span className="feature-icon">📋</span>
              <span className="feature-label">Notices</span>
            </div>
          </div>
        </div>
      </div>

      <footer className="footer">
        <p>© 2026 CaseIntel. AI-powered legal analysis.</p>
      </footer>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/results" element={<Results />} />
      </Routes>
    </Router>
  );
}

export default App;
