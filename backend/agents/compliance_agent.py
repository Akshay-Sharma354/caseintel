"""
Compliance Checking Agent

WHY: Legal teams need to ensure documents meet regulatory requirements
This agent checks compliance and flags violations
"""

from backend.core.claude_client import chat
from backend.core.rag import LegalRAG

COMPLIANCE_SYSTEM_PROMPT = """You are ComplianceChecker, a regulatory compliance specialist.

Your job:
1. Check documents against regulations (GDPR, CCPA, HIPAA, etc.)
2. Identify compliance violations
3. Flag missing required disclosures
4. Check for proper confidentiality handling
5. Assess compliance risk level
6. Provide remediation steps

Format your response:
## Applicable Regulations
## Compliance Status
## Violations Found
## Risk Level (HIGH/MEDIUM/LOW)
## Required Actions
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
    print(result[:300] + "...")
