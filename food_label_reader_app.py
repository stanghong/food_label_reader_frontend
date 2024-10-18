import streamlit as st
import requests
from PIL import Image as PILImage
from io import BytesIO

# Replace with your actual API endpoint
API_URL = 'https://foodlabelreaderapi-production.up.railway.app/api/food-label-reader/'

# Streamlit UI components
st.title("Food Label Reader")

# Initialize session state for image URL
if 'processed_image_url' not in st.session_state:
    st.session_state['processed_image_url'] = None
if 'extracted_labels' not in st.session_state:
    st.session_state['extracted_labels'] = ""
if 'health_recommendations' not in st.session_state:
    st.session_state['health_recommendations'] = ""

# Image uploader
uploaded_image = st.file_uploader("Upload an image with a food label", type=["jpg", "jpeg", "png"], key='image_uploader')
if uploaded_image:
    # Display the uploaded image
    image = PILImage.open(uploaded_image)
    st.image(image, caption='Uploaded Image')

    # Upload image to the API and get the response
    try:
        # Prepare the file for upload
        files = {'image': (uploaded_image.name, uploaded_image, 'image/jpeg')}
        
        # Send request to the API
        response = requests.post(API_URL, files=files)
        
        # Check the status and process the response
        if response.status_code == 200:
            data = response.json()
            st.session_state['processed_image_url'] = data.get('processed_image_url', 'No URL available')
            st.session_state['extracted_labels'] = data.get('extracted_labels', 'No labels extracted')
            st.session_state['health_recommendations'] = data.get('health_recommendations', 'No recommendations available')
        else:
            st.error(f"Server returned an error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Failed to send image to the server: {str(e)}")

# Display the results
if st.session_state['processed_image_url']:
    st.markdown(f"**Processed Image URL:** [View Image]({st.session_state['processed_image_url']})")
if st.session_state['extracted_labels']:
    st.markdown(f"**Extracted Labels:** {st.session_state['extracted_labels']}")
if st.session_state['health_recommendations']:
    st.markdown(f"**Health Recommendations:** {st.session_state['health_recommendations']}")
