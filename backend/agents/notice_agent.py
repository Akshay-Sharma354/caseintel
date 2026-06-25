"""
Legal Notice Processing Agent - Clean Format

WHY: Urgent deadlines stand out, actions are clear
"""

from backend.core.claude_client import chat
from backend.core.rag import LegalRAG

NOTICE_SYSTEM_PROMPT = """You are NoticeProcessor, a legal notice specialist.

Format your response EXACTLY like this:

## Notice Type
[What kind of notice this is]

## Critical Deadlines 🚨
- 🚨 URGENT (Due [DATE]): [What must be done]
- 🚨 URGENT (Due [DATE]): [What must be done]

## Required Actions
1. [Action 1 - most urgent first]
2. [Action 2]
3. [Action 3]

## Key Information Extracted
- Court/Issuing Authority: [Name]
- Case Number: [Number]
- Your Role: [Plaintiff/Defendant/Other]
- Service Method: [How notice was served]

## Default Risk Assessment
🔴 CRITICAL - Default judgment risk if deadline missed
🟡 HIGH - Consequences if not addressed
🟢 MEDIUM - Standard compliance requirement

## Recommendations
- [Immediate step 1]
- [Step 2 before deadline]
- [Step 3 for follow-up]
"""

class NoticeAgent:
    def __init__(self):
        self.system_prompt = NOTICE_SYSTEM_PROMPT
        self.rag = LegalRAG()
        self.rag.load_knowledge_base()
    
    def process_notice(self, notice_text: str) -> str:
        """Process legal notice and extract action items"""
        
        notice_knowledge = self.rag.retrieve_legal_terms("notice deadline")
        
        context = f"Legal notice standards:\n{notice_knowledge[0]}\n\n"
        full_prompt = context + f"Process this legal notice:\n\n{notice_text}"
        
        messages = [{"role": "user", "content": full_prompt}]
        response = chat(system_prompt=self.system_prompt, messages=messages)
        
        return response.content[0].text

if __name__ == "__main__":
    print("🧪 Testing Notice Agent...")
    
    agent = NoticeAgent()
    
    sample_notice = """
    COURT SUMMONS
    
    TO: John Smith
    CASE: Smith vs. Johnson Corp
    COURT: District Court
    DATE RECEIVED: January 20, 2024
    
    You are hereby summoned to appear in court on March 15, 2024
    at 10:00 AM to respond to the above-referenced case.
    
    Failure to appear may result in default judgment.
    Response deadline: February 15, 2024
    """
    
    result = agent.process_notice(sample_notice)
    print("\n✅ Notice Agent Works!")
    print(result)
