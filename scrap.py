import requests
from bs4 import BeautifulSoup
import time
import sys

# --- CONFIGURATION ---
SITES = [
    "https://openai.com/careers",
    "https://careers.google.com/jobs/results/",
    "https://unstop.com/internships?quickApply=true&oppstatus=open",
    "https://www.ubisoft.com/en-us/company/careers/interns-graduates",

    "https://jobs.lever.co/moonfroglabs",         # Moonfrog (Gaming - Very scraper friendly)
    "https://jobs.lever.co/simple",               # Simple (Fintech/Bangalore)
    "https://boards.greenhouse.io/razorpay",      # Razorpay (Fintech - Bangalore)
    "https://boards.greenhouse.io/swiggy",        # Swiggy (Tech/AI - Bangalore)
    "https://www.games24x7.com/careers",          # Games24x7 (Gaming - Bangalore)

    # --- CHENNAI (SaaS Capital) ---
    "https://careers.freshworks.com/jobs",        # Freshworks (Huge SaaS)
    "https://www.zoho.com/careers/",              # Zoho (Might be tricky, but worth trying)
    "https://chargebee.com/careers/",             # Chargebee (Fintech - Chennai)

    # --- KERALA (Kochi/Trivandrum) ---
    "https://www.experionglobal.com/careers/",    # Experion (Kochi)
    "https://www.ibssoftware.com/careers",        # IBS Software (Trivandrum/Kochi)
    # Note: Many Kerala companies use "Technopark" portal which is hard to scrape.
    # It is better to check specific company sites.

    # --- UAE (Dubai/Abu Dhabi) ---
    "https://jobs.lever.co/careem",               # Careem (The 'Uber' of UAE - Uses Lever!)
    "https://www.noon.com/careers/",              # Noon (Amazon of UAE)
    "https://group.talabat.com/careers",          # Talabat (Food delivery)
    "https://boards.greenhouse.io/telegram",      # Telegram (HQ is in Dubai)
    "https://jobs.lever.co/palantir"    

]

KEYWORDS = [
    # --- AI & DATA SCIENCE ---
    "data preprocessing", "model training", "predictive modeling", 
    "deep learning", "neural networks", 
    "supervised learning", "unsupervised learning",

    # --- GAME DEVELOPMENT ---
    "physics engines", "gameplay mechanics", "shader programming", 
    "3d mathematics", "linear algebra", "ray casting", 
    "game developer", "unity", "unreal engine",

    # --- WEB DEVELOPMENT ---
    "react", "react.js", "node.js", 
    "django", "flask", "web developer"
]
# 2. The TYPE of job (It must match at least one of these)
REQUIRED_TYPE = ["intern", "internship", "trainee", "student", "university grad"]

NTFY_TOPIC = "Internships_2026_A24" # Your Topic

def notify(msg):
    try:
        requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", 
                      data=msg.encode('utf-8'),
                      headers={"Title": "Internship Alert!"})
    except:
        pass

def check_jobs():
    print(f"[{time.strftime('%H:%M:%S')}] Checking sites...")
    for url in SITES:
        try:
            # Fake browser header
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            res = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(res.text, 'html.parser')
            page_text = soup.get_text().lower()
            
            # --- THE NEW LOGIC ---
            # Check if ANY internship keyword exists on the page first
            is_internship = any(r_word in page_text for r_word in REQUIRED_TYPE)
            
            if is_internship:
                # If it's an internship page, check for specific roles
                for word in KEYWORDS:
                    if word in page_text:
                        print(f"MATCH: {word} Internship found at {url}")
                        notify(f"INTERNSHIP FOUND: {word} at {url}")
            else:
                print(f"No internships found at {url} (skipping full-time roles)")

        except Exception as e:
            print(f"Error checking {url}: {e}")

if __name__ == "__main__":
    notify("Internship Hunter Started (2 Hours)")
    start_time = time.time()
    two_hours = 2 * 60 * 60 

    while (time.time() - start_time) < two_hours:
        check_jobs()
        time.sleep(900) # Check every 15 mins
    
    notify("Search finished.")
    sys.exit()