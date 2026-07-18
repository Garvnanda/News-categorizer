import os
import joblib
import pandas as pd
import string
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.model_selection import train_test_split

def clean_text(text):
    if not isinstance(text, str):
        return ""
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Remove stop words
    words = text.split()
    words = [w for w in words if w not in ENGLISH_STOP_WORDS]
    return ' '.join(words)

def load_data(filepath):
    """Loads the dataset using pandas."""
    return pd.read_csv(filepath)

def prepare_and_save_data(df, save_dir='saved_models'):
    """Cleans text, splits data, vectorizes, and saves artifacts."""
    # Handle missing values
    df['headline'] = df['headline'].fillna('')
    df['short_description'] = df['short_description'].fillna('')
    
    # Create combined text column
    df['text'] = df['headline'] + ' ' + df['short_description']
    
    # Clean the text
    print("Cleaning text...")
    df['cleaned_text'] = df['text'].apply(clean_text)
    
    # Split the data (80% train, 20% test, stratified)
    print("Splitting data...")
    X = df['cleaned_text']
    y = df['category']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    
    # Implement TF-IDF vectorization (fit on training only)
    print("Fitting TF-IDF...")
    vectorizer = TfidfVectorizer(max_features=15000, ngram_range=(1, 2), min_df=3)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    # Save to disk
    print("Saving artifacts...")
    os.makedirs(save_dir, exist_ok=True)
    
    joblib.dump(vectorizer, os.path.join(save_dir, 'vectorizer.joblib'))
    
    # Save the splits so all models train on the identical dataset
    training_data = {
        'X_train_tfidf': X_train_tfidf,
        'X_test_tfidf': X_test_tfidf,
        'y_train': y_train,
        'y_test': y_test
    }
    joblib.dump(training_data, os.path.join(save_dir, 'training_data.joblib'))
    print(f"Saved artifacts to {save_dir}/")
    
    return vectorizer, training_data

def run_data_pipeline(filepath, save_dir='saved_models'):
    df = load_data(filepath)
    return prepare_and_save_data(df, save_dir)
