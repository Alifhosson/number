import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import random
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
from phonenumbers import parse, region_code_for_number
import phonenumbers
import country_converter as coco

# ============================
# 🔧 CONFIG
# ============================

BOT1_TOKEN = "7142079092:AAE25V-GEdJJ-gPa11xe36YlyqdyTaXE-8E"
BOT1_CHAT_ID = "6006322754"

SMS_USER = "techzonebd1"
SMS_PASS = "techzonebd1"

BASE_DOMAIN = "imssms.org"
BASE_URL = f"https://{BASE_DOMAIN}"

LOGIN_PAGE_URL = f"{BASE_URL}/login"
LOGIN_POST_URL = f"{BASE_URL}/signin"
DASHBOARD_URL = f"{BASE_URL}/client/SMSCDRStats"
API_BASE_URL = f"{BASE_URL}/client/res/data_smscdr.php"

# ============================
# 🟢 RANDOM USER AGENTS
# ============================

USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 15; Infinix X6858)",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B)",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2)",
    "Mozilla/5.0 (Linux; Android 12; Redmi Note 10 Pro)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
]

def get_random_ua():
    return random.choice(USER_AGENTS)

session = requests.Session()
current_ua = get_random_ua()

last_id = None

# ============================
# 🔎 DATE
# ============================

def today_date():
    now = datetime.now()
    return now.strftime("%Y-%m-%d")


# ============================
# 📡 API URL BUILDER
# ============================

def get_api_url():
    today = today_date()
    return (f"{API_BASE_URL}?fdate1={today}%2000:00:00&fdate2={today}%2023:59:59"
            "&iDisplayStart=0&iDisplayLength=25&sEcho=1")


# ============================
# 🔍 OTP EXTRACTOR
# ============================

def extract_otp(text):
    if not text:
        return None
    m = re.search(r"\b\d{3,4}(?:[-\s]?\d{2,4})\b", text)
    return m.group(0) if m else None


# ============================
# 🌍 COUNTRY DETECT
# ============================

def get_country(number):
    try:
        num = parse(number, None)
        iso = region_code_for_number(num)
        name = coco.convert(names=iso, to="name_short")
        flag = coco.convert(names=iso, to="emoji")
        return name, flag
    except:
        return "Unknown", "🌍"


# ============================
# 🔐 LOGIN + CAPTCHA SOLVE
# ============================

def login():
    global current_ua
    current_ua = get_random_ua()

    try:
        r = session.get(LOGIN_PAGE_URL, headers={"User-Agent": current_ua})
        soup = BeautifulSoup(r.text, "html.parser")

        text = soup.text
        cap_match = re.search(r"What is\s*([\-]?\d+)\s*([\+\-\*xX\/])\s*([\-]?\d+)", text)

        captcha = None
        if cap_match:
            a = int(cap_match.group(1))
            op = cap_match.group(2)
            b = int(cap_match.group(3))

            if op == "+":
                captcha = a + b
            elif op == "-":
                captcha = a - b
            elif op in ["*", "x", "X"]:
                captcha = a * b
            elif op == "/" and b != 0:
                captcha = a // b

        form = {
            "username": SMS_USER,
            "password": SMS_PASS,
        }
        if captcha is not None:
            form["capt"] = str(captcha)

        rp = session.post(
            LOGIN_POST_URL,
            data=form,
            headers={"User-Agent": current_ua},
            allow_redirects=False
        )

        if rp.status_code in [302, 303]:
            return True

        return "Dashboard" in rp.text

    except Exception as e:
        print("Login error:", e)
        return False


# ============================
# 📥 FETCH SMS
# ============================

def fetch_sms():
    url = get_api_url()
    r = session.get(url, headers={"User-Agent": current_ua})
    return r.json()


# ============================
# 📤 SEND TO TELEGRAM
# ============================

async def send_sms(bot, sms):
    otp = extract_otp(sms["message"]) or "N/A"
    country, flag = sms["country"]

    number = sms["number"]
    masked = number[:6] + "𝚂𝙼𝚂" + number[-4:]

    msg = f"""
✅ {flag} <b>{country} OTP Received Successfully</b> 🎉

🔑 <b>OTP:</b> <code>{otp}</code>
☎️ <b>Number:</b> <code>{masked}</code>
🌍 <b>Country:</b> {country} {flag}

📩 <b>Full Message:</b>
<pre>{sms["message"]}</pre>
"""

    await bot.send_message(
        chat_id=BOT1_CHAT_ID,
        text=msg,
        parse_mode=ParseMode.HTML
    )


# ============================
# 🔄 MAIN WORKER LOOP
# ============================

async def worker(app):
    global last_id

    print("🚀 Python SMS Bot Started…")

    if not login():
        print("❌ Login Failed!")
        return

    while True:
        try:
            data = fetch_sms()

            rows = data.get("aaData", [])

            if rows:
                row = rows[0]
                unique = f"{row[0]}_{row[2]}_{row[4]}"

                sms = {
                    "id": unique,
                    "displayId": row[0],
                    "number": row[2],
                    "cli": row[3],
                    "message": row[4],
                    "country": get_country(row[2])
                }

                if last_id != sms["id"]:
                    last_id = sms["id"]
                    print("🔥 New SMS:", sms["displayId"])
                    await send_sms(app.bot, sms)

            else:
                print("No SMS…")

        except Exception as e:
            print("Error:", e)
            print("🔄 Re-logging in…")
            login()

        time.sleep(3)


# ============================
# 🚀 START BOT
# ============================

async def main():
    app = ApplicationBuilder().token(BOT1_TOKEN).build()

    await app.initialize()
    await app.start()

    await worker(app)

    await app.stop()


import asyncio
asyncio.run(main())