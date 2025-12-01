"""
Streamlit application for insurance card validation and data extraction
"""
import streamlit as st
from PIL import Image
import io
from insurance_validator import InsuranceCardProcessor
from utils import convert_pdf_to_images, format_extraction_result
import json


# Page configuration
st.set_page_config(
    page_title="Insurance Card Validator",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        color: #155724;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        color: #721c24;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.5rem;
        color: #0c5460;
    }
    </style>
""", unsafe_allow_html=True)


def process_uploaded_file(uploaded_file) -> list:
    """
    Process uploaded file and return list of PIL Images
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        List of PIL Image objects
    """
    # Reset file pointer to beginning before reading
    uploaded_file.seek(0)
    file_bytes = uploaded_file.read()
    file_type = uploaded_file.type
    
    if file_type == "application/pdf":
        # Convert PDF to images
        images = convert_pdf_to_images(file_bytes)
        return images
    else:
        # Load image directly
        image = Image.open(io.BytesIO(file_bytes))
        return [image]


def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<div class="main-header">🏥 Insurance Card Validator & Extractor</div>', 
                unsafe_allow_html=True)
    
    # Description
    st.markdown("""
    This application validates insurance cards and extracts key information using AI.
    
    **How to use:**
    1. Upload the front side of the insurance card (required)
    2. Optionally upload the back side for complete information
    3. Click "Process Insurance Card" to validate and extract data
    """)
    
    st.divider()
    
    # Initialize processor
    if 'processor' not in st.session_state:
        st.session_state.processor = InsuranceCardProcessor()
    
    # File upload section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Front of Card (Required)")
        front_file = st.file_uploader(
            "Upload front side",
            type=["pdf", "png", "jpg", "jpeg"],
            key="front",
            help="Upload the front side of the insurance card"
        )
        
        if front_file:
            st.success(f"✅ Uploaded: {front_file.name}")
            # Display preview
            try:
                images = process_uploaded_file(front_file)
                st.image(images[0], caption="Front Preview", use_container_width=True)
            except Exception as e:
                st.error(f"Error previewing file: {str(e)}")
    
    with col2:
        st.subheader("📄 Back of Card (Optional)")
        back_file = st.file_uploader(
            "Upload back side",
            type=["pdf", "png", "jpg", "jpeg"],
            key="back",
            help="Upload the back side for additional information"
        )
        
        if back_file:
            st.success(f"✅ Uploaded: {back_file.name}")
            # Display preview
            try:
                images = process_uploaded_file(back_file)
                st.image(images[0], caption="Back Preview", use_container_width=True)
            except Exception as e:
                st.error(f"Error previewing file: {str(e)}")
    
    st.divider()
    
    # Processing options
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        skip_validation = st.checkbox(
            "Skip validation (assume it's an insurance card)",
            help="Check this to skip the validation step and go straight to extraction"
        )
        
        process_button = st.button(
            "🚀 Process Insurance Card",
            type="primary",
            use_container_width=True,
            disabled=front_file is None
        )
    
    # Process when button is clicked
    if process_button and front_file:
        with st.spinner("Processing insurance card..."):
            try:
                # Collect all images
                all_images = []
                
                # Process front
                front_images = process_uploaded_file(front_file)
                all_images.extend(front_images)
                
                # Process back if provided
                if back_file:
                    back_images = process_uploaded_file(back_file)
                    all_images.extend(back_images)
                
                # Process with the insurance card processor
                result = st.session_state.processor.process_insurance_card(
                    all_images,
                    skip_validation=skip_validation
                )
                
                # Store result in session state
                st.session_state.last_result = result
                
            except Exception as e:
                st.error(f"Error processing card: {str(e)}")
                st.session_state.last_result = None
    
    # Display results
    if 'last_result' in st.session_state and st.session_state.last_result:
        st.divider()
        st.header("📊 Results")
        
        result = st.session_state.last_result
        
        # Display validation results
        if result.get("validation") and not skip_validation:
            st.subheader("1️⃣ Validation")
            validation = result["validation"]
            
            if validation.get("is_insurance_card"):
                st.markdown(
                    f'<div class="success-box">'
                    f'✅ <strong>Valid Insurance Card</strong><br>'
                    f'Confidence: {validation.get("confidence", "unknown").upper()}<br>'
                    f'Reason: {validation.get("reason", "N/A")}'
                    f'</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="error-box">'
                    f'❌ <strong>Not an Insurance Card</strong><br>'
                    f'Confidence: {validation.get("confidence", "unknown").upper()}<br>'
                    f'Reason: {validation.get("reason", "N/A")}'
                    f'</div>',
                    unsafe_allow_html=True
                )
                st.stop()
        
        # Display extraction results
        if result.get("extraction"):
            st.subheader("2️⃣ Extracted Information")
            extraction = result["extraction"]
            
            if "error" in extraction:
                st.error(f"❌ {extraction['error']}")
            else:
                # Create columns for extracted data
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Core Information")
                    
                    if extraction.get("insurance_company"):
                        st.metric("Insurance Company", extraction["insurance_company"])
                    
                    if extraction.get("member_name"):
                        st.metric("Member Name", extraction["member_name"])
                    
                    if extraction.get("member_id"):
                        st.metric("Member ID", extraction["member_id"])
                
                with col2:
                    st.markdown("### Policy Details")
                    
                    if extraction.get("group_number"):
                        st.metric("Group Number", extraction["group_number"])
                    
                    if extraction.get("effective_date"):
                        st.metric("Effective Date", extraction["effective_date"])
                
                # Additional information
                if extraction.get("additional_info"):
                    st.markdown("### Additional Information")
                    
                    additional = extraction["additional_info"]
                    
                    # Display in expandable sections
                    for key, value in additional.items():
                        if value and value != "null" and value != {}:
                            with st.expander(f"📌 {key.replace('_', ' ').title()}"):
                                if isinstance(value, dict):
                                    st.json(value)
                                else:
                                    st.write(value)
                
                # Download JSON
                st.divider()
                st.markdown("### 💾 Download Results")
                
                json_str = json.dumps(extraction, indent=2)
                st.download_button(
                    label="Download as JSON",
                    data=json_str,
                    file_name="insurance_card_data.json",
                    mime="application/json"
                )


if __name__ == "__main__":
    main()
