import requests
from bs4 import BeautifulSoup
import ssl
import socket
import os
import tldextract
from urllib.parse import urlparse
from datetime import datetime
import shutil
import webbrowser

def banner():
    print("\033[95m" + r"""
 __        __   _     _ _       _             
 \ \      / /__| |__ (_) |_ ___| |__   ___ ___ 
  \ \ /\ / / _ \ '_ \| | __/ __| '_ \ / _ / __|
   \ V  V /  __/ |_) | | || (__| | | |  __\__ \
    \_/\_/ \___|_.__/|_|\__\___|_| |_|\___|___/
""" + "\033[94m" + r"""
__          __ _             _             
\ \        / / |           (_)            
 \ \  /\  / /| | ___   __ _ _ _ __   __ _ 
  \ \/  \/ / | |/ _ \ / _` | | '_ \ / _` |
   \  /\  /  | | (_) | (_| | | | | | (_| |
    \/  \/   |_|\___/ \__, |_|_| |_|\__, |
                      __/ |         __/ |
                     |___/         |___/ 
""" + "\033[92m" + "\n        CREATED BY BISMOY GHOSH\n" + "\033[0m")

def get_ssl_info(hostname):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.settimeout(5)
            s.connect((hostname, 443))
            cert = s.getpeercert()
            return cert
    except Exception as e:
        return str(e)

def get_ip_info(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return "N/A"

def is_phishing(url):
    red_flags = ["@", "bit.ly", "tinyurl", "rb.gy", "t.co", "shorturl.at"]
    flag_count = sum(1 for flag in red_flags if flag in url.lower())
    return flag_count >= 1

def unmask_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        return response.url
    except:
        return url

def generate_html_report(info):
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    domain_name = tldextract.extract(info['original_url']).domain
    html_path = os.path.join(downloads, f"report_{domain_name}.html")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Link Analysis Report - {info['domain']}</title>
    <style>
        body {{ font-family: 'Arial', sans-serif; background-color: #f7f7f7; padding: 20px; }}
        h1 {{ color: #1d3557; }}
        .report-container {{ max-width: 1200px; margin: 0 auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }}
        .box {{ background: #fafafa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 5px solid #1d3557; }}
        h2 {{ color: #1d3557; margin-bottom: 10px; }}
        p {{ font-size: 14px; color: #333; line-height: 1.5; }}
        .key {{ font-weight: bold; color: #1d3557; }}
        .value {{ color: #555; }}
        .phishing {{ color: red; }}
        .safe {{ color: green; }}
        .links {{ list-style-type: none; padding-left: 0; }}
        .links li {{ margin: 5px 0; }}
        .links a {{ color: #1d3557; text-decoration: none; }}
        footer {{ margin-top: 20px; font-size: 12px; text-align: center; color: #555; }}
    </style>
</head>
<body>
    <div class="report-container">
        <h1>Link Analysis Report</h1>
        <div class="box">
            <h2>Report Generated: {info['generated_time']}</h2>
            <p><span class="key">Original URL:</span> <span class="value">{info['original_url']}</span></p>
            <p><span class="key">Final URL (after redirects):</span> <span class="value">{info['final_url']}</span></p>
        </div>
        
        <div class="box">
            <h2>Domain Information</h2>
            <p><span class="key">Domain:</span> <span class="value">{info['domain']}</span></p>
            <p><span class="key">IP Address:</span> <span class="value">{info['ip']}</span></p>
        </div>

        <div class="box">
            <h2>SSL Certificate Information</h2>
            <p><span class="key">Issuer:</span> <span class="value">{info['ssl_issuer']}</span></p>
            <p><span class="key">Valid From:</span> <span class="value">{info['ssl_from']}</span></p>
            <p><span class="key">Valid To:</span> <span class="value">{info['ssl_to']}</span></p>
        </div>

        <div class="box">
            <h2>Content Information</h2>
            <p><span class="key">Server:</span> <span class="value">{info['server']}</span></p>
            <p><span class="key">Content-Type:</span> <span class="value">{info['content_type']}</span></p>
            <p><span class="key">Page Size:</span> <span class="value">{info['size']} bytes</span></p>
            <p><span class="key">Page Title:</span> <span class="value">{info['title']}</span></p>
        </div>

        <div class="box">
            <h2>Redirect History</h2>
            <ul class="links">
                {''.join(f'<li><a href="{url}">{url}</a></li>' for url in info['redirects'])}
            </ul>
        </div>

        <div class="box">
            <h2>Phishing Detection</h2>
            <p class="phishing" style="color: {'red' if info['phishing'] else 'green'};">
                <span class="key">Phishing Risk:</span> {'Yes, suspicious indicators found!' if info['phishing'] else 'No obvious signs of phishing.'}
            </p>
        </div>

        <div class="box">
            <h2>Links Found on the Page</h2>
            <ul class="links">
                {''.join(f'<li><a href="{link}">{link}</a></li>' for link in info['links'])}
            </ul>
        </div>

        <footer>
            <p>Created by Bismoy Ghosh | Link Analysis Tool</p>
        </footer>
    </div>
</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n[+] Report saved as: {html_path}")

def get_link_info(url):
    try:
        unmasked = unmask_url(url)
        response = requests.get(unmasked, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        parsed_url = urlparse(response.url)
        domain = tldextract.extract(response.url).domain
        ip = get_ip_info(parsed_url.hostname)
        ssl_info = {'issuer': 'N/A', 'from': 'N/A', 'to': 'N/A'}
        if parsed_url.scheme == "https":
            cert = get_ssl_info(parsed_url.hostname)
            if isinstance(cert, dict):
                ssl_info = {
                    'issuer': str(cert.get('issuer')),
                    'from': cert.get('notBefore'),
                    'to': cert.get('notAfter')
                }

        title = soup.title.string.strip() if soup.title else 'No Title Found'
        links = [a.get('href') for a in soup.find_all('a') if a.get('href')]

        info = {
            "generated_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "original_url": url,
            "final_url": response.url,
            "status": response.status_code,
            "domain": domain,
            "ip": ip,
            "server": response.headers.get('Server', 'N/A'),
            "content_type": response.headers.get('Content-Type', 'N/A'),
            "size": len(response.content),
            "title": title,
            "redirects": [r.url for r in response.history] + [response.url],
            "ssl_issuer": ssl_info['issuer'],
            "ssl_from": ssl_info['from'],
            "ssl_to": ssl_info['to'],
            "phishing": is_phishing(unmasked),
            "links": links[:20]
        }

        generate_html_report(info)

    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    banner()
    target_url = input("Enter the URL to analyze:(with https://) ")
    get_link_info(target_url)
  
