from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import mimetypes
import fitz
import pdfplumber
from PIL import Image
import io
import base64
from docx import Document
from backend.agents.orchestrator import Orchestrator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = Orchestrator()

def image_to_base64(image: Image.Image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.standard_b64encode(buffer.read()).decode()

def extract_text_from_docx(file_bytes: bytes) -> str:
    try:
        doc = Document(io.BytesIO(file_bytes))
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text if text.strip() else "ERROR: No text found in DOCX file"
    except Exception as e:
        return f"ERROR: Failed to extract text from DOCX: {str(e)}"

def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        text = ""
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text if text.strip() else None
    except Exception as e:
        return None

def is_scanned_pdf(file_bytes: bytes) -> bool:
    text = extract_text_from_pdf(file_bytes)
    return text is None or len(text.strip()) < 50

def extract_image_from_pdf_pymupdf(file_bytes: bytes, page_num: int = 0) -> Image.Image:
    try:
        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
        page = pdf_document[page_num]
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        return img
    except Exception as e:
        raise Exception(f"Failed to extract image from PDF: {str(e)}")

def analyze_with_vision(image_base64: str, document_type: str) -> dict:
    from backend.core.claude_client import client
    
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_base64,
                        },
                    },
                    {
                        "type": "text",
                        "text": f"Analyze this {document_type} document as a legal expert."
                    }
                ],
            }
        ],
    )
    
    return response.content[0].text

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    try:
        print(f"DEBUG: Received file: {file.filename}")
        file_bytes = await file.read()
        file_name = file.filename.lower()
        print(f"DEBUG: File type: {file_name}")
        
        if file_name.endswith('.docx'):
            print("DEBUG: Processing DOCX file")
            document_text = extract_text_from_docx(file_bytes)
            
            if document_text.startswith("ERROR"):
                print(f"DEBUG: DOCX extraction error: {document_text}")
                return JSONResponse({
                    "error": document_text,
                    "agent_used": "Error Handler"
                }, status_code=400)
            
            print(f"DEBUG: Extracted text length: {len(document_text)}")
            result = orchestrator.process_document(document_text)
            print(f"DEBUG: Orchestrator result: {result}")
            return {
                "document_type": "DOCX",
                "agent_used": result.get("agent_type", "Unknown"),
                "analysis": result.get("analysis", "No analysis available")
            }
        
        elif file_name.endswith('.pdf'):
            print("DEBUG: Processing PDF file")
            if is_scanned_pdf(file_bytes):
                print("DEBUG: Detected scanned PDF")
                try:
                    image = extract_image_from_pdf_pymupdf(file_bytes)
                    image_base64 = image_to_base64(image)
                    analysis = analyze_with_vision(image_base64, "PDF")
                    
                    return {
                        "document_type": "PDF (Scanned)",
                        "agent_used": "Claude Vision API",
                        "analysis": analysis
                    }
                except Exception as e:
                    print(f"DEBUG: Vision API error: {str(e)}")
                    return JSONResponse({
                        "error": f"Failed to analyze scanned PDF: {str(e)}",
                        "agent_used": "Error Handler"
                    }, status_code=400)
            else:
                print("DEBUG: Detected text PDF")
                document_text = extract_text_from_pdf(file_bytes)
                result = orchestrator.process_document(document_text)
                
                return {
                    "document_type": "PDF (Text)",
                    "agent_used": result.get("agent_type", "Unknown"),
                    "analysis": result.get("analysis", "No analysis available")
                }
        
        elif file_name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            print("DEBUG: Processing image file")
            try:
                image = Image.open(io.BytesIO(file_bytes))
                image_base64 = image_to_base64(image)
                analysis = analyze_with_vision(image_base64, "Image")
                
                return {
                    "document_type": "Image",
                    "agent_used": "Claude Vision API",
                    "analysis": analysis
                }
            except Exception as e:
                print(f"DEBUG: Image processing error: {str(e)}")
                return JSONResponse({
                    "error": f"Failed to analyze image: {str(e)}",
                    "agent_used": "Error Handler"
                }, status_code=400)
        
        elif file_name.endswith('.txt'):
            print("DEBUG: Processing TXT file")
            try:
                document_text = file_bytes.decode('utf-8')
                result = orchestrator.process_document(document_text)
                
                return {
                    "document_type": "TXT",
                    "agent_used": result.get("agent_type", "Unknown"),
                    "analysis": result.get("analysis", "No analysis available")
                }
            except Exception as e:
                print(f"DEBUG: TXT processing error: {str(e)}")
                return JSONResponse({
                    "error": f"Failed to read TXT file: {str(e)}",
                    "agent_used": "Error Handler"
                }, status_code=400)
        
        else:
            return JSONResponse({
                "error": f"Unsupported file type: {file_name}. Supported: PDF, DOCX, TXT, JPG, PNG",
                "agent_used": "Error Handler"
            }, status_code=400)
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"ERROR TRACEBACK:\n{error_trace}")
        return JSONResponse({
            "error": f"Unexpected error: {str(e)}",
            "agent_used": "Error Handler"
        }, status_code=500)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "CaseIntel Backend"}

@app.get("/agents")
def get_agents():
    return {
        "agents": [
            {"name": "Contract Agent", "icon": "⚖️", "description": "Analyzes contracts and agreements"},
            {"name": "Case Agent", "icon": "🏛️", "description": "Manages litigation and case information"},
            {"name": "Compliance Agent", "icon": "✅", "description": "Checks regulatory compliance"},
            {"name": "Notice Agent", "icon": "📋", "description": "Analyzes legal notices and demands"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
