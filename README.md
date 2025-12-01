# Insurance Card Validator

An AI-powered system to validate insurance cards and extract critical information using AWS Bedrock and Claude 3.5 Sonnet.

## Features

- ✅ Validates if uploaded document is an insurance card
- 📄 Supports PDF, PNG, JPG, and JPEG formats
- 🔍 Extracts key information:
  - Insurance company name
  - Member/patient name
  - Member ID
  - Group number
  - Effective dates
  - Additional policy details
- 🎨 Modern Streamlit UI
- 💾 Export results as JSON

## Quick Start

1. **Activate conda environment**:
   ```bash
   conda activate aws_env
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AWS credentials** (see [setup_instructions.md](setup_instructions.md))

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Project Structure

```
Insurance_card_project/
├── app.py                    # Streamlit UI application
├── bedrock_client.py         # AWS Bedrock integration
├── insurance_validator.py    # Validation and extraction logic
├── config.py                 # Configuration and prompts
├── utils.py                  # Utility functions
├── requirements.txt          # Python dependencies
├── setup_instructions.md     # Detailed setup guide
└── .env.example             # Environment variables template
```

## Usage

1. Open the Streamlit app in your browser (opens automatically)
2. Upload the front side of an insurance card (required)
3. Optionally upload the back side for complete extraction
4. Click "Process Insurance Card"
5. View validation results and extracted data
6. Download results as JSON if needed

## Requirements

- Python 3.10+
- AWS Account with Bedrock access
- Claude 3.5 Sonnet model enabled
- Poppler (for PDF processing)

## Documentation

See [setup_instructions.md](setup_instructions.md) for detailed setup and troubleshooting.

## Example Output

```json
{
  "insurance_company": "Anthem Blue Cross",
  "member_name": "JULIA BOLTER",
  "member_id": "JOU183W24276",
  "group_number": "U5463",
  "effective_date": "Not visible",
  "additional_info": {
    "plan_type": "PPO",
    "pharmacy_info": {
      "rx_bin": "020089",
      "rx_pcn": "WLHA",
      "rx_grp": "040"
    }
  }
}
```

## Tech Stack

- **Frontend**: Streamlit
- **AI/ML**: AWS Bedrock (Claude 3.5 Sonnet)
- **Image Processing**: Pillow, pdf2image
- **Cloud**: AWS (boto3)
