Here is your shiny new README.md for Version 2.0.

This documentation highlights the new "Brain" (Memory) and "Voice" (Discord) of your bot. You can overwrite your old README with this one.

🧠 Intern Hunter V2 (Discord + Memory Edition)
A smart, persistent, and stealthy internship scraper that never forgets.

Python 3 Discord Webhooks JSON Database Automation

🚀 What's New in V2?
🧠 Long-Term Memory: The bot now creates a local database (job_history.json). It remembers every job it has ever seen.

🔇 Zero False Alarms: If you restart the bot, it checks its memory first. It will not spam you with 20 notifications for jobs you already saw yesterday.

💬 Discord Integration: Replaced simple push notifications with beautiful Discord Embeds (Color-coded, Clickable Links, Job Titles).

📱 Multi-Platform: Runs natively on iOS (iSH), Android (Termux), and Laptop/PC.

✨ Key Features
The "Diff" Engine: Scrapes 20+ career sites and compares Current Live Data vs. Stored Memory.

Stealth Mode 2.0: Rotates between 50+ User-Agents (iPhone, Mac, Windows, Pixel) to evade 403 bans.

HTML Sniper: Automatically removes <header>, <footer>, and <nav> garbage to prevent false alarms from copyright date updates.

Smart Filters: Only alerts if the job contains specific keywords (e.g., "React", "Python") AND is an intern role ("Intern", "Fresher").

🛠️ Tech Stack
Core: Python 3.x

Scraping: requests, BeautifulSoup4

Database: Local JSON (No SQL required)

Alerts: Discord Webhooks API

⚙️ Installation
1. Prerequisites
You need a Discord Webhook URL.

Create a private Discord Server.

Go to Channel Settings ⚙️ → Integrations → Webhooks.

Copy the URL.

2. Setup (Laptop or Phone)
Clone the Repository:

Bash
git clone https://github.com/YOUR_USERNAME/InternHunter.git
cd InternHunter
Install Dependencies:

Bash
pip install requests beautifulsoup4
Configure the Bot: Open scrap.py and paste your Webhook URL:

Python
# Inside scrap.py
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/YOUR_KEY_HERE"
🏃 Usage
First Run (The Learning Phase)
Bash
python3 scrap.py
The bot will scan all websites.

It will populate job_history.json with all existing jobs.

Expect a spam of notifications (only this one time) as it "learns" the current state of the world.

Subsequent Runs (The Watchdog Phase)
The bot stays silent for all known jobs.

It only sends a notification if a NEW job appears that is not in job_history.json.

📱 Mobile Automation
iOS (iSH): Uses cat /dev/location hack to keep running in background.

Android (Termux): Uses termux-wake-lock to prevent sleep mode.

📂 Project Structure
Plaintext
InternHunter/
├── scrap.py            # The Main Brain (Logic + Scraper)
├── job_history.json    # The Memory (Auto-generated, DO NOT EDIT)
├── README.md           # This file
└── .gitignore          # Ignores junk files
⚠️ Disclaimer
This tool is for educational purposes. Please respect robots.txt and do not lower the CHECK_INTERVAL below 15 minutes to avoid overloading career portals.