from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def main():
    print("Testing POST /predict endpoint...")
    sample_text = "Apple unveils its new iPhone model with an advanced camera and longer battery life."
    
    response = client.post("/predict", json={"text": sample_text})
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response JSON: {response.json()}")
        print("\nAPI verification successful!")
    else:
        print("API verification failed!")

if __name__ == "__main__":
    main()
