#Iter1 debugging file - to be used for checking appropraite streamlit UI aspects
import streamlit as st
import requests
import os
import tempfile

# Custom CSS placeholder (add your CSS in this string)
CUSTOM_CSS = """
<style>
/* Add custom CSS here later */
</style>
"""

def inject_custom_css():
    """Inject custom CSS into the Streamlit app"""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Define waste categories with keywords
WASTE_CATEGORIES = {
    # Electronics
    'Smartphones': ['cell phone', 'mobile phone'],
    'Laptops': ['laptop', 'computer'],
    'Tablets': ['tablet'],
    'Speakers': ['speaker'],
    'Headphones': ['headphones'],
    'Keyboards': ['keyboard'],
    'Mouse': ['mouse'],
    'Cameras': ['camera'],
    
    # Plastics
    'Plastic Bottles': ['bottle'],
    'Plastic Bags': ['bag'],
    'Straws': ['straw'],
    'Plastic Cups': ['cup'],
    'Plastic Containers': ['container'],
    
    # E-Waste
    'Circuit Boards': ['board', 'circuit'],
    'Storage Drives': ['drive', 'disk'],
    'Cables': ['cable', 'wire'],
    'Wires': ['wire'],
    'USB Sticks': ['usb', 'stick'],
    
    # Textiles
    'Cotton Fabrics': ['fabric', 'cloth'],
    'Polyester Fabrics': ['fabric'],
    'Wool Fabrics': ['fabric'],
    'Denim': ['jeans'],
    'Fabric': ['fabric'],
    
    # Other
    'Cardboard': ['cardboard', 'box'],
    'Glass Bottles': ['bottle', 'glass'],
    'Metal Cans': ['can', 'tin'],
    
    # Batteries
    'Batteries': ['battery']
}

def classify_image(image_file_path):
    """Use RapidAPI's General Detection API for image classification"""
    url = "https://general-detection.p.rapidapi.com/v1/results"
    querystring = {"algo": "algo1"}
    
    # Ensure the image file exists
    if not os.path.exists(image_file_path):
        print(f"Error: {image_file_path} not found.")
        return None
    
    print(f"Using image file: {image_file_path}")
    
    # Prepare the file for upload
    files = {
        "image": (os.path.basename(image_file_path), open(image_file_path, "rb"), "image/jpeg"),
    }
    
    # Additional form data (like the URL)
    data = {
        "url": ""  # Leave empty if using file upload
    }
    
    # Headers (only API key and host are needed)
    headers = {
        "x-rapidapi-key": "566a6b1d9amsh8049a873803169dp1f2884jsn52eeb9d80e1b",  # Replace with your actual API key
        "x-rapidapi-host": "general-detection.p.rapidapi.com",
    }
    
    try:
        print("Sending request to API...")
        response = requests.post(url, headers=headers, params=querystring, files=files, data=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print("Request sent successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")
        return None

def detect_waste(image_file_path):
    """Hybrid detection using RapidAPI + custom keyword mapping"""
    result = classify_image(image_file_path)
    if result:
        print(f"API Response: {result}")
        
        # Extract detected object classes
        detected_classes = []
        for res in result['results']:
            for entity in res['entities']:
                if entity['kind'] == 'objects':
                    for obj in entity['objects']:
                        for class_entity in obj['entities']:
                            if class_entity['kind'] == 'classes':
                                for class_name, confidence in class_entity['classes'].items():
                                    print(f"Detected Class: {class_name} with confidence {confidence}")
                                    detected_classes.append(class_name)
        
        # Match detected classes against waste categories
        detected_categories = []
        for category, keywords in WASTE_CATEGORIES.items():
            for class_name in detected_classes:
                if any(keyword in class_name.lower() for keyword in keywords):
                    print(f"Match Found: {category} with class {class_name}")
                    detected_categories.append({
                        'category': category,
                        'matched_class': class_name
                    })
        
        # Return best match
        if detected_categories:
            print(f"Best Match: {detected_categories[0]['category']}")
            return {
                'category': detected_categories[0]['category'],
                'all_matches': detected_categories
            }
        else:
            print("No matches found.")
            return {'category': 'Other', 'all_matches': []}
    else:
        print("Failed to retrieve API response.")
        return {'category': 'Other', 'all_matches': []}

def main():
    # Streamlit app configuration
    st.set_page_config(
        page_title="Waste Classifier",
        page_icon="♻️",
        layout="centered"
    )
    
    inject_custom_css()
    
    # App header
    st.title("♻️ Smart Waste Classifier")
    st.subheader("Upload an image to identify proper disposal methods")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=False
    )
    
    if uploaded_file is not None:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        # Display uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        # Process image
        with st.spinner("Analyzing waste..."):
            result = detect_waste(tmp_path)
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        # Display results
        if result['category'] != 'Other':
            st.success(f"**Detected Category:** {result['category']}")
            
            # Display disposal and recycling info (connect to your database here later)
            with st.expander("♻️ Recycling Methods"):
                st.write("Display recycling methods from database here")
                
            with st.expander("🗑️ Disposal Methods"):
                st.write("Display disposal methods from database here")
            
            # Show all potential matches
            if result['all_matches']:
                with st.expander("🔍 All Potential Matches"):
                    for match in result['all_matches']:
                        st.write(f"- {match['category']} ({match['matched_class']})")
        else:
            st.warning("No recognized waste category found")

if __name__ == "__main__":
    # Check for API key
    if "x-rapidapi-key" not in st.secrets:
        st.error("Missing API key in secrets.toml")
    else:
        main()
