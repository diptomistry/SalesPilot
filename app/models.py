"""Data models for the AI Sales CRM."""
from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum


class Priority(str, Enum):
    """Lead priority levels."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class ResponseStatus(str, Enum):
    """Email response status."""
    INTERESTED = "Interested"
    NOT_INTERESTED = "Not Interested"
    FOLLOW_UP = "Follow Up"
    PENDING = "Pending"


class Lead(BaseModel):
    """Lead data model."""
    name: str
    email: str
    company: Optional[str] = None
    industry: Optional[str] = None
    job_title: Optional[str] = None
    status: Optional[str] = None
    score: Optional[int] = None
    priority: Optional[Priority] = None
    persona: Optional[str] = None
    email_subject: Optional[str] = None
    email_body: Optional[str] = None
    response_status: Optional[ResponseStatus] = None
    
    class Config:
        use_enum_values = True


class CampaignSummary(BaseModel):
    """Campaign summary data model."""
    total_leads: int
    high_priority: int
    medium_priority: int
    low_priority: int
    persona_distribution: dict[str, int]
    response_breakdown: dict[str, int]
    average_score: float
    summary_text: str

