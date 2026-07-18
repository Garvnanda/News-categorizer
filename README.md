# Multi-Algorithm News Classifier

Welcome to the Multi-Algorithm News Classifier! This project is an interactive educational dashboard designed to classify news headlines and descriptions into 10 categories. Rather than just serving a single model, this platform trains, evaluates, and compares **six different machine learning algorithms** on the exact same dataset to demonstrate their relative strengths, weaknesses, and theoretical differences.

## 🏗️ Architecture

The project is split into an offline training pipeline and an online serving pipeline.

```text
[ Offline Training Phase ]
news_data.csv 
  └──> data_loader.py (Cleans text, Stratified 80/20 split, fits shared TF-IDF)
         └──> train_all_models.py (Orchestrates training across 6 algorithms)
                ├──> saved_models/*.joblib (Trained model weights)
                └──> saved_models/metrics/*.json (Standardized UI contracts + Leaderboard)

[ Online Inference Phase ]
app.py (FastAPI) 
  ├── Loads all .joblib models and .json metadata into RAM at startup
  └── Exposes /models, /predict, /predict/compare, and /leaderboard endpoints
         ^
         | (HTTP)
         v
streamlit_app.py (Frontend)
  ├── 4-Page Interactive Dashboard (Predict, Explore, Leaderboard, Compare)
  └── Renders metrics, LaTeX formulas, and Plotly charts dynamically
```

### Design Principle: The Shared Vectorizer
All 6 models are compared on equal footing. They share a single `TfidfVectorizer` (capped at 15,000 features) fit exclusively on a static 80% training split. This guarantees that any difference in accuracy or latency between the models is due purely to the algorithmic approach, not the data preparation.

---

## 🧠 The Six Models: What They Teach Us

| Model | Category | Core Teaching Takeaway |
| :--- | :--- | :--- |
| **Logistic Regression** | Linear / Probabilistic | The gold standard baseline. It proves that a simple linear combination of word weights is incredibly effective and fast for high-dimensional text classification. |
| **Multinomial Naive Bayes** | Probabilistic | Demonstrates how the "naive" assumption of word independence allows for near-instantaneous training by simply counting probabilities, at the cost of a slight accuracy drop. |
| **Linear SVM** | Margin-based | Shows that maximizing the decision boundary (margin) between classes often yields the absolute highest accuracy for sparse text data, though it requires calibration to output probabilities. |
| **Decision Tree** | Tree-based | A highly interpretable flowchart model. However, it demonstrates severe **overfitting** when trained alone on 15,000 features, resulting in the lowest test accuracy. |
| **Random Forest** | Tree Ensemble | Demonstrates how ensembling (averaging 200 trees) fixes the Decision Tree's overfitting problem, capturing complex non-linear patterns at the cost of memory and speed. |
| **K-Nearest Neighbors** | Instance-based | Highlights the **curse of dimensionality**. With zero training time (it just memorizes data), it struggles to compute distance metrics effectively across 15,000 dimensions and is incredibly slow during inference. |

---

## 🚀 How to Run

### 1. Train the Models (Offline Phase)
Before launching the server, you must train the models and generate the artifacts.
```bash
python train_all_models.py
```
*(Note: Random Forest and SVM might take a couple of minutes to train over 15,000 features).*

### 2. Launch the API Backend
The backend uses FastAPI and must be running to serve the frontend.
```bash
uvicorn app:app --reload
# Runs on http://127.0.0.1:8000
```

### 3. Launch the Dashboard
In a separate terminal, launch the Streamlit frontend.
```bash
streamlit run streamlit_app.py
# Runs on http://localhost:8501
```

---

## ✅ Verifying the Build
This repository includes a suite of verification scripts to ensure data integrity and schema compliance at every step.
- `python verify_m4.py`: Verifies the train/test split and vectorizer integrity.
- `python verify_m5.py`: Validates that all 6 generated JSON contracts match the required UI schema.
- `python verify_m6.py`: Runs a test client against all FastAPI endpoints.