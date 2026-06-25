import React, { useState } from 'react';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to analyze document');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>CaseIntel</h1>
        <p>Multi-Agent Legal AI System</p>
      </header>

      <div className="container">
        <div className="upload-section">
          <h2>Upload Legal Document</h2>
          <input
            type="file"
            onChange={handleFileChange}
            accept=".txt,.pdf,.doc,.docx"
          />
          <button onClick={handleUpload} disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze Document'}
          </button>
        </div>

        {error && <div className="error">{error}</div>}

        {result && (
          <div className="results-section">
            <h2>Analysis Results</h2>
            <div className="result-card">
              <h3>Document Type</h3>
              <p className="highlight">{result.document_type}</p>
            </div>
            <div className="result-card">
              <h3>Agent Used</h3>
              <p className="highlight">{result.agent_used}</p>
            </div>
            <div className="result-card">
              <h3>Analysis</h3>
              <p>{result.analysis}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;