# Environment Setup

## Create .env File

Create a `.env` file in the project root directory (`/Users/diptajoymistry/Desktop/SalesPilot/.env`) with the following content:

```env
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# SMTP Configuration (MailHog - defaults work for Docker)
SMTP_HOST=mailhog
SMTP_PORT=1025
SMTP_USER=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=sales@example.com
SMTP_FROM_NAME=Sales Team

# Application Settings
CSV_FILE_PATH=/app/data/leads.csv
REPORTS_DIR=/app/reports
```

## Getting Your Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account (no credit card required)
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and paste it in your `.env` file

## Important

- The `.env` file is already in `.gitignore` and will not be committed to version control
- Replace `your_groq_api_key_here` with your actual Groq API key
- The other settings have sensible defaults for Docker Compose

