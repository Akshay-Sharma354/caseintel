"""
Legal Notice Processing Agent

WHY: Courts send notices with tight deadlines that must not be missed
This agent categorizes notices and flags urgent deadlines
"""

from backend.core.claude_client import chat
from backend.core.rag import LegalRAG

NOTICE_SYSTEM_PROMPT = """You are NoticeProcessor, a legal notice specialist.

Your job:
1. Categorize the notice type (summons, motion, discovery request, etc.)
2. Extract critical deadlines
3. Identify what actions are required
4. Flag urgency level
5. Summarize key requirements
6. Highlight any default risks

Format your response:
## Notice Type
## Critical Deadlines
## Required Actions
## Urgency Level (URGENT/NORMAL/LOW)
## Risk of Default if Not Addressed
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
    print(result[:300] + "...")
