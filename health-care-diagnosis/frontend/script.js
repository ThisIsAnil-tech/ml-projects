const API_URL = 'http://127.0.0.1:8000/api/predict';
const SYMPTOMS_URL = 'http://127.0.0.1:8000/api/symptoms';
const selectBox = document.getElementById('selectBox');
const searchInput = document.getElementById('symptomSearch');
const dropdownList = document.getElementById('dropdownList');
const selectedSymptomsContainer = document.getElementById('selectedSymptoms');
const predictBtn = document.getElementById('predictBtn');
const dashboard = document.getElementById('dashboard');
const resetBtn = document.getElementById('resetBtn');
const predictionsContainer = document.getElementById('predictionsContainer');
const shapContainer = document.getElementById('shapContainer');
const precautionsList = document.getElementById('precautionsList');
const emergencyAlert = document.getElementById('emergencyAlert');
const emergencyText = document.getElementById('emergencyText');

let allSymptoms = [];
let filteredSymptoms = [];
let selectedSymptoms = new Set();
let focusedIndex = -1;

async function fetchSymptoms() {
    try {
        const response = await fetch(SYMPTOMS_URL);
        if (response.ok) {
            allSymptoms = await response.json();
            filteredSymptoms = [...allSymptoms];
            renderDropdown();
        }
    } catch (error) {
        console.error("Error fetching symptoms:", error);
    }
}

function renderDropdown(query = "") {
    dropdownList.innerHTML = '';
    const available = filteredSymptoms.filter(s => !selectedSymptoms.has(s));

    if (available.length === 0) {
        dropdownList.innerHTML = '<div class="dropdown-item" style="color:var(--text-secondary); cursor:default;">No matching symptoms</div>';
        return;
    }

    available.forEach((symptom, index) => {
        const div = document.createElement('div');
        div.className = 'dropdown-item';
        if (index === focusedIndex) {
            div.classList.add('active');
        }

        let displayText = symptom.charAt(0).toUpperCase() + symptom.slice(1);
        if (query) {
            const regex = new RegExp(`(${query})`, 'gi');
            displayText = displayText.replace(regex, '<span class="highlight">$1</span>');
        }

        div.innerHTML = displayText;
        div.onmousedown = (e) => {
            e.preventDefault();
            addSymptom(symptom);
        };

        div.onmouseenter = () => {
            focusedIndex = index;
            updateActiveItem();
        };

        dropdownList.appendChild(div);
    });
}

function updateActiveItem() {
    const items = dropdownList.querySelectorAll('.dropdown-item');
    items.forEach((item, idx) => {
        if (idx === focusedIndex) {
            item.classList.add('active');
            item.scrollIntoView({ block: 'nearest' });
        } else {
            item.classList.remove('active');
        }
    });
}

function addSymptom(symptom) {
    if (!selectedSymptoms.has(symptom)) {
        selectedSymptoms.add(symptom);
        renderSelectedSymptoms();
        searchInput.value = '';
        filteredSymptoms = [...allSymptoms];
        focusedIndex = -1;
        renderDropdown();
        searchInput.focus();
    }
}

function removeSymptom(symptom) {
    selectedSymptoms.delete(symptom);
    renderSelectedSymptoms();
    renderDropdown(searchInput.value);
}

function renderSelectedSymptoms() {
    selectedSymptomsContainer.innerHTML = '';
    selectedSymptoms.forEach(symptom => {
        const tag = document.createElement('div');
        tag.className = 'symptom-tag';
        tag.innerHTML = `
            ${symptom.charAt(0).toUpperCase() + symptom.slice(1)}
            <i class="fa-solid fa-xmark" onclick="removeSymptom('${symptom}')"></i>
        `;
        selectedSymptomsContainer.appendChild(tag);
    });
}

selectBox.addEventListener('click', () => {
    searchInput.focus();
});

searchInput.addEventListener('focus', () => {
    selectBox.classList.add('focused');
    dropdownList.classList.add('show');
    focusedIndex = -1;
    renderDropdown(searchInput.value);
});

searchInput.addEventListener('blur', () => {
    selectBox.classList.remove('focused');
    dropdownList.classList.remove('show');
});

searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();
    filteredSymptoms = allSymptoms.filter(s => s.toLowerCase().includes(query));
    focusedIndex = -1;
    dropdownList.classList.add('show');
    renderDropdown(query);
});

searchInput.addEventListener('keydown', (e) => {
    const available = filteredSymptoms.filter(s => !selectedSymptoms.has(s));

    if (e.key === 'ArrowDown') {
        e.preventDefault();
        dropdownList.classList.add('show');
        if (focusedIndex < available.length - 1) {
            focusedIndex++;
            updateActiveItem();
        }
    } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (focusedIndex > 0) {
            focusedIndex--;
            updateActiveItem();
        }
    } else if (e.key === 'Enter') {
        e.preventDefault();
        if (focusedIndex >= 0 && focusedIndex < available.length) {
            addSymptom(available[focusedIndex]);
        }
    } else if (e.key === 'Escape') {
        dropdownList.classList.remove('show');
        searchInput.blur();
    } else if (e.key === 'Backspace' && searchInput.value === '' && selectedSymptoms.size > 0) {
        const lastSymptom = Array.from(selectedSymptoms).pop();
        removeSymptom(lastSymptom);
    }
});

predictBtn.addEventListener('click', async () => {
    if (selectedSymptoms.size === 0) {
        alert("Please select at least one symptom from the list.");
        return;
    }

    const symptomsString = Array.from(selectedSymptoms).join(", ");

    const originalContent = predictBtn.innerHTML;
    predictBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Analyzing...';
    predictBtn.disabled = true;

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symptoms: symptomsString })
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const data = await response.json();

        if (data.status === 'emergency') {
            handleEmergency(data);
        } else {
            renderDashboard(data);
        }
    } catch (error) {
        console.error(error);
        alert("Failed to reach the diagnostic engine. Is the server running?");
    } finally {
        predictBtn.innerHTML = originalContent;
        predictBtn.disabled = false;
    }
});

function handleEmergency(data) {
    dashboard.style.display = 'block';
    emergencyAlert.style.display = 'flex';
    emergencyText.innerText = data.message;
    document.querySelector('.dashboard-grid').style.display = 'none';
    document.querySelector('.precautions-card').style.display = 'none';
    dashboard.scrollIntoView({ behavior: 'smooth' });
}

function renderDashboard(data) {
    dashboard.style.display = 'block';
    emergencyAlert.style.display = 'none';
    document.querySelector('.dashboard-grid').style.display = 'grid';
    document.querySelector('.precautions-card').style.display = 'block';

    predictionsContainer.innerHTML = '';
    const preds = data.current_predictions || data.predictions;
    preds.forEach((pred, index) => {
        const percentage = (pred.confidence * 100).toFixed(1);
        const item = document.createElement('div');
        item.classList.add('prediction-item');
        item.innerHTML = `
            <div class="pred-header">
                <span class="pred-disease">${pred.disease}</span>
                <span class="pred-score">${percentage}%</span>
            </div>
            <div class="bar-bg">
                <div class="bar-fill" style="width: 0%"></div>
            </div>
        `;
        predictionsContainer.appendChild(item);

        setTimeout(() => {
            item.querySelector('.bar-fill').style.width = `${percentage}%`;
        }, 100 + (index * 200));
    });

    shapContainer.innerHTML = '';
    if (data.shap_factors && data.shap_factors.length > 0) {
        data.shap_factors.forEach(factor => {
            const isPositive = factor.value >= 0;
            const sign = isPositive ? '+' : '';
            const valClass = isPositive ? 'shap-positive' : 'shap-negative';

            const item = document.createElement('div');
            item.classList.add('shap-item');
            item.innerHTML = `
                <span class="shap-feature">${factor.feature}</span>
                <span class="shap-badge ${valClass}">${sign}${factor.value.toFixed(3)}</span>
            `;
            shapContainer.appendChild(item);
        });
    } else {
        shapContainer.innerHTML = '<p style="color:var(--text-secondary)">No significant factors identified.</p>';
    }

    precautionsList.innerHTML = '';
    if (data.precautions && data.precautions.length > 0) {
        data.precautions.forEach(prec => {
            const li = document.createElement('li');
            li.innerHTML = `<i class="fa-solid fa-check-circle"></i> <span>${prec}</span>`;
            precautionsList.appendChild(li);
        });
    } else {
        precautionsList.innerHTML = '<li><i class="fa-solid fa-info-circle"></i> Consult a medical professional for advice.</li>';
    }

    setTimeout(() => {
        dashboard.scrollIntoView({ behavior: 'smooth' });
    }, 100);
}

resetBtn.addEventListener('click', () => {
    selectedSymptoms.clear();
    renderSelectedSymptoms();
    dashboard.style.display = 'none';
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

fetchSymptoms();
renderSelectedSymptoms();
