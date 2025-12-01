"""
AWS Bedrock client for invoking Claude models with vision capabilities
"""
import json
import boto3
from typing import Dict, Any, Optional
from config import AWS_REGION, MODEL_ID, MAX_TOKENS, TEMPERATURE


class BedrockClient:
    """Client for interacting with AWS Bedrock"""
    
    def __init__(self, region_name: str = AWS_REGION, model_id: str = MODEL_ID):
        """
        Initialize Bedrock client
        
        Args:
            region_name: AWS region
            model_id: Bedrock model identifier
        """
        self.region_name = region_name
        self.model_id = model_id
        self.client = boto3.client('bedrock-runtime', region_name=region_name)
    
    def invoke_with_image(
        self, 
        prompt: str, 
        image_base64: str,
        max_tokens: int = MAX_TOKENS,
        temperature: float = TEMPERATURE
    ) -> str:
        """
        Invoke Claude model with an image
        
        Args:
            prompt: Text prompt
            image_base64: Base64 encoded image
            max_tokens: Maximum tokens in response
            temperature: Temperature for generation
            
        Returns:
            Model response text
        """
        # Construct message for Claude
        message = {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_base64
                    }
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
        
        # Prepare request body
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [message]
        }
        
        try:
            # Invoke model
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            
            # Extract text from response
            if 'content' in response_body and len(response_body['content']) > 0:
                return response_body['content'][0]['text']
            else:
                raise ValueError("No content in model response")
                
        except Exception as e:
            raise RuntimeError(f"Bedrock API call failed: {str(e)}")
    
    def invoke_with_multiple_images(
        self,
        prompt: str,
        images_base64: list,
        max_tokens: int = MAX_TOKENS,
        temperature: float = TEMPERATURE
    ) -> str:
        """
        Invoke Claude model with multiple images (e.g., front and back of card)
        
        Args:
            prompt: Text prompt
            images_base64: List of base64 encoded images
            max_tokens: Maximum tokens in response
            temperature: Temperature for generation
            
        Returns:
            Model response text
        """
        # Build content list with all images
        content = []
        
        for idx, image_base64 in enumerate(images_base64):
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": image_base64
                }
            })
        
        # Add text prompt at the end
        content.append({
            "type": "text",
            "text": prompt
        })
        
        message = {
            "role": "user",
            "content": content
        }
        
        # Prepare request body
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [message]
        }
        
        try:
            # Invoke model
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            
            # Extract text from response
            if 'content' in response_body and len(response_body['content']) > 0:
                return response_body['content'][0]['text']
            else:
                raise ValueError("No content in model response")
                
        except Exception as e:
            raise RuntimeError(f"Bedrock API call failed: {str(e)}")
