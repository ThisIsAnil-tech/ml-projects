import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import json

DATA_PATH = "../../datasets/Healthcare.csv"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "ensemble_pipeline.pkl")
TFIDF_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
METRICS_PATH = os.path.join(MODEL_DIR, "metrics.json")

def train_and_save_model():
    print("Loading data...")
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")
    
    df = pd.read_csv(DATA_PATH)
    
    # We use the 'Symptoms' column as our text feature and 'Disease' as the target
    X = df['Symptoms'].fillna("")
    y = df['Disease']
    
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training TF-IDF Vectorizer...")
    tfidf = TfidfVectorizer(max_features=500, lowercase=True)
    X_train_vec = tfidf.fit_transform(X_train)
    X_test_vec = tfidf.transform(X_test)
    
    print("Initializing models...")
    nb_clf = MultinomialNB()
    svm_clf = SVC(probability=True, random_state=42)
    mlp_clf = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=300, random_state=42)
    
    ensemble_clf = VotingClassifier(
        estimators=[
            ('nb', nb_clf),
            ('svm', svm_clf),
            ('mlp', mlp_clf)
        ],
        voting='soft'
    )
    
    print("Training Ensemble Model...")
    ensemble_clf.fit(X_train_vec, y_train)
    
    print("Evaluating Model...")
    y_pred = ensemble_clf.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.4f}")
    
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
        
    print(f"Saving models and metrics to {MODEL_DIR}...")
    joblib.dump(tfidf, TFIDF_PATH)
    joblib.dump(ensemble_clf, MODEL_PATH)
    
    metrics = {
        "accuracy": acc,
        "classes_count": len(ensemble_clf.classes_)
    }
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f)
        
    print("Training complete and models saved successfully.")

if __name__ == "__main__":
    train_and_save_model()
