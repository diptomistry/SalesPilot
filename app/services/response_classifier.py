"""Response classification service."""
import random
from typing import Dict
from app.models import Lead, ResponseStatus
from app.services.llm_service import LLMService
from app.utils.prompts import RESPONSE_CLASSIFICATION_PROMPT


class ResponseClassifier:
    """Service for classifying email responses."""
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
    
    def _calculate_base_response(self, lead: Lead) -> ResponseStatus:
        """Calculate base response status using score and persona."""
        score = lead.score or 5
        
        # High scores are more likely to be interested
        if score >= 8:
            # 60% Interested, 30% Follow Up, 10% Not Interested
            rand = random.random()
            if rand < 0.6:
                return ResponseStatus.INTERESTED
            elif rand < 0.9:
                return ResponseStatus.FOLLOW_UP
            else:
                return ResponseStatus.NOT_INTERESTED
        elif score >= 5:
            # Medium scores: 20% Interested, 50% Follow Up, 30% Not Interested
            rand = random.random()
            if rand < 0.2:
                return ResponseStatus.INTERESTED
            elif rand < 0.7:
                return ResponseStatus.FOLLOW_UP
            else:
                return ResponseStatus.NOT_INTERESTED
        else:
            # Low scores: 10% Interested, 40% Follow Up, 50% Not Interested
            rand = random.random()
            if rand < 0.1:
                return ResponseStatus.INTERESTED
            elif rand < 0.5:
                return ResponseStatus.FOLLOW_UP
            else:
                return ResponseStatus.NOT_INTERESTED
    
    async def classify_response(self, lead: Lead) -> Dict:
        """Classify the likely response status for a lead."""
        # Calculate base response using probabilistic logic
        base_response = self._calculate_base_response(lead)
        
        # Use LLM to refine based on context
        prompt = RESPONSE_CLASSIFICATION_PROMPT.format(
            name=lead.name or "Unknown",
            company=lead.company or "Unknown",
            industry=lead.industry or "Unknown",
            job_title=lead.job_title or "Unknown",
            persona=lead.persona or "Other",
            score=lead.score or 5,
            priority=lead.priority or "Medium",
            email_subject=lead.email_subject or "Partnership Opportunity",
            base_response=base_response.value
        )
        
        try:
            result = await self.llm_service.generate_json(prompt)
            
            status_str = result.get("response_status", base_response.value)
            
            # Map to enum
            status_map = {
                "interested": ResponseStatus.INTERESTED,
                "not interested": ResponseStatus.NOT_INTERESTED,
                "not_interested": ResponseStatus.NOT_INTERESTED,
                "follow up": ResponseStatus.FOLLOW_UP,
                "follow-up": ResponseStatus.FOLLOW_UP,
                "followup": ResponseStatus.FOLLOW_UP
            }
            
            response_status = status_map.get(status_str.lower(), base_response)
            
            return {
                "response_status": response_status,
                "reasoning": result.get("reasoning", f"Base: {base_response.value}, Refined: {response_status.value}")
            }
        except Exception as e:
            # Fallback to probabilistic logic
            return {
                "response_status": base_response,
                "reasoning": f"Probabilistic classification applied. Error: {str(e)}"
            }

