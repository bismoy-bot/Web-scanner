#!/bin/bash
clear
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

echo -e "${purple}Do you want to visit the documentation before using the scanner? (Y/N)${reset}"
read doc_choice

if [[ "$doc_choice" =~ ^[Yy]$ ]]; then
    xdg-open "$DOC_URL" 2>/dev/null || termux-open-url "$DOC_URL"
fi

echo -e "${purple}Have you installed all the required Python packages ? (Y/N)${reset}"
read req_choice

if [[ "$req_choice" =~ ^[Nn]$ ]]; then
    echo -e "${green}Installing requirements...${reset}"
    pip install -r requirements.txt
fi

echo -e "${green}Running scanner...${reset}"
clear
python scanner.py
sleep 1
cd Report 
python -m http.server 8080 &
sleep 1 &

# Open mobile browser

echo -e"${green}[+] Wait it will redirect to your browser...${reset}"
echo -e "${green}[+] Opening browser at http://0.0.0.0:8000${reset}"
echo -e "${green}[+] Or Open browser at http://0.0.0.0:8000${reset}"
xdg-open http://0.0.0.0:8000
