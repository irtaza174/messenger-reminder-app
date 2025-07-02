import requests
import schedule
from psid_fetcher import get_recent_psids
import streamlit as st

ACCESS_TOKEN = st.secrets["PAGE_ACCESS_TOKEN"]
PAGE_ID = st.secrets["PAGE_ID"]

def send_message(psid, text):
    url = "https://graph.facebook.com/v19.0/me/messages"
    params = {"access_token": ACCESS_TOKEN}
    payload = {
        "recipient": {"id": psid},
        "message": {"text": text},
        "tag": "CONFIRMED_EVENT_UPDATE",
        "messaging_type": "MESSAGE_TAG"
    }
    res = requests.post(url, params=params, json=payload)
    return res.status_code == 200

def send_reminders(message):
    psids = get_recent_psids()
    if not psids:
        print("⚠️ No users to message.")
        return
    for psid in psids:
        success = send_message(psid, message)
        print(f"{'✅' if success else '❌'} Sent to {psid}")

def schedule_messages(message, times):
    for t in times:
        schedule.every().day.at(t).do(send_reminders, message=message)
