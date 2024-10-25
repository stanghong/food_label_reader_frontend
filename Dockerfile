# Use the official Python image as a base
FROM python:3.9.6

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt first, to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of your app's code
COPY . .

# Expose port 8501
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "minimum_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]

