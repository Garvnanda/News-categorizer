import os
import json
from model_registry import MODEL_REGISTRY

def main():
    print("--- Verifying Milestone 5 ---")
    
    models_dir = 'saved_models'
    metrics_dir = os.path.join(models_dir, 'metrics')
    
    # 1. Check leaderboard
    leaderboard_path = os.path.join(metrics_dir, 'leaderboard.json')
    assert os.path.exists(leaderboard_path), f"Missing: {leaderboard_path}"
    
    with open(leaderboard_path, 'r') as f:
        leaderboard = json.load(f)
        
    assert len(leaderboard) == len(MODEL_REGISTRY), "Leaderboard doesn't have all models."
    
    # Check it's sorted descending by accuracy
    accs = [m['accuracy'] for m in leaderboard]
    assert accs == sorted(accs, reverse=True), "Leaderboard is not sorted by accuracy descending!"
    
    # 2. Check each model
    for model_id in MODEL_REGISTRY.keys():
        joblib_path = os.path.join(models_dir, f'{model_id}.joblib')
        json_path = os.path.join(metrics_dir, f'{model_id}.json')
        
        assert os.path.exists(joblib_path), f"Missing model: {joblib_path}"
        assert os.path.exists(json_path), f"Missing metrics: {json_path}"
        
        with open(json_path, 'r') as f:
            data = json.load(f)
            
        # Verify schema keys
        expected_keys = ['model_id', 'display_name', 'category', 'one_liner', 'explanation', 'pros', 'cons', 'best_for', 'metrics', 'timing', 'top_features_per_class']
        for key in expected_keys:
            assert key in data, f"{model_id}.json missing key: {key}"
            
        assert 'plain_language' in data['explanation']
        assert 'formula' in data['explanation']
        assert 'accuracy' in data['metrics']
        assert 'confusion_matrix' in data['metrics']
        assert 'train_seconds' in data['timing']
        assert 'avg_inference_ms' in data['timing']
        
        # Verify top features has entries for our classes
        labels_order = data['metrics']['labels_order']
        for label in labels_order:
            assert label in data['top_features_per_class'], f"Missing top features for class {label} in {model_id}"
            assert len(data['top_features_per_class'][label]) > 0
            
    print("[SUCCESS] Milestone 5 Verification Passed! All schemas and models are correct.")

if __name__ == "__main__":
    main()
