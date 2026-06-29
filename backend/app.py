from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from backend.agents.orchestrator import Orchestrator
from backend.email_service import send_analysis_email

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = Orchestrator()

class EmailRequest(BaseModel):
    email: str
    analysis: str
    document_type: str

def extract_text_from_file(file_contents: bytes, filename: str) -> str:
    try:
        if filename.lower().endswith('.txt'):
            return file_contents.decode('utf-8', errors='ignore')
        else:
            raise ValueError(f"Unsupported: {filename}")
    except Exception as e:
        raise ValueError(f"Extract failed: {str(e)}")

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        print(f">>> File: {file.filename}")
        contents = await file.read()
        print(f">>> Size: {len(contents)} bytes")
        
        text = extract_text_from_file(contents, file.filename)
        print(f">>> Extracted: {len(text)} chars")
        
        result = orchestrator.process_document(text)
        print(f">>> SUCCESS")
        
        return result
    except Exception as e:
        print(f">>> ERROR: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/send-email")
async def send_email(request: EmailRequest):
    try:
        result = send_analysis_email(request.email, request.analysis, request.document_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}
