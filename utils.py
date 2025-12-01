"""
Utility functions for image processing and data parsing
"""
import base64
import io
import json
from typing import List, Optional
from PIL import Image
from pdf2image import convert_from_bytes


def convert_pdf_to_images(pdf_bytes: bytes, dpi: int = 300) -> List[Image.Image]:
    """
    Convert PDF bytes to a list of PIL Images
    
    Args:
        pdf_bytes: PDF file content as bytes
        dpi: Resolution for conversion (default 300)
        
    Returns:
        List of PIL Image objects
    """
    try:
        images = convert_from_bytes(pdf_bytes, dpi=dpi)
        return images
    except Exception as e:
        raise ValueError(f"Failed to convert PDF to images: {str(e)}")


def encode_image(image: Image.Image, format: str = "PNG") -> str:
    """
    Encode PIL Image to base64 string
    
    Args:
        image: PIL Image object
        format: Image format (PNG, JPEG, etc.)
        
    Returns:
        Base64 encoded string
    """
    buffered = io.BytesIO()
    
    # Convert RGBA to RGB if saving as JPEG
    if format.upper() == "JPEG" and image.mode == "RGBA":
        image = image.convert("RGB")
    
    image.save(buffered, format=format)
    img_bytes = buffered.getvalue()
    return base64.b64encode(img_bytes).decode('utf-8')


def encode_image_from_bytes(image_bytes: bytes) -> str:
    """
    Encode image bytes to base64 string
    
    Args:
        image_bytes: Image file content as bytes
        
    Returns:
        Base64 encoded string
    """
    image = Image.open(io.BytesIO(image_bytes))
    return encode_image(image)


def parse_json_response(response_text: str) -> dict:
    """
    Parse JSON response from LLM, handling potential formatting issues
    
    Args:
        response_text: Text response from LLM
        
    Returns:
        Parsed JSON as dictionary
    """
    try:
        # Try direct JSON parsing
        return json.loads(response_text)
    except json.JSONDecodeError:
        # Try to extract JSON from markdown code blocks
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            json_text = response_text[start:end].strip()
            return json.loads(json_text)
        elif "```" in response_text:
            start = response_text.find("```") + 3
            end = response_text.find("```", start)
            json_text = response_text[start:end].strip()
            return json.loads(json_text)
        else:
            # Try to find JSON-like structure
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            if start != -1 and end != 0:
                json_text = response_text[start:end]
                return json.loads(json_text)
            raise ValueError(f"Could not parse JSON from response: {response_text}")


def format_extraction_result(data: dict) -> str:
    """
    Format extraction result as readable text
    
    Args:
        data: Extracted data dictionary
        
    Returns:
        Formatted string
    """
    output = []
    
    if data.get("insurance_company"):
        output.append(f"**Insurance Company:** {data['insurance_company']}")
    
    if data.get("member_name"):
        output.append(f"**Member Name:** {data['member_name']}")
    
    if data.get("member_id"):
        output.append(f"**Member ID:** {data['member_id']}")
    
    if data.get("group_number"):
        output.append(f"**Group Number:** {data['group_number']}")
    
    if data.get("effective_date"):
        output.append(f"**Effective Date:** {data['effective_date']}")
    
    # Add additional info if present
    if data.get("additional_info"):
        additional = data["additional_info"]
        if any(additional.values()):
            output.append("\n**Additional Information:**")
            for key, value in additional.items():
                if value and value != "null":
                    # Format key nicely
                    formatted_key = key.replace("_", " ").title()
                    if isinstance(value, dict):
                        output.append(f"  - {formatted_key}:")
                        for k, v in value.items():
                            if v and v != "null":
                                output.append(f"    - {k}: {v}")
                    else:
                        output.append(f"  - {formatted_key}: {value}")
    
    return "\n".join(output) if output else "No data extracted"
