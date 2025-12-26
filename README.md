# AI-Enhanced Sales Campaign CRM

An end-to-end AI-powered Sales Campaign CRM MVP that ingests leads from CSV, scores and enriches them using AI, generates personalized outreach emails, and produces comprehensive campaign reports.

## 🎯 Overview

This MVP demonstrates a complete sales campaign automation pipeline:

1. **Lead Ingestion** - Reads leads from CSV file
2. **AI Lead Scoring** - Uses Groq LLM to score leads (1-10) and assign priority
3. **Lead Enrichment** - Infers missing data and assigns buyer personas
4. **Email Generation** - Creates personalized outreach emails
5. **Email Sending** - Sends emails via MailHog (local SMTP)
6. **Response Classification** - Simulates and classifies email responses
7. **CSV Write-Back** - Updates CSV with all AI-generated data
8. **Campaign Reports** - Auto-generates Markdown summary reports

## 🏗️ Architecture

### Tech Stack

- **Backend**: FastAPI (Python 3.11)
- **LLM**: Groq API (free tier, using Llama 3.1 70B)
- **Email**: MailHog (local SMTP server)
- **Data Storage**: CSV files (no database)
- **Containerization**: Docker + Docker Compose

### Project Structure

```
ai-sales-crm/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration settings
│   ├── models.py               # Data models
│   ├── services/
│   │   ├── csv_service.py      # CSV read/write operations
│   │   ├── llm_service.py      # Groq API integration
│   │   ├── lead_scoring.py     # Lead scoring service
│   │   ├── persona_agent.py    # Persona assignment & enrichment
│   │   ├── email_agent.py      # Email generation
│   │   ├── response_classifier.py  # Response classification
│   │   ├── mail_service.py     # SMTP email sending
│   │   └── report_generator.py # Campaign report generation
│   └── utils/
│       └── prompts.py          # LLM prompt templates
├── data/
│   └── leads.csv               # Input leads (20+ sample leads)
├── reports/
│   └── campaign_summary.md     # Generated campaign report
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker image definition
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── README.md                   # This file
```

## 🤖 LLM Choice & Prompt Strategy

### Why Groq?

- **Free API** - No credit card required
- **Fast Inference** - Optimized for speed
- **High-Quality Models** - Llama 3.1 70B provides excellent results
- **Simple Integration** - OpenAI-compatible API

### Prompt Strategy

The system uses structured prompts for each task:

1. **Lead Scoring** - Analyzes lead data to assign 1-10 score and priority
2. **Enrichment** - Infers missing fields and assigns buyer personas
3. **Email Generation** - Creates personalized, professional outreach emails
4. **Response Classification** - Simulates likely response based on lead profile
5. **Campaign Summary** - Generates insightful campaign analysis

All prompts request JSON responses for structured data extraction, with fallback handling for edge cases.

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Step-by-Step Setup

1. **Clone or navigate to the project directory**

```bash
cd SalesPilot
```

2. **Create environment file**

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:

```env
GROQ_API_KEY=your_actual_groq_api_key_here
```

3. **Start the application**

```bash
docker compose up --build
```

This will:

- Build the FastAPI application container
- Start MailHog email server
- Process all leads automatically
- Generate campaign report
- Send all emails

4. **Access the services**

- **FastAPI API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MailHog UI**: http://localhost:8025 (view all sent emails)

## 📊 Demo Flow

### 1. Lead Processing

When you run `docker compose up`, the system automatically:

1. Reads `data/leads.csv` (20+ sample leads)
2. For each lead:
   - Enriches missing data (industry, job title)
   - Assigns a buyer persona (Founder, CTO, Marketing Manager, etc.)
   - Scores the lead (1-10) and assigns priority (High/Medium/Low)
   - Generates a personalized email subject and body
   - Classifies likely response (Interested/Not Interested/Follow Up)
   - Sends the email via MailHog

### 2. CSV Updates

The original CSV is updated with:

- `score` - AI-generated lead score (1-10)
- `priority` - High, Medium, or Low
- `persona` - Assigned buyer persona
- `email_subject` - Generated email subject
- `email_body` - Generated email body
- `response_status` - Classified response status

### 3. Campaign Report

A comprehensive Markdown report is generated at `reports/campaign_summary.md` including:

- Total leads processed
- Priority breakdown (High/Medium/Low)
- Persona distribution
- Response classification breakdown
- AI-generated summary insights

### 4. Email Viewing

All sent emails are captured by MailHog and visible at:

- **Web UI**: http://localhost:8025
- View email content, recipients, and details

## 🔧 API Endpoints

### `GET /`

Root endpoint - returns API information

### `GET /health`

Health check endpoint

### `GET /leads`

Get all leads from CSV file

### `POST /campaign/process`

Process all leads in the campaign:

- Scores and enriches leads
- Generates and sends emails
- Updates CSV file
- Generates campaign report

## 📝 CSV Format

The `data/leads.csv` file should have the following columns:

- `name` - Lead's name (required)
- `email` - Lead's email (required)
- `company` - Company name (optional)
- `industry` - Industry (optional, will be inferred)
- `job_title` - Job title (optional, will be inferred)
- `status` - Lead status (optional)

After processing, additional columns are added:

- `score` - Lead score (1-10)
- `priority` - High/Medium/Low
- `persona` - Buyer persona
- `email_subject` - Generated email subject
- `email_body` - Generated email body
- `response_status` - Response classification

## 🐳 Docker Details

### Services

1. **api** - FastAPI application

   - Port: 8000
   - Automatically processes campaign on startup
   - Volumes: `./data` and `./reports`

2. **mailhog** - MailHog SMTP server
   - Web UI: Port 8025
   - SMTP: Port 1025

### Volumes

- `./data` - Mounted to `/app/data` (CSV files)
- `./reports` - Mounted to `/app/reports` (generated reports)

## 🔑 Environment Variables

Create a `.env` file with:

```env
GROQ_API_KEY=your_groq_api_key_here
SMTP_HOST=mailhog
SMTP_PORT=1025
SMTP_FROM_EMAIL=sales@example.com
SMTP_FROM_NAME=Sales Team
CSV_FILE_PATH=/app/data/leads.csv
REPORTS_DIR=/app/reports
```

## 📈 Example Output

### Processed Lead Example

```csv
name,email,company,industry,job_title,status,score,priority,persona,email_subject,email_body,response_status
John Smith,john.smith@techcorp.com,TechCorp,Technology,CEO,Active,9,High,CEO,"Partnership Opportunity for TechCorp","Hello John, I'd like to discuss...",Interested
```

### Campaign Report

See `reports/campaign_summary.md` for a complete example with:

- Statistics breakdown
- Persona distribution
- Response classification
- AI-generated insights

