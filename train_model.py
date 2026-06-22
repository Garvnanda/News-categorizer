import data_loader
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import os

def main():
    print("Loading and preprocessing data...")
    df, tfidf_matrix, vectorizer = data_loader.load_and_preprocess_data('news_data.csv')
    
    print("Splitting data into training and testing sets (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        tfidf_matrix, 
        df['category'], 
        test_size=0.2, 
        random_state=42
    )
    
    print("Training Logistic Regression model...")
    # Increase max_iter to ensure convergence and tune C parameter for better accuracy
    model = LogisticRegression(max_iter=1000, C=5.0)
    model.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)
    
    print("\n--- Classification Report ---")
    print(report)
    print("-----------------------------\n")
    
    print("Saving model and vectorizer...")
    joblib.dump(model, 'model.joblib')
    joblib.dump(vectorizer, 'vectorizer.joblib')
    print("Saved as model.joblib and vectorizer.joblib.")

if __name__ == "__main__":
    main()
