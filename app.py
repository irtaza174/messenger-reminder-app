import streamlit as st
import schedule
import time
import threading
from messenger_bot import schedule_messages

st.set_page_config(page_title="Messenger Reminder App", page_icon="💬")
st.title("📨 Messenger Reminder Scheduler")

with st.form("reminder_form"):
    message = st.text_area("✍️ Enter the message to send", height=100)
    time1 = st.time_input("⏰ Time 1 (Required)")
    time2 = st.time_input("⏰ Time 2 (Optional)", value=None)
    time3 = st.time_input("⏰ Time 3 (Optional)", value=None)
    submitted = st.form_submit_button("✅ Start Sending Reminders")

if submitted:
    times = [str(time1)]
    if time2: times.append(str(time2))
    if time3: times.append(str(time3))

    schedule.clear()
    schedule_messages(message, times)
    st.success(f"Reminders scheduled at: {', '.join(times)}")

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=run_scheduler, daemon=True).start()
    st.info("Bot is now running. Keep this app open.")
