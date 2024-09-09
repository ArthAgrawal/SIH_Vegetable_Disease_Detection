const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const plantTypeSelect = document.getElementById('plantType');  // New: Reference to the dropdown

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
    }
});

async function uploadImage() {
    const file = fileInput.files[0];
    const plantType = plantTypeSelect.value;  // Get selected plant type

    if (!file) {
        alert('Please select a file.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('plant_type', plantType);  // Include plant type in form data

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
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        alert('There was a problem with the upload. Check the console for more details.');
    }
}
