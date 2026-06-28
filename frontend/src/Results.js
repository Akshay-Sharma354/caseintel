import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import './Results.css';

function Results() {
  const location = useLocation();
  const result = location.state?.result;
  const [expandedSections, setExpandedSections] = useState({});

  if (!result) {
    return (
      <div className="results-container">
        <div className="results-content">
          <h2>No Analysis Found</h2>
          <p>Please upload a document and analyze it first.</p>
          <button className="back-button" onClick={() => 
window.history.back()}>
            Back to Upload
          </button>
        </div>
      </div>
    );
  }

  const getAgentIcon = () => {
    const type = result.document_type?.toUpperCase() || '';
    if (type.includes('CONTRACT')) return '⚖️';
    if (type.includes('CASE')) return '🏛️';
    if (type.includes('COMPLIANCE')) return '✅';
    if (type.includes('NOTICE')) return '📋';
    return '🤖';
  };

  const toggleSection = (sectionKey) => {
    setExpandedSections(prev => ({
      ...prev,
      [sectionKey]: !prev[sectionKey]
    }));
  };

  return (
    <div className="results-page">
      <div className="results-header-bar">
        <button className="back-button" onClick={() => 
window.history.back()}>
          Back to Upload
        </button>
        <div className="results-title-section">
          <span className="result-icon">{getAgentIcon()}</span>
          <div>
            <h1>Legal Analysis Results</h1>
            <p className="agent-label">{result.agent_used}</p>
          </div>
        </div>
      </div>

      <div className="results-main">
        <div className="results-content">
          
          <div className="results-card disclaimer-card">
            <div style={{
              background: '#ffe0e0',
              padding: '12px',
              borderRadius: '6px',
              fontSize: '12px',
              color: '#991b1b',
              lineHeight: '1.5'
            }}>
              <strong>Legal Disclaimer:</strong> This analysis is for 
educational purposes only and based on US legal standards. This is NOT 
legal advice. Please consult a qualified attorney in your jurisdiction 
before making any legal decisions.
            </div>
          </div>

          <div className="results-card analysis-card">
            <button
              className="section-toggle"
              onClick={() => toggleSection('fullAnalysis')}
            >
              <span className="toggle-icon">{expandedSections.fullAnalysis 
? 'v' : '>'}</span>
              <span className="section-title">Full Analysis</span>
            </button>
            
            {expandedSections.fullAnalysis && (
              <div className="section-content">
                <div className="markdown-content">
                  <ReactMarkdown>{result.analysis}</ReactMarkdown>
                </div>
              </div>
            )}
          </div>

          <div className="results-card actions-card">
            <h2 className="card-title">Share & Export</h2>
            <div className="result-actions">
              <button
                className="action-button"
                onClick={() => {
                  navigator.clipboard.writeText(result.analysis);
                  alert('Analysis copied!');
                }}
              >
                Copy Analysis
              </button>
              <button
                className="action-button secondary"
                onClick={() => {
                  const email = prompt('Enter email:');
                  if (email) {
                    
fetch('https://caseintel-u3yl.onrender.com/send-email', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({
                        email: email,
                        analysis: result.analysis,
                        document_type: result.document_type,
                      }),
                    })
                    .then(res => res.json())
                    .then(data => {
                      if (data.success) {
                        alert('Email sent!');
                      } else {
                        alert('Failed');
                      }
                    })
                    .catch(err => alert('Error'));
                  }
                }}
              >
                Share via Email
              </button>
            </div>
          </div>

        </div>
      </div>

      <footer className="results-footer">
        <p>2026 CaseIntel</p>
      </footer>
    </div>
  );
}

export default Results;
