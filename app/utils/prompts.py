"""Prompt templates for LLM interactions."""


LEAD_SCORING_PROMPT = """You are an expert sales lead scoring system. Analyze the following lead information and refine the base score.

Lead Information:
- Name: {name}
- Email: {email}
- Company: {company}
- Industry: {industry}
- Job Title: {job_title}
- Status: {status}

Base Score (rule-based): {base_score}/10

Scoring Guidelines:
- Score 8-10: C-level executives (CEO, CTO, CFO), Founders, VPs in high-value industries
- Score 5-7: Directors, Managers, decision-makers in mid-market companies
- Score 1-4: Lower-level roles, missing information, less relevant industries

Consider these factors:
1. Decision-making authority (job title hierarchy)
2. Industry value (Technology, Finance, Healthcare = higher value)
3. Company presence (having a company name is positive)
4. Data completeness (missing fields reduce score)

Provide a refined score that adjusts the base score based on nuanced context. The score should vary between leads.

Respond in JSON format only:
{{
    "score": <number 1-10, should differ from base_score if context warrants>,
    "reasoning": "<brief explanation of why this score was assigned, mention specific factors>"
}}
"""


LEAD_ENRICHMENT_PROMPT = """You are a lead enrichment agent. Analyze the following lead and:
1. Infer any missing fields (industry, job_title) based on available information (email domain, company name, etc.)
2. Refine or confirm the suggested persona, or suggest a better one if the mapping seems incorrect

Lead Information:
- Name: {name}
- Email: {email}
- Company: {company}
- Industry: {industry}
- Job Title: {job_title}

Suggested Persona (from title mapping): {suggested_persona}

Persona Categories:
- Decision Maker: CEO, Founder, President, Owner
- Technical Buyer: CTO, Engineering Manager/Director, VP Engineering
- Financial Decision Maker: CFO, Finance Director, VP Finance
- Influencer: Marketing Director/Manager, Sales Director/Manager, CMO, VP Sales/Marketing
- Operations Manager: COO, Operations Director/Manager, VP Operations, General Manager
- HR Director: HR Director/Manager, Chief People Officer
- Product Manager: Product Manager/Director, CPO, VP Product
- Director: Generic Director roles
- Manager: Generic Manager roles
- Partner: Partners in consulting/law firms
- Other: Everything else

If the suggested persona seems correct, confirm it. If the job title or context suggests a different persona, suggest the better one.

Respond in JSON format only:
{{
    "industry": "<inferred or original industry, be specific>",
    "job_title": "<inferred or original job title, be specific>",
    "persona": "<refined buyer persona category from the list above>",
    "reasoning": "<brief explanation of enrichment decisions>"
}}
"""


EMAIL_GENERATION_PROMPT = """You are an expert sales email copywriter. Generate a personalized outreach email for this lead.

Lead Information:
- Name: {name}
- Company: {company}
- Industry: {industry}
- Job Title: {job_title}
- Persona: {persona}
- Score: {score}/10
- Priority: {priority}
- High Priority: {is_high_priority}

Requirements:
- Professional, friendly, and sales-oriented tone
- Personalized to the lead's role and industry
- Clear value proposition
- Call-to-action
- Keep email body under 150 words

Special Instructions for High Priority Leads (Priority = High, Score 8+):
- Use more direct, executive-level language
- Emphasize strategic value and ROI
- Reference their decision-making authority
- Be concise and respect their time
- Use a more confident, value-driven tone

For Medium/Low Priority Leads:
- Use a more consultative, nurturing approach
- Focus on relationship building
- Provide more context and education

Respond in JSON format only:
{{
    "subject": "<email subject line>",
    "body": "<email body text>"
}}
"""


RESPONSE_CLASSIFICATION_PROMPT = """You are an email response classifier. Based on the lead's profile and the email sent, simulate a realistic response classification.

Lead Information:
- Name: {name}
- Company: {company}
- Industry: {industry}
- Job Title: {job_title}
- Persona: {persona}
- Score: {score}/10
- Priority: {priority}

Email Subject: {email_subject}

Base Response (probabilistic): {base_response}

Response Guidelines:
- "Interested": High-scoring leads (8+), decision-makers, relevant industry fit, personalized email
- "Not Interested": Low-scoring leads (1-4), wrong persona fit, generic outreach, busy executives
- "Follow Up": Medium-scoring leads (5-7), needs nurturing, timing not right, requires more information

Consider:
1. Lead score (higher = more likely interested)
2. Persona fit (Decision Makers more likely to respond)
3. Industry relevance
4. Email personalization quality

IMPORTANT: Vary your responses! Not all leads should have the same classification. Consider the specific context of each lead.

Respond in JSON format only:
{{
    "response_status": "<Interested|Not Interested|Follow Up>",
    "reasoning": "<brief explanation considering the specific lead's context>"
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

