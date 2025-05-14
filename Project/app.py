import streamlit as st
import requests
import os
import tempfile
import mysql.connector

# Custom CSS placeholder
CUSTOM_CSS = """
<style>
/* Add custom CSS here later */
</style>
"""

def inject_custom_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Database configuration
def get_db_connection():
    return mysql.connector.connect(
        host=st.secrets["DB_HOST"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        database=st.secrets["DB_NAME"],
        port=st.secrets["DB_PORT"]
    )

# Fetch disposal/recycle methods from database
def get_waste_info(category_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Map category to table name
        table_mapping = {
            'Plastic Bottles': 'Plastics',
            'Plastic Bags': 'Plastics',
            'Plastic Cups': 'Plastics',
            'Plastic Containers': 'Plastics',
            'Straws': 'Plastics',
            'Smartphones': 'Electronics',
            'Laptops': 'Electronics',
            'Tablets': 'Electronics',
            'Speakers': 'Electronics',
            'Headphones': 'Electronics',
            'Keyboards': 'Electronics',
            'Mouse': 'Electronics',
            'Cameras': 'Electronics',
            'Circuit Boards': 'E_Waste',
            'Storage Drives': 'E_Waste',
            'Cables': 'E_Waste',
            'Wires': 'E_Waste',
            'USB Sticks': 'E_Waste',
            'Cotton Fabrics': 'Textiles',
            'Polyester Fabrics': 'Textiles',
            'Wool Fabrics': 'Textiles',
            'Denim': 'Textiles',
            'Fabric': 'Textiles',
            'Cardboard': 'Other_Waste',
            'Glass Bottles': 'Other_Waste',
            'Metal Cans': 'Other_Waste',
            'Batteries': 'Batteries'
        }
        
        table_name = table_mapping.get(category_name, 'Plastics')  # Default to Plastics
        
        query = f"""
        SELECT dispose, recycle, invalid 
        FROM {table_name}
        WHERE img_label = %s
        """
        cursor.execute(query, (category_name,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result and not result['invalid']:
            # print(f"Disposal: {result['dispose']}, Recycling: {result['recycle']}")
            return {
                'dispose': result['dispose'].split(', '),
                'recycle': result['recycle'].split(', ')
            }
        return None
    
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return None

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
        "x-rapidapi-key": st.secrets["x-rapidapi-key"],
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
    st.set_page_config(
        page_title="Waste Classifier",
        page_icon="♻️",
        layout="centered"
    )
    inject_custom_css()
    
    st.title("♻️ JunkBuddy \(◕‿◕)/ ")
    st.subheader(" Waste Classification and Recycling Helper ")
    
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=["jpg", "jpeg", "png"]
    )
    
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        st.image(uploaded_file, use_container_width=True)
        
        with st.spinner("Analyzing waste..."):
            result = detect_waste(tmp_path)
        
        os.unlink(tmp_path)
        
        if result['category'] != 'Other':
            st.success(f"**Detected Category:** {result['category']}")
            waste_info = get_waste_info(result['category'])
            
            if waste_info:
                with st.expander("♻️ Recycling Methods"):
                    for method in waste_info['recycle']:
                        st.markdown(f"- {method.strip()}")
                        # print(f"Recycling method: {method.strip()}")
                        
                with st.expander("🗑️ Disposal Methods"):
                    for method in waste_info['dispose']:
                        st.markdown(f"- {method.strip()}")
                        # print(f"Disposal method: {method.strip()}")
            else:
                st.warning("No disposal/recycling info found in database")
            
            if result['all_matches']:
                with st.expander("🔍 All Potential Matches"):
                    for match in result['all_matches']:
                        st.write(f"- {match['category']} ({match['matched_class']})")
        else:
            st.warning("No recognized waste category found")

if __name__ == "__main__":
    required_secrets = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME", "DB_PORT", "x-rapidapi-key"]
    
    # Check if all required secrets are available
    if all(key in st.secrets for key in required_secrets):
        if "x-rapidapi-key" in st.secrets:
            main()
        else:
            st.error("Missing API key in secrets.toml")
    else:
        st.error("Missing database credentials in secrets.toml")

# This script is a Streamlit application that allows users to upload an image of waste and classify it into various categories using a machine learning model. The app uses the RapidAPI General Detection API for image classification and has a custom CSS placeholder for future styling.
# The waste categories are defined in a dictionary, and the app matches detected classes against these categories. The app also provides a file uploader for users to upload images and displays the results of the classification.
# The app is designed to be user-friendly and provides feedback on the classification process, including potential matches and disposal methods.
# The script includes error handling for API requests and temporary file management for uploaded images. The main function initializes the Streamlit app and handles user interactions.
# The app is set to run in a centered layout with a title and subheader for clarity. The code is structured to be modular, allowing for easy updates and enhancements in the future.
# The script is ready for deployment and can be run using Streamlit's command-line interface.
# The app is designed to be responsive and can handle various image formats, making it versatile for different use cases.
# The app is also designed to be scalable, allowing for future integration with a database for recycling and disposal methods.
# The app is built with best practices in mind, ensuring maintainability and readability for future developers.
