# Quick Start Guide

## Installation (3 Easy Steps)

### Step 1: Install LibreOffice (Required for Office conversions)

**Debian/Ubuntu:**
```bash
sudo apt-get update && sudo apt-get install libreoffice
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
Download from: https://www.libreoffice.org/download/download/

### Step 2: Run Setup Script

```bash
cd /home/leapfrog/poc/converter
./setup.sh
```

This will:
- Create a virtual environment
- Install all Python dependencies
- Verify your system is ready

### Step 3: Start the Application

```bash
./start.sh
```

Or manually:
```bash
source venv/bin/activate
python app.py
```

### Step 4: Open Your Browser

Navigate to: **http://localhost:5000**

## Features Available

✅ Merge multiple PDFs  
✅ Split PDF into pages  
✅ Compress PDF files  
✅ Rotate PDF pages  
✅ PDF ↔ Word conversion  
✅ Excel → PDF  
✅ PowerPoint → PDF  
✅ HTML → PDF  
✅ Images ↔ PDF  

## Privacy Features

🔒 All processing happens locally  
🔒 No internet required (after setup)  
🔒 No file uploads to external servers  
🔒 Automatic file cleanup after 2 hours  

## Troubleshooting

**Port 5000 in use?**
Edit `app.py` line 51: change `port=5000` to `port=5001`

**LibreOffice not found?**
Ensure it's in your PATH: `libreoffice --version`

**Module errors?**
Reinstall dependencies: `pip install -r requirements.txt`

## Need Help?

Check the full README.md for detailed documentation.
