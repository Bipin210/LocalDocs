let selectedFiles = [];
let selectedFormat = 'jpg';
let selectedQuality = 70;

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
        handleFiles(Array.from(e.dataTransfer.files));
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFiles(Array.from(e.target.files));
    }
});

function handleFiles(files) {
    selectedFiles = files;
    updateFileList();
}

function updateFileList() {
    if (selectedFiles.length === 0) {
        fileList.innerHTML = '';
        processBtn.style.display = 'none';
        document.getElementById('compressionOptions').style.display = 'none';
        return;
    }

    fileList.innerHTML = selectedFiles.map((file, index) => `
        <div class="file-item">
            <div class="file-info">
                <i class="fas fa-image"></i>
                <span>${file.name}</span>
                <small style="color: #666; margin-left: 0.5rem;">(${(file.size / 1024).toFixed(1)} KB)</small>
            </div>
            <button class="remove-file" onclick="removeFile(${index})">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `).join('');

    document.getElementById('compressionOptions').style.display = 'block';
    processBtn.style.display = 'block';
}

function removeFile(index) {
    selectedFiles.splice(index, 1);
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
    if (selectedFiles.length === 0) {
        showError('Please select at least one image.');
        return;
    }

    const formData = new FormData();
    selectedFiles.forEach(file => {
        formData.append('files', file);
    });
    formData.append('format', selectedFormat);
    formData.append('quality', selectedQuality);

    loading.style.display = 'flex';
    processBtn.style.display = 'none';
    error.style.display = 'none';
    result.style.display = 'none';

    try {
        const response = await fetch('/api/compress-images', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success && data.files) {
            const totalOriginal = data.files.reduce((sum, f) => sum + f.originalSize, 0);
            const totalCompressed = data.files.reduce((sum, f) => sum + f.compressedSize, 0);
            const savings = ((1 - totalCompressed / totalOriginal) * 100).toFixed(1);
            
            result.querySelector('p').textContent = 
                `Compressed ${data.files.length} images. Total size reduced from ${(totalOriginal / 1024).toFixed(1)}KB to ${(totalCompressed / 1024).toFixed(1)}KB (${savings}% smaller)`;
            
            const downloadLinks = document.getElementById('downloadLinks');
            downloadLinks.innerHTML = data.files.map((file, index) => `
                <a href="/download/${data.folder}/${file.filename}" class="btn btn-success" style="margin: 0.5rem;" download>
                    <i class="fas fa-download"></i> ${file.originalName} 
                    <small>(${(file.compressedSize / 1024).toFixed(1)}KB)</small>
                </a>
            `).join('');
            
            result.style.display = 'block';
        } else {
            showError(data.error || 'An error occurred during compression.');
        }
    } catch (err) {
        showError('Failed to compress images. Please try again.');
    } finally {
        loading.style.display = 'none';
    }
});

function showError(message) {
    error.textContent = message;
    error.style.display = 'block';
}
