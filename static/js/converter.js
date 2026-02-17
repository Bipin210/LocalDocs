let selectedFile = null;
const apiEndpoint = document.currentScript.getAttribute('data-api');

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
const processBtn = document.getElementById('processBtn');
const loading = document.getElementById('loading');
const result = document.getElementById('result');
const error = document.getElementById('error');
const downloadBtn = document.getElementById('downloadBtn');

uploadArea.addEventListener('click', (e) => {
    if (e.target !== fileInput) {
        fileInput.click();
    }
});

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    if (e.dataTransfer.files.length > 0) {
        handleFile(e.dataTransfer.files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

function handleFile(file) {
    selectedFile = file;
    updateFileList();
}

function updateFileList() {
    if (!selectedFile) {
        fileList.innerHTML = '';
        processBtn.style.display = 'none';
        return;
    }

    fileList.innerHTML = `
        <div class="file-item">
            <div class="file-info">
                <i class="fas fa-file"></i>
                <span>${selectedFile.name}</span>
            </div>
            <button class="remove-file" onclick="removeFile()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;

    processBtn.style.display = 'block';
}

function removeFile() {
    selectedFile = null;
    fileInput.value = '';
    updateFileList();
}

processBtn.addEventListener('click', async () => {
    if (!selectedFile) {
        showError('Please select a file.');
        return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    loading.classList.add('active');
    processBtn.disabled = true;
    error.classList.remove('active');
    result.classList.remove('active');

    try {
        const response = await fetch(apiEndpoint, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            downloadBtn.href = '/download/' + data.filename;
            result.classList.add('active');
        } else {
            showError(data.error || 'An error occurred during conversion.');
        }
    } catch (err) {
        showError('Failed to convert file. Please try again.');
    } finally {
        loading.classList.remove('active');
        processBtn.disabled = false;
    }
});

function showError(message) {
    error.textContent = message;
    error.classList.add('active');
}
