"""Prompt templates for LLM interactions."""


LEAD_SCORING_PROMPT = """You are an expert sales lead scoring system. Analyze the following lead information and provide a score from 1-10 and a priority level (High, Medium, or Low).

Lead Information:
- Name: {name}
- Email: {email}
- Company: {company}
- Industry: {industry}
- Job Title: {job_title}
- Status: {status}

Respond in JSON format only:
{{
    "score": <number 1-10>,
    "priority": "<High|Medium|Low>",
    "reasoning": "<brief explanation>"
}}
"""


LEAD_ENRICHMENT_PROMPT = """You are a lead enrichment agent. Analyze the following lead and:
1. Infer any missing fields (industry, job_title) based on available information
2. Assign a buyer persona from these categories: Founder, CTO, Marketing Manager, Sales Lead, Product Manager, CEO, CFO, HR Director, Operations Manager, or Other

Lead Information:
- Name: {name}
- Email: {email}
- Company: {company}
- Industry: {industry}
- Job Title: {job_title}

Respond in JSON format only:
{{
    "industry": "<inferred or original industry>",
    "job_title": "<inferred or original job title>",
    "persona": "<buyer persona category>",
    "reasoning": "<brief explanation>"
}}
"""


EMAIL_GENERATION_PROMPT = """You are an expert sales email copywriter. Generate a personalized outreach email for this lead.

Lead Information:
- Name: {name}
- Company: {company}
- Industry: {industry}
- Job Title: {job_title}
- Persona: {persona}
- Score: {score}
- Priority: {priority}

Requirements:
- Professional, friendly, and sales-oriented tone
- Personalized to the lead's role and industry
- Clear value proposition
- Call-to-action
- Keep email body under 150 words

Respond in JSON format only:
{{
    "subject": "<email subject line>",
    "body": "<email body text>"
}}
"""


RESPONSE_CLASSIFICATION_PROMPT = """You are an email response classifier. Based on the lead's profile and the email sent, simulate a likely response classification.

Lead Information:
- Name: {name}
- Company: {company}
- Industry: {industry}
- Job Title: {job_title}
- Persona: {persona}
- Score: {score}
- Priority: {priority}

Email Subject: {email_subject}

Classify the likely response as one of:
- "Interested" - Lead shows interest and may engage
- "Not Interested" - Lead is unlikely to respond positively
- "Follow Up" - Lead needs more nurturing before decision

Respond in JSON format only:
{{
    "response_status": "<Interested|Not Interested|Follow Up>",
    "reasoning": "<brief explanation>"
}}
"""


CAMPAIGN_SUMMARY_PROMPT = """You are a sales campaign analyst. Generate a comprehensive summary paragraph for this campaign based on the following metrics:

- Total Leads: {total_leads}
- High Priority: {high_priority}
- Medium Priority: {medium_priority}
- Low Priority: {low_priority}
- Average Score: {average_score}
- Persona Distribution: {persona_distribution}
- Response Breakdown: {response_breakdown}

Write a professional, insightful summary paragraph (3-4 sentences) that highlights:
1. Overall campaign performance
2. Key insights about lead quality
3. Recommendations for next steps

Respond with only the summary text, no JSON formatting.
"""

