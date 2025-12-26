"""Persona assignment and lead enrichment service."""
from typing import Dict
from app.models import Lead
from app.services.llm_service import LLMService
from app.utils.prompts import LEAD_ENRICHMENT_PROMPT


class PersonaAgent:
    """Service for enriching leads and assigning personas."""
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
    
    def _map_persona_from_title(self, job_title: str) -> str:
        """Map job title to persona using deterministic rules."""
        if not job_title:
            return "Other"
        
        title_lower = job_title.lower()
        
        # Decision Makers
        if any(title in title_lower for title in ["ceo", "founder", "president", "owner", "co-founder"]):
            return "Decision Maker"
        
        # Technical Buyers
        if any(title in title_lower for title in ["cto", "chief technology", "engineering manager", 
                                                   "engineering director", "vp engineering", "technical director"]):
            return "Technical Buyer"
        
        # Financial Decision Makers
        if any(title in title_lower for title in ["cfo", "chief financial", "finance director", "vp finance"]):
            return "Financial Decision Maker"
        
        # Marketing/Sales Influencers
        if any(title in title_lower for title in ["marketing director", "marketing manager", "cmo", 
                                                   "chief marketing", "sales director", "sales manager", 
                                                   "vp sales", "vp marketing"]):
            return "Influencer"
        
        # Operations
        if any(title in title_lower for title in ["operations manager", "operations director", "coo", 
                                                   "chief operations", "vp operations", "general manager"]):
            return "Operations Manager"
        
        # HR
        if any(title in title_lower for title in ["hr director", "hr manager", "human resources", 
                                                   "chief people", "people operations"]):
            return "HR Director"
        
        # Product
        if any(title in title_lower for title in ["product manager", "product director", "cpo", 
                                                   "chief product", "vp product"]):
            return "Product Manager"
        
        # Directors (generic)
        if "director" in title_lower:
            return "Director"
        
        # Managers (generic)
        if "manager" in title_lower:
            return "Manager"
        
        # Partners
        if "partner" in title_lower:
            return "Partner"
        
        return "Other"
    
    async def enrich_lead(self, lead: Lead) -> Dict:
        """Enrich lead data and assign persona."""
        # First, try deterministic mapping
        persona = self._map_persona_from_title(lead.job_title or "")
        
        # Use LLM to enrich missing fields and refine persona if needed
        prompt = LEAD_ENRICHMENT_PROMPT.format(
            name=lead.name or "Unknown",
            email=lead.email or "Unknown",
            company=lead.company or "Unknown",
            industry=lead.industry or "Unknown",
            job_title=lead.job_title or "Unknown",
            suggested_persona=persona
        )
        
        try:
            result = await self.llm_service.generate_json(prompt)
            
            # Use LLM's industry and job_title if they're better
            enriched_industry = result.get("industry") or lead.industry
            enriched_job_title = result.get("job_title") or lead.job_title
            
            # Use LLM persona if it's more specific, otherwise use our mapping
            llm_persona = result.get("persona", "Other")
            if llm_persona != "Other" and persona == "Other":
                final_persona = llm_persona
            elif persona != "Other":
                final_persona = persona
            else:
                final_persona = llm_persona
            
            return {
                "industry": enriched_industry or "Unknown",
                "job_title": enriched_job_title or "Unknown",
                "persona": final_persona,
                "reasoning": result.get("reasoning", f"Mapped from title: {persona}")
            }
        except Exception as e:
            # Fallback to deterministic mapping
            return {
                "industry": lead.industry or "Unknown",
                "job_title": lead.job_title or "Unknown",
                "persona": persona,
                "reasoning": f"Deterministic mapping applied. Error: {str(e)}"
            }

