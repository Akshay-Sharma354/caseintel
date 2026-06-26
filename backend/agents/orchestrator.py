from backend.agents.contract_agent import ContractAgent
from backend.agents.case_agent import CaseAgent
from backend.agents.compliance_agent import ComplianceAgent
from backend.agents.notice_agent import NoticeAgent
from backend.core.claude_client import client

class Orchestrator:
    def __init__(self):
        self.contract_agent = ContractAgent()
        self.case_agent = CaseAgent()
        self.compliance_agent = ComplianceAgent()
        self.notice_agent = NoticeAgent()

    def classify_document(self, text: str) -> str:
        """Classify document type using Claude Haiku (FAST!)"""
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=50,
            system="You are a legal document classifier. Respond with ONLY one of these exact words: CONTRACT, CASE, COMPLIANCE, or NOTICE. No other text.",
            messages=[
                {
                    "role": "user",
                    "content": f"Classify this document:\n\n{text[:500]}"
                }
            ]
        )
        
        classification = response.content[0].text.strip().upper()
        print(f"DEBUG: Classified as {classification}")
        
        if classification not in ["CONTRACT", "CASE", "COMPLIANCE", "NOTICE"]:
            return "CONTRACT"
        
        return classification

    def process_document(self, document_text: str) -> dict:
        """Route document to appropriate agent based on classification"""
        
        document_type = self.classify_document(document_text)
        print(f"DEBUG: Document type: {document_type}")
        
        try:
            if document_type == "CONTRACT":
                analysis = self.contract_agent.analyze_contract(document_text)
                agent_used = "Contract Agent"
            elif document_type == "CASE":
                analysis = self.case_agent.analyze_case(document_text)
                agent_used = "Case Agent"
            elif document_type == "COMPLIANCE":
                analysis = self.compliance_agent.analyze_compliance(document_text)
                agent_used = "Compliance Agent"
            elif document_type == "NOTICE":
                analysis = self.notice_agent.analyze_notice(document_text)
                agent_used = "Notice Agent"
            else:
                analysis = self.contract_agent.analyze_contract(document_text)
                agent_used = "Contract Agent (default)"
            
            return {
                "document_type": document_type,
                "agent_used": agent_used,
                "analysis": analysis
            }
        
        except Exception as e:
            print(f"ERROR: {str(e)}")
            raise
