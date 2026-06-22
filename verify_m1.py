import data_loader
import pandas as pd
import sys

def main():
    try:
        df, tfidf_matrix, vectorizer = data_loader.load_and_preprocess_data('news_data.csv')
        print("Data loaded successfully.")
        print(f"Shape of dataframe: {df.shape}")
        print(f"Shape of TF-IDF matrix: {tfidf_matrix.shape}")
        
        # We'll print the markdown of the head
        print("\n---MARKDOWN_START---")
        print(df[['category', 'headline', 'cleaned_text']].head().to_markdown(index=False))
        print("---MARKDOWN_END---")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
