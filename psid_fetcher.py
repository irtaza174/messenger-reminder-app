import requests
import streamlit as st

ACCESS_TOKEN = st.secrets["PAGE_ACCESS_TOKEN"]
PAGE_ID = st.secrets["PAGE_ID"]

def get_recent_psids():
    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/conversations"
    params = {"access_token": ACCESS_TOKEN, "fields": "participants", "limit": 100}
    res = requests.get(url, params=params)
    if res.status_code != 200:
        print("Error:", res.json())
        return []
    psids = set()
    for convo in res.json().get("data", []):
        for p in convo.get("participants", {}).get("data", []):
            if p["id"] != PAGE_ID:
                psids.add(p["id"])
    return list(psids)
