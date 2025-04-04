from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import torch
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Transformer Model Service")

# Initialize the model
MODEL_NAME = os.getenv("MODEL_NAME", "distilbert-base-uncased-finetuned-sst-2-english")
classifier = None

class TextInput(BaseModel):
    text: str

class PredictionOutput(BaseModel):
    label: str
    score: float

@app.on_event("startup")
async def startup_event():
    global classifier
    try:
        logger.info(f"Loading model: {MODEL_NAME}")
        classifier = pipeline("sentiment-analysis", model=MODEL_NAME)
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: TextInput):
    if classifier is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Get prediction
        result = classifier(input_data.text)[0]
        
        return PredictionOutput(
            label=result['label'],
            score=result['score']
        )
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 