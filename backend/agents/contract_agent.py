"""
Contract Analysis Agent

WHY: Lawyers spend hours reading contracts manually
This agent reads contracts, identifies risks, and extracts key terms
"""

from backend.core.claude_client import chat
from backend.core.rag import LegalRAG

CONTRACT_SYSTEM_PROMPT = """You are ContractIntel, a specialized legal contract analyst.

Your job:
1. Analyze contracts thoroughly
2. Extract key sections: parties, terms, payment, liability, termination
3. Identify red flags (unlimited liability, missing terms, vague language)
4. Compare to standard templates
5. Calculate risk score (HIGH/MEDIUM/LOW)
6. Provide recommendations

Format your response with clear sections:
## Summary
## Parties & Key Terms
## Red Flags Identified
## Risk Assessment
## Recommendations
"""

class ContractAgent:
    def __init__(self):
        self.system_prompt = CONTRACT_SYSTEM_PROMPT
        self.rag = LegalRAG()
        self.rag.load_knowledge_base()
    
    def analyze_contract(self, contract_text: str) -> str:
        """Analyze a contract and return findings"""
        
        # Get contract knowledge from RAG
        contract_knowledge = self.rag.retrieve_contract_knowledge(contract_text)
        
        # Build prompt with RAG context
        context = f"Reference templates and standards:\n{contract_knowledge[0]}\n\n"
        full_prompt = context + f"Analyze this contract:\n\n{contract_text}"
        
        # Call Claude
        messages = [{"role": "user", "content": full_prompt}]
        response = chat(system_prompt=self.system_prompt, messages=messages)
        
        return response.content[0].text

if __name__ == "__main__":
    print("🧪 Testing Contract Agent...")
    
    agent = ContractAgent()
    
    sample_contract = """
    SERVICE AGREEMENT
    
    Parties: TechCorp Inc and ClientCo LLC
    
    Terms: 
    - Duration: 1 year
    - Services: Software development and support
    - Payment: $50,000 per month
    - Liability: Unlimited
    - No termination clause
    - Confidentiality: Not specified
    """
    
    result = agent.analyze_contract(sample_contract)
    print("\n✅ Contract Agent Works!")
    print(result[:300] + "...")
