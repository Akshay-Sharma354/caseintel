"""
Compliance Checking Agent - Clean Format

WHY: Clear compliance status with what's good and what needs fixing
"""

from backend.core.claude_client import chat
from backend.core.rag import LegalRAG

COMPLIANCE_SYSTEM_PROMPT = """You are ComplianceChecker, a regulatory compliance specialist.

Format your response EXACTLY like this:

## Document Analysis
[Brief description of document type]

## Compliant Areas ✅
- ✅ [Regulation met and how]
- ✅ [Regulation met and how]

## Compliance Violations 🚨
- 🚨 **[Regulation name]**: [What's wrong and why it matters]
- 🚨 **[Regulation name]**: [What's wrong and why it matters]

## Missing Disclosures ❌
- ❌ GDPR Privacy Notice (EU users)
- ❌ CCPA Data Processing Agreement (CA users)
- ❌ [Others if applicable]

## Risk Assessment
LOW / MEDIUM / HIGH / CRITICAL

## Required Actions (Priority Order)
- 🔴 URGENT: [Action and deadline]
- 🟡 HIGH: [Action and deadline]
- 🟢 MEDIUM: [Action and deadline]

## Recommended Compliance Framework
[What regulations apply and what needs to be done]
"""

class ComplianceAgent:
    def __init__(self):
        self.system_prompt = COMPLIANCE_SYSTEM_PROMPT
        self.rag = LegalRAG()
        self.rag.load_knowledge_base()
    
    def check_compliance(self, document_text: str) -> str:
        """Check document for compliance violations"""
        
        compliance_knowledge = self.rag.retrieve_compliance_knowledge(document_text)
        
        context = f"Compliance rules and standards:\n{compliance_knowledge[0]}\n\n"
        full_prompt = context + f"Check this document for compliance:\n\n{document_text}"
        
        messages = [{"role": "user", "content": full_prompt}]
        response = chat(system_prompt=self.system_prompt, messages=messages)
        
        return response.content[0].text

if __name__ == "__main__":
    print("🧪 Testing Compliance Agent...")
    
    agent = ComplianceAgent()
    
    sample_doc = """
    CUSTOMER DATA PROCESSING AGREEMENT
    
    We collect and store customer data including:
    - Names and emails
    - Phone numbers
    - Purchase history
    - Payment information
    
    Data is stored in our servers in California.
    We do not provide GDPR or CCPA disclosures.
    """
    
    result = agent.check_compliance(sample_doc)
    print("\n✅ Compliance Agent Works!")
    print(result)
