const express = require('express');
const multer = require('multer');
const axios = require('axios');
const path = require('path');
const fs = require('fs');

// Replace with your actual API endpoint
const API_URL = 'https://foodlabelreaderapi-production.up.railway.app/api/food-label-reader/';

const app = express();
const port = process.env.PORT || 3000;

// Set up multer for handling file uploads
const upload = multer({ dest: 'uploads/' });

app.use(express.static('public')); // Serve static files from the "public" folder

// Endpoint for serving the frontend form
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Endpoint to handle image uploads
app.post('/upload', upload.single('image'), async (req, res) => {
    try {
        const imagePath = req.file.path;
        const image = fs.createReadStream(imagePath);

        // Send the image to the API
        const response = await axios.post(API_URL, {
            image: image
        }, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });

        // Clean up the uploaded file
        fs.unlinkSync(imagePath);

        // Extract the data from the API response
        const { processed_image_url, extracted_labels, health_recommendations } = response.data;

        // Send the data back to the client
        res.json({
            processed_image_url,
            extracted_labels,
            health_recommendations
        });
    } catch (error) {
        console.error('Error processing image:', error.message);
        res.status(500).json({ error: 'Failed to process image' });
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
