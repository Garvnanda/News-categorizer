import pandas as pd
import string
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS

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

def preprocess_data(df):
    """Cleans the text and implements TF-IDF vectorization."""
    # Handle missing values
    df['headline'] = df['headline'].fillna('')
    df['short_description'] = df['short_description'].fillna('')
    
    # Create combined text column
    df['text'] = df['headline'] + ' ' + df['short_description']
    
    # Clean the text
    df['cleaned_text'] = df['text'].apply(clean_text)
    
    # Implement TF-IDF vectorization
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_df=0.9, min_df=2, sublinear_tf=True)
    tfidf_matrix = vectorizer.fit_transform(df['cleaned_text'])
    
    return df, tfidf_matrix, vectorizer

def load_and_preprocess_data(filepath):
    df = load_data(filepath)
    return preprocess_data(df)
