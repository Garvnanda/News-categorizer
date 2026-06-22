from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
from data_loader import clean_text

app = FastAPI(title="News Classifier API", description="API for predicting news categories from text.")

# Attempt to load model and vectorizer
try:
    model = joblib.load('model.joblib')
    vectorizer = joblib.load('vectorizer.joblib')
except Exception as e:
    model = None
    vectorizer = None
    print(f"Error loading models: {e}. Please ensure 'model.joblib' and 'vectorizer.joblib' exist.")

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    category: str

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    if model is None or vectorizer is None:
        raise HTTPException(status_code=500, detail="Model is not loaded.")
    
    # Preprocess the text
    cleaned_text = clean_text(request.text)
    
    # Vectorize
    vectorized_text = vectorizer.transform([cleaned_text])
    
    # Predict
    prediction = model.predict(vectorized_text)[0]
    
    return PredictResponse(category=prediction)
