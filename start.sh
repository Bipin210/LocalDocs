#!/bin/bash

echo "Starting PDF Tools..."
echo ""

if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup first..."
    ./setup.sh
fi

source venv/bin/activate
python app.py
