"""LLM service using Groq API."""
import json
import asyncio
from typing import Dict, Optional
import httpx
from app.config import settings


class LLMService:
    """Service for interacting with Groq LLM API."""
    
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model = settings.GROQ_MODEL
        self.api_url = settings.GROQ_API_URL
        self.max_retries = settings.MAX_RETRIES
        self.timeout = settings.REQUEST_TIMEOUT
    
    def _extract_json(self, text: str) -> Dict:
        """Extract JSON from LLM response text."""
        # Try to find JSON in the response
        text = text.strip()
        
        # Remove markdown code blocks if present
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        text = text.strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to find JSON object in the text
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(text[start:end])
            raise
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate text using Groq API."""
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not set in environment variables")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        self.api_url,
                        headers=headers,
                        json=payload
                    )
                    response.raise_for_status()
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise Exception(f"Failed to generate after {self.max_retries} attempts: {str(e)}")
                await asyncio.sleep(1 * (attempt + 1))  # Exponential backoff
    
    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict:
        """Generate and parse JSON response from LLM."""
        response_text = await self.generate(prompt, system_prompt)
        return self._extract_json(response_text)

