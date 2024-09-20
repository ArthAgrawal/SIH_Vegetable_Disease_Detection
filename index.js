const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const plantTypeSelect = document.getElementById('plantType');

uploadBox.addEventListener('click', () => fileInput.click());

uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('dragover');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('dragover');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        // Optional: Display the uploaded image
        const reader = new FileReader();
        reader.onload = (event) => {
            uploadBox.innerHTML = `<img src="${event.target.result}" style="max-width: 200px;">`;
        };
        reader.readAsDataURL(files[0]);
    }
});

async function uploadImage() {
    const file = fileInput.files[0];
    const plantType = plantTypeSelect.value;

    if (!file) {
        alert('Please select a file.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('plant_type', plantType);

    try {
        const response = await fetch('http://localhost:8000/predict', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok. Status: ' + response.statusText);
        }

        const result = await response.json();
        document.getElementById('result').innerText = `Class: ${result.class}, Confidence: ${result.confidence}`;
        
        // Display the remedy properly
        const remedy = result.remedy;
        if (remedy) {
            document.getElementById('remedy').innerText = `Remedy: ${remedy.remedies.join(', ')}; Home Remedies: ${remedy.home_remedies.join(', ')}`;
        } else {
            document.getElementById('remedy').innerText = 'No remedy found for this disease.';
        }

    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        alert('There was a problem with the upload. Check the console for more details.');
    }
}
