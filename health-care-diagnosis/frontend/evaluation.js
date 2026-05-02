const API_URL = 'http://127.0.0.1:8000/api/evaluation';

async function fetchEvaluation() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        
        if (data.accuracy) {
            const accuracyPercent = (data.accuracy * 100).toFixed(2);
            document.getElementById('accuracyValue').innerText = `${accuracyPercent}%`;
            
            // If accuracy is low (e.g. < 50%), color it red
            if (data.accuracy < 0.5) {
                document.getElementById('accuracyValue').style.background = 'linear-gradient(135deg, #ef4444, #f59e0b)';
                document.getElementById('accuracyValue').style.webkitBackgroundClip = 'text';
                document.getElementById('accuracyValue').style.webkitTextFillColor = 'transparent';
            }
        }
        
        if (data.classes_count) {
            document.getElementById('classesValue').innerText = data.classes_count;
        }
    } catch (error) {
        console.error("Error fetching evaluation metrics:", error);
        document.getElementById('accuracyValue').innerText = "Error";
        document.getElementById('classesValue').innerText = "Error";
        document.getElementById('accuracyValue').style.fontSize = "2rem";
        document.getElementById('classesValue').style.fontSize = "2rem";
    }
}

fetchEvaluation();
