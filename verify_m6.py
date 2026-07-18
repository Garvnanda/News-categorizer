from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def main():
    print("--- Verifying Milestone 6 ---")
    
    # 1. Trigger startup event explicitly since TestClient doesn't do it automatically
    # Wait, TestClient(app) using the context manager *does* trigger startup events.
    # We can do `with TestClient(app) as client:`
    
    with TestClient(app) as client:
        # 1. GET /models
        response = client.get("/models")
        assert response.status_code == 200
        models = response.json()
        assert len(models) == 6, "Expected 6 models in registry."
        assert "accuracy" in models[0], "Missing accuracy in summary."
        print("[x] GET /models returned 6 items.")
        
        # 2. GET /models/{model_id}
        response = client.get("/models/logistic_regression")
        assert response.status_code == 200
        data = response.json()
        assert data['model_id'] == 'logistic_regression'
        assert 'metrics' in data
        print("[x] GET /models/{model_id} returned full JSON.")
        
        # 3. Invalid model_id 404
        response = client.get("/models/fake_model")
        assert response.status_code == 404
        print("[x] GET /models/fake_model returned 404.")
        
        # 4. POST /predict
        payload = {"text": "A new sports team won the big championship game.", "model_id": "logistic_regression"}
        response = client.post("/predict", json=payload)
        assert response.status_code == 200, f"Error: {response.text}"
        res_data = response.json()
        assert "predicted_category" in res_data
        assert "confidence" in res_data
        assert "probabilities" in res_data
        assert "top_contributing_words" in res_data
        assert len(res_data["probabilities"]) == 10, "Expected 10 class probabilities"
        print(f"[x] POST /predict returned category: {res_data['predicted_category']} with {len(res_data['top_contributing_words'])} top words.")
        
        # 5. POST /predict/compare
        compare_payload = {"text": "A huge business merger was announced today in the stock market."}
        response = client.post("/predict/compare", json=compare_payload)
        assert response.status_code == 200, f"Error: {response.text}"
        compare_data = response.json()
        assert len(compare_data) == 6, "Expected 6 compare results."
        assert "predicted_category" in compare_data[0]
        assert "confidence" in compare_data[0]
        print("[x] POST /predict/compare returned 6 predictions.")
        
        # 6. GET /leaderboard
        response = client.get("/leaderboard")
        assert response.status_code == 200
        leaderboard = response.json()
        assert len(leaderboard) == 6
        assert leaderboard[0]['accuracy'] >= leaderboard[-1]['accuracy'], "Leaderboard not sorted."
        print("[x] GET /leaderboard returned valid data.")
        
    print("\n[SUCCESS] Milestone 6 Verification Passed! All endpoints are working.")

if __name__ == "__main__":
    main()
