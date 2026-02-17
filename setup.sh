#!/bin/bash

echo "======================================"
echo "PDF Tools - Setup Script"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 is installed"
echo ""

# Check LibreOffice
echo "Checking LibreOffice installation..."
libreoffice --version

if [ $? -ne 0 ]; then
    echo "⚠️  LibreOffice is not installed."
    echo "LibreOffice is required for Office document conversions (Word, Excel, PowerPoint to PDF)."
    echo ""
    echo "To install LibreOffice:"
    
    # Detect package manager
    if command -v apt-get &> /dev/null; then
        echo "  Detected: Debian/Ubuntu system"
        echo "  Run: sudo apt-get update && sudo apt-get install libreoffice"
    elif command -v dnf &> /dev/null; then
        echo "  Detected: Fedora/RHEL 8+ system"
        echo "  Run: sudo dnf install libreoffice"
    elif command -v yum &> /dev/null; then
        echo "  Detected: RHEL/CentOS 7 system"
        echo "  Run: sudo yum install libreoffice"
    elif command -v zypper &> /dev/null; then
        echo "  Detected: openSUSE system"
        echo "  Run: sudo zypper install libreoffice"
    elif command -v pacman &> /dev/null; then
        echo "  Detected: Arch Linux system"
        echo "  Run: sudo pacman -S libreoffice-fresh"
    elif command -v brew &> /dev/null; then
        echo "  Detected: macOS system"
        echo "  Run: brew install --cask libreoffice"
    else
        echo "  Manual download: https://www.libreoffice.org/download/download/"
    fi
    
    echo ""
    read -p "Continue without LibreOffice? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ LibreOffice is installed"
fi

echo ""
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created"
echo ""

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"
echo ""

echo "======================================"
echo "Setup Complete! 🎉"
echo "======================================"
echo ""
echo "To start the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the app: python app.py"
echo "  3. Open browser: http://localhost:5000"
echo ""
echo "Enjoy your privacy-first PDF tools!"
