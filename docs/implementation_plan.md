# Multi-Algorithm News Classifier — Ideology & Implementation Plan

**Project:** News-categorizer (Garvnanda/News-categorizer)
**Goal:** Turn the existing single-model (Logistic Regression) classifier into an interactive, educational multi-algorithm comparison tool that a non-ML mentor can explore and understand.
**Builder:** This plan is written to be handed to a coding agent (e.g. Antigravity) milestone by milestone.

---

## PART 1 — THE IDEOLOGY

### 1.1 What problem this solves
Right now the project proves *one* algorithm works. Your mentor's ask is bigger: show that you understand the *landscape* of algorithms applicable to text classification, and can explain, in an evidence-backed way, why one might be chosen over another. The product isn't "a classifier" anymore — it's "a teaching tool that happens to classify news."

### 1.2 Design principle: Train once, explore forever
All 6 models train **offline**, once, in a batch script. Each model + its full evaluation report is saved to disk. The web app **never trains anything live** — it only loads pre-trained artifacts and runs predictions. This is critical for an agent build: training-on-request is slow, flaky, and hard to debug live; loading a `.joblib` file is instant and deterministic.

### 1.3 Design principle: One shared vectorizer, fair comparison
All 6 models must be compared on equal footing. That means **one TF-IDF vectorizer, fit once**, reused by every model. If each model got its own differently-tuned vectorizer, differences in accuracy could come from the vectorizer, not the algorithm — which would undermine the entire teaching goal. (One exception, explained in 2.3, for KNN's feature cap.)

### 1.4 Design principle: Every model is a "citizen" with the same metadata contract
Each of the 6 models gets an identical metadata record: description, math, pros/cons, accuracy, confusion matrix, timing, top keywords. The frontend never special-cases a model — it just renders whatever the registry gives it. This means adding a 7th algorithm later is a config change, not a rewrite.

### 1.5 Design principle: Explanation lives next to evidence
Semi-technical means: plain-language sentence **first**, formula **second**, live numbers from *this dataset* **third**. Never show a formula floating with no connection to what the user just did.

---

## PART 2 — THE SIX ALGORITHMS

All trained on the same cleaned `headline + short_description` text, same TF-IDF features, same 80/20 split (stratified by category, same random_state across all models so the test set is identical for every one).

| # | Model | sklearn class | Why it's here | Watch-out |
|---|-------|---------------|----------------|-----------|
| 1 | Logistic Regression | `LogisticRegression(max_iter=1000, class_weight='balanced')` | Your existing baseline; linear, probabilistic, fast | Already built — keep as the reference point |
| 2 | Multinomial Naive Bayes | `MultinomialNB(alpha=0.1)` | The classic "made for text" algorithm — trains in seconds, strong baseline | Needs non-negative features (TF-IDF is fine); assumes word independence — good talking point |
| 3 | Linear SVM | `LinearSVC(class_weight='balanced')` | Often the *best* accuracy for sparse high-dimensional text | No native `predict_proba` — wrap in `CalibratedClassifierCV(cv=3)` so the frontend can still show confidence % |
| 4 | Random Forest | `RandomForestClassifier(n_estimators=200, max_depth=50, n_jobs=-1)` | Shows ensemble/bagging as a contrast to linear models | Slow & memory-heavy on very high-dimensional sparse TF-IDF — cap vectorizer `max_features` (see 2.3) |
| 5 | Decision Tree | `DecisionTreeClassifier(max_depth=30, class_weight='balanced')` | Most interpretable — you can literally draw it; good teaching contrast to Random Forest (1 tree vs. 200) | Prone to overfitting — expect visibly lower test accuracy than Random Forest; that gap *is* the lesson |
| 6 | K-Nearest Neighbors | `KNeighborsClassifier(n_neighbors=15, metric='cosine')` | Shows a completely non-parametric, "no training, just memorize and compare" approach | Slow at inference over 40k training vectors; cosine metric works far better than Euclidean for TF-IDF — use it deliberately and explain why in the UI |

### 2.1 Shared preprocessing (reuse & extend `data_loader.py`)
- Combine `headline` + `short_description` into one `text` field (more signal than headline alone).
- Lowercase → strip punctuation/URLs → remove stopwords → (optional) lemmatize.
- Fit `TfidfVectorizer(max_features=15000, ngram_range=(1,2), min_df=3)` **once** on the training split only, save as `vectorizer.joblib`.

### 2.2 Split
`train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)` — same call, same seed, used once, and the resulting indices/matrices reused for every model so all 6 are scored on the exact same held-out 10,000 rows.

### 2.3 The KNN exception
KNN over a 15,000-dim sparse matrix with 40,000 training points will be noticeably slow and its accuracy will suffer from the "curse of dimensionality" — this is a *real, honest result*, not a bug. Do **not** silently shrink its feature space to make it look better; instead, surface the timing and accuracy as-is and let the UI explain *why* KNN struggles here. This honesty is itself a good demonstration to a mentor.

---

## PART 3 — WHAT GETS SAVED PER MODEL (the metadata contract)

For every model, `train_all_models.py` produces one JSON file, e.g. `saved_models/metrics/naive_bayes.json`:

```json
{
  "model_id": "naive_bayes",
  "display_name": "Multinomial Naive Bayes",
  "category": "Probabilistic",
  "one_liner": "Predicts the category with the highest probability given the words in the headline, assuming words are independent.",
  "explanation": {
    "plain_language": "Naive Bayes looks at every word in a headline and asks: 'historically, which category do headlines with this word usually belong to?' It multiplies these word-level probabilities together to pick the most likely category.",
    "formula": "P(class|words) \\propto P(class) \\times \\prod_{i} P(word_i|class)",
    "why_naive": "It's called 'naive' because it assumes every word's probability is independent of the others — which isn't really true (word order and context matter), but works surprisingly well for text."
  },
  "pros": ["Extremely fast to train and predict", "Works well with small data", "Naturally handles many classes"],
  "cons": ["Ignores word order and context", "Independence assumption is unrealistic", "Can be overconfident in its probabilities"],
  "best_for": "Quick baselines and situations with limited training data or compute.",
  "metrics": {
    "accuracy": 0.87,
    "macro_f1": 0.86,
    "macro_precision": 0.87,
    "macro_recall": 0.86,
    "per_class": { "SPORTS": {"precision":0.96,"recall":0.95,"f1":0.955,"support":1000}, "...": "..." },
    "confusion_matrix": [[...]],
    "labels_order": ["BUSINESS","ENTERTAINMENT","..."]
  },
  "timing": { "train_seconds": 0.8, "avg_inference_ms": 0.4 },
  "top_features_per_class": { "SPORTS": ["game","team","season","player","coach"], "...": "..." }
}
```

This one contract is what makes the frontend simple: it renders the same template 6 times with different data.

`leaderboard.json` aggregates all 6 into one array, sorted by accuracy, for the comparison page.

---

## PART 4 — BACKEND (FastAPI) — extend `app.py`

Keep the existing `POST /predict` for backward compatibility, but expand it and add:

| Endpoint | Method | Input | Output |
|---|---|---|---|
| `/models` | GET | – | List of `{model_id, display_name, category, one_liner, accuracy}` for all 6 — powers the dropdown |
| `/models/{model_id}` | GET | – | Full metadata JSON for that model (the contract in Part 3) |
| `/predict` | POST | `{text, model_id}` | `{predicted_category, confidence, probabilities: {category: prob, ...}, top_contributing_words}` |
| `/predict/compare` | POST | `{text}` | Runs **all 6 models** on the same text, returns an array of each model's prediction + confidence — powers the "Compare Models" page |
| `/leaderboard` | GET | – | Sorted array of all 6 models' accuracy/F1/timing for the leaderboard chart |

Load all 6 `.joblib` models + the shared vectorizer + all metadata JSONs **once at startup** into memory (a simple `MODEL_REGISTRY` dict keyed by `model_id`), not per-request — keeps `/predict` fast.

`top_contributing_words`: for linear models (LogReg, SVM, NB) pull the highest-weighted TF-IDF features present in the input for the predicted class. For tree-based/KNN models, use the model's global `top_features_per_class` for the predicted class as a reasonable stand-in (explain this distinction in the UI copy — "exact contribution" vs. "typical top words for this category").

---

## PART 5 — FRONTEND (Streamlit, multi-page)

Use `st.tabs()` or a sidebar `st.radio` for navigation between 4 views. Use **Plotly** (`plotly.express` / `plotly.graph_objects`) for every chart — interactive, hover tooltips, and renders cleanly inside Streamlit, which will read far better in a live mentor demo than static matplotlib PNGs.

### Page 1 — 🔮 Predict
- Text input box.
- Dropdown: choose one model (default: Logistic Regression) — populated from `GET /models`.
- "Predict" button → calls `POST /predict`.
- Shows: big category tag, confidence %, a horizontal bar chart of probability across all 10 categories, and a small "why" panel listing top contributing words.

### Page 2 — 📊 Model Explorer
- Dropdown to pick one of the 6 models.
- Renders, in order: plain-language explanation → `st.latex()` formula → pros/cons as two columns → metric cards (accuracy, macro F1, precision, recall) → an interactive confusion matrix heatmap (Plotly) → top keywords per category (grouped bar chart or one bar chart per category in an expander).

### Page 3 — 🏆 Leaderboard
- Grouped bar chart: accuracy + macro F1 for all 6 models side by side.
- Table: model, accuracy, train time, inference time.
- A short auto-generated takeaway line, e.g. "Linear SVM has the highest accuracy; Naive Bayes trains 40x faster with only a 3-point accuracy trade-off; KNN is both the slowest and least accurate here — a natural fit for the 'curse of dimensionality' discussion."

### Page 4 — ⚔️ Compare Models
- One text input, one button.
- Calls `POST /predict/compare`.
- Shows a table/grid: one row per model, with its predicted category, confidence, and a ✅/⚠️ flag showing whether it agrees with the majority vote across all 6 — this is the single most demo-friendly feature for a mentor walkthrough.

---

## PART 6 — UPDATED DIRECTORY STRUCTURE

```
News-categorizer/
├── data_loader.py                # extended: shared cleaning + shared TF-IDF fit/save
├── model_registry.py             # NEW: config dict — one entry per algorithm (class, hyperparams, description, math, pros/cons)
├── train_all_models.py           # NEW: orchestrator — loops model_registry, trains, evaluates, saves model + metrics JSON for all 6
├── app.py                        # extended FastAPI: /models, /models/{id}, /predict, /predict/compare, /leaderboard
├── streamlit_app.py              # rebuilt: 4-page dashboard described in Part 5
├── saved_models/
│   ├── vectorizer.joblib
│   ├── logistic_regression.joblib
│   ├── naive_bayes.joblib
│   ├── linear_svm.joblib
│   ├── random_forest.joblib
│   ├── decision_tree.joblib
│   ├── knn.joblib
│   └── metrics/
│       ├── logistic_regression.json
│       ├── naive_bayes.json
│       ├── linear_svm.json
│       ├── random_forest.json
│       ├── decision_tree.json
│       ├── knn.json
│       └── leaderboard.json
├── verify_m4.py … verify_m8.py   # one verification script per new milestone, mirroring your existing verify_m1.py/verify_m3.py pattern
├── news_data.csv
└── README.md
```

---

## PART 7 — MILESTONES FOR THE AGENT (hand these to Antigravity one at a time)

Build and verify each milestone before moving to the next — don't let the agent jump ahead, since M6/M7 depend on the JSON contract from M5 being correct.

### Milestone 4 — Shared preprocessing & vectorizer
> Extend `data_loader.py` so it: (1) combines `headline` and `short_description` into one `text` column, (2) applies the existing cleaning steps to it, (3) fits a `TfidfVectorizer(max_features=15000, ngram_range=(1,2), min_df=3)` on an 80% stratified training split (`random_state=42`), and (4) saves the vectorizer to `saved_models/vectorizer.joblib` along with the train/test split indices so every later model trains and evaluates on identical data. Write `verify_m4.py` that asserts the vectorizer file exists, loads correctly, and that train/test class distributions are balanced.

### Milestone 5 — Model registry + training orchestrator
> Create `model_registry.py` containing a Python dict with one entry per algorithm (the 6 in Part 2), each holding: the sklearn class + hyperparameters, `display_name`, `category`, `one_liner`, `plain_language` explanation, `formula` (LaTeX string), `pros`, `cons`, `best_for`. Then create `train_all_models.py` that loops through the registry, trains each model on the shared vectorizer's output, evaluates on the shared test split, extracts top TF-IDF features per class (via `coef_` for linear models, `feature_importances_` for tree models, or class-conditional TF-IDF means for KNN), times training and average per-sample inference, and saves both the trained model (`saved_models/{model_id}.joblib`) and its full metrics JSON (matching the Part 3 contract) to `saved_models/metrics/{model_id}.json`. After all 6 finish, write `saved_models/metrics/leaderboard.json` — an array of all 6 summaries sorted by accuracy descending. Write `verify_m5.py` asserting all 6 `.joblib` and `.json` files exist and every metrics JSON matches the Part 3 schema.

### Milestone 6 — Extended FastAPI backend
> Extend `app.py` to load the vectorizer and all 6 models + metrics JSONs once at startup into an in-memory registry. Implement `GET /models`, `GET /models/{model_id}`, `POST /predict` (now accepting `model_id`), `POST /predict/compare` (runs all 6), and `GET /leaderboard`, matching the request/response shapes in Part 4. Handle unknown `model_id` with a 404 and a clear error message. Write `verify_m6.py` that spins up the app with FastAPI's `TestClient` and hits every endpoint with valid and invalid inputs.

### Milestone 7 — Multi-page Streamlit dashboard
> Rebuild `streamlit_app.py` into the 4-page app described in Part 5, calling the FastAPI backend for all data (do not re-load models directly in Streamlit — always go through the API, so the API stays the single source of truth). Use `st.set_page_config(layout="wide")`, Plotly for every chart, and `st.latex()` for formulas. Add a loading spinner around every API call and a friendly error message if the backend is unreachable.

### Milestone 8 — Explainability polish
> On the Predict and Compare pages, add the "top contributing words" panel described in Part 4, clearly labeled as "exact contribution" for linear models vs. "typical top words for this category" for tree/KNN models. On the Model Explorer page, add a short "How this differs from the other 5 models" callout per model (e.g., for Decision Tree: "Unlike Random Forest's 200 trees, this is a single tree — faster to explain, but more prone to overfitting, which you can see in its lower test accuracy").

### Milestone 9 — README & final verification
> Update `README.md` with the new architecture diagram (text-based is fine), how to run `train_all_models.py`, how to launch `app.py` + `streamlit_app.py`, and a short "what each model teaches you" table. Run all `verify_m*.py` scripts end-to-end and fix any failures.

---

## PART 8 — WHAT TO TELL YOUR MENTOR THIS DEMONSTRATES

- Comparative evaluation methodology (identical train/test split, identical features, fair scoring).
- Understanding of algorithm families: probabilistic (Naive Bayes), linear/margin-based (Logistic Regression, SVM), tree-based single & ensemble (Decision Tree, Random Forest), instance-based (KNN).
- Awareness of *why* results differ (high-dimensional sparse text data suits linear models; distance-based methods suffer from the curse of dimensionality; single trees overfit vs. forests).
- Full-stack ML delivery: offline training pipeline → served API → interactive UI aimed at a non-technical audience.

---

## Notes / assumptions made
- Kept FastAPI as the serving layer (matches your existing Milestone 3 deliverable) with Streamlit as the richer presentation layer on top, rather than discarding either.
- Capped TF-IDF at 15,000 features with min_df=3 to keep Random Forest/Decision Tree/KNN training times reasonable on 40k rows without materially hurting the linear models' accuracy — flagged as a design choice above rather than hidden.
- If Antigravity's environment can't install `plotly`, matplotlib + `st.pyplot()` is a drop-in fallback — just less interactive.
