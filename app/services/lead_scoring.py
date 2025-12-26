"""Lead scoring service."""
from typing import Dict
from app.models import Lead, Priority
from app.services.llm_service import LLMService
from app.utils.prompts import LEAD_SCORING_PROMPT


class LeadScoringService:
    """Service for scoring leads using rule-based logic and LLM enhancement."""
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
    
    def _calculate_base_score(self, lead: Lead) -> int:
        """Calculate base score using rule-based logic."""
        score = 5  # Base score
        
        job_title = (lead.job_title or "").lower()
        industry = (lead.industry or "").lower()
        company = (lead.company or "").strip()
        
        # Job title scoring (decision-making authority)
        if any(title in job_title for title in ["ceo", "founder", "president", "owner"]):
            score += 3
        elif any(title in job_title for title in ["cto", "cfo", "coo", "vp", "vice president"]):
            score += 2
        elif any(title in job_title for title in ["director", "head of", "chief"]):
            score += 1
        elif any(title in job_title for title in ["manager", "lead"]):
            score += 0
        else:
            score -= 1  # Unknown or lower-level roles
        
        # Industry scoring (high-value industries)
        high_value_industries = ["technology", "finance", "healthcare", "pharmaceutical", "aerospace"]
        if any(ind in industry for ind in high_value_industries):
            score += 1
        
        # Company presence (having a company name is better)
        if company and company != "Unknown":
            score += 1
        
        # Status scoring
        if lead.status and "active" in (lead.status or "").lower():
            score += 1
        
        return max(1, min(10, score))
    
    def _derive_priority(self, score: int) -> Priority:
        """Derive priority from score."""
        if score >= 8:
            return Priority.HIGH
        elif score >= 5:
            return Priority.MEDIUM
        else:
            return Priority.LOW
    
    async def score_lead(self, lead: Lead) -> Dict:
        """Score a lead using rule-based logic with LLM refinement."""
        # Calculate base score using rules
        base_score = self._calculate_base_score(lead)
        
        # Use LLM to refine the score based on context
        prompt = LEAD_SCORING_PROMPT.format(
            name=lead.name or "Unknown",
            email=lead.email or "Unknown",
            company=lead.company or "Unknown",
            industry=lead.industry or "Unknown",
            job_title=lead.job_title or "Unknown",
            status=lead.status or "Unknown",
            base_score=base_score
        )
        
        try:
            result = await self.llm_service.generate_json(prompt)
            
            # Get LLM score, but use base_score as fallback
            llm_score = result.get("score")
            if llm_score is not None:
                try:
                    llm_score = int(llm_score)
                    # Blend base score (70%) with LLM score (30%) for stability
                    final_score = int(base_score * 0.7 + llm_score * 0.3)
                except (ValueError, TypeError):
                    final_score = base_score
            else:
                final_score = base_score
            
            final_score = max(1, min(10, final_score))
            
            # Derive priority from score (not from LLM)
            priority = self._derive_priority(final_score)
            
            return {
                "score": final_score,
                "priority": priority,
                "reasoning": result.get("reasoning", f"Base score: {base_score}, Refined: {final_score}")
            }
        except Exception as e:
            # Fallback to rule-based scoring
            priority = self._derive_priority(base_score)
            return {
                "score": base_score,
                "priority": priority,
                "reasoning": f"Rule-based scoring applied. Error: {str(e)}"
            }

