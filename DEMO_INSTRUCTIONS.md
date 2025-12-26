# Demo Presentation Instructions

## 🎯 Quick Demo Flow

### 1. **Before Starting the Demo**

✅ **Reset Complete!** The project has been reset:

- ✅ CSV restored to original input format (20 leads, no AI data), leads.csv
- ✅ Campaign report deleted, campaign_summary.md
- ✅ Ready for fresh demo run

## leads.csv
name,email,company,industry,job_title,status
John Smith,john.smith@techcorp.com,TechCorp,Technology,CEO,Active
Sarah Johnson,sarah.j@marketingpro.com,Marketing Pro,Marketing,Marketing Director,Active
Michael Chen,mchen@startup.io,StartupIO,Technology,CTO,Active
Emily Davis,emily.davis@retailco.com,RetailCo,Retail,Operations Manager,Active
David Wilson,dwilson@financegroup.com,Finance Group,Finance,CFO,Active
Lisa Anderson,lisa.anderson@healthcare.com,HealthCare Plus,Healthcare,HR Director,Active
Robert Brown,robert.brown@manufacturing.com,Manufacturing Inc,Manufacturing,Operations Manager,Active
Jennifer Lee,jlee@consulting.com,Consulting Partners,Consulting,Partner,Active
William Taylor,wtaylor@education.com,Education First,Education,Director,Active
Amanda Martinez,amartinez@realestate.com,Real Estate Pro,Real Estate,Sales Manager,Active
Christopher White,cwhite@logistics.com,Logistics Solutions,Logistics,VP Operations,Active
Jessica Harris,jharris@foodservice.com,Food Service Co,Food Service,General Manager,Active
Matthew Clark,mclark@energy.com,Energy Solutions,Energy,Project Manager,Active
Ashley Lewis,alewis@hospitality.com,Hospitality Group,Hospitality,Operations Director,Active
Daniel Walker,dwalker@construction.com,Construction Ltd,Construction,Project Manager,Active
Michelle Hall,mhall@automotive.com,Auto Solutions,Automotive,Sales Director,Active
James Allen,jallen@telecom.com,Telecom Services,Telecommunications,Technical Director,Active
Nicole Young,nyoung@pharmaceutical.com,Pharma Corp,Pharmaceutical,Research Director,Active
Kevin King,kking@aerospace.com,Aerospace Systems,Aerospace,Engineering Manager,Active
Rachel Green,rgreen@ecommerce.com,E-Commerce Plus,E-Commerce,Product Manager,Active


### 2. **Start the Demo**

```bash
docker compose up --build
```

**What happens:**

- FastAPI starts
- MailHog starts
- Campaign automatically processes all 20 leads
- Takes ~4-5 minutes (LLM API calls)

### 3. **During the Demo - Show These Points**

#### **A. Input Data (Before)**

```bash
# Show the original CSV
cat data/leads.csv
```

**Highlight:** Simple CSV with basic lead info (name, email, company, industry, job_title, status)

#### **B. Processing in Real-Time**

- Show Docker logs: `docker compose logs -f api`
- Show MailHog receiving emails: http://localhost:8025
- Explain the AI pipeline:
  1. Lead enrichment & persona assignment
  2. AI lead scoring (1-10)
  3. Priority assignment (High/Medium/Low)
  4. Personalized email generation
  5. Response classification

#### **C. Output Data (After)**

```bash
# Show the updated CSV
cat data/leads.csv
```

**Highlight:** CSV now has:

- `score` - AI-generated lead score
- `priority` - High/Medium/Low
- `persona` - Buyer persona (Founder, CTO, etc.)
- `email_subject` - Generated email subject
- `email_body` - Personalized email content
- `response_status` - Classified response (Interested/Not Interested/Follow Up)

#### **D. Campaign Report**

```bash
# Show the generated report
cat reports/campaign_summary.md
```

**Highlight:**

- Total leads processed
- Priority breakdown
- Persona distribution
- Response classification
- AI-generated insights

#### **E. Email Viewing**

- Open http://localhost:8025
- Show all 20 personalized emails
- Click on emails to show personalized content

### 4. **Key Talking Points**

1. **AI-Powered Automation**

   - No manual lead scoring
   - Automatic data enrichment
   - Personalized email generation at scale

2. **Free LLM Integration**

   - Uses Groq API (free tier)
   - Fast inference with Llama 3.1 70B
   - No credit card required

3. **End-to-End Pipeline**

   - CSV input → AI processing → CSV output
   - Email sending via MailHog
   - Automatic report generation

4. **Scalable Architecture**
   - Docker containerization
   - FastAPI backend
   - Ready for production deployment

### 5. **Demo Script (2-3 minutes)**

**Opening:**

> "I've built an AI-powered Sales Campaign CRM that automates the entire lead processing pipeline. Let me show you how it works."

**Step 1 - Show Input:**

> "We start with a simple CSV file containing 20 leads with basic information."

**Step 2 - Run Processing:**

> "When I run `docker compose up`, the system automatically:
>
> - Enriches each lead with missing data
> - Scores leads using AI (1-10 scale)
> - Assigns buyer personas
> - Generates personalized outreach emails
> - Sends emails via SMTP
> - Creates a comprehensive campaign report"

**Step 3 - Show Output:**

> "After processing, the CSV is updated with all AI-generated insights. We can see personalized emails in MailHog, and a detailed campaign report is automatically generated."

**Step 4 - Highlight Results:**

> "The system processed 20 leads, generated personalized emails for each, and provided actionable insights - all automatically using AI."

### 6. **If Something Goes Wrong**

**If processing is slow:**

- "The LLM API calls take a few minutes for 20 leads - this is normal"
- "In production, we'd batch process or use async queues"

**If API key issue:**

- Make sure `.env` file has `GROQ_API_KEY` set
- Check console.groq.com for API key

**If containers won't start:**

- `docker compose down` to stop
- `docker compose up --build` to restart

### 7. **After Demo**

```bash
# Stop containers
docker compose down
```

---

## 🎤 Presentation Tips

1. **Start with the problem:** Manual lead processing is time-consuming
2. **Show the solution:** AI automation handles everything
3. **Demonstrate value:** Show before/after CSV comparison
4. **Highlight tech:** FastAPI, Groq LLM, Docker, MailHog
5. **End with impact:** Scalable, automated, AI-powered

---

**Good luck with your presentation! 🚀**
