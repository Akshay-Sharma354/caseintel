"""
CaseIntel FastAPI Backend

WHY: Exposes agents via REST API
- Frontend sends documents
- Backend processes with agents
- Returns analysis as JSON
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from backend.agents.orchestrator import Orchestrator

# Initialize FastAPI app
app = FastAPI(
    title="CaseIntel API",
    description="Multi-agent legal AI system",
    version="1.0.0"
)

# Enable CORS (allow frontend to call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = Orchestrator()

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "CaseIntel API is running!",
        "version": "1.0.0"
    }

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    """Analyze a legal document"""
    
    try:
        content = await file.read()
        document_text = content.decode("utf-8")
        
        result = orchestrator.process_document(document_text)
        
        return {
            "status": "success",
            "document_type": result["document_type"],
            "agent_used": result["agent_used"],
            "analysis": result["analysis"]
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error processing document: {str(e)}"
        )

@app.get("/agents")
def get_available_agents():
    """Get list of available agents"""
    return {
        "agents": [
            {
                "name": "Contract Agent",
                "type": "CONTRACT",
                "description": "Analyzes contracts and identifies risks"
            },
            {
                "name": "Case Agent",
                "type": "CASE",
                "description": "Organizes case information and timelines"
            },
            {
                "name": "Compliance Agent",
                "type": "COMPLIANCE",
                "description": "Checks regulatory compliance"
            },
            {
                "name": "Notice Agent",
                "type": "NOTICE",
                "description": "Processes legal notices and deadlines"
            }
        ]
    }

@app.get("/health")
def health_check():
    """Health check for monitoring"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
