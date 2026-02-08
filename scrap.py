import requests
from bs4 import BeautifulSoup
import time
import sys
import os

# --- CONFIGURATION ---
NTFY_TOPIC = "Internships_2026_A24"  # Your Topic Name

# 1. The Websites to Monitor
SITES = [
    "https://openai.com/careers",
    "https://careers.google.com/jobs/results/",
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

# 2. Must contain AT LEAST ONE of these (The Role Type)
REQUIRED_TYPE = ["intern", "internship", "trainee", "student", "grad", "fresher"]

# 3. Must ALSO contain AT LEAST ONE of these (The Tech/Skill)
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

# Settings
CHECK_INTERVAL = 900  # Check every 15 minutes (900 seconds)
DURATION = 7200       # Run for 2 hours

# --- NOTIFICATION SYSTEM ---
def notify(message, priority="default"):
    """Sends a notification to your iPhone via Ntfy"""
    try:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=message.encode('utf-8'),
            headers={
                "Title": "Intern Hunter Alert",
                "Priority": priority,
                "Tags": "briefcase"
            },
            timeout=10
        )
        print(f"-> Notification sent: {message}")
    except Exception as e:
        print(f"Failed to send notification: {e}")

# --- MAIN LOGIC ---
def get_site_lines(url):
    """Downloads website and splits it into a set of text lines"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15'}
        res = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Get all text, lowercase it, split by lines, remove empty space
        text = soup.get_text().lower()
        lines = set(line.strip() for line in text.splitlines() if line.strip())
        return lines
    except Exception as e:
        print(f"Error reading {url}: {e}")
        return set()

def main():
    print(f"--- STARTING MULTI-SITE HUNTER ({len(SITES)} Sites) ---")
    notify(f"Hunter started. Monitoring {len(SITES)} sites for 2 hours.")
    
    start_time = time.time()
    
    # MEMORY: This dictionary stores the 'Old Text' for every single website
    # Format: { "google.com": {"line1", "line2"}, "openai.com": {...} }
    site_memory = {}

    # 1. INITIAL SCAN (Learn the current state of all websites)
    print("Performing initial scan (Training memory)...")
    for url in SITES:
        lines = get_site_lines(url)
        if lines:
            site_memory[url] = lines
            print(f"Learned: {url}")
        else:
            print(f"Failed to learn: {url}")
    
    print("Initial scan complete. Waiting for changes...")

    # 2. MAIN LOOP
    while time.time() - start_time < DURATION:
        # Sleep first (so we don't spam requests instantly)
        time.sleep(CHECK_INTERVAL)
        
        print(f"\n[{time.strftime('%H:%M')}] Checking for updates...")
        
        for url in SITES:
            # Skip if we never learned this site originally
            if url not in site_memory:
                continue

            # Fetch new version
            new_lines = get_site_lines(url)
            old_lines = site_memory[url]
            
            # --- THE SMART MATH ---
            # (New Lines) - (Old Lines) = The Updates
            added_lines = new_lines - old_lines
            
            if added_lines:
                # We found changes! Now check if they are interesting.
                found_matches = []
                
                for line in added_lines:
                    # Check 1: Is it an internship?
                    if any(t in line for t in REQUIRED_TYPE):
                        # Check 2: Does it match our tech keywords?
                        if any(k in line for k in KEYWORDS):
                            found_matches.append(line)

                # Notify if we found valid matches
                if found_matches:
                    top_match = found_matches[0] # Take the first one
                    msg = f"NEW OPENING: {top_match} | {url}"
                    notify(msg, priority="high")
                    
                    # Update memory so we don't notify again
                    site_memory[url] = new_lines
                else:
                    # Content changed, but it was boring (e.g. updated copyright date)
                    # We still update memory so we don't check it again
                    site_memory[url] = new_lines

    # 3. SHUTDOWN SEQUENCE
    notify("Hunter finished. Shutting down server.")
    print("Killing Keep-Awake...")
    os.system("pkill -f location")
    print("Killing Server...")
    os.system("pkill sshd")
    sys.exit()

if __name__ == "__main__":
    main()