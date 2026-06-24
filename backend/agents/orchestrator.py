"""
Orchestrator - Main Router for CaseIntel

WHY: Different documents need different agents
- A contract needs Contract Agent
- A case file needs Case Agent
- A compliance doc needs Compliance Agent
- A court notice needs Notice Agent

Orchestrator analyzes the document and routes it!
"""

from backend.agents.contract_agent import ContractAgent
from backend.agents.case_agent import CaseAgent
from backend.agents.compliance_agent import ComplianceAgent
from backend.agents.notice_agent import NoticeAgent
from backend.core.claude_client import chat

ORCHESTRATOR_PROMPT = """You are the CaseIntel Document Router.

Analyze the document type and respond with ONLY one of these:
CONTRACT
CASE
COMPLIANCE
NOTICE

Be concise - just the category name."""

class Orchestrator:
    def __init__(self):
        self.contract_agent = ContractAgent()
        self.case_agent = CaseAgent()
        self.compliance_agent = ComplianceAgent()
        self.notice_agent = NoticeAgent()
    
    def identify_document_type(self, document_text: str) -> str:
        """Identify which type of document this is"""
        
        messages = [{"role": "user", "content": document_text[:500]}]
        response = chat(
            system_prompt=ORCHESTRATOR_PROMPT,
            messages=messages
        )
        
        doc_type = response.content[0].text.strip().upper()
        return doc_type
    
    def process_document(self, document_text: str) -> dict:
        """Process document with appropriate agent"""
        
        # Identify document type
        doc_type = self.identify_document_type(document_text)
        
        # Route to appropriate agent
        if "CONTRACT" in doc_type:
            analysis = self.contract_agent.analyze_contract(document_text)
            agent_used = "Contract Agent"
        
        elif "CASE" in doc_type:
            analysis = self.case_agent.process_case(document_text)
            agent_used = "Case Agent"
        
        elif "COMPLIANCE" in doc_type:
            analysis = self.compliance_agent.check_compliance(document_text)
            agent_used = "Compliance Agent"
        
        elif "NOTICE" in doc_type:
            analysis = self.notice_agent.process_notice(document_text)
            agent_used = "Notice Agent"
        
        else:
            analysis = "Unable to classify document"
            agent_used = "None"
        
        return {
            "document_type": doc_type,
            "agent_used": agent_used,
            "analysis": analysis
        }


if __name__ == "__main__":
    print("🧪 Testing Orchestrator...")
    
    orchestrator = Orchestrator()
    
    # Test with a contract
    test_contract = """
    SERVICE AGREEMENT
    Parties: TechCorp Inc and ClientCo LLC
    Terms: 1 year, $50,000/month
    Liability: Unlimited
    """
    
    result = orchestrator.process_document(test_contract)
    
    print(f"\n📄 Document Type: {result['document_type']}")
    print(f"🤖 Agent Used: {result['agent_used']}")
    print(f"✅ Orchestrator Works!")
    print(f"Analysis: {result['analysis'][:200]}...")
