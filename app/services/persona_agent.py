"""Persona assignment and lead enrichment service."""
from typing import Dict
from app.models import Lead
from app.services.llm_service import LLMService
from app.utils.prompts import LEAD_ENRICHMENT_PROMPT


class PersonaAgent:
    """Service for enriching leads and assigning personas."""
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
    
    async def enrich_lead(self, lead: Lead) -> Dict:
        """Enrich lead data and assign persona."""
        prompt = LEAD_ENRICHMENT_PROMPT.format(
            name=lead.name or "Unknown",
            email=lead.email or "Unknown",
            company=lead.company or "Unknown",
            industry=lead.industry or "Unknown",
            job_title=lead.job_title or "Unknown"
        )
        
        try:
            result = await self.llm_service.generate_json(prompt)
            
            return {
                "industry": result.get("industry", lead.industry),
                "job_title": result.get("job_title", lead.job_title),
                "persona": result.get("persona", "Other"),
                "reasoning": result.get("reasoning", "")
            }
        except Exception as e:
            # Fallback to default values
            return {
                "industry": lead.industry or "Unknown",
                "job_title": lead.job_title or "Unknown",
                "persona": "Other",
                "reasoning": f"Error in enrichment: {str(e)}"
            }

