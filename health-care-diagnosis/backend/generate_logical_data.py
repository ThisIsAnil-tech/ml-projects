import pandas as pd
import random
import os

DATA_PATH = "../../datasets/Healthcare.csv"

disease_symptom_map = {
    "Allergy": ["sneezing", "runny nose", "itchy eyes", "rash", "swelling"],
    "Thyroid Disorder": ["fatigue", "weight gain", "weight loss", "mood swings", "cold intolerance"],
    "Influenza": ["fever", "chills", "muscle pain", "cough", "fatigue", "headache"],
    "Stroke": ["numbness", "difficulty speaking", "blurred vision", "dizziness", "confusion"],
    "Heart Disease": ["chest pain", "shortness of breath", "sweating", "nausea", "fatigue"],
    "Food Poisoning": ["nausea", "vomiting", "diarrhea", "abdominal pain", "fever"],
    "Bronchitis": ["cough", "mucus", "fatigue", "shortness of breath", "chest discomfort"],
    "COVID-19": ["fever", "cough", "loss of taste", "shortness of breath", "fatigue", "body aches"],
    "Dermatitis": ["rash", "itching", "red skin", "dry skin", "blisters"],
    "Diabetes": ["frequent urination", "increased thirst", "fatigue", "blurred vision", "weight loss"],
    "Arthritis": ["joint pain", "stiffness", "swelling", "decreased range of motion"],
    "Sinusitis": ["facial pain", "nasal congestion", "runny nose", "headache", "sore throat"],
    "Dementia": ["memory loss", "confusion", "difficulty speaking", "personality changes"],
    "Parkinson's": ["tremors", "slow movement", "stiffness", "loss of balance"],
    "Obesity": ["excessive weight gain", "fatigue", "shortness of breath", "joint pain"],
    "IBS": ["abdominal pain", "bloating", "diarrhea", "constipation", "cramping"],
    "Gastritis": ["upper abdominal pain", "nausea", "vomiting", "fullness", "indigestion"],
    "Asthma": ["wheezing", "shortness of breath", "chest tightness", "cough"],
    "Epilepsy": ["seizures", "confusion", "staring spells", "loss of consciousness"],
    "Pneumonia": ["cough with phlegm", "fever", "chills", "shortness of breath"],
    "Anemia": ["fatigue", "weakness", "pale skin", "cold hands", "dizziness"],
    "Tuberculosis": ["persistent cough", "weight loss", "night sweats", "fever", "chest pain"],
    "Chronic Kidney Disease": ["fatigue", "swelling", "frequent urination", "nausea", "muscle cramps"],
    "Ulcer": ["abdominal pain", "heartburn", "nausea", "vomiting", "bloating"],
    "Common Cold": ["runny nose", "sore throat", "sneezing", "mild cough", "low-grade fever"],
    "Liver Disease": ["yellow skin", "abdominal pain", "swelling", "dark urine", "chronic fatigue"],
    "Hypertension": ["headache", "shortness of breath", "nosebleeds", "dizziness", "chest pain"],
    "Migraine": ["severe headache", "sensitivity to light", "nausea", "blurred vision", "dizziness"],
    "Depression": ["insomnia", "fatigue", "appetite loss", "anxiety", "persistent sadness"]
}

all_symptoms = list(set([sym for symptoms in disease_symptom_map.values() for sym in symptoms]))

def generate_logical_dataset(num_records=5000):
    print(f"Generating a logical dataset with {num_records} records...")
    data = []
    
    for i in range(1, num_records + 1):
        disease = random.choice(list(disease_symptom_map.keys()))
        
        core_symptoms = random.sample(disease_symptom_map[disease], k=random.randint(2, min(4, len(disease_symptom_map[disease]))))
        
        if random.random() > 0.5:
            noise = random.choice(all_symptoms)
            if noise not in core_symptoms:
                core_symptoms.append(noise)
                
        random.shuffle(core_symptoms)
        symptoms_str = ", ".join(core_symptoms)
        
        data.append({
            "Patient_ID": i,
            "Age": random.randint(5, 85),
            "Gender": random.choice(["Male", "Female", "Other"]),
            "Symptoms": symptoms_str,
            "Symptom_Count": len(core_symptoms),
            "Disease": disease
        })
        
    df = pd.DataFrame(data)
    
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    
    df.to_csv(DATA_PATH, index=False)
    print(f"Successfully generated logical dataset at {DATA_PATH}")

if __name__ == "__main__":
    generate_logical_dataset()
