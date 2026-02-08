import requests
from bs4 import BeautifulSoup
import time
import sys
import os
import random
import json

# --- CONFIGURATION ---
# 1. PASTE YOUR DISCORD WEBHOOK URL HERE (Keep the quotes!)
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1470059124078149749/mbdfVHQJwNXUskEKgcsJDEQ7js0NPGbfPYCRlTdTyY4RtFynALU0ZAw-65LFsDOwyFMB"

# 2. File Name for the database
MEMORY_FILE = "job_history.json"

# [Stealth Mode] User Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Build/UQ1A.240105.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.143 Mobile Safari/537.36"
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

# --- DATABASE ENGINE ---
def load_memory():
    """Tries to read the history file. If missing, starts fresh."""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {} 

def save_memory(memory):
    """Saves the current list of jobs to the file"""
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=4)

# --- NOTIFICATION SYSTEM (DISCORD) ---
def notify_discord(job_title, url):
    """Sends the alert to your Discord Channel"""
    data = {
        "embeds": [{
            "title": "🎯 New Internship Found!",
            "description": f"**Role:** {job_title}\n**Link:** [Click to Apply]({url})",
            "color": 5763719, # Green Color
            "footer": {"text": "Hunter Bot 2.0"}
        }]
    }
    try:
        requests.post(DISCORD_WEBHOOK, json=data)
        print(f"-> Discord alert sent: {job_title}")
    except Exception as e:
        print(f"Failed to send to Discord: {e}")

# --- MAIN LOGIC ---
def get_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
    }

def get_site_lines(url):
    try:
        headers = get_random_headers()
        res = requests.get(url, headers=headers, timeout=20)
        if res.status_code != 200: return None
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Noise Removal
        for tag in soup(['header', 'footer', 'nav', 'script', 'style', 'iframe', 'meta']):
            tag.decompose()
            
        text = soup.get_text().lower()
        lines = set(line.strip() for line in text.splitlines() if line.strip() and len(line.strip()) < 200)
        return lines
    except:
        return None

def main():
    print("--- STARTING PERMANENT MEMORY HUNTER ---")
    
    # 1. Load Memory
    history = load_memory()
    print(f"Memory loaded. I remember {sum(len(v) for v in history.values())} past jobs.")

    start_time = time.time()
    
    # 2. Main Loop
    while time.time() - start_time < DURATION:
        print(f"\n[{time.strftime('%H:%M')}] Scanning websites...")
        
        for url in SITES:
            current_lines = get_site_lines(url)
            if current_lines is None: continue 

            if url not in history: history[url] = []

            found_something_new = False
            for line in current_lines:
                if any(t in line for t in REQUIRED_TYPE) and any(k in line for k in KEYWORDS):
                    if line not in history[url]:
                        print(f"NEW FOUND: {line}")
                        notify_discord(line, url)
                        history[url].append(line)
                        found_something_new = True
            
            if found_something_new:
                save_memory(history)

        print("Scan complete. Sleeping for 15 mins...")
        time.sleep(CHECK_INTERVAL)

    print("Hunter finished.")
    # Detect if we are on iPhone (iSH) or Laptop
    if os.path.exists("/dev/location"):
        os.system("pkill -f location") # Only run this on iPhone
    sys.exit()

if __name__ == "__main__":
    main()