"""
Case Management Agent - Clean Format

WHY: Organized case information with clear tracking
"""

from backend.core.claude_client import chat
from backend.core.rag import LegalRAG

CASE_SYSTEM_PROMPT = """You are CaseOrganizer, a case management specialist.

Format your response EXACTLY like this:

## Case Overview
[Summary of the case]

## Parties Involved
- Plaintiff: [name]
- Defendant: [name]
- Attorneys: [names]

## Key Dates & Timeline ⏰
- 📅 Filed: [date]
- 📅 First Hearing: [date]
- 📅 Next Deadline: [date]
- 📅 Trial Date: [date if set]

## Case Status ✅
- Current Phase: [Discovery/Trial/Settlement/etc]
- Progress: [percentage or description]

## Claims & Causes
- ⚖️ [Claim 1]
- ⚖️ [Claim 2]

## Key Evidence & Documents
- 📄 [Document 1]
- 📄 [Document 2]

## Next Steps 👉
- [Action 1 with deadline]
- [Action 2 with deadline]
- [Action 3 with deadline]

## Risk Assessment
LOW / MEDIUM / HIGH / CRITICAL
"""

class CaseAgent:
    def __init__(self):
        self.system_prompt = CASE_SYSTEM_PROMPT
        self.rag = LegalRAG()
        self.rag.load_knowledge_base()
    
    def process_case(self, case_text: str) -> str:
        """Process case documents and organize information"""
        
        case_knowledge = self.rag.retrieve_legal_terms("case management")
        
        context = f"Case terminology and standards:\n{case_knowledge[0]}\n\n"
        full_prompt = context + f"Organize this case information:\n\n{case_text}"
        
        messages = [{"role": "user", "content": full_prompt}]
        response = chat(system_prompt=self.system_prompt, messages=messages)
        
        return response.content[0].text

if __name__ == "__main__":
    print("🧪 Testing Case Agent...")
    
    agent = CaseAgent()
    
    sample_case = """
    CASE FILE: Smith vs. Johnson Corp
    
    Plaintiff: John Smith
    Defendant: Johnson Corporation
    Attorney for Plaintiff: Sarah Williams, Esq.
    Filed: January 15, 2024
    Court: District Court, County XYZ
    Case Number: 2024-001234
    
    Claims: Product liability, negligence
    Hearing scheduled: March 20, 2024
    Status: Discovery phase
    """
    
    result = agent.process_case(sample_case)
    print("\n✅ Case Agent Works!")
    print(result)
