🚨 ESLINT ERROR!
nextSteps is extracted but never used!

🔧 FIX: Remove unused variable
bashcat > ~/Desktop/caseintel/frontend/src/Results.js << 'EOF'
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
          <button className="back-button" onClick={() => window.history.back()}>
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

  // Extract key sections from markdown analysis
  const extractSection = (text, sectionName) => {
    const patterns = [
      new RegExp(`#{1,3}\\s*${sectionName}[^#]*?(?=#{1,3}\\s|$)`, 'is'),
      new RegExp(`\\*\\*${sectionName}\\*\\*[^#]*?(?=#{1,3}\\s|\\*\\*|$)`, 'is'),
    ];

    for (let pattern of patterns) {
      const match = text.match(pattern);
      if (match) {
        return match[0]
          .replace(new RegExp(`#{1,3}\\s*${sectionName}`, 'i'), '')
          .replace(/\*\*.*?\*\*/g, '')
          .trim();
      }
    }
    return null;
  };

  const toggleSection = (sectionKey) => {
    setExpandedSections(prev => ({
      ...prev,
      [sectionKey]: !prev[sectionKey]
    }));
  };

  const KeySection = ({ title, icon, content, sectionKey }) => {
    const isExpanded = expandedSections[sectionKey];
    
    if (!content) return null;

    return (
      <div className="results-card key-section-card">
        <button
          className="section-toggle"
          onClick={() => toggleSection(sectionKey)}
        >
          <span className="toggle-icon">{isExpanded ? '▼' : '▶'}</span>
          <span className="section-title">{icon} {title}</span>
        </button>
        
        {isExpanded && (
          <div className="section-content">
            <div className="markdown-content">
              <ReactMarkdown>{content}</ReactMarkdown>
            </div>
          </div>
        )}
      </div>
    );
  };

  // Extract all key sections
  const analysis = result.analysis || '';
  const criticalIssues = extractSection(analysis, 'Critical Issues');
  const recommendations = extractSection(analysis, 'Recommendations');
  const potentialOutcomes = extractSection(analysis, 'Potential Outcomes');
  const litigationRisk = extractSection(analysis, 'Litigation Risk');
  const settlement = extractSection(analysis, 'Settlement');

  return (
    <div className="results-page">
      <div className="results-header-bar">
        <button className="back-button" onClick={() => window.history.back()}>
          ← Back to Upload
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
          
          {/* Legal Disclaimer */}
          <div className="results-card disclaimer-card">
            <div style={{
              background: '#ffe0e0',
              padding: '12px',
              borderRadius: '6px',
              fontSize: '12px',
              color: '#991b1b',
              lineHeight: '1.5'
            }}>
              <strong>⚠️ Legal Disclaimer:</strong> This analysis is for educational purposes only and based on US legal standards. This is NOT legal advice. Please consult a qualified attorney in your jurisdiction before making any legal decisions.
            </div>
          </div>

          {/* Key Sections - Expandable */}
          <KeySection 
            title="Critical Issues" 
            icon="🚨" 
            content={criticalIssues}
            sectionKey="criticalIssues"
          />

          <KeySection 
            title="Potential Outcomes" 
            icon="📊" 
            content={potentialOutcomes}
            sectionKey="potentialOutcomes"
          />

          <KeySection 
            title="Recommendations" 
            icon="✅" 
            content={recommendations}
            sectionKey="recommendations"
          />

          <KeySection 
            title="Litigation & Settlement Strategy" 
            icon="⚖️" 
            content={settlement || litigationRisk}
            sectionKey="settlement"
          />

          {/* Full Analysis */}
          <div className="results-card analysis-card">
            <button
              className="section-toggle"
              onClick={() => toggleSection('fullAnalysis')}
            >
              <span className="toggle-icon">{expandedSections.fullAnalysis ? '▼' : '▶'}</span>
              <span className="section-title">📋 Full Detailed Analysis</span>
            </button>
            
            {expandedSections.fullAnalysis && (
              <div className="section-content">
                <div className="markdown-content">
                  <ReactMarkdown>{result.analysis}</ReactMarkdown>
                </div>
              </div>
            )}
          </div>

          {/* Share & Copy Actions */}
          <div className="results-card actions-card">
            <h2 className="card-title">🔗 Share & Export</h2>
            <div className="result-actions">
              <button
                className="action-button"
                onClick={() => {
                  navigator.clipboard.writeText(result.analysis);
                  alert('Analysis copied to clipboard!');
                }}
              >
                📋 Copy Analysis
              </button>
              <button
                className="action-button secondary"
                onClick={() => {
                  const email = prompt('Enter email address to send analysis:');
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
                        alert('Email sent successfully!');
                      } else {
                        alert('Failed to send email');
                      }
                    })
                    .catch(err => alert('Error sending email'));
                  }
                }}
              >
                📧 Share via Email
              </button>
            </div>
          </div>

        </div>
      </div>

      <footer className="results-footer">
        <p>© 2026 CaseIntel. AI-powered legal analysis.</p>
      </footer>
    </div>
  );
}

export default Results;
