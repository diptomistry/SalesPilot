"""Email generation service."""
from typing import Dict
from app.models import Lead
from app.services.llm_service import LLMService
from app.utils.prompts import EMAIL_GENERATION_PROMPT


class EmailAgent:
    """Service for generating personalized emails."""
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
    
    async def generate_email(self, lead: Lead) -> Dict:
        """Generate personalized email for a lead."""
        prompt = EMAIL_GENERATION_PROMPT.format(
            name=lead.name or "there",
            company=lead.company or "your company",
            industry=lead.industry or "your industry",
            job_title=lead.job_title or "professional",
            persona=lead.persona or "Other",
            score=lead.score or 5,
            priority=lead.priority or "Medium"
        )
        
        try:
            result = await self.llm_service.generate_json(prompt)
            
            return {
                "subject": result.get("subject", "Partnership Opportunity"),
                "body": result.get("body", "Hello, I'd like to discuss a potential partnership opportunity.")
            }
        except Exception as e:
            # Fallback to default email
            return {
                "subject": f"Partnership Opportunity for {lead.company or 'Your Company'}",
                "body": f"Hello {lead.name or 'there'},\n\nI hope this email finds you well. I'd like to discuss a potential partnership opportunity that could benefit {lead.company or 'your company'}.\n\nBest regards,\nSales Team"
            }

