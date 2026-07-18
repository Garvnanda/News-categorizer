import os
import joblib
from data_loader import run_data_pipeline

def main():
    print("Running data pipeline to generate artifacts...")
    run_data_pipeline('news_data.csv')
    
    vectorizer_path = 'saved_models/vectorizer.joblib'
    training_data_path = 'saved_models/training_data.joblib'
    
    print("\n--- Verifying Milestone 4 ---")
    
    # 1. Assert files exist
    assert os.path.exists(vectorizer_path), f"File missing: {vectorizer_path}"
    assert os.path.exists(training_data_path), f"File missing: {training_data_path}"
    print("[x] Artifact files exist.")
    
    # 2. Assert they load correctly
    try:
        vectorizer = joblib.load(vectorizer_path)
        training_data = joblib.load(training_data_path)
        print("[x] Artifacts loaded successfully.")
    except Exception as e:
        assert False, f"Failed to load artifacts: {e}"
        
    # 3. Assert train/test class distributions are balanced (stratified)
    y_train = training_data['y_train']
    y_test = training_data['y_test']
    
    train_dist = y_train.value_counts(normalize=True)
    test_dist = y_test.value_counts(normalize=True)
    
    for category in train_dist.index:
        train_prop = train_dist[category]
        test_prop = test_dist.get(category, 0)
        # Check that proportions are close (within 1% difference)
        diff = abs(train_prop - test_prop)
        assert diff < 0.01, f"Distribution mismatch for {category}: train={train_prop:.4f}, test={test_prop:.4f}"
    print("\n[SUCCESS] Milestone 4 Verification Passed!")

if __name__ == "__main__":
    main()
