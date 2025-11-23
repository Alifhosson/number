import os
import time
import re
import json
import random
import urllib.parse
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import phonenumbers
from phonenumbers import geocoder
import telebot
from telebot import types

# === 🟢 BOT CONFIGURATION ===
BOT_TOKEN = os.getenv("BOT1_TOKEN", "7994972018:AAH66pdWPF6pm_yNr7666GAbofYQg_Pj3NQ")
CHAT_ID = os.getenv("BOT1_CHAT_ID", "-1003418731250")

# === SERVER CONFIG ===
BASE_DOMAIN = "imssms.org"
BASE_URL = f"https://{BASE_DOMAIN}"
LOGIN_PAGE_URL = f"{BASE_URL}/login"
LOGIN_POST_URL = f"{BASE_URL}/signin"
DASHBOARD_URL = f"{BASE_URL}/client/SMSCDRStats"
API_BASE_URL = f"{BASE_URL}/client/res/data_smscdr.php"

# === CREDENTIALS ===
USERNAME = os.getenv("SMS_USER", "personal")
PASSWORD = os.getenv("SMS_PASS", "personal")

# === 🔄 RANDOM USER AGENTS LIST ===
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 15; Infinix X6858 Build/AP3A.240905.015.A2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.7444.102 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Redmi Note 10 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; OnePlus 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
]

# Initialize Bot
bot = telebot.TeleBot(BOT_TOKEN)

# Session management
session = requests.Session()
current_ua = random.choice(USER_AGENTS)
last_id = None

def get_random_ua():
    return random.choice(USER_AGENTS)

def get_today_date():
    return datetime.now().strftime("%Y-%m-%d")

def get_flag_emoji(country_code):
    """Converts ISO country code to emoji flag."""
    if not country_code:
        return "🌍"
    return ''.join(chr(ord(c) + 127397) for c in country_code.upper())

def get_country_info(number):
    """Detects country and flag from phone number."""
    if not number:
        return {"name": "Unknown", "flag": "🌍"}
    
    clean_num = str(number).strip().replace(" ", "").replace("-", "")
    if clean_num.startswith("00"):
        clean_num = "+" + clean_num[2:]
    if not clean_num.startswith("+"):
        clean_num = "+" + clean_num

    try:
        phone_obj = phonenumbers.parse(clean_num, None)
        region_code = phonenumbers.region_code_for_number(phone_obj)
        country_name = geocoder.country_name_for_number(phone_obj, "en")
        flag = get_flag_emoji(region_code) if region_code else "🌍"
        
        return {"name": country_name or region_code or "Unknown", "flag": flag}
    except Exception:
        return {"name": "Unknown", "flag": "🌍"}

def extract_otp(text):
    if not text:
        return None
    match = re.search(r'\b\d{3,4}(?:[-\s]?\d{2,4})\b', text)
    return match.group(0) if match else None

def get_api_url():
    today = get_today_date()
    fdate1 = urllib.parse.quote(f"{today} 00:00:00")
    fdate2 = urllib.parse.quote(f"{today} 23:59:59")
    
    return (f"{API_BASE_URL}?fdate1={fdate1}&fdate2={fdate2}"
            "&frange=&fnum=&fcli=&fgdate=&fgmonth=&fgrange=&fgnumber=&fgcli=&fg=0"
            "&sEcho=1&iColumns=7&sColumns=%2C%2C%2C%2C%2C%2C&iDisplayStart=0"
            "&iDisplayLength=25&mDataProp_0=0&sSearch_0=&bRegex_0=false"
            "&bSearchable_0=true&bSortable_0=true&mDataProp_1=1&sSearch_1="
            "&bRegex_1=false&bSearchable_1=true&bSortable_1=true&mDataProp_2=2"
            "&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true"
            "&mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true"
            "&bSortable_3=true&mDataProp_4=4&sSearch_4=&bRegex_4=false"
            "&bSearchable_4=true&bSortable_4=true&mDataProp_5=5&sSearch_5="
            "&bRegex_5=false&bSearchable_5=true&bSortable_5=true&mDataProp_6=6"
            "&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true"
            "&sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=desc&iSortingCols=1")

def map_row(row):
    msg_index = 4
    unique_hash = f"{row[0]}_{row[2]}_{row[msg_index]}"
    return {
        "id": unique_hash,
        "displayId": row[0],
        "number": row[2],
        "cli": row[3],
        "message": row[msg_index],
        "countryData": get_country_info(row[2]),
    }

def send_telegram_sms(sms):
    otp = extract_otp(sms['message']) or "N/A"
    country_name = sms['countryData']['name']
    flag = sms['countryData']['flag']
    service = sms['cli'] or "Service"

    # Mask Number
    masked_number = sms['number']
    if masked_number and len(masked_number) >= 7:
        visible_start = masked_number[:6]
        visible_end = masked_number[-4:]
        masked_number = f"{visible_start}𝚂𝙼𝚂{visible_end}"

    final_msg = (
        f"✅ {flag} <b>{country_name} {service} Otp Code Received Successfully</b> 🎉\n\n"
        f"🔑 <b>𝐘𝐨𝐮𝐫 𝐎𝐓𝐏:</b>  <code>{otp}</code>\n\n"
        f"☎️ <b>Number:</b> <code>{masked_number}</code>\n"
        f"⚙️ <b>Service:</b> {service}\n"
        f"🌍 <b>Country:</b> {country_name} {flag}\n\n"
        f"📩 <b>𝐅𝐮𝐥𝐥-𝐌𝐞𝐬𝐬𝐚𝐠𝐞:</b>\n"
        f"<pre>{sms['message']}</pre>"
    )

    # Inline Keyboard (Optional: Copy Code Logic simulation)
    markup = types.InlineKeyboardMarkup()
    # You can add buttons here if needed
    # btn_copy = types.InlineKeyboardButton("Copy Code", callback_data=f"copy_{otp}")
    # markup.add(btn_copy)

    try:
        bot.send_message(CHAT_ID, final_msg, parse_mode="HTML", reply_markup=markup)
    except Exception as e:
        print(f"❌ Bot failed to send message: {e}")

# Login Logic
def perform_login():
    global current_ua
    current_ua = get_random_ua()
    
    headers = {
        "User-Agent": current_ua,
        "Host": BASE_DOMAIN
    }

    try:
        print(f"🔐 Logging in with UA: {current_ua[:50]}...")
        
        # 1. GET Login Page
        res_get = session.get(LOGIN_PAGE_URL, headers=headers)
        soup = BeautifulSoup(res_get.text, "html.parser")
        
        # Parse Captcha
        body_text = soup.get_text()
        captcha_answer = None
        match = re.search(r'What is\s*([\-]?\d+)\s*([\+\-\*xX\/])\s*([\-]?\d+)', body_text, re.IGNORECASE)
        
        if match:
            a = int(match.group(1))
            op = match.group(2)
            b = int(match.group(3))
            
            if op == "+":
                captcha_answer = str(a + b)
            elif op == "-":
                captcha_answer = str(a - b)
            elif op in ["*", "x", "X"]:
                captcha_answer = str(a * b)
            elif op == "/":
                captcha_answer = str(a // b) if b != 0 else "0"
            
            print(f"Detected captcha: {match.group(0)} => {captcha_answer}")

        # Prepare Form Data
        payload = {
            "username": USERNAME,
            "password": PASSWORD,
        }
        if captcha_answer:
            payload["capt"] = captcha_answer

        # Add hidden fields
        for hidden in soup.find_all("input", type="hidden"):
            name = hidden.get("name")
            val = hidden.get("value", "")
            if name and name not in ["username", "password", "capt"]:
                payload[name] = val

        # 2. POST Login
        post_headers = headers.copy()
        post_headers.update({
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": BASE_URL,
            "Referer": LOGIN_PAGE_URL,
            "sec-ch-ua-platform": '"Android"',
            "sec-ch-ua-mobile": "?1",
            "Upgrade-Insecure-Requests": "1"
        })

        res_post = session.post(LOGIN_POST_URL, data=payload, headers=post_headers, allow_redirects=False)

        # Check success (Status 302/303 usually means redirect to dashboard)
        if res_post.status_code in [302, 303] or (res_post.status_code == 200 and "<title>Login" not in res_post.text):
            return True
        
        print("❌ Login failed (Status or Content check).")
        return False

    except Exception as e:
        print(f"Login error: {e}")
        return False

def fetch_sms_api():
    url = get_api_url()
    headers = {
        "User-Agent": current_ua,
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": DASHBOARD_URL,
        "Host": BASE_DOMAIN,
        "sec-ch-ua-platform": '"Android"',
        "sec-ch-ua-mobile": "?1",
    }
    
    try:
        res = session.get(url, headers=headers)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        raise Exception(f"Fetch SMS API error: {e}")

def loop():
    global last_id
    try:
        data = fetch_sms_api()

        if data and 'aaData' in data and isinstance(data['aaData'], list) and len(data['aaData']) > 0:
            latest_row = data['aaData'][0]
            latest = map_row(latest_row)

            if last_id is None:
                last_id = latest['id']
                # Optional: Send on startup or just mark as read
                send_telegram_sms(latest)
            elif latest['id'] != last_id:
                last_id = latest['id']
                print(f"🔥 New SMS Found! ID: {latest['displayId']}")
                send_telegram_sms(latest)
            else:
                print(".", end="", flush=True)
            
            time.sleep(3)
        else:
            print("x", end="", flush=True)
            time.sleep(3)

    except Exception as e:
        print(f"\n❌ Connection Error or Session Expired: {e}")
        print("🔄 Re-authenticating in 5 seconds...")
        time.sleep(5)
        
        try:
            if perform_login():
                print("✅ Re-login successful.")
            else:
                print("❌ Re-login failed.")
        except Exception as login_err:
            print(f"❌ Fatal Login Error: {login_err}")
            time.sleep(10)

def start_worker():
    print("🚀 Seven1Tel Bot Started (Python Version)...")
    if not perform_login():
        print("Initial login failed, retrying in 10s...")
        time.sleep(10)
        start_worker()
        return
    
    while True:
        loop()

if __name__ == "__main__":
    try:
        start_worker()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user.")
