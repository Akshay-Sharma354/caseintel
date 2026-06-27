from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from backend.agents.orchestrator import Orchestrator
import python_docx
from pdf2image import convert_from_bytes
from PIL import Image
import io
import pdfplumber
from backend.core.claude_client import client

load_dotenv()

app = FastAPI(title="CaseIntel API")

# Add CORS middleware
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

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "CaseIntel backend is running!"}

@app.get("/agents")
def get_agents():
    return {
        "agents": [
            "Contract Agent",
            "Case Agent",
            "Compliance Agent",
            "Notice Agent"
        ]
    }

def extract_text_from_docx(file_content: bytes) -> str:
    try:
        doc = python_docx.Document(io.BytesIO(file_content))
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        print(f"ERROR extracting DOCX: {str(e)}")
        raise

def extract_text_from_pdf(file_content: bytes) -> tuple:
    try:
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        
        is_scanned = len(text.strip()) < 100
        
        return text if not is_scanned else "", is_scanned
    except Exception as e:
        print(f"ERROR extracting PDF text: {str(e)}")
        return "", True

def extract_text_from_image(file_content: bytes) -> str:
    try:
        import base64
        
        base64_image = base64.standard_b64encode(file_content).decode("utf-8")
        
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": base64_image,
                            },
                        },
                        {
                            "type": "text",
                            "text": "Extract all text from this image/document. Return only the text content."
                        }
                    ],
                }
            ],
        )
        
        return response.content[0].text
    except Exception as e:
        print(f"ERROR extracting image text: {str(e)}")
        raise

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        file_name = file.filename.lower()
        
        print(f"DEBUG: Received file: {file.filename}")
        print(f"DEBUG: File type: {file_name}")
        
        document_text = ""
        
        if file_name.endswith('.docx'):
            print("DEBUG: Processing DOCX file")
            document_text = extract_text_from_docx(file_content)
            print(f"DEBUG: Extracted text length: {len(document_text)}")
        
        elif file_name.endswith('.pdf'):
            print("DEBUG: Processing PDF file")
            text, is_scanned = extract_text_from_pdf(file_content)
            
            if is_scanned:
                print("DEBUG: Detected scanned PDF")
                document_text = extract_text_from_image(file_content)
            else:
                print("DEBUG: Detected text-based PDF")
                document_text = text
            
            print(f"DEBUG: Extracted text length: {len(document_text)}")
        
        elif file_name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            print("DEBUG: Processing image file")
            document_text = extract_text_from_image(file_content)
            print(f"DEBUG: Extracted text length: {len(document_text)}")
        
        elif file_name.endswith('.txt'):
            print("DEBUG: Processing TXT file")
            document_text = file_content.decode('utf-8')
            print(f"DEBUG: Extracted text length: {len(document_text)}")
        
        else:
            return JSONResponse(
                status_code=400,
                content={"error": f"Unsupported file type: {file_name}"}
            )
        
        print("DEBUG: Sending to orchestrator")
        result = orchestrator.process_document(document_text)
        
        return {
            "status": "success",
            "document_type": result["document_type"],
            "agent_used": result["agent_used"],
            "analysis": result["analysis"]
        }
    
    except Exception as e:
        print(f"ERROR TRACEBACK:")
        import traceback
        traceback.print_exc()
        
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "type": type(e).__name__}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
@app.post("/send-email")
async def send_email(email: str, analysis: str, document_type: str):
    """Send analysis results via email"""
    from backend.email_service import send_analysis_email
    
    result = send_analysis_email(email, analysis, document_type)
    return result
