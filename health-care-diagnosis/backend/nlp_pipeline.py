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
    text_lower = text.lower()
    for keyword in EMERGENCY_KEYWORDS:
        if keyword in text_lower:
            return True
    return False

def extract_symptoms(text: str) -> str:
    cleaned = re.sub(r'[^\w\s,]', '', text)
    return cleaned.lower()
