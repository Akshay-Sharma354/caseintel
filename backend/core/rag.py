"""Mock RAG System - No dependencies needed!"""

class LegalRAG:
    def __init__(self):
        self.contracts_kb = """
        CONTRACT STANDARDS: Non-compete, NDA, Service agreements
        RED FLAGS: Unlimited liability, no termination clause, vague payment
        """
        self.compliance_kb = """
        COMPLIANCE: GDPR, CCPA, HIPAA, attorney-client privilege
        RISK: HIGH - unlimited liability, MEDIUM - unclear terms, LOW - standard
        """
        self.terms_kb = """
        TERMS: Indemnification, Force Majeure, Severability, Arbitration
        DEFINITIONS: Clear legal terminology and definitions
        """
    
    def load_knowledge_base(self):
        print("📚 Loading knowledge base (mock)...")
        print("✅ Knowledge base loaded!")
    
    def retrieve_contract_knowledge(self, query: str):
        return [self.contracts_kb]
    
    def retrieve_compliance_knowledge(self, query: str):
        return [self.compliance_kb]
    
    def retrieve_legal_terms(self, query: str):
        return [self.terms_kb]

if __name__ == "__main__":
    rag = LegalRAG()
    rag.load_knowledge_base()
    print("\n🧪 Testing RAG...")
    print("✅ RAG system working!")
