import subprocess
import os
from pdf2docx import Converter
from PIL import Image
import pypdf
from pypdf import PdfWriter
import fitz

def pdf_to_word(input_path, output_path):
    cv = Converter(input_path)
    cv.convert(output_path)
    cv.close()

def word_to_pdf(input_path, output_path):
    subprocess.run([
        'libreoffice', '--headless', '--convert-to', 'pdf',
        '--outdir', os.path.dirname(output_path), input_path
    ], check=True)
    
    temp_output = os.path.join(
        os.path.dirname(output_path),
        os.path.splitext(os.path.basename(input_path))[0] + '.pdf'
    )
    if os.path.exists(temp_output) and temp_output != output_path:
        os.rename(temp_output, output_path)

def excel_to_pdf(input_path, output_path):
    subprocess.run([
        'libreoffice', '--headless', '--convert-to', 'pdf',
        '--outdir', os.path.dirname(output_path), input_path
    ], check=True)
    
    temp_output = os.path.join(
        os.path.dirname(output_path),
        os.path.splitext(os.path.basename(input_path))[0] + '.pdf'
    )
    if os.path.exists(temp_output) and temp_output != output_path:
        os.rename(temp_output, output_path)

def ppt_to_pdf(input_path, output_path):
    subprocess.run([
        'libreoffice', '--headless', '--convert-to', 'pdf',
        '--outdir', os.path.dirname(output_path), input_path
    ], check=True)
    
    temp_output = os.path.join(
        os.path.dirname(output_path),
        os.path.splitext(os.path.basename(input_path))[0] + '.pdf'
    )
    if os.path.exists(temp_output) and temp_output != output_path:
        os.rename(temp_output, output_path)

def html_to_pdf(input_path, output_path):
    from weasyprint import HTML
    HTML(filename=input_path).write_pdf(output_path)

def images_to_pdf(input_paths, output_path):
    images = []
    for img_path in input_paths:
        img = Image.open(img_path)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        images.append(img)
    
    if images:
        images[0].save(output_path, save_all=True, append_images=images[1:])

def pdf_to_images(input_path, output_dir, format_type='png', quality=95):
    doc = fitz.open(input_path)
    result_files = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        
        if format_type in ['jpg', 'jpeg', 'webp', 'tiff']:
            img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
            output_file = os.path.join(output_dir, f'page_{page_num+1}.{format_type}')
            
            if format_type in ['jpg', 'jpeg']:
                img.save(output_file, 'JPEG', quality=quality, optimize=True)
            elif format_type == 'webp':
                img.save(output_file, 'WEBP', quality=quality)
            elif format_type == 'tiff':
                img.save(output_file, 'TIFF', compression='tiff_lzw')
        else:
            output_file = os.path.join(output_dir, f'page_{page_num+1}.png')
            if quality < 100:
                img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
                img.save(output_file, 'PNG', optimize=True, compress_level=int((100-quality)/10))
            else:
                pix.save(output_file)
        
        result_files.append(os.path.basename(output_file))
    
    doc.close()
    return result_files


def compress_images(input_paths, output_dir, format_type='original', quality=70):
    result_files = []
    
    for input_path in input_paths:
        img = Image.open(input_path)
        original_size = os.path.getsize(input_path)
        
        if img.mode == 'RGBA' and format_type in ['jpg', 'jpeg']:
            img = img.convert('RGB')
        
        original_name = os.path.basename(input_path)
        if format_type == 'original':
            ext = os.path.splitext(original_name)[1].lower()
            output_file = os.path.join(output_dir, original_name)
            
            if ext in ['.jpg', '.jpeg']:
                img.save(output_file, 'JPEG', quality=quality, optimize=True)
            elif ext == '.png':
                img.save(output_file, 'PNG', optimize=True, compress_level=int((100-quality)/10))
            elif ext == '.webp':
                img.save(output_file, 'WEBP', quality=quality)
            else:
                img.save(output_file, quality=quality, optimize=True)
        else:
            base_name = os.path.splitext(original_name)[0]
            output_file = os.path.join(output_dir, f'{base_name}.{format_type}')
            
            if format_type in ['jpg', 'jpeg']:
                img.save(output_file, 'JPEG', quality=quality, optimize=True)
            elif format_type == 'png':
                img.save(output_file, 'PNG', optimize=True, compress_level=int((100-quality)/10))
            elif format_type == 'webp':
                img.save(output_file, 'WEBP', quality=quality)
        
        compressed_size = os.path.getsize(output_file)
        
        result_files.append({
            'filename': os.path.basename(output_file),
            'originalName': original_name,
            'originalSize': original_size,
            'compressedSize': compressed_size
        })
    
    return result_files
