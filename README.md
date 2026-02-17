# PDF Tools - Local PDF Converter & Editor

A professional, privacy-first PDF manipulation web application that runs entirely on your local machine. All file processing happens locally - your documents never leave your computer.

## Features

### Organize PDF
- **Merge PDF** - Combine multiple PDFs into one document
- **Split PDF** - Extract pages from your PDF
- **Compress PDF** - Reduce file size while maintaining quality
- **Rotate PDF** - Rotate pages to the right orientation

### Convert from PDF
- **PDF to Word** - Convert PDF to editable Word document (.docx)
- **PDF to Images** - Extract images from PDF pages

### Convert to PDF
- **Word to PDF** - Convert Word documents (.doc, .docx) to PDF
- **Excel to PDF** - Convert Excel spreadsheets (.xls, .xlsx) to PDF
- **PowerPoint to PDF** - Convert presentations (.ppt, .pptx) to PDF
- **HTML to PDF** - Convert HTML files to PDF
- **Images to PDF** - Convert multiple images to a single PDF

## Why Choose This Tool?

✅ **100% Private** - All files are processed locally on your machine  
✅ **Fast Processing** - No upload/download time, instant results  
✅ **Unlimited Use** - No file size limits or usage restrictions  
✅ **Works Offline** - No internet connection required after setup  

## Prerequisites

### System Requirements
- Python 3.8 or higher
- LibreOffice (for Office document conversions)

### Install LibreOffice

**Debian/Ubuntu:**
```bash
sudo apt-get update
sudo apt-get install libreoffice
```

**Fedora/RHEL 8+/CentOS 8+:**
```bash
sudo dnf install libreoffice
```

**RHEL 7/CentOS 7:**
```bash
sudo yum install libreoffice
```

**openSUSE:**
```bash
sudo zypper install libreoffice
```

**Arch Linux:**
```bash
sudo pacman -S libreoffice-fresh
```

**macOS:**
```bash
brew install --cask libreoffice
```

**Windows:**
Download and install from: https://www.libreoffice.org/download/download/

## Installation

1. **Clone or download this repository**
```bash
cd /home/<user name>/converter
```

2. **Create a virtual environment (recommended)**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

4. **Verify LibreOffice installation**
```bash
libreoffice --version
```

## Running the Application

1. **Start the Flask server**
```bash
python app.py
```

2. **Open your browser and navigate to**
```
http://localhost:5000
```

3. **Start using the tools!**
   - Select a tool from the homepage
   - Upload your file(s)
   - Process and download the result

## Usage Examples

### Merge PDFs
1. Go to "Merge PDF"
2. Select 2 or more PDF files
3. Click "Merge PDFs"
4. Download the combined PDF

### Convert Word to PDF
1. Go to "Word to PDF"
2. Select a .docx or .doc file
3. Click "Convert to PDF"
4. Download the PDF

### Compress PDF
1. Go to "Compress PDF"
2. Select a PDF file
3. Click "Compress PDF"
4. Download the compressed version

## Project Structure

```
converter/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── utils/
│   ├── pdf_operations.py  # PDF manipulation functions
│   └── converters.py      # Format conversion functions
├── templates/             # HTML templates
│   ├── index.html
│   ├── merge_pdf.html
│   ├── split_pdf.html
│   └── ...
├── static/
│   ├── css/
│   │   └── style.css      # Professional styling
│   └── js/
│       ├── merge.js       # Merge functionality
│       └── converter.js   # Generic converter
├── uploads/               # Temporary upload storage
└── outputs/               # Processed file storage
```

## Security & Privacy

- All file processing happens locally on your machine
- Files are automatically cleaned up after 2 hours
- No data is sent to external servers
- No tracking or analytics
- Open source - you can review the code

## Troubleshooting

### LibreOffice conversion fails
- Ensure LibreOffice is installed: `libreoffice --version`
- **Debian/Ubuntu**: `sudo apt-get install libreoffice-writer libreoffice-calc libreoffice-impress`
- **Fedora/RHEL 8+**: `sudo dnf install libreoffice-writer libreoffice-calc libreoffice-impress`
- **RHEL 7/CentOS 7**: `sudo yum install libreoffice-writer libreoffice-calc libreoffice-impress`

### Port 5000 already in use
Edit `app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Module not found errors
Make sure you've activated the virtual environment and installed requirements:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Technology Stack

- **Backend**: Flask (Python)
- **PDF Processing**: pypdf, PyMuPDF
- **Conversions**: pdf2docx, LibreOffice, weasyprint
- **Image Processing**: Pillow
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **UI/UX**: Modern gradient design, responsive layout

## License

This project is open source and available for personal and commercial use.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Support

For issues or questions, please create an issue in the repository.

---

**Made with ❤️ for privacy-conscious users**
