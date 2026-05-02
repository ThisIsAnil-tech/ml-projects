disease_precautions = {
    "Allergy": ["Apply calamine", "Cover area with bandage", "Use ice to compress itching"],
    "Thyroid Disorder": ["Eat healthy diet", "Exercise regularly", "Get enough sleep", "Manage stress"],
    "Influenza": ["Rest and sleep", "Keep warm", "Drink plenty of liquids", "Take over-the-counter painkillers"],
    "Stroke": ["Call emergency services immediately", "Note the time symptoms started", "Do not give them anything to eat or drink"],
    "Heart Disease": ["Call emergency services", "Chew an aspirin if recommended by a doctor", "Stay calm and rest"],
    "Food Poisoning": ["Drink plenty of fluids", "Eat bland foods", "Rest", "Avoid dairy and caffeine"],
    "Bronchitis": ["Drink clear fluids", "Get plenty of rest", "Use a humidifier", "Avoid smoking"],
    "COVID-19": ["Isolate yourself", "Wear a mask", "Monitor oxygen levels", "Rest and hydrate"],
    "Dermatitis": ["Avoid triggers", "Moisturize skin", "Apply topical creams", "Use mild soaps"],
    "Diabetes": ["Monitor blood sugar", "Eat a balanced diet", "Exercise regularly", "Take prescribed medication"],
    "Arthritis": ["Exercise", "Apply heat or cold", "Manage weight", "Take pain relievers"],
    "Sinusitis": ["Use a humidifier", "Use saline nasal spray", "Drink plenty of fluids", "Rest"],
    "Dementia": ["Maintain a routine", "Keep the environment safe", "Encourage physical activity", "Provide cognitive stimulation"],
    "Parkinson's": ["Exercise regularly", "Eat a balanced diet", "Prevent falls", "Take prescribed medication"],
    "Obesity": ["Eat a healthy, calorie-controlled diet", "Exercise regularly", "Monitor weight", "Seek nutritional counseling"],
    "IBS": ["Avoid trigger foods", "Eat high-fiber foods", "Drink plenty of fluids", "Exercise regularly"],
    "Gastritis": ["Eat smaller, more frequent meals", "Avoid irritating foods", "Avoid alcohol", "Manage stress"],
    "Asthma": ["Use an inhaler", "Avoid triggers", "Monitor breathing", "Seek emergency care if severe"],
    "Epilepsy": ["Take medication as prescribed", "Avoid seizure triggers", "Get enough sleep", "Wear a medical alert bracelet"],
    "Pneumonia": ["Rest", "Drink fluids", "Take prescribed antibiotics", "Monitor fever"],
    "Anemia": ["Eat iron-rich foods", "Take supplements as prescribed", "Eat vitamin C rich foods", "Rest"],
    "Tuberculosis": ["Take medication strictly as prescribed", "Cover your mouth when coughing", "Ensure good ventilation", "Rest"],
    "Chronic Kidney Disease": ["Control blood pressure", "Manage blood sugar", "Eat a kidney-friendly diet", "Take prescribed medication"],
    "Ulcer": ["Avoid spicy foods", "Avoid alcohol and NSAIDs", "Eat a healthy diet", "Manage stress"],
    "Common Cold": ["Rest", "Drink fluids", "Soothe a sore throat", "Use saline nasal drops"],
    "Liver Disease": ["Avoid alcohol", "Eat a healthy diet", "Maintain a healthy weight", "Follow doctor's advice"],
    "Hypertension": ["Reduce sodium intake", "Exercise regularly", "Limit alcohol", "Manage stress"],
    "Migraine": ["Rest in a quiet, dark room", "Apply a cold compress", "Drink fluids", "Take pain relievers"],
    "Depression": ["Seek professional therapy", "Stay connected with others", "Exercise regularly", "Maintain a routine"]
}

def get_precautions(disease: str) -> list:
    """Retrieve precautions for a given disease, or generic advice if not found."""
    # Attempt to find the disease (case-insensitive mapping might be better, but exact match for now)
    return disease_precautions.get(
        disease, 
        ["Consult a healthcare professional", "Rest and hydrate", "Monitor your symptoms closely"]
    )
