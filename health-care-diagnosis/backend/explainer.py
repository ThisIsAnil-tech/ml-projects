import shap
import numpy as np

# We'll use a global explainer to avoid re-initializing it on every request
_explainer = None
_vectorizer = None

def init_explainer(model, vectorizer, X_background):
    """
    Initialize the SHAP explainer using a background dataset.
    For text with TF-IDF, a KernelExplainer or LinearExplainer can be used.
    """
    global _explainer, _vectorizer
    _vectorizer = vectorizer
    
    # We use a wrapper function because shap needs to call predict_proba on the raw arrays
    def predict_fn(X):
        return model.predict_proba(X)
        
    # We use a small subset of the background data to initialize KernelExplainer to keep it fast
    # X_background is expected to be a sparse TF-IDF matrix
    background_dense = X_background[:10].toarray()
    
    try:
        _explainer = shap.KernelExplainer(predict_fn, background_dense)
    except Exception as e:
        print(f"Warning: Failed to initialize SHAP explainer: {e}")
        _explainer = None

def get_shap_values(text: str, top_class_idx: int):
    """
    Calculate SHAP values for a given input text and format the top contributing features.
    """
    if _explainer is None or _vectorizer is None:
        return [{"feature": "Explainability not initialized", "value": 0.0}]
        
    try:
        # Vectorize input
        X_vec = _vectorizer.transform([text]).toarray()
        
        # Calculate SHAP values
        shap_values = _explainer.shap_values(X_vec, nsamples=100)
        
        # shap_values is typically a list of arrays (one for each class)
        # We want the explanation for the top predicted class
        if isinstance(shap_values, list):
            class_shap_values = shap_values[top_class_idx][0]
        else:
            if len(shap_values.shape) == 3:
                # Shape is (n_samples, n_features, n_classes)
                class_shap_values = shap_values[0, :, top_class_idx]
            else:
                class_shap_values = shap_values[0]
            
        feature_names = _vectorizer.get_feature_names_out()
        
        # Pair feature names with their shap values
        contributions = []
        for i, val in enumerate(class_shap_values):
            if abs(val) > 0.01: # Filter out negligible contributions
                contributions.append({"feature": feature_names[i], "value": float(val)})
                
        # Sort by absolute value descending
        contributions.sort(key=lambda x: abs(x["value"]), reverse=True)
        return contributions[:5] # Return top 5 contributing features
        
    except Exception as e:
        print(f"Error calculating SHAP values: {e}")
        return []
