import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [showEmailModal, setShowEmailModal] = useState(false);
  const [emailInput, setEmailInput] = useState('');
  const [emailLoading, setEmailLoading] = useState(false);
  const [emailError, setEmailError] = useState(null);
  const [emailSuccess, setEmailSuccess] = useState(false);
  const [copyFeedback, setCopyFeedback] = useState(false);

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

  const handleCopy = () => {
    navigator.clipboard.writeText(result.analysis);
    setCopyFeedback(true);
    setTimeout(() => setCopyFeedback(false), 1500);
  };

  const handleSendEmail = async () => {
    if (!emailInput.trim()) {
      setEmailError('Please enter an email address');
      return;
    }
    setEmailLoading(true);
    setEmailError(null);
    setEmailSuccess(false);
    try {
      const response = await fetch('https://caseintel-u3yl.onrender.com/send-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: emailInput,
          analysis: result.analysis,
          document_type: result.document_type,
        }),
      });
      if (!response.ok) {
        throw new Error('Failed to send email');
      }
      const data = await response.json();
      if (data.success) {
        setEmailSuccess(true);
        setEmailInput('');
        setTimeout(() => {
          setShowEmailModal(false);
          setEmailSuccess(false);
        }, 2000);
      } else {
        setEmailError('Failed to send email: ' + data.error);
      }
    } catch (err) {
      setEmailError('Error sending email: ' + err.message);
    } finally {
      setEmailLoading(false);
    }
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
          {!result ? (
            <>
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
            </>
          ) : (
            <>
              <div className="results-header">
                <button
                  className="back-button"
                  onClick={() => {
                    setResult(null);
                    setFile(null);
                  }}
                >
                  ← Back
                </button>
                <div className="result-title">
                  <span className="result-icon">{getAgentIcon()}</span>
                  <div>
                    <h2>Analysis Complete</h2>
                    <p className="result-agent">{result.agent_used}</p>
                  </div>
                </div>
              </div>

              <div className="results-card">
                <div className="markdown-content">
                  <ReactMarkdown>{result.analysis}</ReactMarkdown>
                </div>

                <div className="result-actions">
                  <button
                    className="action-button"
                    onClick={handleCopy}
                    style={{ position: 'relative' }}
                  >
                    {copyFeedback && <span className="copy-feedback">✓ Copied!</span>}
                    Copy
                  </button>
                  <button
                    className="action-button secondary"
                    onClick={() => setShowEmailModal(true)}
                  >
                    📧 Share via Email
                  </button>
                </div>
              </div>

              {showEmailModal && (
                <div className="email-modal-overlay" onClick={() => setShowEmailModal(false)}>
                  <div className="email-modal" onClick={(e) => e.stopPropagation()}>
                    <h3>Share Analysis via Email</h3>
                    {emailSuccess ? (
                      <div className="email-success">✅ Email sent successfully!</div>
                    ) : (
                      <>
                        <input
                          type="email"
                          placeholder="Enter email address"
                          value={emailInput}
                          onChange={(e) => setEmailInput(e.target.value)}
                          className="email-input"
                        />
                        {emailError && <div className="email-error">{emailError}</div>}
                        <div className="email-modal-actions">
                          <button
                            className="email-send-button"
                            onClick={handleSendEmail}
                            disabled={emailLoading}
                          >
                            {emailLoading ? 'Sending...' : 'Send Email'}
                          </button>
                          <button
                            className="email-cancel-button"
                            onClick={() => setShowEmailModal(false)}
                          >
                            Cancel
                          </button>
                        </div>
                      </>
                    )}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>

      <footer className="footer">
        <p>© 2026 CaseIntel. AI-powered legal analysis.</p>
      </footer>
    </div>
  );
}

export default App;
