"""Response classification service."""
from typing import Dict
from app.models import Lead, ResponseStatus
from app.services.llm_service import LLMService
from app.utils.prompts import RESPONSE_CLASSIFICATION_PROMPT


class ResponseClassifier:
    """Service for classifying email responses."""
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
    
    async def classify_response(self, lead: Lead) -> Dict:
        """Classify the likely response status for a lead."""
        prompt = RESPONSE_CLASSIFICATION_PROMPT.format(
            name=lead.name or "Unknown",
            company=lead.company or "Unknown",
            industry=lead.industry or "Unknown",
            job_title=lead.job_title or "Unknown",
            persona=lead.persona or "Other",
            score=lead.score or 5,
            priority=lead.priority or "Medium",
            email_subject=lead.email_subject or "Partnership Opportunity"
        )
        
        try:
            result = await self.llm_service.generate_json(prompt)
            
            status_str = result.get("response_status", "Follow Up")
            
            # Map to enum
            status_map = {
                "interested": ResponseStatus.INTERESTED,
                "not interested": ResponseStatus.NOT_INTERESTED,
                "follow up": ResponseStatus.FOLLOW_UP,
                "follow-up": ResponseStatus.FOLLOW_UP
            }
            
            response_status = status_map.get(status_str.lower(), ResponseStatus.FOLLOW_UP)
            
            return {
                "response_status": response_status,
                "reasoning": result.get("reasoning", "")
            }
        except Exception as e:
            # Fallback based on score
            if lead.score and lead.score >= 8:
                status = ResponseStatus.INTERESTED
            elif lead.score and lead.score <= 3:
                status = ResponseStatus.NOT_INTERESTED
            else:
                status = ResponseStatus.FOLLOW_UP
            
            return {
                "response_status": status,
                "reasoning": f"Error in classification: {str(e)}"
            }

