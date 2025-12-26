"""Email generation service."""
from typing import Dict
from app.models import Lead, Priority
from app.services.llm_service import LLMService
from app.utils.prompts import EMAIL_GENERATION_PROMPT


class EmailAgent:
    """Service for generating personalized emails."""
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
    
    async def generate_email(self, lead: Lead) -> Dict:
        """Generate personalized email for a lead."""
        # Determine urgency and tone based on priority
        is_high_priority = lead.priority == Priority.HIGH if lead.priority else False
        
        prompt = EMAIL_GENERATION_PROMPT.format(
            name=lead.name or "there",
            company=lead.company or "your company",
            industry=lead.industry or "your industry",
            job_title=lead.job_title or "professional",
            persona=lead.persona or "Other",
            score=lead.score or 5,
            priority=lead.priority or "Medium",
            is_high_priority=is_high_priority
        )
        
        try:
            result = await self.llm_service.generate_json(prompt)
            
            subject = result.get("subject", "Partnership Opportunity")
            body = result.get("body", "Hello, I'd like to discuss a potential partnership opportunity.")
            
            # Add urgency indicators for high priority leads
            if is_high_priority and not any(word in subject.lower() for word in ["urgent", "priority", "important"]):
                # Don't modify if already has urgency, but ensure professional tone
                pass
            
            return {
                "subject": subject,
                "body": body
            }
        except Exception as e:
            # Fallback to default email with priority-aware messaging
            if is_high_priority:
                subject = f"High-Priority Partnership Opportunity for {lead.company or 'Your Company'}"
                body = f"Hello {lead.name or 'there'},\n\nI hope this email finds you well. Given your role as {lead.job_title or 'a key decision maker'}, I believe there's a significant partnership opportunity that could benefit {lead.company or 'your company'}.\n\nI'd appreciate the opportunity to discuss this further at your earliest convenience.\n\nBest regards,\nSales Team"
            else:
                subject = f"Partnership Opportunity for {lead.company or 'Your Company'}"
                body = f"Hello {lead.name or 'there'},\n\nI hope this email finds you well. I'd like to discuss a potential partnership opportunity that could benefit {lead.company or 'your company'}.\n\nBest regards,\nSales Team"
            
            return {
                "subject": subject,
                "body": body
            }

