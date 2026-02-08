import requests
from bs4 import BeautifulSoup
import time
import sys
import os
import random

# --- CONFIGURATION ---
NTFY_TOPIC = "Internships_2026_A24" 

# [UPGRADE 1] The Bag of Masks (User Agents)
# This makes the script pretend to be a different device every time
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Build/UQ1A.240105.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.143 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15"
]

SITES = [
    "https://openai.com/careers/search",
    "https://www.google.com/about/careers/applications/jobs/results/",
    "https://unstop.com/internships?quickApply=true&oppstatus=open",
    "https://www.ubisoft.com/en-us/company/careers/interns-graduates",
    "https://jobs.lever.co/moonfroglabs",
    "https://jobs.lever.co/simple",
    "https://boards.greenhouse.io/razorpay",
    "https://boards.greenhouse.io/swiggy",
    "https://www.games24x7.com/careers",
    "https://careers.freshworks.com/jobs",
    "https://www.zoho.com/careers/",
    "https://chargebee.com/careers/",
    "https://www.experionglobal.com/careers/",
    "https://www.ibssoftware.com/careers",
    "https://jobs.lever.co/careem",
    "https://www.noon.com/careers/",
    "https://group.talabat.com/careers",
    "https://boards.greenhouse.io/telegram",
    "https://jobs.lever.co/palantir"
]

REQUIRED_TYPE = ["intern", "internship", "trainee", "student", "grad", "fresher"]

KEYWORDS = [
    "data preprocessing", "model training", "predictive modeling", 
    "deep learning", "neural networks", 
    "supervised learning", "unsupervised learning",
    "physics engines", "gameplay mechanics", "shader programming", 
    "3d mathematics", "linear algebra", "ray casting", 
    "game developer", "unity", "unreal engine",
    "react", "node.js", "django", "flask", "web developer",
    "software engineer", "backend", "frontend"
]

CHECK_INTERVAL = 900  # 15 Minutes
DURATION = 7200       # 2 Hours

def notify(message, priority="default", title="Intern Hunter"):
    try:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=message.encode('utf-8'),
            headers={
                "Title": title,
                "Priority": priority,
                "Tags": "briefcase"
            },
            timeout=10
        )
        print(f"-> Notification sent: {message}")
    except Exception as e:
        print(f"Failed to send notification: {e}")

def get_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
    }

def get_site_lines(url):
    try:
        # 1. Use Random Mask
        headers = get_random_headers()
        res = requests.get(url, headers=headers, timeout=20)
        
        if res.status_code != 200:
            print(f"Error: {url} returned status code {res.status_code}")
            return None

        soup = BeautifulSoup(res.text, 'html.parser')
        
        # --- [UPGRADE 2] THE SNIPER SCOPE (NOISE REMOVAL) ---
        # We find and DELETE these tags from the page before reading it
        for tag in soup(['header', 'footer', 'nav', 'script', 'style', 'iframe', 'meta', 'noscript']):
            tag.decompose()
        # ----------------------------------------------------
        
        # Now we only read what's left (The Body/Content)
        text = soup.get_text().lower()
        lines = set(line.strip() for line in text.splitlines() if line.strip())
        return lines
    except Exception as e:
        print(f"Error reading {url}: {e}")
        return None

def main():
    print(f"--- STARTING SNIPER HUNTER ({len(SITES)} Sites) ---")
    notify(f"Hunter started with Noise Removal active.", title="Sniper Mode ON")
    
    start_time = time.time()
    site_memory = {}
    failed_sites = []

    print("Performing initial scan...")
    for url in SITES:
        print(f"Scanning: {url}...")
        lines = get_site_lines(url)
        
        if lines is not None:
            site_memory[url] = lines
        else:
            failed_sites.append(url)

    if failed_sites:
        print(f"Warning: {len(failed_sites)} sites failed.")
        broken_list = "\n".join([u.split('//')[1].split('/')[0] for u in failed_sites])
        notify(f"Could not scrape these sites:\n{broken_list}", priority="high", title="⚠️ Broken Sites Report")
    else:
        print("All sites scanned successfully!")

    print("Initial scan complete. Waiting for changes...")

    while time.time() - start_time < DURATION:
        time.sleep(CHECK_INTERVAL)
        
        print(f"\n[{time.strftime('%H:%M')}] Checking for updates...")
        
        for url in list(site_memory.keys()):
            new_lines = get_site_lines(url)
            
            if new_lines is None:
                continue

            old_lines = site_memory[url]
            added_lines = new_lines - old_lines
            
            if added_lines:
                found_matches = []
                for line in added_lines:
                    if any(t in line for t in REQUIRED_TYPE):
                        if any(k in line for k in KEYWORDS):
                            found_matches.append(line)

                if found_matches:
                    top_match = found_matches[0]
                    display_text = top_match[:100] + "..." if len(top_match) > 100 else top_match
                    msg = f"FOUND: {display_text}\nLink: {url}"
                    notify(msg, priority="high", title="🎯 INTERNSHIP FOUND")
                    site_memory[url] = new_lines
                else:
                    # Content changed, but it was just noise or boring text
                    site_memory[url] = new_lines

    notify("Hunter finished. Shutting down server.", title="Hunter Offline")
    os.system("pkill -f location")
    os.system("pkill sshd")
    sys.exit()

if __name__ == "__main__":
    main()