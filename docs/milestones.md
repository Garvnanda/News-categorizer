# Project Milestones: News Classifier

## Milestone 1: Data Setup and Preprocessing
- Create `data_loader.py`.
- Load the dataset using pandas.
- Clean the text (lowercase, remove punctuation, remove stop words).
- Implement TF-IDF vectorization.

## Milestone 2: Model Training and Evaluation
- Create `train_model.py`.
- Split data into training (80%) and testing (20%).
- Train a Logistic Regression model.
- Output a classification report (accuracy, precision, recall).
- Save the trained model and vectorizer using `joblib`.

## Milestone 3: The Prediction API
- Create `app.py`.
- Build a basic FastAPI application.
- Load the saved model and vectorizer.
- Create a `POST /predict` endpoint that takes a raw string and returns the predicted category.