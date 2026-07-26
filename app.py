from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import joblib
import json
import os
import numpy as np
from data_loader import clean_text

app = FastAPI(title="News Classifier API", description="API for predicting news categories from text.")

MODEL_REGISTRY = {}
VECTORIZER = None
LEADERBOARD = []

@app.on_event("startup")
def load_models():
    global VECTORIZER, LEADERBOARD, MODEL_REGISTRY
    try:
        VECTORIZER = joblib.load('saved_models/vectorizer.joblib')
        
        with open('saved_models/metrics/leaderboard.json', 'r') as f:
            LEADERBOARD = json.load(f)
            
        for item in LEADERBOARD:
            model_id = item['model_id']
            # Load model
            model_path = f'saved_models/{model_id}.joblib'
            model = joblib.load(model_path)
            
            # Load metrics
            metrics_path = f'saved_models/metrics/{model_id}.json'
            with open(metrics_path, 'r') as f:
                metrics_json = json.load(f)
                
            MODEL_REGISTRY[model_id] = {
                'model': model,
                'metrics': metrics_json
            }
        print(f"Loaded {len(MODEL_REGISTRY)} models successfully.")
    except Exception as e:
        print(f"Error loading models on startup: {e}")

class PredictRequest(BaseModel):
    text: str
    model_id: str = "logistic_regression"

class PredictResponse(BaseModel):
    predicted_category: str
    confidence: float
    probabilities: Dict[str, float]
    top_contributing_words: List[str]
    
class CompareRequest(BaseModel):
    text: str

@app.get("/models")
def get_models():
    summaries = []
    for model_id, data in MODEL_REGISTRY.items():
        metrics = data['metrics']
        summaries.append({
            "model_id": metrics['model_id'],
            "display_name": metrics['display_name'],
            "category": metrics['category'],
            "one_liner": metrics['one_liner'],
            "accuracy": metrics['metrics']['accuracy']
        })
    return summaries

@app.get("/models/{model_id}")
def get_model_details(model_id: str):
    if model_id not in MODEL_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Model {model_id} not found.")
    return MODEL_REGISTRY[model_id]['metrics']

@app.get("/leaderboard")
def get_leaderboard():
    return LEADERBOARD

def get_linear_top_words(model, model_id, vectorized_text, feature_names, predicted_category, metrics_json):
    nonzero_indices = vectorized_text.nonzero()[1]
    if len(nonzero_indices) == 0:
        return []
        
    labels_order = metrics_json['metrics']['labels_order']
    
    try:
        class_idx = list(model.classes_).index(predicted_category) if hasattr(model, 'classes_') else labels_order.index(predicted_category)
    except ValueError:
        class_idx = labels_order.index(predicted_category)
    
    coefs = None
    if hasattr(model, 'coef_'):
        coefs = model.coef_
    elif hasattr(model, 'feature_log_prob_'):
        coefs = model.feature_log_prob_
    elif hasattr(model, 'calibrated_classifiers_'):
        try:
            base = model.calibrated_classifiers_[0].estimator
            if hasattr(base, 'coef_'):
                coefs = base.coef_
        except:
            pass
    elif hasattr(model, 'estimators_'):
        try:
            base = model.estimators_[0].estimator
            if hasattr(base, 'coef_'):
                coefs = base.coef_
        except:
            pass
            
    if coefs is not None and len(coefs.shape) > 1 and coefs.shape[0] > class_idx:
        class_coefs = coefs[class_idx]
        word_weights = [(feature_names[idx], class_coefs[idx]) for idx in nonzero_indices]
        word_weights.sort(key=lambda x: x[1], reverse=True)
        return [w[0] for w in word_weights[:10]]
    return metrics_json['top_features_per_class'].get(predicted_category, [])

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    if not VECTORIZER or not MODEL_REGISTRY:
        raise HTTPException(status_code=500, detail="Models not loaded.")
        
    if request.model_id not in MODEL_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Model {request.model_id} not found.")
        
    registry_entry = MODEL_REGISTRY[request.model_id]
    model = registry_entry['model']
    metrics_json = registry_entry['metrics']
    labels_order = metrics_json['metrics']['labels_order']
    cleaned_text = clean_text(request.text)
    vectorized_text = VECTORIZER.transform([cleaned_text])
    
    prediction_idx = model.predict(vectorized_text)[0]
    predicted_category = str(prediction_idx)
    
    if hasattr(model, 'predict_proba'):
        probs = model.predict_proba(vectorized_text)[0]
    else:
        probs = [1.0 if str(c) == predicted_category else 0.0 for c in labels_order]
        
    classes = model.classes_ if hasattr(model, 'classes_') else labels_order
    probabilities = {str(c): float(p) for c, p in zip(classes, probs)}
    confidence = probabilities.get(predicted_category, 0.0)
    
    feature_names = VECTORIZER.get_feature_names_out()
    top_words = get_linear_top_words(model, request.model_id, vectorized_text, feature_names, predicted_category, metrics_json)
    
    return PredictResponse(
        predicted_category=predicted_category,
        confidence=confidence,
        probabilities=probabilities,
        top_contributing_words=top_words
    )

@app.post("/predict/compare")
def predict_compare(request: CompareRequest):
    if not VECTORIZER or not MODEL_REGISTRY:
        raise HTTPException(status_code=500, detail="Models not loaded.")
        
    cleaned_text = clean_text(request.text)
    vectorized_text = VECTORIZER.transform([cleaned_text])
    
    results = []
    for model_id, registry_entry in MODEL_REGISTRY.items():
        model = registry_entry['model']
        metrics = registry_entry['metrics']
        
        predicted_category = str(model.predict(vectorized_text)[0])
        
        if hasattr(model, 'predict_proba'):
            probs = model.predict_proba(vectorized_text)[0]
            classes = model.classes_ if hasattr(model, 'classes_') else metrics['metrics']['labels_order']
            prob_dict = {str(c): float(p) for c, p in zip(classes, probs)}
            confidence = prob_dict.get(predicted_category, 0.0)
        else:
            confidence = 1.0
            
        results.append({
            "model_id": model_id,
            "display_name": metrics['display_name'],
            "predicted_category": predicted_category,
            "confidence": confidence
        })
        
    return results
