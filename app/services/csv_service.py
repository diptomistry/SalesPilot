"""CSV service for reading and writing leads."""
import csv
import os
from typing import List, Dict, Optional
from app.models import Lead, Priority, ResponseStatus


class CSVService:
    """Service for CSV operations."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._ensure_directory()
    
    def _ensure_directory(self):
        """Ensure the directory exists."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
    
    def read_leads(self) -> List[Dict[str, Optional[str]]]:
        """Read leads from CSV file."""
        if not os.path.exists(self.file_path):
            return []
        
        leads = []
        with open(self.file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Clean up the row data
                cleaned_row = {k.strip(): (v.strip() if v else None) for k, v in row.items()}
                leads.append(cleaned_row)
        
        return leads
    
    def write_leads(self, leads: List[Lead]):
        """Write leads to CSV file."""
        self._ensure_directory()
        
        # Define all possible columns
        fieldnames = [
            'name', 'email', 'company', 'industry', 'job_title', 'status',
            'score', 'priority', 'persona', 'email_subject', 'email_body', 'response_status'
        ]
        
        with open(self.file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for lead in leads:
                row = {
                    'name': lead.name,
                    'email': lead.email,
                    'company': lead.company or '',
                    'industry': lead.industry or '',
                    'job_title': lead.job_title or '',
                    'status': lead.status or '',
                    'score': lead.score or '',
                    'priority': lead.priority or '',
                    'persona': lead.persona or '',
                    'email_subject': lead.email_subject or '',
                    'email_body': lead.email_body or '',
                    'response_status': lead.response_status or ''
                }
                writer.writerow(row)
    
    def update_leads(self, updated_leads: List[Lead]):
        """Update existing CSV with new lead data."""
        existing_leads = self.read_leads()
        
        # Create a mapping of email to lead data
        lead_map = {lead.email: lead for lead in updated_leads}
        
        # Update existing leads
        updated_rows = []
        for row in existing_leads:
            email = row.get('email', '').strip()
            if email in lead_map:
                lead = lead_map[email]
                row.update({
                    'score': str(lead.score) if lead.score else '',
                    'priority': lead.priority or '',
                    'persona': lead.persona or '',
                    'email_subject': lead.email_subject or '',
                    'email_body': lead.email_body or '',
                    'response_status': lead.response_status or ''
                })
                # Also update any enriched fields
                if lead.industry:
                    row['industry'] = lead.industry
                if lead.job_title:
                    row['job_title'] = lead.job_title
            updated_rows.append(row)
        
        # Write back to CSV
        fieldnames = [
            'name', 'email', 'company', 'industry', 'job_title', 'status',
            'score', 'priority', 'persona', 'email_subject', 'email_body', 'response_status'
        ]
        
        with open(self.file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_rows)

