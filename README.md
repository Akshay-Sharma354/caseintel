# CaseIntel — AI-Powered Legal Document Analysis

CaseIntel is a full-stack AI application that analyzes legal documents using specialized LLM agents. Upload a contract, case summary, compliance audit, or legal notice — get expert-level analysis in seconds.

## Problem

Legal professionals use ChatGPT for document analysis and get generic summaries. A contract analysis doesn't understand litigation strategy. A compliance review doesn't quantify penalty exposure. One-size-fits-all AI fails for specialized domains.

## Solution

**Multi-Agent Orchestration**

CaseIntel routes documents to specialist agents based on type:
- **ContractAgent** — Identifies liability gaps, payment terms, IP risks, with dollar impact
- **CaseAgent** — Calculates litigation probability, settlement range, expected value
- **ComplianceAgent** — Quantifies penalty exposure, regulatory deadlines, remediation costs
- **NoticeAgent** — Assesses legal threats, litigation risk, settlement strategy

**Result:** Actionable legal strategy, not summaries. Built for small law firms.

## Architecture

Document Upload (Frontend)

↓

Orchestrator (Claude Haiku) — Fast classification

↓

Route to Specialist Agent (Claude Opus) — Deep expertise

↓

Structured Analysis with Recommendations

↓

Results Page (Expandable sections, copy/share)

## Tech Stack

**Backend:** Python, FastAPI, Uvicorn
**AI:** Claude API (Haiku for classification, Opus for analysis)
**Frontend:** React, React Router, ReactMarkdown, Custom CSS
**Deployment:** Vercel (Frontend), Render (Backend), GitHub (Version control)
**File Processing:** pdfplumber, python-docx, PIL, PyMuPDF
**Email:** SendGrid API

## Live Demo

🔴 **Frontend (Live):** https://caseintel-rho.vercel.app/
🔴 **Backend (Live):** https://caseintel-u3yl.onrender.com/health

## Features

✅ Multi-agent document analysis
✅ Real-time document classification
✅ Expandable result sections (Critical Issues, Potential Outcomes, Recommendations)
✅ Email sharing via SendGrid
✅ Copy-to-clipboard analysis
✅ Support for .txt, .docx, .pdf files
✅ US jurisdiction-focused legal analysis

## Results Example

**Input:** Commercial software license agreement

**Output:**
- **Critical Issues:** Unequal liability caps ($500K vs. Unlimited), one-sided indemnification
- **Potential Outcomes:** 
  - Best case: Renegotiate liability terms (20% probability)
  - Realistic: Accept with reservations (60% probability)
  - Worst case: Walk away from deal (20% probability)
- **Recommendations:**
  1. Cap Licensor liability at $2M minimum
  2. Reduce indemnification scope
  3. Limit annual price increases to 10%
- **Financial Impact:** Changes could save $1M+ over 5-year term

## Project Status

| Phase | Status | Features |
|-------|--------|----------|
| Phase 1 | ✅ Complete | 4 agents, orchestrator, RAG mock |
| Phase 2 | ✅ Complete | FastAPI backend, React frontend, email sharing |
| Phase 3 | 🔄 In Progress | Vision API for scanned PDFs, expandable sections |
| Phase 4 | 📋 Planned | Multi-jurisdiction support, advanced UI, auth |

## Getting Started

### Backend
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

Visit http://localhost:3000

## Key Learnings

- **Pydantic v2 breaks ChromaDB** → Implemented mock RAG
- **Specialized agents > generic AI** → ContractAgent finds risks ChatGPT misses
- **Jurisdiction matters in legal AI** → US-focused for v1, multi-jurisdiction roadmap
- **Quantified results win deals** → "Expected value: $37K" > "you might win"

## Next Steps

- [ ] Multi-jurisdiction support (India, UK, EU)
- [ ] Vision API for scanned documents
- [ ] User authentication (Supabase)
- [ ] Practice management API integrations
- [ ] Advanced analytics dashboard

## Contact

**GitHub:** https://github.com/Akshay-Sharma354/caseintel
**Demo:** https://caseintel-rho.vercel.app/

Built by **Arjun Sharma** — AI Engineer, Delhi
