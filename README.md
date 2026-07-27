# News Category Classifier — The Night Desk

A machine learning project that classifies news headlines into one of 10
categories, built as a full multi-algorithm comparison tool rather than a
single model. Six classical ML algorithms are trained on identical data and
exposed through an interactive dashboard, so anyone — technical or not — can
explore how each one thinks, where they agree, and where they don't.

> **Note:** this README describes the current full architecture (6-model
> registry + FastAPI backend + multi-page Streamlit dashboard). If your local
> file layout differs slightly from what's listed below, adjust the paths in
> the commands to match your actual filenames before running.

---

## What It Does

- Takes a news headline (or short description) as input
- Cleans and vectorizes the text (TF-IDF)
- Runs it through one or more of 6 trained classifiers:
  Logistic Regression, Multinomial Naive Bayes, Linear SVM, Decision Tree,
  Random Forest, and K-Nearest Neighbors
- Returns the predicted category, confidence score, and (per page) an
  explanation of *why* — top contributing words, confusion matrix, formula,
  and pros/cons for that algorithm
- Lets you compare all 6 models side by side on the same input, browse a
  leaderboard, batch-classify a CSV, and explore the training data

Categories: `WELLNESS`, `POLITICS`, `ENTERTAINMENT`, `TRAVEL`,
`STYLE & BEAUTY`, `PARENTING`, `FOOD & DRINK`, `WORLD NEWS`, `BUSINESS`,
`SPORTS`.

---

## Features / Pages

| Page | What it does |
|---|---|
| **File a Story** | Type a headline, pick a model, get a prediction + confidence + top contributing words |
| **Correspondent Profiles** | Per-model deep dive: plain-language explanation, formula, confusion matrix, pros/cons |
| **Standings** | Full leaderboard — accuracy, F1, training/inference time, per model |
| **All Hands on Deck** | Run all 6 models on one input at once, see where they agree/disagree |
| **Batch Wire** | Upload a CSV of headlines, classify in bulk, download results |
| **The Morgue** | Browse real training examples by category |
| **Editor's Challenge** | Guess the category yourself before the models reveal theirs |
| **Head-to-Head** | Pick any 2 models and compare their predictions side by side |

---

## Tech Stack

- **Python 3.10+**
- **Pandas** — data loading/manipulation
- **Scikit-learn** — all 6 ML models, TF-IDF vectorization, evaluation metrics
- **FastAPI** — backend API that serves trained models
- **Uvicorn** — ASGI server running the FastAPI app
- **Streamlit** — interactive multi-page frontend dashboard
- **Plotly** — charts (leaderboard bars, confusion matrices)
- **Joblib** — saving/loading trained models and the vectorizer

---

## Project Structure

```
News-categorizer/
├── app.py                  # FastAPI backend — serves /models, /predict, /predict/compare, /leaderboard
├── streamlit_app.py        # Streamlit multi-page frontend dashboard
├── data_loader.py          # Loads and cleans the raw CSV dataset
├── train_model.py          # Trains all 6 models on a shared TF-IDF vectorizer + split
├── news_data.csv           # Training dataset (~50k labeled headlines, 10 categories)
├── vectorizer.joblib       # Saved, fitted TF-IDF vectorizer (shared across all models)
├── model.joblib            # Saved trained model(s) — check if this is a single file
│                            #   or a models/ directory with one .joblib per algorithm
│                            #   in your actual setup, and adjust accordingly
├── verify_m1.py             # Milestone verification scripts (one per project milestone)
├── verify_m3.py
├── docs/
│   └── implementation_plan.md   # Full architecture/spec doc used to guide development
├── .agent/                 # Antigravity agent config (not needed to run the app)
├── LICENSE                 # MIT License
└── README.md
```

---

## Prerequisites

Before running anything, make sure you have:

- **Python 3.10 or higher** installed — check with:
  ```bash
  python --version
  ```
- **pip** (comes with Python)
- (Recommended) a virtual environment tool — `venv` is built into Python

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Garvnanda/News-categorizer.git
   cd News-categorizer
   ```

2. **Create and activate a virtual environment** (recommended, keeps
   dependencies isolated from the rest of your system)
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   Install directly:
   ```bash
   pip install pandas scikit-learn fastapi "uvicorn[standard]" streamlit plotly joblib python-multipart
   ```
   or
   ```bash
   pip install -r requirements.txt
   ```


---

## How to Run

The project has two parts that run separately — a backend (FastAPI) and a
frontend (Streamlit). You'll need **two terminal windows**, both with the
virtual environment activated.

### Step 1 — Train the models (only needed once, or after changing the dataset)

```bash
python train_all_models.py
```

This reads `news_data.csv`, cleans it, fits the TF-IDF vectorizer, trains
all 6 models on an identical train/test split, evaluates each one, and
saves the vectorizer + trained models to disk. Skip this step if
`vectorizer.joblib` and the trained model files already exist and you
haven't changed the dataset.

### Step 2 — Start the backend API

In your first terminal:
```bash
uvicorn app:app --reload --port 8001
```

This starts the FastAPI server at `http://localhost:8001`. You can check it's
running by visiting `http://localhost:8001/docs` in a browser — FastAPI
auto-generates an interactive API doc page there.

### Step 3 — Start the frontend dashboard

In a second terminal (with the same virtual environment activated):
```bash
streamlit run streamlit_app.py
```

This opens the dashboard in your browser automatically, usually at
`http://localhost:8501`. Make sure the backend (Step 2) is already running
first — the frontend calls the backend's API for every prediction.

---

## API Endpoints (backend)

| Endpoint | Method | What it returns |
|---|---|---|
| `/models` | GET | List of all available models with metadata |
| `/models/{model_id}` | GET | Details for one specific model |
| `/predict` | POST | Prediction from one chosen model for a given text input |
| `/predict/compare` | POST | Predictions from all 6 models for the same input |
| `/leaderboard` | GET | Accuracy/F1/timing comparison across all models |

Full interactive docs available at `http://localhost:8001/docs` once the
backend is running.

---

## The 6 Algorithms at a Glance

| Algorithm | Type | Notes |
|---|---|---|
| Logistic Regression | Linear | Strong baseline on sparse high-dimensional text |
| Multinomial Naive Bayes | Probabilistic | Fast to train, solid baseline for word-count-style features |
| Linear SVM | Linear (margin-based) | Typically a top performer on TF-IDF text |
| Decision Tree | Tree-based | Prone to overfitting on high-dimensional data on its own |
| Random Forest | Ensemble of trees | Reduces the single tree's overfitting via averaging |
| K-Nearest Neighbors | Distance-based | Included deliberately — expected to underperform here due to the "curse of dimensionality" on sparse TF-IDF vectors, which is itself a useful demonstration |

---

## Dataset

- ~50,000 labeled news headlines/descriptions
- 10 balanced categories (roughly equal samples each, to avoid class-imbalance bias)
- Stored as `news_data.csv`, loaded via Pandas in `data_loader.py`

---

## Troubleshooting

- **Frontend loads but predictions fail** — make sure the FastAPI backend
  (Step 2) is running *before* you start Streamlit, and that the port in
  `streamlit_app.py`'s API calls matches the port you started `uvicorn` on.
- **`ModuleNotFoundError`** — you likely forgot to activate the virtual
  environment, or a dependency wasn't installed. Re-run the install command
  in the activated environment.
- **Model/vectorizer files not found** — run `train_model.py` first (Step 1)
  to generate `vectorizer.joblib` and the model files before starting the app.

---

## License

MIT License — see `LICENSE` for details.
