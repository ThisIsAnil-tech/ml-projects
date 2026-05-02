import re

EMERGENCY_KEYWORDS = [
    "chest pain", 
    "shortness of breath", 
    "difficulty breathing", 
    "severe bleeding", 
    "unconscious", 
    "heart attack", 
    "stroke",
    "cannot breathe"
]

def check_emergency(text: str) -> bool:
    """Check if the input text contains any emergency keywords."""
    text_lower = text.lower()
    for keyword in EMERGENCY_KEYWORDS:
        if keyword in text_lower:
            return True
    return False

def extract_symptoms(text: str) -> str:
    """
    Extract and clean symptoms from user input.
    In a more complex system, this would use NER (e.g. spaCy) to identify exact medical entities.
    For this prototype, since we are using TF-IDF on the entire symptom string, 
    we will perform basic cleaning and pass it to the vectorizer.
    """
    # Remove punctuation that might interfere with TF-IDF, keep commas if they separate symptoms
    cleaned = re.sub(r'[^\w\s,]', '', text)
    return cleaned.lower()
