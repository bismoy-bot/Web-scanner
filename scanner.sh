#!/bin/bash

# Your Blogspot documentation URL
DOC_URL="https://infoverseb.blogspot.com/2025/04/python-web-scannereasy-to-use.html?m=1"

echo "Do you want to visit the documentation before using the scanner? (Y/N)"
read doc_choice

if [[ "$doc_choice" =~ ^[Yy]$ ]]; then
    xdg-open "$DOC_URL" 2>/dev/null || termux-open-url "$DOC_URL"
fi

echo "Have you installed all the required Python packages from requirements.txt? (Y/N)"
read req_choice

if [[ "$req_choice" =~ ^[Nn]$ ]]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
fi

echo "Running scanner..."
python scanner.py
