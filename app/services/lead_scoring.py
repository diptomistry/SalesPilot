"""Lead scoring service."""
from typing import Dict
from app.models import Lead, Priority
from app.services.llm_service import LLMService
from app.utils.prompts import LEAD_SCORING_PROMPT


class LeadScoringService:
    """Service for scoring leads using LLM."""
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
    
    async def score_lead(self, lead: Lead) -> Dict:
        """Score a lead and assign priority."""
        prompt = LEAD_SCORING_PROMPT.format(
            name=lead.name or "Unknown",
            email=lead.email or "Unknown",
            company=lead.company or "Unknown",
            industry=lead.industry or "Unknown",
            job_title=lead.job_title or "Unknown",
            status=lead.status or "Unknown"
        )
        
        try:
            result = await self.llm_service.generate_json(prompt)
            
            score = int(result.get("score", 5))
            priority_str = result.get("priority", "Medium")
            
            # Validate and normalize priority
            priority_map = {
                "high": Priority.HIGH,
                "medium": Priority.MEDIUM,
                "low": Priority.LOW
            }
            priority = priority_map.get(priority_str.lower(), Priority.MEDIUM)
            
            return {
                "score": max(1, min(10, score)),  # Clamp between 1-10
                "priority": priority,
                "reasoning": result.get("reasoning", "")
            }
        except Exception as e:
            # Fallback to default values
            return {
                "score": 5,
                "priority": Priority.MEDIUM,
                "reasoning": f"Error in scoring: {str(e)}"
            }

