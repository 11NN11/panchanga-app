import streamlit as st
from datetime import datetime
from calculator import get_panchang_for_location

st.set_page_config(page_title="🕉 Panchang App", layout="wide")
st.title("🕉 Real-Time Panchang App")

city = st.text_input("📍 Enter your location", "Delhi")
date = st.date_input("📆 Select a date", value=datetime.now().date())

use_now = st.toggle("⏰ Use current time?", value=True)
if use_now:
    dt = datetime.now()
else:
    hour = st.slider("Hour", 0, 23, 12)
    minute = st.slider("Minute", 0, 59, 0)
    dt = datetime.combine(date, datetime.min.time()).replace(hour=hour, minute=minute)

result = get_panchang_for_location(city, dt)

if result:
    st.success(f"Panchang for {result['location']} on {result['time_str']}")
    st.write(f"🌞 Vaara (Day): {result['vaara']}")
    st.write(f"🌙 Tithi: {result['tithi']}")
    st.write(f"🌌 Nakshatra: {result['nakshatra']}")
    st.write(f"🧮 Moon Longitude: {result['moon_long']}°")
    st.write(f"🔭 Sun Longitude: {result['sun_long']}°")
else:
    st.error("❌ Could not fetch location. Please try again.")
