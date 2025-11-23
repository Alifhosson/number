import time
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

# ====== CONFIGURATION ======
LOGIN_URL    = "http://94.23.120.156/ints/login"
REPORT_URL   = "http://94.23.120.156/ints/agent/SMSCDRReports"
BOT_TOKEN    = "7142079092:AAE25V-GEdJJ-gPa11xe36YlyqdyTaXE-8E"
GROUP_ID     = "6006322754"
SIGNATURE    = "@alifhosson"
CHECK_INTERVAL = 2  # seconds
# ===========================

sent_otps = set()

# Setup Chrome WebDriver
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# 1) Open login page and manual login
driver.get(LOGIN_URL)
input("👉 লগইন সম্পন্ন হলে Enter চাপুন...")

# 2) Navigate to SMS report page
driver.get(REPORT_URL)
time.sleep(5)

def extract_otps():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    rows = soup.select("table tbody tr")
    out = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 6:
            continue

        # Column mapping
        time_str  = cols[0].text.strip()   # Date column
        number_raw = cols[1].text.strip()  # Number column
        sms_text   = cols[5].text.strip()  # SMS column (full message)

        # Extract OTP (4–8 digits, including formats like 123-456)
        m = re.search(r"\b\d{3,4}[-]?\d{3,4}\b", sms_text)
        if not m:
            continue
        otp_code = m.group()

        # Detect service
        sms_lower = sms_text.lower()
        if "telegram" in sms_lower:
            service = "Telegram"
        elif "whatsapp" in sms_lower:
            service = "WhatsApp"
        elif "facebook" in sms_lower:
            service = "Facebook"
        elif "temu" in sms_lower:
            service = "Temu"
        else:
            service = "Unknown"

        # Format number (8–14 digits, fallback to CLI if needed)
        digits = re.sub(r"\D", "", number_raw)
        if not (8 <= len(digits) <= 14):
            digits = re.sub(r"\D", "", cols[2].text.strip())
        formatted_number = f"+{digits}" if 8 <= len(digits) <= 14 else "Unknown"

        # Convert time to Dhaka 12h format
        try:
            dt_utc = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.utc)
            dt_dhaka = dt_utc.astimezone(pytz.timezone("Asia/Dhaka"))
            time_str = dt_dhaka.strftime("%d %B %Y, %I:%M %p")
        except:
            pass

        key = f"{formatted_number}_{otp_code}_{service}"
        if key in sent_otps:
            continue

        message = f"""⚔️ NEW OTP ALERT 📯

⏰ Time : <code>{time_str}</code>
☎️ Number : <code>{formatted_number}</code>
⛓️ Main OTP : <code>{otp_code}</code>
⚙️ Service : <code>{service}</code>
💬 Full Message :

<pre>{sms_text}</pre>

📌 Don't share this code with anyone 
🔔 Stay Alert For New Message 🚀 
🔱 Powered by : {SIGNATURE}
"""
        out.append((key, message))

    return out

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": GROUP_ID, "text": text, "parse_mode": "HTML"})

print("🚀 Bot is running... Waiting for OTPs.")
while True:
    try:
        driver.refresh()
        time.sleep(3)
        for key, msg in extract_otps():
            send_to_telegram(msg)
            sent_otps.add(key)
        time.sleep(CHECK_INTERVAL)
    except Exception as e:
        print("❌ Error:", e)
        time.sleep(10)
