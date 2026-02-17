import pypdf
from pypdf import PdfReader, PdfWriter
import os
import fitz  # PyMuPDF
from PIL import Image
import io

def merge_pdfs(input_paths, output_path):
    writer = PdfWriter()
    for pdf in input_paths:
        reader = PdfReader(pdf)
        for page in reader.pages:
            writer.add_page(page)
    with open(output_path, 'wb') as f:
        writer.write(f)

def split_pdf(input_path, output_dir, mode='all', pages=''):
    reader = PdfReader(input_path)
    result_files = []
    
    if mode == 'all':
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            output_file = os.path.join(output_dir, f'page_{i+1}.pdf')
            with open(output_file, 'wb') as f:
                writer.write(f)
            result_files.append(os.path.basename(output_file))
    elif mode == 'range' and pages:
        page_ranges = pages.split(',')
        for idx, page_range in enumerate(page_ranges):
            writer = PdfWriter()
            if '-' in page_range:
                start, end = map(int, page_range.split('-'))
                for i in range(start-1, min(end, len(reader.pages))):
                    writer.add_page(reader.pages[i])
            else:
                page_num = int(page_range) - 1
                if 0 <= page_num < len(reader.pages):
                    writer.add_page(reader.pages[page_num])
            
            output_file = os.path.join(output_dir, f'split_{idx+1}.pdf')
            with open(output_file, 'wb') as f:
                writer.write(f)
            result_files.append(os.path.basename(output_file))
    
    return result_files

def compress_pdf(input_path, output_path, quality=70):
    quality = int(quality) if isinstance(quality, str) else quality
    
    doc = fitz.open(input_path)
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images()
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            
            image = Image.open(io.BytesIO(image_bytes))
            
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            
            output_buffer = io.BytesIO()
            image.save(output_buffer, format='JPEG', quality=quality, optimize=True)
            output_buffer.seek(0)
            
            doc._deleteObject(xref)
            page.insert_image(page.rect, stream=output_buffer.getvalue())
    
    doc.save(output_path, garbage=4, deflate=True, clean=True)
    doc.close()

def rotate_pdf(input_path, output_path, angle, pages='all'):
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    for i, page in enumerate(reader.pages):
        if pages == 'all' or str(i+1) in pages.split(','):
            page.rotate(angle)
        writer.add_page(page)
    
    with open(output_path, 'wb') as f:
        writer.write(f)

def extract_pages(input_path, output_path, page_numbers):
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    for page_num in page_numbers:
        if 0 <= page_num < len(reader.pages):
            writer.add_page(reader.pages[page_num])
    
    with open(output_path, 'wb') as f:
        writer.write(f)

def add_watermark(input_path, output_path, watermark_text):
    pass

def protect_pdf(input_path, output_path, password):
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    for page in reader.pages:
        writer.add_page(page)
    
    writer.encrypt(password)
    
    with open(output_path, 'wb') as f:
        writer.write(f)

def unlock_pdf(input_path, output_path, password):
    reader = PdfReader(input_path)
    if reader.is_encrypted:
        reader.decrypt(password)
    
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    
    with open(output_path, 'wb') as f:
        writer.write(f)
