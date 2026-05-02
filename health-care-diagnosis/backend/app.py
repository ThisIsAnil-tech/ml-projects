from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import pandas as pd
import json

from nlp_pipeline import check_emergency, extract_symptoms
from questioning_engine import requires_follow_up, generate_follow_up_question
from precautions import get_precautions
from explainer import init_explainer, get_shap_values

app = Flask(__name__)
CORS(app)

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "ensemble_pipeline.pkl")
TFIDF_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")

model = None
vectorizer = None

def load_models():
    global model, vectorizer
    try:
        if os.path.exists(MODEL_PATH) and os.path.exists(TFIDF_PATH):
            model = joblib.load(MODEL_PATH)
            vectorizer = joblib.load(TFIDF_PATH)
            print("Models loaded successfully.")
            
            dummy_data = ["fever cough headache", "chest pain shortness of breath", "stomach ache vomiting diarrhea"]
            dummy_vec = vectorizer.transform(dummy_data)
            init_explainer(model, vectorizer, dummy_vec)
        else:
            print("Warning: Models not found. Please run train_model.py first.")
    except Exception as e:
        print(f"Error loading models: {e}")

load_models()

@app.route('/api/predict', methods=['POST'])
def predict():
    if model is None or vectorizer is None:
        return jsonify({"error": "Model not loaded. Ensure training is completed."}), 500

    data = request.json
    if not data or 'symptoms' not in data:
        return jsonify({"error": "No symptoms provided."}), 400

    text = data['symptoms']
    
    if check_emergency(text):
        return jsonify({
            "status": "emergency",
            "message": "URGENT: Critical symptoms detected! Please seek immediate medical attention or call emergency services.",
            "disclaimer": "This is an automated AI response, not a medical diagnosis."
        })

    cleaned_symptoms = extract_symptoms(text)
    
    try:
        X_vec = vectorizer.transform([cleaned_symptoms])
        probabilities = model.predict_proba(X_vec)[0]
        
        classes = model.classes_
        top_indices = probabilities.argsort()[-3:][::-1]
        
        predictions = []
        for idx in top_indices:
            predictions.append({
                "disease": classes[idx],
                "confidence": float(probabilities[idx])
            })
            
        top_disease = predictions[0]['disease']
        top_confidence = predictions[0]['confidence']
        
        if requires_follow_up(cleaned_symptoms, top_confidence):
            follow_up_q = generate_follow_up_question(top_disease)
            return jsonify({
                "status": "needs_clarification",
                "question": follow_up_q,
                "current_predictions": predictions
            })

        top_class_idx = top_indices[0]
        shap_factors = get_shap_values(cleaned_symptoms, top_class_idx)
        
        precautions = get_precautions(top_disease)
        
        return jsonify({
            "status": "success",
            "predictions": predictions,
            "shap_factors": shap_factors,
            "precautions": precautions,
            "disclaimer": "DISCLAIMER: This system is for informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment."
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/evaluation', methods=['GET'])
def get_evaluation():
    metrics_path = os.path.join("models", "metrics.json")
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            metrics = json.load(f)
        return jsonify(metrics)
    else:
        return jsonify({"error": "Metrics not found. Please train the model first."}), 404

@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    if vectorizer is None:
        return jsonify({"error": "Model not loaded."}), 500
    try:
        features = vectorizer.get_feature_names_out().tolist()
        return jsonify(features)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
