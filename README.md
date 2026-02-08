🕵️ Intern Hunter 2.0 (iOS Edition)
An automated, stealthy, and intelligent internship scraper running natively on iPhone via iSH (Alpine Linux).

Python Web Scraping iOS Automation Alpine Linux BeautifulSoup

📖 Overview
Finding an internship involves checking the same 20+ career pages every day. Intern Hunter automates this process. It runs as a background process on an iPhone (using the iSH terminal emulator), scrapes target career portals, and uses "Smart Diff" logic to detect new job postings. If a relevant role (e.g., "Backend Intern") appears, it instantly pushes a notification to the phone via Ntfy.sh.

✨ Key Features
🧠 Smart Diffing: Doesn't just check if the "site changed." It calculates the exact text difference (New - Old) to ignore existing jobs and only alert on fresh postings.

🥷 Stealth Mode: Rotates through a bag of random User-Agents (iPhone, Chrome, Windows, Mac) for every request to evade bot detection and 403 bans.

🎯 Sniper Scope (Noise Removal): Automatically strips HTML clutter (<header>, <footer>, <script>, <nav>) to focus strictly on job content, eliminating false alarms from copyright date updates.

⚡ Double Filtering:

Role Filter: Must contain "Intern", "Grad", or "Fresher".

Tech Filter: Must contain specific skills (e.g., "React", "Python", "Data Science").

🔋 Battery Optimized: Runs for a set duration (2 hours) and automatically kills background processes (location, sshd) upon completion.

📢 Ntfy Integration: Sends instant push notifications with the exact Job Title and Link.

🛠️ Tech Stack
Language: Python 3.11

Libraries: requests, BeautifulSoup4 (bs4), fake_useragent (custom logic)

Environment: iSH Shell (Alpine Linux on iOS)

Automation: Apple Shortcuts (SSH Trigger)

Notifications: Ntfy.sh

⚙️ Installation (On iPhone/iSH)
Install System Dependencies:

Bash
apk add python3 py3-pip git openssh nano
Clone the Repository:

Bash
git clone https://github.com/YOUR_USERNAME/InternHunter.git
cd InternHunter
Install Python Libraries:

Bash
pip3 install requests beautifulsoup4
🚀 Usage
Option 1: Manual Run
Bash
python3 scrap.py
Option 2: iOS Shortcut (One-Tap Trigger)
This project is designed to be triggered by an iOS Shortcut that connects via SSH to localhost.

Host: 127.0.0.1

Port: 2022 (Bypasses iOS limitations)

User: root

Command:

Bash
# Keeps the script alive in background even if app closes
cat /dev/location > /dev/null & cd InternHunter && python3 scrap.py > /dev/null 2>&1 &
📝 Configuration
Edit scrap.py to customize your hunt:

Python
# Add your target websites
SITES = [
    "https://careers.google.com/jobs/results/",
    "https://openai.com/careers/search",
    # ... add more
]

# Define what you are looking for
REQUIRED_TYPE = ["intern", "fresher"]
KEYWORDS = ["react", "python", "backend"]
⚠️ Disclaimer
This tool is for educational purposes and personal use only. Please respect robots.txt policies and do not overload servers with aggressive request intervals. The default check interval is set to 15 minutes to be polite.