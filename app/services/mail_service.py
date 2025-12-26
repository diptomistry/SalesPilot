"""Email sending service using SMTP."""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from app.config import settings


class MailService:
    """Service for sending emails via SMTP."""
    
    def __init__(self):
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.user = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM_EMAIL
        self.from_name = settings.SMTP_FROM_NAME
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        to_name: Optional[str] = None
    ) -> bool:
        """Send an email via SMTP."""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(self.host, self.port) as server:
                if self.user and self.password:
                    server.login(self.user, self.password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Error sending email to {to_email}: {str(e)}")
            return False

