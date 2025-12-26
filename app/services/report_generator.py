"""Campaign summary report generator."""
import os
from typing import List, Dict
from app.models import Lead, CampaignSummary, Priority, ResponseStatus
from app.services.llm_service import LLMService
from app.utils.prompts import CAMPAIGN_SUMMARY_PROMPT


class ReportGenerator:
    """Service for generating campaign summary reports."""
    
    def __init__(self, llm_service: LLMService, reports_dir: str):
        self.llm_service = llm_service
        self.reports_dir = reports_dir
        self._ensure_directory()
    
    def _ensure_directory(self):
        """Ensure reports directory exists."""
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def _calculate_statistics(self, leads: List[Lead]) -> Dict:
        """Calculate campaign statistics."""
        total = len(leads)
        high_priority = sum(1 for lead in leads if lead.priority == Priority.HIGH)
        medium_priority = sum(1 for lead in leads if lead.priority == Priority.MEDIUM)
        low_priority = sum(1 for lead in leads if lead.priority == Priority.LOW)
        
        scores = [lead.score for lead in leads if lead.score]
        average_score = sum(scores) / len(scores) if scores else 0.0
        
        # Persona distribution
        persona_dist = {}
        for lead in leads:
            if lead.persona:
                persona_dist[lead.persona] = persona_dist.get(lead.persona, 0) + 1
        
        # Response breakdown
        response_dist = {
            ResponseStatus.INTERESTED: 0,
            ResponseStatus.NOT_INTERESTED: 0,
            ResponseStatus.FOLLOW_UP: 0,
            ResponseStatus.PENDING: 0
        }
        for lead in leads:
            if lead.response_status:
                response_dist[lead.response_status] = response_dist.get(lead.response_status, 0) + 1
        
        return {
            "total": total,
            "high_priority": high_priority,
            "medium_priority": medium_priority,
            "low_priority": low_priority,
            "average_score": average_score,
            "persona_distribution": persona_dist,
            "response_breakdown": {k.value: v for k, v in response_dist.items()}
        }
    
    async def generate_report(self, leads: List[Lead]) -> str:
        """Generate campaign summary report."""
        stats = self._calculate_statistics(leads)
        
        # Generate AI summary
        prompt = CAMPAIGN_SUMMARY_PROMPT.format(
            total_leads=stats["total"],
            high_priority=stats["high_priority"],
            medium_priority=stats["medium_priority"],
            low_priority=stats["low_priority"],
            average_score=f"{stats['average_score']:.2f}",
            persona_distribution=stats["persona_distribution"],
            response_breakdown=stats["response_breakdown"]
        )
        
        try:
            ai_summary = await self.llm_service.generate(prompt)
        except Exception as e:
            ai_summary = f"Campaign processed {stats['total']} leads with an average score of {stats['average_score']:.2f}."
        
        # Generate markdown report
        total = stats['total']
        # Avoid division by zero
        high_pct = (stats['high_priority']/total*100) if total > 0 else 0.0
        medium_pct = (stats['medium_priority']/total*100) if total > 0 else 0.0
        low_pct = (stats['low_priority']/total*100) if total > 0 else 0.0
        
        report_content = f"""# Campaign Summary Report

## Overview

**Total Leads Processed:** {total}

**Average Lead Score:** {stats['average_score']:.2f}/10

---

## Priority Breakdown

- **High Priority:** {stats['high_priority']} leads ({high_pct:.1f}%)
- **Medium Priority:** {stats['medium_priority']} leads ({medium_pct:.1f}%)
- **Low Priority:** {stats['low_priority']} leads ({low_pct:.1f}%)

---

## Persona Distribution

"""
        
        for persona, count in sorted(stats['persona_distribution'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total * 100) if total > 0 else 0.0
            report_content += f"- **{persona}:** {count} leads ({percentage:.1f}%)\n"
        
        report_content += "\n---\n\n## Response Classification\n\n"
        
        for status, count in stats['response_breakdown'].items():
            if count > 0:
                percentage = (count / total * 100) if total > 0 else 0.0
                report_content += f"- **{status}:** {count} leads ({percentage:.1f}%)\n"
        
        report_content += f"\n---\n\n## AI-Generated Summary\n\n{ai_summary}\n\n---\n\n*Report generated automatically by AI Sales CRM*\n"
        
        # Save report
        report_path = os.path.join(self.reports_dir, "campaign_summary.md")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return report_path

