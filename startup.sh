#!/bin/bash
set -e

echo "Waiting for FastAPI to be ready..."
sleep 10

echo "Processing campaign..."
curl -X POST http://localhost:8000/campaign/process || echo "Campaign processing failed, but API is running"

echo "Campaign processing complete!"
echo "API is running at http://localhost:8000"
echo "MailHog UI is available at http://localhost:8025"

