"""FastAPI main application."""
import asyncio
from fastapi import FastAPI, HTTPException
from typing import List
from app.config import settings
from app.models import Lead, Priority
from app.services.csv_service import CSVService
from app.services.llm_service import LLMService
from app.services.lead_scoring import LeadScoringService
from app.services.persona_agent import PersonaAgent
from app.services.email_agent import EmailAgent
from app.services.response_classifier import ResponseClassifier
from app.services.mail_service import MailService
from app.services.report_generator import ReportGenerator


app = FastAPI(title="AI Sales CRM", version="1.0.0")

# Initialize services
csv_service = CSVService(settings.CSV_FILE_PATH)
llm_service = LLMService()
lead_scoring_service = LeadScoringService(llm_service)
persona_agent = PersonaAgent(llm_service)
email_agent = EmailAgent(llm_service)
response_classifier = ResponseClassifier(llm_service)
mail_service = MailService()
report_generator = ReportGenerator(llm_service, settings.REPORTS_DIR)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI Sales CRM API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


async def process_lead(lead_data: dict) -> Lead:
    """Process a single lead through the entire pipeline."""
    # Create Lead object from CSV data
    lead = Lead(
        name=lead_data.get("name", ""),
        email=lead_data.get("email", ""),
        company=lead_data.get("company"),
        industry=lead_data.get("industry"),
        job_title=lead_data.get("job_title"),
        status=lead_data.get("status")
    )
    
    # Step 1: Enrich lead and assign persona
    enrichment = await persona_agent.enrich_lead(lead)
    lead.industry = enrichment["industry"]
    lead.job_title = enrichment["job_title"]
    lead.persona = enrichment["persona"]
    
    # Step 2: Score lead
    scoring = await lead_scoring_service.score_lead(lead)
    lead.score = scoring["score"]
    lead.priority = scoring["priority"]
    
    # Step 3: Generate email
    email_data = await email_agent.generate_email(lead)
    lead.email_subject = email_data["subject"]
    lead.email_body = email_data["body"]
    
    # Step 4: Classify response
    classification = await response_classifier.classify_response(lead)
    lead.response_status = classification["response_status"]
    
    # Step 5: Send email
    if lead.email:
        mail_service.send_email(
            to_email=lead.email,
            subject=lead.email_subject,
            body=lead.email_body,
            to_name=lead.name
        )
    
    return lead


@app.post("/campaign/process")
async def process_campaign():
    """Process all leads in the campaign."""
    try:
        # Read leads from CSV
        leads_data = csv_service.read_leads()
        
        if not leads_data:
            raise HTTPException(status_code=404, detail="No leads found in CSV file")
        
        # Process each lead
        processed_leads = []
        high_priority_count = 0
        
        for lead_data in leads_data:
            if not lead_data.get("email"):
                continue  # Skip leads without email
            
            try:
                lead = await process_lead(lead_data)
                processed_leads.append(lead)
                
                # Track and log high priority leads
                if lead.priority == Priority.HIGH:
                    high_priority_count += 1
                    print(f"🚨 HIGH PRIORITY LEAD: {lead.name} ({lead.company}) - Score: {lead.score} - Persona: {lead.persona}")
            except Exception as e:
                print(f"Error processing lead {lead_data.get('email', 'unknown')}: {str(e)}")
                continue
        
        # Log summary
        if high_priority_count > 0:
            print(f"\n📊 Campaign Summary: {high_priority_count} high-priority lead(s) identified and processed with enhanced email templates.")
        
        # Write updated leads back to CSV
        csv_service.write_leads(processed_leads)
        
        # Generate campaign summary report
        report_path = await report_generator.generate_report(processed_leads)
        
        return {
            "status": "success",
            "leads_processed": len(processed_leads),
            "report_path": report_path,
            "message": f"Campaign processed successfully. {len(processed_leads)} leads processed."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing campaign: {str(e)}")


@app.get("/leads")
async def get_leads():
    """Get all leads from CSV."""
    try:
        leads_data = csv_service.read_leads()
        return {"leads": leads_data, "count": len(leads_data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading leads: {str(e)}")


@app.get("/leads/high-priority")
async def get_high_priority_leads():
    """Get all high-priority leads from CSV."""
    try:
        leads_data = csv_service.read_leads()
        high_priority_leads = [
            lead for lead in leads_data 
            if lead.get("priority", "").lower() == "high"
        ]
        return {
            "high_priority_leads": high_priority_leads,
            "count": len(high_priority_leads),
            "message": f"Found {len(high_priority_leads)} high-priority lead(s) requiring immediate attention."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading leads: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

