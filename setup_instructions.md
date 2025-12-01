# Setup Instructions for Insurance Card Validator

## Prerequisites

### 1. AWS Credentials Configuration

You need AWS credentials with access to Amazon Bedrock. Choose one of these methods:

#### Option A: AWS CLI (Recommended)
```bash
aws configure
```
Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., `us-east-1`)

#### Option B: Environment Variables
Create a `.env` file in the project directory:
```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
```
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
```

### 2. Enable Bedrock Model Access

1. Go to AWS Console → Amazon Bedrock
2. Navigate to "Model access"
3. Enable access to: **Claude 3.5 Sonnet** (`anthropic.claude-3-5-sonnet-20240620-v1:0`)
4. Wait for approval (usually instant)

### 3. Install Poppler (Required for PDF processing)

#### Windows:
1. Download Poppler from: https://github.com/oschwartz10612/poppler-windows/releases/
2. Extract to `C:\Program Files\poppler`
3. Add to PATH: `C:\Program Files\poppler\Library\bin`

To add to PATH:
- Press Win + X → System
- Click "Advanced system settings"
- Click "Environment Variables"
- Under "System variables", find "Path" and click "Edit"
- Click "New" and add: `C:\Program Files\poppler\Library\bin`
- Click OK on all dialogs

Verify installation:
```bash
pdftoppm -h
```

## Installation Steps

### 1. Activate your conda environment
```bash
conda activate aws_env
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Verify installation
```bash
python -c "import boto3; import streamlit; print('All packages installed successfully!')"
```

## Running the Application

### Start the Streamlit app
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## Usage

1. **Upload Front Side**: Click "Front of Card" and upload the insurance card front (PDF/PNG/JPG)
2. **Upload Back Side** (Optional): Upload the back side for complete information
3. **Process**: Click "Process Insurance Card" to validate and extract data
4. **Review Results**: View validation status and extracted information
5. **Download**: Download extracted data as JSON if needed

## Troubleshooting

### "No credentials found"
- Ensure AWS credentials are configured (see Prerequisites)
- Check `.env` file or AWS CLI configuration

### "Model not found" or "Access denied"
- Verify Bedrock model access is enabled in AWS Console
- Check that you're using the correct region

### "PDF conversion failed"
- Ensure Poppler is installed and in PATH
- Restart terminal after adding to PATH

### "Module not found"
- Ensure conda environment is activated: `conda activate aws_env`
- Reinstall dependencies: `pip install -r requirements.txt`

## Testing with Sample Cards

Sample insurance cards are provided for testing. Upload them to verify the system works correctly.

Expected extractions:
- **Insurance Company**: Anthem Blue Cross
- **Member Name**: JULIA BOLTER
- **Member ID**: JOU183W24276
- **Group Number**: U5463

## Cost Considerations

AWS Bedrock charges per request:
- Claude 3.5 Sonnet: ~$3 per 1000 input images (approximate)
- Each card processing = 1-2 API calls
- Monitor usage in AWS Cost Explorer

## Support

For issues or questions:
1. Check AWS Bedrock service health
2. Review CloudWatch logs for detailed errors
3. Verify model access and credentials
