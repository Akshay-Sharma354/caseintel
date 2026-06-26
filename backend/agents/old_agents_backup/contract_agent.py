"""
Contract Analysis Agent - IMPROVED FORMAT

WHY: Clean, scannable results with checkmarks and red flags
"""

from backend.core.claude_client import chat
from backend.core.rag import LegalRAG

CONTRACT_SYSTEM_PROMPT = """You are ContractIntel, a contract analysis specialist.

IMPORTANT: Format your response EXACTLY like this:

## Contract Summary
[2-3 sentence summary]

## Key Parties
- Party 1: [name]
- Party 2: [name]

## Positive Aspects ✅
- ✅ [Good thing found]
- ✅ [Good thing found]

## Critical Issues 🚨
- 🚨 [CRITICAL issue and why it matters]
- 🚨 [CRITICAL issue and why it matters]

## Major Issues ⚠️
- ⚠️ [Issue and explanation]
- ⚠️ [Issue and explanation]

## Missing Clauses ❌
- ❌ Termination Clause
- ❌ Confidentiality
- ❌ [Others if missing]

## Risk Score
CRITICAL / HIGH / MEDIUM / LOW

## Key Recommendations
- [Action 1]
- [Action 2]
- [Action 3]
"""

class ContractAgent:
    def __init__(self):
        self.system_prompt = CONTRACT_SYSTEM_PROMPT
        self.rag = LegalRAG()
        self.rag.load_knowledge_base()
    
    def analyze_contract(self, contract_text: str) -> str:
        """Analyze a contract and return clean findings"""
        
        contract_knowledge = self.rag.retrieve_contract_knowledge(contract_text)
        
        context = f"Reference templates and standards:\n{contract_knowledge[0]}\n\n"
        full_prompt = context + f"Analyze this contract:\n\n{contract_text}"
        
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
    print(result)
