def requires_follow_up(symptoms_text: str, max_confidence: float) -> bool:
    """
    Determine if a follow-up question is required.
    Trigger if confidence is low or the user provided very few words.
    """
    # Simple heuristic: If confidence < 0.5 or less than 3 words were provided
    word_count = len(symptoms_text.split())
    if max_confidence < 0.45 or word_count < 3:
        return True
    return False

def generate_follow_up_question(top_predicted_disease: str) -> str:
    """
    Generate a dynamic follow-up question based on the top predicted disease.
    This acts like a doctor asking for associated symptoms.
    """
    # A simple mapping of common associated symptoms to ask about based on the top prediction
    follow_up_map = {
        "COVID-19": "Do you also have a loss of taste or smell, or a persistent cough?",
        "Influenza": "Are you experiencing body aches, chills, or extreme fatigue?",
        "Heart Disease": "Is the chest pain radiating to your arm or jaw? Do you feel dizzy?",
        "Stroke": "Are you experiencing any numbness on one side of your body or difficulty speaking?",
        "Food Poisoning": "Have you been vomiting or experiencing severe diarrhea?",
        "Diabetes": "Have you noticed increased thirst or frequent urination?",
        "Migraine": "Are you sensitive to light or sound?",
        "Dengue": "Do you have severe joint pain or a rash?",
        "Asthma": "Is the shortness of breath accompanied by wheezing?",
        "Allergy": "Are your eyes itchy or watery? Do you have a rash?",
    }
    
    # Return a specific question if mapped, else a generic one
    return follow_up_map.get(
        top_predicted_disease, 
        "Could you please describe any other symptoms you are experiencing? (e.g., duration, severity)"
    )
