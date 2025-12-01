"""
Configuration for AWS Bedrock and Insurance Card Processing
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS Configuration
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
MODEL_ID = os.getenv("MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")

# Model parameters
MAX_TOKENS = 4096
TEMPERATURE = 0.0  # Use 0 for deterministic output

# Validation Prompt
VALIDATION_PROMPT = """You are an expert at identifying insurance cards. 
Analyze this image and determine if it is an insurance card (health/medical insurance).

Look for these characteristics:
- Insurance company name/logo
- Member ID or Subscriber ID
- Group number
- Plan information
- Coverage details
- Medical insurance terminology

Respond ONLY with a JSON object in this exact format:
{
    "is_insurance_card": true or false,
    "confidence": "high" or "medium" or "low",
    "reason": "Brief explanation of your decision"
}"""

# Extraction Prompt
EXTRACTION_PROMPT = """You are an expert at extracting information from insurance cards.
Extract all relevant information from this insurance card image.

Required fields to extract (if visible):
1. Insurance Company Name
2. Member/Patient Name
3. Member ID (or Subscriber ID or ID#)
4. Group Number (or Group ID or Group#)
5. Effective Date (or Start Date or End Date)

Also extract any additional useful information like:
- Plan Type (PPO, HMO, etc.)
- RxBin, RxPCN, RxGrp (pharmacy information)
- Copay information
- Contact phone numbers

Respond ONLY with a JSON object in this exact format:
{
    "insurance_company": "company name or null",
    "member_name": "name or null",
    "member_id": "ID or null",
    "group_number": "group number or null",
    "effective_date": "date or null",
    "additional_info": {
        "plan_type": "type or null",
        "pharmacy_info": {},
        "other_details": {}
    }
}

If a field is not visible or cannot be determined, use null.
"""
