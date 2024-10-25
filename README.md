
# NutriSnap

This Streamlit app allows users to upload an image of a food label, sends it to an API for analysis, and displays extracted labels and health recommendations.

## Features
- Upload an image containing a food label (supported formats: JPG, JPEG, PNG).
- The app sends the uploaded image to a specified API endpoint for processing.
- Displays the processed image URL, extracted labels, and health recommendations.

## Prerequisites
- Python 3.x
- Streamlit
- `requests` library
- `Pillow` library for image handling

## Installation

1. Clone this repository or download the code:
   ```bash
   git clone <repository_url>
   cd food-label-reader-app
   ```

2. Install the required libraries:
   ```bash
   pip install streamlit requests pillow
   ```

3. Replace the `API_URL` with your actual API endpoint:
   ```python
   API_URL = 'https://foodlabelreaderapi-production.up.railway.app/api/food-label-reader/'
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open the provided local URL in your web browser.

3. Upload an image containing a food label.

4. View the processed image, extracted labels, and health recommendations returned by the API.

## Example
- **Upload Image**: Upload an image file with a food label.
- **View Processed Image**: A link to view the processed image.
- **Extracted Labels**: Displays the text extracted from the food label.
- **Health Recommendations**: Provides dietary recommendations based on the extracted labels.

## API Endpoint
This app interacts with an external API for processing food label images. The API is expected to accept a POST request with an image file and return a JSON response containing:
- `processed_image_url`: URL of the processed image.
- `extracted_labels`: Text extracted from the image.
- `health_recommendations`: Health-related recommendations based on the labels.

## License
This project is licensed under the MIT License.
