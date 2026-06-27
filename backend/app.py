from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from backend.agents.orchestrator import Orchestrator
from backend.email_service import send_analysis_email
from backend.core.claude_client import client
import fitz
import pdfplumber
from docx import Document
from PIL import Image
import io
import base64

load_dotenv()

app = FastAPI()

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

def extract_text_from_file(file_contents: bytes, filename: str) -> str:
    """Extract text from various file types"""
    
    try:
        # DOCX files
        if filename.lower().endswith('.docx'):
            doc = Document(io.BytesIO(file_contents))
            text = '\n'.join([para.text for para in doc.paragraphs])
            return text
        
        # TXT files
        elif filename.lower().endswith('.txt'):
            return file_contents.decode('utf-8', errors='ignore')
        
        # PDF files (try text extraction first)
        elif filename.lower().endswith('.pdf'):
            try:
                with pdfplumber.open(io.BytesIO(file_contents)) as pdf:
                    text = ''
                    for page in pdf.pages:
                        text += page.extract_text() + '\n'
                    if text.strip():
                        return text
            except:
                pass
            
            # If text extraction failed, try Vision API for scanned PDF
            doc = fitz.open(stream=file_contents, filetype="pdf")
            pix = doc[0].get_pixmap()
            png_bytes = pix.tobytes("png")
            png_b64 = base64.standard_b64encode(png_bytes).decode('utf-8')
            
            response = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=4000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": png_b64
                                }
                            },
                            {
                                "type": "text",
                                "text": "Extract all text from this image. Return ONLY the extracted text, no commentary."
                            }
                        ]
                    }
                ]
            )
            return response.content[0].text
        
        # Image files (JPG, PNG)
        elif filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            img = Image.open(io.BytesIO(file_contents))
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            png_b64 = base64.standard_b64encode(img_bytes.getvalue()).decode('utf-8')
            
            response = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=4000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": png_b64
                                }
                            },
                            {
                                "type": "text",
                                "text": "Extract all text from this image. Return ONLY the extracted text, no commentary."
                            }
                        ]
                    }
                ]
            )
            return response.content[0].text
        
        else:
            raise ValueError(f"Unsupported file type: {filename}")
    
    except Exception as e:
        raise ValueError(f"Failed to extract text: {str(e)}")

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        
        # Extract text from file
        document_text = extract_text_from_file(contents, file.filename)
        
        # Send extracted text to orchestrator
        result = orchestrator.process_document(document_text)
        
        return result
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
