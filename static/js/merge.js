let selectedFiles = [];

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
    handleFiles(e.dataTransfer.files);
});

fileInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

function handleFiles(files) {
    for (let file of files) {
        if (file.type === 'application/pdf') {
            selectedFiles.push(file);
        }
    }
    updateFileList();
}

function updateFileList() {
    if (selectedFiles.length === 0) {
        fileList.innerHTML = '';
        processBtn.style.display = 'none';
        return;
    }

    fileList.innerHTML = '<h3>Selected Files (' + selectedFiles.length + ')</h3>';
    selectedFiles.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.innerHTML = `
            <div class="file-info">
                <i class="fas fa-file-pdf"></i>
                <span>${file.name}</span>
            </div>
            <button class="remove-file" onclick="removeFile(${index})">
                <i class="fas fa-times"></i>
            </button>
        `;
        fileList.appendChild(fileItem);
    });

    processBtn.style.display = selectedFiles.length >= 2 ? 'block' : 'none';
}

function removeFile(index) {
    selectedFiles.splice(index, 1);
    updateFileList();
}

processBtn.addEventListener('click', async () => {
    if (selectedFiles.length < 2) {
        showError('Please select at least 2 PDF files to merge.');
        return;
    }

    const formData = new FormData();
    selectedFiles.forEach(file => {
        formData.append('files', file);
    });

    loading.classList.add('active');
    processBtn.disabled = true;
    error.classList.remove('active');
    result.classList.remove('active');

    try {
        const response = await fetch('/api/merge', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            downloadBtn.href = '/download/' + data.filename;
            result.classList.add('active');
        } else {
            showError(data.error || 'An error occurred while merging PDFs.');
        }
    } catch (err) {
        showError('Failed to merge PDFs. Please try again.');
    } finally {
        loading.classList.remove('active');
        processBtn.disabled = false;
    }
});

function showError(message) {
    error.textContent = message;
    error.classList.add('active');
}
