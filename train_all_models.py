import os
import time
import json
import joblib
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report, confusion_matrix
from model_registry import MODEL_REGISTRY

def get_class_conditional_top_features(X_train, y_train, feature_names, top_n=10):
    """Fallback method to get 'typical' words per class using TF-IDF means."""
    classes = np.unique(y_train)
    top_features = {}
    for cls in classes:
        cls_indices = np.where(y_train == cls)[0]
        cls_mean_tfidf = np.asarray(X_train[cls_indices].mean(axis=0)).flatten()
        top_indices = cls_mean_tfidf.argsort()[-top_n:][::-1]
        top_features[cls] = [feature_names[i] for i in top_indices]
    return top_features

def extract_top_features(model, feature_names, classes, fallback_features, top_n=10):
    """Extracts top features per class if the model supports it, else uses fallback."""
    top_features = {}
    
    if hasattr(model, 'coef_'):
        coefs = model.coef_
        if coefs.shape[0] == 1 and len(classes) == 2:
            pass
        else:
            for i, cls in enumerate(classes):
                top_indices = coefs[i].argsort()[-top_n:][::-1]
                top_features[cls] = [feature_names[idx] for idx in top_indices]
        return top_features
    
    if hasattr(model, 'feature_log_prob_'):
        for i, cls in enumerate(classes):
            top_indices = model.feature_log_prob_[i].argsort()[-top_n:][::-1]
            top_features[cls] = [feature_names[idx] for idx in top_indices]
        return top_features
        
    if hasattr(model, 'calibrated_classifiers_') or hasattr(model, 'estimators_'):
        try:
            if hasattr(model, 'calibrated_classifiers_'):
                base = model.calibrated_classifiers_[0].estimator
            else:
                base = model.estimators_[0].estimator
                
            if hasattr(base, 'coef_'):
                coefs = base.coef_
                for i, cls in enumerate(classes):
                    top_indices = coefs[i].argsort()[-top_n:][::-1]
                    top_features[cls] = [feature_names[idx] for idx in top_indices]
                return top_features
        except:
            pass
            
    return fallback_features

def main():
    print("Loading data and vectorizer...")
    vectorizer = joblib.load('saved_models/vectorizer.joblib')
    training_data = joblib.load('saved_models/training_data.joblib')
    
    X_train = training_data['X_train_tfidf']
    X_test = training_data['X_test_tfidf']
    y_train = np.array(training_data['y_train'])
    y_test = np.array(training_data['y_test'])
    
    feature_names = vectorizer.get_feature_names_out()
    classes = np.unique(y_train)
    labels_order = list(classes)
    
    print("Computing class-conditional TF-IDF means for fallback feature extraction...")
    fallback_features = get_class_conditional_top_features(X_train, y_train, feature_names)
    
    os.makedirs('saved_models/metrics', exist_ok=True)
    leaderboard = []
    
    for model_id, config in MODEL_REGISTRY.items():
        print(f"\n--- Training {config['display_name']} ---")
        model = config['estimator']
        
        t0 = time.time()
        model.fit(X_train, y_train)
        train_seconds = time.time() - t0
        
        t0 = time.time()
        y_pred = model.predict(X_test)
        inference_seconds = time.time() - t0
        avg_inference_ms = (inference_seconds / len(y_test)) * 1000
        
        acc = accuracy_score(y_test, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='macro', zero_division=0)
        
        report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
        per_class = {cls: report[cls] for cls in labels_order if cls in report}
        
        cm = confusion_matrix(y_test, y_pred, labels=labels_order)
        
        top_features = extract_top_features(model, feature_names, classes, fallback_features)
        
        metrics_json = {
            "model_id": model_id,
            "display_name": config['display_name'],
            "category": config['category'],
            "one_liner": config['one_liner'],
            "explanation": config['explanation'],
            "how_it_differs": config.get('how_it_differs', ''),
            "pros": config['pros'],
            "cons": config['cons'],
            "best_for": config['best_for'],
            "metrics": {
                "accuracy": round(acc, 4),
                "macro_f1": round(f1, 4),
                "macro_precision": round(precision, 4),
                "macro_recall": round(recall, 4),
                "per_class": per_class,
                "confusion_matrix": cm.tolist(),
                "labels_order": labels_order
            },
            "timing": {
                "train_seconds": round(train_seconds, 4),
                "avg_inference_ms": round(avg_inference_ms, 4)
            },
            "top_features_per_class": top_features
        }
        
        joblib.dump(model, f'saved_models/{model_id}.joblib')
        with open(f'saved_models/metrics/{model_id}.json', 'w') as f:
            json.dump(metrics_json, f, indent=2)
            
        print(f"Accuracy: {acc:.4f} | Train Time: {train_seconds:.2f}s | Infer: {avg_inference_ms:.3f}ms")
        
        leaderboard.append({
            "model_id": model_id,
            "display_name": config['display_name'],
            "accuracy": round(acc, 4),
            "macro_f1": round(f1, 4),
            "train_seconds": round(train_seconds, 4),
            "avg_inference_ms": round(avg_inference_ms, 4)
        })
        
    leaderboard.sort(key=lambda x: x['accuracy'], reverse=True)
    with open('saved_models/metrics/leaderboard.json', 'w') as f:
        json.dump(leaderboard, f, indent=2)
        
    print("\nAll models trained and evaluated. Leaderboard saved.")

if __name__ == "__main__":
    main()
