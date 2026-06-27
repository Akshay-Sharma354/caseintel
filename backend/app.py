from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from backend.agents.orchestrator import Orchestrator
from backend.email_service import send_analysis_email

load_dotenv()

app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://caseintel-rho.vercel.app",
        "http://localhost:3000",
        "http://localhost:3001",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = Orchestrator()

class EmailRequest(BaseModel):
    email: str
    analysis: str
    document_type: str

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        document_type, agent_used, analysis = orchestrator.process_document(contents)
        
        return {
            "document_type": document_type,
            "agent_used": agent_used,
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/send-email")
async def send_email(request: EmailRequest):
    """Send analysis results via email"""
    try:
        result = send_analysis_email(request.email, request.analysis, request.document_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}
