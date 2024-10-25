
# %%
# Streamlit frontend for the food label reader

import streamlit as st
import requests
from PIL import Image as PILImage
from io import BytesIO
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
_ = load_dotenv(find_dotenv())

# Ensure the API URL is properly formatted
API_URL = os.getenv('API_URL', 'https://foodlabelreaderapi-production.up.railway.app/api/food-label-reader/')
if not API_URL.startswith(('http://', 'https://')):
    st.error("Invalid API URL. Please make sure it starts with 'http://' or 'https://'.")
#     st.stop()
# API_URL = os.getenv('API_URL', 'http://127.0.0÷.1:8000/api/food-label-reader/')

# Streamlit UI components
st.title("NutriSnap: Eat Smart, Live Better")

# Initialize session state for the API response data
if 'processed_image_url' not in st.session_state:
    st.session_state['processed_image_url'] = None
if 'extracted_labels' not in st.session_state:
    st.session_state['extracted_labels'] = ""
if 'health_recommendations' not in st.session_state:
    st.session_state['health_recommendations'] = ""
if 'spider_plot_url' not in st.session_state:
    st.session_state['spider_plot_url'] = ""

# Image uploader
uploaded_image = st.file_uploader("Upload an image with a food label", type=["jpg", "jpeg", "png"])

# Check if an image has been uploaded
if uploaded_image:
    # Display the uploaded image
    image = PILImage.open(uploaded_image)
    st.image(image, caption='Uploaded Image')

    # Button to send the image to the API
    if st.button("Analyze Image"):
        # Prepare the image for upload
        try:
            # Convert the image to RGB format (to ensure compatibility with JPEG/PNG)
            image = image.convert('RGB')

            # Resize the image if it's too large (e.g., max dimension 2048x2048)
            max_size = (2048, 2048)
            image.thumbnail(max_size)

            # Save the image to a BytesIO object in the correct format
            buffer = BytesIO()
            image.save(buffer, format="JPEG")
            buffer.seek(0)

            # Prepare the file for the API request
            files = {'image': (uploaded_image.name, buffer, 'image/jpeg')}
            
            # Send the request to the API
            response = requests.post(API_URL, files=files)

            # Check the status and process the response
            if response.status_code == 200:
                data = response.json()
                st.session_state['processed_image_url'] = data.get('processed_image_url', 'No URL available')
                st.session_state['extracted_labels'] = data.get('extracted_labels', 'No labels extracted')
                st.session_state['health_recommendations'] = data.get('health_recommendations', 'No recommendations available')
                st.session_state['spider_plot_url'] = data.get('spider_plot_url', 'No plot URL available')
                st.success("Image processed successfully!")
            else:
                st.error(f"Server returned an error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Failed to send image to the server: {str(e)}")

# Display the results if available
if st.session_state['processed_image_url']:
    st.markdown(f"**Processed Image URL:** [View Image]({st.session_state['processed_image_url']})")
if st.session_state['extracted_labels']:
    st.markdown(f"**Extracted Labels:** {st.session_state['extracted_labels']}")
if st.session_state['health_recommendations']:
    st.markdown(f"**Health Recommendations:** {st.session_state['health_recommendations']}")
if st.session_state['spider_plot_url']:
    st.markdown(f"**Spider Plot URL:** [View Image]({st.session_state['spider_plot_url']})")
    # st.markdown(f"**Spider Plot URL:** [View Plot]({st.session_state['spider_plot_url']})")
    # Display the spider plot image directly on the frontend
    response = requests.get(st.session_state['spider_plot_url'])
    if response.status_code == 200:
        spider_plot_image = PILImage.open(BytesIO(response.content))
        st.image(spider_plot_image, caption='Spider Plot')
    else:
        st.error(f"Failed to load spider plot image: {response.status_code}")