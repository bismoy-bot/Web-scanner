#!/bin/bash

purple="\033[95m"
blue="\033[94m"
green="\033[92m"
reset="\033[0m"

# Print the colored ASCII art
echo -e "${purple}"
cat << "EOF"
 __        __   _     _ _       _
 \ \      / /__| |__ (_) |_ ___| |__   ___ ___
  \ \ /\ / / _ \ '_ \| | __/ __| '_ \ / _ / __|
   \ V  V /  __/ |_) | | || (__| | | |  __\__ \
    \_/\_/ \___|_.__/|_|\__\___|_| |_|\___|___/
EOF

echo -e "${blue}"
cat << "EOF"
__          __ _             _
\ \        / / |           (_)
 \ \  /\  / /| | ___   __ _ _ _ __   __ _
  \ \/  \/ / | |/ _ \ / _` | | '_ \ / _` |
   \  /\  /  | | (_) | (_| | | | | | (_| |
    \/  \/   |_|\___/ \__, |_|_| |_|\__, |
                      __/ |         __/ |
                     |___/         |___/
EOF

echo -e "${green}        CREATED BY BISMOY GHOSH${reset}"
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
clear
python scanner.py
