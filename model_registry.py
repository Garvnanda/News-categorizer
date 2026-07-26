from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

MODEL_REGISTRY = {
    "logistic_regression": {
        "estimator": LogisticRegression(max_iter=1000, class_weight='balanced'),
        "display_name": "Logistic Regression",
        "category": "Linear / Probabilistic",
        "one_liner": "A statistical model that predicts probabilities for each class using a linear combination of features.",
        "explanation": {
            "plain_language": "Logistic Regression calculates a score for each category by weighting every word in the headline. It then squashes these scores into percentages (probabilities) that add up to 100%.",
            "formula": "P(Y=k|X) = \\frac{e^{\\beta_k \\cdot X}}{\\sum_{j} e^{\\beta_j \\cdot X}}",
            "why_name": "It uses the 'logistic' function (the sigmoid or softmax curve) to convert raw linear scores into probabilities between 0 and 1."
        },
        "how_it_differs": "Unlike tree-based models, Logistic Regression assumes a linear relationship between words and categories. It's our baseline reference model: fast, interpretable, and very strong on text data.",
        "pros": ["Fast to train and predict", "Interpretable word weights", "Well-calibrated probabilities"],
        "cons": ["Assumes linear relationships", "Can struggle with highly complex, non-linear patterns"],
        "best_for": "A strong, fast baseline for high-dimensional text data."
    },
    
    "naive_bayes": {
        "estimator": MultinomialNB(alpha=0.1),
        "display_name": "Multinomial Naive Bayes",
        "category": "Probabilistic",
        "one_liner": "Predicts the category with the highest probability given the words in the headline, assuming words are independent.",
        "explanation": {
            "plain_language": "Naive Bayes looks at every word in a headline and asks: 'historically, which category do headlines with this word usually belong to?' It multiplies these word-level probabilities together to pick the most likely category.",
            "formula": "P(C|words) \\propto P(C) \\times \\prod_{i} P(word_i|C)",
            "why_name": "It's called 'naive' because it assumes every word's probability is independent of the others — which isn't true for language, but works surprisingly well."
        },
        "how_it_differs": "Unlike Logistic Regression which optimizes weights based on errors, Naive Bayes simply counts historical word frequencies. This makes it train almost instantly, but its 'naive' assumption that word occurrences are completely independent means it is slightly less accurate.",
        "pros": ["Extremely fast to train and predict", "Works well with small data", "Naturally handles many classes"],
        "cons": ["Ignores word order and context", "Independence assumption is unrealistic", "Overconfident probabilities"],
        "best_for": "Quick baselines and situations with limited training data or compute."
    },
    
    "linear_svm": {
        "estimator": CalibratedClassifierCV(LinearSVC(class_weight='balanced'), cv=3),
        "display_name": "Linear SVM",
        "category": "Margin-based",
        "one_liner": "Finds the widest possible 'street' (margin) between different categories in the high-dimensional word space.",
        "explanation": {
            "plain_language": "Imagine plotting every headline as a point in space. An SVM tries to draw a straight line (or hyperplane) that perfectly separates the categories, pushing the boundary as far away from the points as possible.",
            "formula": "\\min_{w, b} \\frac{1}{2} ||w||^2 + C \\sum_{i} \\max(0, 1 - y_i(w \\cdot x_i - b))",
            "why_name": "'Support Vector Machine' refers to the 'support vectors' — the specific data points that lie exactly on the edge of the margin and define where the boundary is drawn."
        },
        "how_it_differs": "Unlike Logistic Regression which tries to maximize the likelihood of probabilities, an SVM only cares about finding the widest possible boundary (margin) between classes. This often yields the absolute highest accuracy for high-dimensional text data, at the cost of native probability estimates.",
        "pros": ["Often the highest accuracy for text", "Handles high-dimensional sparse data beautifully", "Robust against overfitting"],
        "cons": ["No native probabilities (requires calibration)", "Hard to interpret directly", "Slower to train than Naive Bayes"],
        "best_for": "Achieving maximum accuracy on high-dimensional data like TF-IDF vectors."
    },
    
    "random_forest": {
        "estimator": RandomForestClassifier(n_estimators=200, max_depth=50, n_jobs=-1),
        "display_name": "Random Forest",
        "category": "Tree Ensemble",
        "one_liner": "Builds hundreds of decision trees and averages their votes to make a final prediction.",
        "explanation": {
            "plain_language": "Instead of relying on one expert, a Random Forest creates a 'committee' of 200 different decision trees. Each tree only sees a random subset of words and data. The final prediction is made by majority vote.",
            "formula": "\\hat{y} = \\text{mode}\\{h_1(x), h_2(x), ..., h_B(x)\\}",
            "why_name": "It builds a 'forest' of decision trees, and introduces 'randomness' by giving each tree slightly different data and features to look at."
        },
        "how_it_differs": "Unlike a single Decision Tree which memorizes the training data and overfits, this model averages the votes of 200 different trees. It is highly robust but much slower and uses far more memory on 15,000 TF-IDF features than the linear models.",
        "pros": ["Highly accurate and robust", "Less prone to overfitting than a single tree", "Captures non-linear patterns"],
        "cons": ["Slow and memory-heavy on TF-IDF text", "Black box (hard to interpret 200 trees)", "Inference can be slower"],
        "best_for": "Capturing complex, non-linear interactions between features when explainability isn't strictly required."
    },
    
    "decision_tree": {
        "estimator": DecisionTreeClassifier(max_depth=30, class_weight='balanced'),
        "display_name": "Decision Tree",
        "category": "Tree-based",
        "one_liner": "Learns a flowchart-like set of if/then rules based on word presence to categorize headlines.",
        "explanation": {
            "plain_language": "A Decision Tree acts like a game of 20 Questions. It asks things like: 'Does the text contain the word game?' If yes, go left (sports). If no, go right (ask another question).",
            "formula": "Gini = 1 - \\sum_{i=1}^c (p_i)^2 \\quad \\text{(Splitting criteria)}",
            "why_name": "It literally builds a tree structure of decisions from the root down to the 'leaves' (the final predictions)."
        },
        "how_it_differs": "Unlike the Random Forest's 200 trees, this is a single tree. It is perfectly transparent and easy to explain, but highly prone to overfitting, which you can clearly see in its significantly lower test accuracy.",
        "pros": ["Extremely easy to explain and visualize", "Captures non-linear rules natively", "Fast to predict"],
        "cons": ["Prone to severe overfitting", "Often lower accuracy on its own", "Unstable (small data changes change the whole tree)"],
        "best_for": "Situations where absolute interpretability and transparency of the exact decision path are required."
    },
    
    "knn": {
        "estimator": KNeighborsClassifier(n_neighbors=15, metric='cosine'),
        "display_name": "K-Nearest Neighbors",
        "category": "Instance-based",
        "one_liner": "Finds the 15 most similar past headlines and assigns the most common category among them.",
        "explanation": {
            "plain_language": "KNN doesn't actually 'learn' rules. When given a new headline, it searches the entire training database for the 15 most similar headlines (using cosine similarity) and takes a majority vote.",
            "formula": "\\text{Similarity}(A,B) = \\frac{A \\cdot B}{||A|| ||B||}",
            "why_name": "It looks at the 'K' (in our case, 15) 'nearest' (most similar) 'neighbors' (past data points) to make a prediction."
        },
        "how_it_differs": "Unlike every other model here, KNN doesn't actually 'learn' any parameters during training. It simply memorizes the training data. This means training is instantaneous, but predicting a new article requires comparing it to all 40,000 training examples, making its inference incredibly slow.",
        "pros": ["No real training phase (just stores data)", "Very intuitive 'similarity' concept", "Adapts immediately if new data is added"],
        "cons": ["Suffers heavily from the 'curse of dimensionality'", "Inference is very slow (compares against all data)", "Requires storing the entire dataset in memory"],
        "best_for": "Recommendation systems or simple baselines where training time must be zero."
    }
}
