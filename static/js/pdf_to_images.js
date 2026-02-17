let selectedFile = null;
let selectedFormat = 'png';
let selectedQuality = 95;

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
const processBtn = document.getElementById('processBtn');
const loading = document.getElementById('loading');
const result = document.getElementById('result');
const error = document.getElementById('error');

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
        document.getElementById('formatOptions').style.display = 'none';
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

    document.getElementById('formatOptions').style.display = 'block';
    processBtn.style.display = 'block';
}

function removeFile() {
    selectedFile = null;
    fileInput.value = '';
    updateFileList();
}

function setFormat(format) {
    selectedFormat = format;
    document.querySelectorAll('.format-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelector(`[data-format="${format}"]`).classList.add('active');
}

function updateQuality(value) {
    selectedQuality = parseInt(value);
    document.getElementById('qualityValue').textContent = value;
}

processBtn.addEventListener('click', async () => {
    if (!selectedFile) {
        showError('Please select a file.');
        return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('format', selectedFormat);
    formData.append('quality', selectedQuality);

    loading.style.display = 'flex';
    processBtn.style.display = 'none';
    error.style.display = 'none';
    result.style.display = 'none';

    try {
        const response = await fetch('/api/pdf-to-images', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success && data.files) {
            result.querySelector('p').textContent = `Converted to ${data.files.length} images (${selectedFormat.toUpperCase()}).`;
            
            const downloadLinks = document.getElementById('downloadLinks');
            downloadLinks.innerHTML = data.files.map((file, index) => `
                <a href="/download/${data.folder}/${file}" class="btn btn-success" style="margin: 0.5rem;" download>
                    <i class="fas fa-download"></i> Image ${index + 1}
                </a>
            `).join('');
            
            result.style.display = 'block';
        } else {
            showError(data.error || 'An error occurred during conversion.');
        }
    } catch (err) {
        showError('Failed to convert file. Please try again.');
    } finally {
        loading.style.display = 'none';
    }
});

function showError(message) {
    error.textContent = message;
    error.style.display = 'block';
}
