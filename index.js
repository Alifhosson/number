const fs = require('fs');
const path = require('path');
const axios = require('axios');
const TelegramBot = require('node-telegram-bot-api');

const TELEGRAM_TOKEN = process.env.TELEGRAM_TOKEN || '8005753249:AAGCvVOxTY0BHbs-mlGsK6yv8MPP44oSTws';
const CHAT_ID = process.env.CHAT_ID || '-1002898274575';
const GET_HEADERS_LOGIN = 'https://get-headers-pied.vercel.app/login';
const GET_USER = process.env.GET_USER || 'rohanwork';
const GET_PASS = process.env.GET_PASS || 'rohanwork';

let REQUEST_HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': '',
    'Referer': 'http://94.23.120.156/ints/client/SMSCDRStats',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
};

const DB_FILE = path.resolve(__dirname, 'otps.json');
const POLL_INTERVAL_MS = 2000;
const COOKIE_REFRESH_MS = 3600 * 1000;
const bot = new TelegramBot(TELEGRAM_TOKEN, { polling: false });

function getApiUrl() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const fdate1 = `${year}-${month}-${day} 00:00:00`;
  const fdate2 = `${year}-${month}-${day} 23:59:59`;
  return `http://94.23.120.156/ints/client/res/data_smscdr.php?fdate1=${encodeURIComponent(fdate1)}&fdate2=${encodeURIComponent(fdate2)}&frange=&fnum=&fcli=&fgdate=&fgmonth=&fgrange=&fgnumber=&fgcli=&fg=0&sEcho=1&iColumns=7&sColumns=%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=25&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&mDataProp_6=6&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true&sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=desc&iSortingCols=1&_=1758981136431`;
}
const fs = require('fs');
const path = require('path');
const axios = require('axios');
const TelegramBot = require('node-telegram-bot-api');

const TELEGRAM_TOKEN = process.env.TELEGRAM_TOKEN || '8005753249:AAGCvVOxTY0BHbs-mlGsK6yv8MPP44oSTws';
const CHAT_ID = process.env.CHAT_ID || '-1002898274575';
const GET_HEADERS_LOGIN = 'https://get-headers-pied.vercel.app/login';
const GET_USER = process.env.GET_USER || 'rohanwork';
const GET_PASS = process.env.GET_PASS || 'rohanwork';

let REQUEST_HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': '',
    'Referer': 'http://94.23.120.156/ints/client/SMSCDRStats',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
};

const DB_FILE = path.resolve(__dirname, 'otps.json');
const POLL_INTERVAL_MS = 2000;
const COOKIE_REFRESH_MS = 3600 * 1000;
const bot = new TelegramBot(TELEGRAM_TOKEN, { polling: false });

function getApiUrl() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const fdate1 = `${year}-${month}-${day} 00:00:00`;
  const fdate2 = `${year}-${month}-${day} 23:59:59`;
  return `http://94.23.120.156/ints/client/res/data_smscdr.php?fdate1=${encodeURIComponent(fdate1)}&fdate2=${encodeURIComponent(fdate2)}&frange=&fnum=&fcli=&fgdate=&fgmonth=&fgrange=&fgnumber=&fgcli=&fg=0&sEcho=1&iColumns=7&sColumns=%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=25&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&mDataProp_6=6&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true&sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=desc&iSortingCols=1&_=
function loadDB() {
  try {
    if (!fs.existsSync(DB_FILE)) {
      fs.writeFileSync(DB_FILE, JSON.stringify({ seen: [] }, null, 2));
      return { seen: [] };
    }
    return JSON.parse(fs.readFileSync(DB_FILE, 'utf8'));
  } catch {
    return { seen: [] };
  }
}

function saveDB(db) {
  fs.writeFileSync(DB_FILE, JSON.stringify(db, null, 2));
}

function extractOtpsFromApi(apiJson) {
  const results = [];
  if (!apiJson?.aaData) return results;
  for (const row of apiJson.aaData) {
    if (!Array.isArray(row) || row.length < 5) continue;
    const timestamp = row[0];
    const number = row[2];
    const service = row[3];
    const message = row[4];
    const codeMatch = String(message).match(/\b(\d{4,6})\b/);
    const code = codeMatch ? codeMatch[1] : null;
    const id = `${timestamp}||${number}||${code}`;
    results.push({ id, timestamp, number, service, message, code });
  }
  return results;
}

async function fetchApi() {
  try {
    const resp = await axios.get(getApiUrl(), { headers: REQUEST_HEADERS, timeout: 10000 });
    return resp.data;
  } catch {
    return null;
  }
}

const countryMap = {
  "1": { name: "United States / Canada", flag: "🇺🇸" },
  "7": { name: "Russia", flag: "🇷🇺" }
};

function formatOtp(entry) {
  let countryFlag = "❓";
  let countryName = "Unknown";

  
  let numStr = "";
  try {
    numStr = Array.isArray(entry.number) ? entry.number.join("") : String(entry.number || "");
  
    numStr = numStr.replace(/\D+/g, "");
  } catch (e) {
    numStr = "";
  }

  
  for (let len = 3; len >= 1; len--) {
    const code = numStr.slice(0, len);
    if (code && countryMap[code]) {
      countryFlag = countryMap[code].flag;
      countryName = countryMap[code].name;
      break;
    }
  }

  
  let maskedNumber;
  if (numStr.length >= 8) {
    const first = numStr.slice(0, 5);
    const last = numStr.slice(-3);
    const starsCount = Math.max(0, numStr.length - 8);
    maskedNumber = first + "*".repeat(starsCount) + last;
  } else {
    
    if (numStr.length <= 4) {
      maskedNumber = numStr;
    } else {
      const first = numStr.slice(0, Math.floor(numStr.length / 2));
      const last = numStr.slice(-Math.floor(numStr.length / 4) || 1);
      maskedNumber = first + "*".repeat(Math.max(1, numStr.length - first.length - last.length)) + last;
    }
  }

  
  entry.number = maskedNumber;

  
  const safeMessage = String(entry.message || "").replace(/```/g, "`​``");

  return `✅ *${countryFlag} ${countryName} ${entry.service}* OTP Received 🎉

🔑 *OTP*: \`${entry.code || "N/A"}\`
☎️ *Number*: \`${entry.number}\`
⚙️ *Service*: \`${entry.service || "N/A"}\`
🌍 *Country*: \`${countryName} ${countryFlag}\`

\`\`\`
📩 Full Message:
${safeMessage}
\`\`\``;
}


async function sendToTelegram(entry) {
  try {
    await bot.sendMessage(CHAT_ID, formatOtp(entry));
    console.log('Sent:', entry.id);
  } catch (err) {
    console.error('Send error:', err.message || err);
  }
}

async function getCookie(user, pass) {
  try {
    const payload = {
      username: user,
      password: pass,
      url: 'http://94.23.120.156/ints/signin',
      referer: 'http://94.23.120.156/ints'
    };
    const resp = await axios.post(GET_HEADERS_LOGIN, payload, {
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Origin: 'https://get-headers-pied.vercel.app',
        Referer: 'https://get-headers-pied.vercel.app/',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
      },
      timeout: 10000
    });
    if (resp?.data?.headers) {
      const cookieStr = resp.data.headers.Cookie;
      const match = cookieStr.match(/PHPSESSID=[^;]+/);
      if (match) return match[0];
      return cookieStr;
    }
    return null;
  } catch (err) {
    return null;
  }
}

(async () => {
  const db = loadDB();
  const seen = new Set(db.seen);
  const cookieValue = await getCookie(GET_USER, GET_PASS);
  if (cookieValue) {
    REQUEST_HEADERS.Cookie = cookieValue;
    console.log('Initial cookie set:', cookieValue);
  } else {
    console.log('Initial cookie fetch failed');
  }
  setInterval(async () => {
    const c = await getCookie(GET_USER, GET_PASS);
    if (c) {
      REQUEST_HEADERS.Cookie = c;
      console.log('Cookie refreshed:', c);
    } else {
      console.log('Cookie refresh failed');
    }
  }, COOKIE_REFRESH_MS);

  const first = await fetchApi();
  const initEntries = extractOtpsFromApi(first);
  for (const e of initEntries) seen.add(e.id);
  db.seen = [...seen];
  saveDB(db);
  console.log('Initial population done. Monitoring started...');
  setInterval(async () => {
    const data = await fetchApi();
    if (!data) return;
    const entries = extractOtpsFromApi(data);
    const fresh = entries.filter(e => !seen.has(e.id));
    for (const e of fresh) {
      await sendToTelegram(e);
      seen.add(e.id);
      await new Promise(r => setTimeout(r, 300));
    }
    if (fresh.length) {
      db.seen = [...seen];
      saveDB(db);
    }
  }, POLL_INTERVAL_MS);
})();
