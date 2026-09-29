from openai import AsyncOpenAI, OpenAI
from src.config import settings
from src.models.chat import Companion, Message
from src.models.user import User
from typing import List

class LLMService:
    def __init__(self):
        self.openai_client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url
        )
        self.deepseek_client = OpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url
        ) if settings.deepseek_api_key else None
    
    async def generate_response(
        self,
        companion: Companion,
        user: User,
        history: List[Message],
        user_message: str
    ) -> str:
        """
        Generate response using multiple LLM backends.
        Tries: DeepSeek → OpenAI → Fallback message
        """
        
        # Build system prompt with personality
        system_prompt = f"""{companion.personality_prompt}

User Information:
- Name: {user.full_name or user.username}
- Preferences: {user.preferences or {}}

Maintain the character personality at all times. Respond naturally and engagingly.
"""
        
        # Build conversation history
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add recent history (last 10 messages)
        for msg in history[-10:]:
            messages.append({
                "role": msg.role.value,
                "content": msg.content
            })
        
        # Try DeepSeek first (uncensored)
        if self.deepseek_client:
            try:
                response = self.deepseek_client.chat.completions.create(
                    model="deepseek-chat",
                    messages=messages,
                    temperature=0.8,
                    max_tokens=1024
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"DeepSeek error: {e}")
        
        # Fallback to OpenAI
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.8,
                max_tokens=1024
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI error: {e}")
        
        # Ultimate fallback
        return f"Desculpa, tive um problema técnico. Tenta denovo em alguns segundos."
