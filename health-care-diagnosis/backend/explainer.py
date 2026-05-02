import shap
import numpy as np

_explainer = None
_vectorizer = None

def init_explainer(model, vectorizer, X_background):
    global _explainer, _vectorizer
    _vectorizer = vectorizer
    
    def predict_fn(X):
        return model.predict_proba(X)
        
    background_dense = X_background[:10].toarray()
    
    try:
        _explainer = shap.KernelExplainer(predict_fn, background_dense)
    except Exception as e:
        print(f"Warning: Failed to initialize SHAP explainer: {e}")
        _explainer = None

def get_shap_values(text: str, top_class_idx: int):
    if _explainer is None or _vectorizer is None:
        return [{"feature": "Explainability not initialized", "value": 0.0}]
        
    try:
        X_vec = _vectorizer.transform([text]).toarray()
        
        shap_values = _explainer.shap_values(X_vec, nsamples=100)
        
        if isinstance(shap_values, list):
            class_shap_values = shap_values[top_class_idx][0]
        else:
            if len(shap_values.shape) == 3:
                class_shap_values = shap_values[0, :, top_class_idx]
            else:
                class_shap_values = shap_values[0]
            
        feature_names = _vectorizer.get_feature_names_out()
        
        contributions = []
        for i, val in enumerate(class_shap_values):
                contributions.append({"feature": feature_names[i], "value": float(val)})
                
        contributions.sort(key=lambda x: abs(x["value"]), reverse=True)
        return contributions[:5] 
        
    except Exception as e:
        print(f"Error calculating SHAP values: {e}")
        return []
