# NTAVis_bot.py
# Sends Telegram alerts when threats are detected in network traffic.
# NOTE: Replace TOKEN and CHAT_ID with your own credentials.

import requests

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  
CHAT_ID = "YOUR_CHAT_ID"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

# Example usage
send_telegram_alert("🚨 Threat detected: SYN Flood from 192.168.1.10")
