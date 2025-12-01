"""
Insurance card validation and data extraction
"""
from typing import Dict, List, Optional
from PIL import Image
from bedrock_client import BedrockClient
from utils import encode_image, parse_json_response
from config import VALIDATION_PROMPT, EXTRACTION_PROMPT


class InsuranceCardProcessor:
    """Processes insurance cards for validation and data extraction"""
    
    def __init__(self):
        """Initialize the processor with Bedrock client"""
        self.bedrock_client = BedrockClient()
    
    def validate_insurance_card(self, image: Image.Image) -> Dict:
        """
        Validate if the image is an insurance card
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary with validation results
        """
        try:
            # Encode image
            image_b64 = encode_image(image)
            
            # Call Bedrock
            response = self.bedrock_client.invoke_with_image(
                prompt=VALIDATION_PROMPT,
                image_base64=image_b64
            )
            
            # Parse JSON response
            result = parse_json_response(response)
            
            return result
            
        except Exception as e:
            return {
                "is_insurance_card": False,
                "confidence": "low",
                "reason": f"Error during validation: {str(e)}"
            }
    
    def extract_card_data(self, images: List[Image.Image]) -> Dict:
        """
        Extract data from insurance card images (front and/or back)
        
        Args:
            images: List of PIL Image objects (typically front and back)
            
        Returns:
            Dictionary with extracted data
        """
        try:
            # Encode all images
            images_b64 = [encode_image(img) for img in images]
            
            # Build prompt with context about multiple images
            if len(images) > 1:
                context_prompt = (
                    f"{EXTRACTION_PROMPT}\n\n"
                    f"Note: You are analyzing {len(images)} images of the same insurance card "
                    f"(likely front and back). Combine information from all images."
                )
            else:
                context_prompt = EXTRACTION_PROMPT
            
            # Call Bedrock with all images
            if len(images) == 1:
                response = self.bedrock_client.invoke_with_image(
                    prompt=context_prompt,
                    image_base64=images_b64[0]
                )
            else:
                response = self.bedrock_client.invoke_with_multiple_images(
                    prompt=context_prompt,
                    images_base64=images_b64
                )
            
            # Parse JSON response
            result = parse_json_response(response)
            
            return result
            
        except Exception as e:
            return {
                "error": f"Failed to extract data: {str(e)}",
                "insurance_company": None,
                "member_name": None,
                "member_id": None,
                "group_number": None,
                "effective_date": None,
                "additional_info": {}
            }
    
    def process_insurance_card(
        self, 
        images: List[Image.Image],
        skip_validation: bool = False
    ) -> Dict:
        """
        Complete workflow: validate and extract data from insurance card
        
        Args:
            images: List of PIL Image objects
            skip_validation: If True, skip validation step
            
        Returns:
            Dictionary with validation and extraction results
        """
        result = {
            "validation": None,
            "extraction": None,
            "success": False
        }
        
        # Validate first image (front of card)
        if not skip_validation:
            validation = self.validate_insurance_card(images[0])
            result["validation"] = validation
            
            # If not an insurance card, don't proceed with extraction
            if not validation.get("is_insurance_card", False):
                result["success"] = False
                result["error"] = "Not an insurance card"
                return result
        
        # Extract data from all images
        extraction = self.extract_card_data(images)
        result["extraction"] = extraction
        result["success"] = "error" not in extraction
        
        return result
