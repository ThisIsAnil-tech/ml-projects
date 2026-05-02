import os
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

class MLModels:
    def __init__(self):
        self.log_reg = LogisticRegression(max_iter=1000)
        self.rf = RandomForestClassifier(n_estimators=100, random_state=42)

    def train_logistic_regression(self, X_train, y_train):
        print("Training Logistic Regression...")
        self.log_reg.fit(X_train, y_train)

    def train_random_forest(self, X_train, y_train):
        print("Training Random Forest...")
        self.rf.fit(X_train, y_train)

    def evaluate(self, model_name, X_test, y_test):
        if model_name == 'logistic_regression':
            preds = self.log_reg.predict(X_test)
        elif model_name == 'random_forest':
            preds = self.rf.predict(X_test)
        else:
            raise ValueError("Unknown model name")
            
        acc = accuracy_score(y_test, preds)
        print(f"[{model_name}] Accuracy: {acc:.4f}")
        print(classification_report(y_test, preds))
        return acc

    def predict(self, model_name, X):
        if model_name == 'logistic_regression':
            return self.log_reg.predict(X), self.log_reg.predict_proba(X)
        elif model_name == 'random_forest':
            return self.rf.predict(X), self.rf.predict_proba(X)
        else:
            raise ValueError("Unknown model name")

    def save_models(self, save_dir):
        os.makedirs(save_dir, exist_ok=True)
        with open(os.path.join(save_dir, 'log_reg_model.pkl'), 'wb') as f:
            pickle.dump(self.log_reg, f)
        with open(os.path.join(save_dir, 'rf_model.pkl'), 'wb') as f:
            pickle.dump(self.rf, f)

    def load_models(self, save_dir):
        with open(os.path.join(save_dir, 'log_reg_model.pkl'), 'rb') as f:
            self.log_reg = pickle.load(f)
        with open(os.path.join(save_dir, 'rf_model.pkl'), 'rb') as f:
            self.rf = pickle.load(f)
