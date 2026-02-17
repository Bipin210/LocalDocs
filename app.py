from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime, timedelta
import threading
import time
from utils.pdf_operations import (
    merge_pdfs, split_pdf, compress_pdf, rotate_pdf, 
    extract_pages, add_watermark, protect_pdf, unlock_pdf
)
from utils.converters import (
    pdf_to_word, word_to_pdf, excel_to_pdf, 
    ppt_to_pdf, html_to_pdf, images_to_pdf, pdf_to_images, compress_images
)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {
    'pdf', 'docx', 'doc', 'xlsx', 'xls', 'pptx', 'ppt', 
    'html', 'htm', 'png', 'jpg', 'jpeg', 'gif', 'bmp'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanup_old_files():
    while True:
        time.sleep(3600)  # Run every hour
        now = datetime.now()
        for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
            for filename in os.listdir(folder):
                filepath = os.path.join(folder, filename)
                if os.path.isfile(filepath):
                    file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    if now - file_time > timedelta(hours=2):
                        os.remove(filepath)

cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
cleanup_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge-pdf')
def merge_pdf_page():
    return render_template('merge_pdf.html')

@app.route('/split-pdf')
def split_pdf_page():
    return render_template('split_pdf.html')

@app.route('/compress-pdf')
def compress_pdf_page():
    return render_template('compress_pdf.html')

@app.route('/pdf-to-word')
def pdf_to_word_page():
    return render_template('pdf_to_word.html')

@app.route('/word-to-pdf')
def word_to_pdf_page():
    return render_template('word_to_pdf.html')

@app.route('/excel-to-pdf')
def excel_to_pdf_page():
    return render_template('excel_to_pdf.html')

@app.route('/ppt-to-pdf')
def ppt_to_pdf_page():
    return render_template('ppt_to_pdf.html')

@app.route('/html-to-pdf')
def html_to_pdf_page():
    return render_template('html_to_pdf.html')

@app.route('/images-to-pdf')
def images_to_pdf_page():
    return render_template('images_to_pdf.html')

@app.route('/pdf-to-images')
def pdf_to_images_page():
    return render_template('pdf_to_images.html')

@app.route('/rotate-pdf')
def rotate_pdf_page():
    return render_template('rotate_pdf.html')

@app.route('/compress-images')
def compress_images_page():
    return render_template('compress_images.html')

@app.route('/api/merge', methods=['POST'])
def api_merge():
    try:
        files = request.files.getlist('files')
        if len(files) < 2:
            return jsonify({'error': 'At least 2 PDF files required'}), 400
        
        input_paths = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                input_paths.append(filepath)
        
        output_filename = f"{uuid.uuid4()}_merged.pdf"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        merge_pdfs(input_paths, output_path)
        
        return jsonify({'success': True, 'filename': output_filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/split', methods=['POST'])
def api_split():
    try:
        file = request.files['file']
        mode = request.form.get('mode', 'all')
        pages = request.form.get('pages', '')
        
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        folder_id = str(uuid.uuid4())
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], folder_id)
        os.makedirs(output_dir, exist_ok=True)
        
        result_files = split_pdf(filepath, output_dir, mode, pages)
        
        return jsonify({'success': True, 'files': result_files, 'folder': folder_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compress', methods=['POST'])
def api_compress():
    try:
        file = request.files['file']
        quality = int(request.form.get('quality', 70))
        
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        original_size = os.path.getsize(filepath)
        
        output_filename = f"{uuid.uuid4()}_compressed.pdf"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        compress_pdf(filepath, output_path, quality)
        
        compressed_size = os.path.getsize(output_path)
        
        return jsonify({
            'success': True, 
            'filename': output_filename,
            'originalSize': original_size,
            'compressedSize': compressed_size
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rotate', methods=['POST'])
def api_rotate():
    try:
        file = request.files['file']
        angle = int(request.form.get('angle', 90))
        pages = request.form.get('pages', 'all')
        
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        output_filename = f"{uuid.uuid4()}_rotated.pdf"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        rotate_pdf(filepath, output_path, angle, pages)
        
        return jsonify({'success': True, 'filename': output_filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pdf-to-word', methods=['POST'])
def api_pdf_to_word():
    try:
        file = request.files['file']
        
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        output_filename = f"{uuid.uuid4()}_converted.docx"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        pdf_to_word(filepath, output_path)
        
        return jsonify({'success': True, 'filename': output_filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/word-to-pdf', methods=['POST'])
def api_word_to_pdf():
    try:
        file = request.files['file']
        
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        output_filename = f"{uuid.uuid4()}_converted.pdf"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        word_to_pdf(filepath, output_path)
        
        return jsonify({'success': True, 'filename': output_filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/excel-to-pdf', methods=['POST'])
def api_excel_to_pdf():
    try:
        file = request.files['file']
        
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        output_filename = f"{uuid.uuid4()}_converted.pdf"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        excel_to_pdf(filepath, output_path)
        
        return jsonify({'success': True, 'filename': output_filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ppt-to-pdf', methods=['POST'])
def api_ppt_to_pdf():
    try:
        file = request.files['file']
        
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        output_filename = f"{uuid.uuid4()}_converted.pdf"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        ppt_to_pdf(filepath, output_path)
        
        return jsonify({'success': True, 'filename': output_filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/html-to-pdf', methods=['POST'])
def api_html_to_pdf():
    try:
        file = request.files['file']
        
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        output_filename = f"{uuid.uuid4()}_converted.pdf"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        html_to_pdf(filepath, output_path)
        
        return jsonify({'success': True, 'filename': output_filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/images-to-pdf', methods=['POST'])
def api_images_to_pdf():
    try:
        files = request.files.getlist('files')
        
        input_paths = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                input_paths.append(filepath)
        
        output_filename = f"{uuid.uuid4()}_converted.pdf"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        images_to_pdf(input_paths, output_path)
        
        return jsonify({'success': True, 'filename': output_filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pdf-to-images', methods=['POST'])
def api_pdf_to_images():
    try:
        file = request.files['file']
        format_type = request.form.get('format', 'png')
        quality = int(request.form.get('quality', 95))
        
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        folder_id = str(uuid.uuid4())
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], folder_id)
        os.makedirs(output_dir, exist_ok=True)
        
        result_files = pdf_to_images(filepath, output_dir, format_type, quality)
        
        return jsonify({'success': True, 'files': result_files, 'folder': folder_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    return send_file(
        os.path.join(app.config['OUTPUT_FOLDER'], filename),
        as_attachment=True,
        download_name=filename.split('_', 1)[1] if '_' in filename else filename
    )

@app.route('/download/<folder>/<filename>')
def download_from_folder(folder, filename):
    return send_file(
        os.path.join(app.config['OUTPUT_FOLDER'], folder, filename),
        as_attachment=True,
        download_name=filename
    )

@app.route('/api/compress-images', methods=['POST'])
def api_compress_images():
    try:
        files = request.files.getlist('files')
        format_type = request.form.get('format', 'original')
        quality = int(request.form.get('quality', 70))
        
        if len(files) == 0:
            return jsonify({'error': 'No files provided'}), 400
        
        input_paths = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                input_paths.append(filepath)
        
        folder_id = str(uuid.uuid4())
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], folder_id)
        os.makedirs(output_dir, exist_ok=True)
        
        result_files = compress_images(input_paths, output_dir, format_type, quality)
        
        return jsonify({'success': True, 'files': result_files, 'folder': folder_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
