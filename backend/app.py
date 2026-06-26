from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import io
import base64
import pdfplumber
from pdf2image import convert_from_bytes
from docx import Document
from PIL import Image
from backend.agents.orchestrator import Orchestrator
from backend.core.claude_client import client
import os
os.environ['PATH'] = '/opt/homebrew/bin:' + os.environ.get('PATH', '')
app = FastAPI(
    title="CaseIntel API",
    description="Multi-agent legal AI system with Vision support",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = Orchestrator()

def image_to_base64(image_obj) -> str:
    img_bytes = io.BytesIO()
    image_obj.save(img_bytes, format='JPEG', quality=85)
    img_bytes.seek(0)
    return base64.standard_b64encode(img_bytes.getvalue()).decode('utf-8')

def analyze_with_vision(image_base64: str) -> str:
    system_prompt = """You are ContractIntel analyzing a legal document.
Format with: ## Summary, ## Key Parties, ## Critical Issues, ## Missing Clauses, ## Risk Score"""
    
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2048,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_base64
                        }
                    },
                    {
                        "type": "text",
                        "text": "Analyze this document completely."
                    }
                ]
            }
        ]
    )
    
    return response.content[0].text

def extract_text_from_pdf(content: bytes) -> str:
    try:
        document_text = ""
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    document_text += extracted + "\n"
        return document_text if document_text.strip() else None
    except:
        return None

def is_scanned_pdf(content: bytes) -> bool:
    text = extract_text_from_pdf(content)
    return text is None or len(text.strip()) < 50

@app.get("/")
def read_root():
    return {"status": "CaseIntel API running!", "version": "2.0.0", "vision_support": True}

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    try:
        content = await file.read()
        filename = file.filename.lower()
        document_text = None
        image_base64 = None
        
        if filename.endswith('.pdf'):
            if is_scanned_pdf(content):
                print("📸 Scanned PDF detected!")
                images = convert_from_bytes(content, first_page=1, last_page=1)
                if images:
                    image_base64 = image_to_base64(images[0])
            else:
                print("📄 Text PDF detected!")
                document_text = extract_text_from_pdf(content)
        
        elif filename.endswith('.docx'):
            doc = Document(io.BytesIO(content))
            document_text = "\n".join([p.text for p in doc.paragraphs])
        
        elif filename.endswith('.txt'):
            document_text = content.decode("utf-8")
        
        elif filename.endswith(('.jpg', '.jpeg', '.png')):
            print("🖼️ Image detected!")
            image = Image.open(io.BytesIO(content))
            image_base64 = image_to_base64(image)
        
        else:
            raise ValueError("Unsupported file type")
        
        if image_base64:
            analysis = analyze_with_vision(image_base64)
            return {
                "status": "success",
                "method": "vision",
                "document_type": "Legal Document (Vision)",
                "agent_used": "Claude Vision API",
                "analysis": analysis
            }
        
        if document_text and document_text.strip():
            result = orchestrator.process_document(document_text)
            return {
                "status": "success",
                "method": "text",
                "document_type": result["document_type"],
                "agent_used": result["agent_used"],
                "analysis": result["analysis"]
            }
        
        raise ValueError("No content extracted")
    
    except Exception as e:
        print(f"🔴 ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

@app.get("/agents")
def get_available_agents():
    return {
        "agents": [
            {"name": "Contract Agent", "type": "CONTRACT", "description": "Analyzes contracts"},
            {"name": "Case Agent", "type": "CASE", "description": "Organizes cases"},
            {"name": "Compliance Agent", "type": "COMPLIANCE", "description": "Checks compliance"},
            {"name": "Notice Agent", "type": "NOTICE", "description": "Processes notices"}
        ],
        "vision_support": "✅ Scanned PDFs & Images"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "vision_support": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
