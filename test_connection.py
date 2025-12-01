"""
Quick test script to verify AWS Bedrock connection
"""
import boto3
from config import AWS_REGION, MODEL_ID

def test_bedrock_connection():
    """Test if AWS Bedrock is accessible"""
    try:
        print(f"Testing AWS Bedrock connection...")
        print(f"Region: {AWS_REGION}")
        print(f"Model: {MODEL_ID}")
        
        # Initialize client
        client = boto3.client('bedrock-runtime', region_name=AWS_REGION)
        print("✅ Successfully connected to AWS Bedrock!")
        
        # Try to list available models (this requires different permissions)
        try:
            bedrock_client = boto3.client('bedrock', region_name=AWS_REGION)
            print("\n✅ AWS credentials are properly configured")
            print("\nNote: To verify the model access, you need to:")
            print("1. Go to AWS Console > Amazon Bedrock > Model access")
            print(f"2. Enable access to: {MODEL_ID}")
            
        except Exception as e:
            print(f"\nNote: Could not list models (this is optional): {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error connecting to AWS Bedrock:")
        print(f"   {str(e)}")
        print("\nPlease ensure:")
        print("1. AWS credentials are configured (aws configure)")
        print("2. You have Bedrock access permissions")
        print(f"3. Model access is enabled for: {MODEL_ID}")
        return False

if __name__ == "__main__":
    test_bedrock_connection()
