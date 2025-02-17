from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image
import io
from model import get_model
from utils import preprocess_image

app = FastAPI(title="MNIST Classification API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model at startup
model = get_model()

@app.get("/")
async def root():
    return {"message": "MNIST Classification API"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read image
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    
    # Preprocess image
    processed_image = preprocess_image(image)
    
    # Make prediction
    prediction = model.predict(np.expand_dims(processed_image, axis=0))
    predicted_class = np.argmax(prediction[0])
    confidence = float(prediction[0][predicted_class])
    
    return {
        "predicted_digit": int(predicted_class),
        "confidence": confidence
    }