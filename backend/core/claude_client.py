"""
Claude API Client for CaseIntel

WHY: Wrapper around Claude API for legal reasoning
- Claude is excellent at contracts and legal analysis
- Better reasoning than other models for complex documents
- Consistent interface for agents to use
"""

import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("❌ ANTHROPIC_API_KEY not found in .env!")

client = anthropic.Anthropic(api_key=api_key)

def chat(system_prompt: str, messages: list, tools: list = None):
    """
    Call Claude API
    
    Args:
        system_prompt: Instructions for Claude
        messages: List of messages [{"role": "user", "content": "..."}, ...]
        tools: Optional tools (for later)
    
    Returns:
        Claude response object
    """
    
    params = {
        "model": "claude-opus-4-6",
        "max_tokens": 1024,
        "system": system_prompt,
        "messages": messages,
    }
    
    if tools:
        params["tools"] = tools
    
    try:
        response = client.messages.create(**params)
        return response
    except Exception as e:
        print(f"❌ Claude Error: {e}")
        raise

if __name__ == "__main__":
    print("🧪 Testing Claude API...")
    try:
        response = chat(
            system_prompt="You are a helpful legal assistant.",
            messages=[{"role": "user", "content": "What is a non-compete agreement?"}]
        )
        print("\n✅ Claude API Works!")
        print(f"Response: {response.content[0].text[:200]}...")
    except Exception as e:
        print(f"❌ Error: {e}")
