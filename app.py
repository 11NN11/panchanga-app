import streamlit as st
from datetime import datetime
from calculator import get_panchang_for_location

from streamlit_autorefresh import st_autorefresh
if use_now:
    st_autorefresh(interval=60000)  # Refresh every 1 min

# Title & description
st.set_page_config(page_title="Panchang App", layout="wide")
st.title("📿 Real-Time Panchang Explorer")

# Get user location and date
city = st.text_input("Enter your location", "Delhi")
date = st.date_input("Select date", value=datetime.now().date())

# Time selector or real-time clock
use_now = st.toggle("Use current time?", value=True)
if use_now:
    time = datetime.now()
else:
    hour = st.slider("Hour", 0, 23, 12)
    minute = st.slider("Minute", 0, 59, 0)
    time = datetime.combine(date, datetime.min.time()).replace(hour=hour, minute=minute)

# Call calculator
result = get_panchang_for_location(city, time)

# Display results
if result:
    st.write("📍", result["location"])
    st.write("🕰️", result["time_str"])
    st.write("🌞 Vaara:", result["vaara"])
    st.write("🌙 Tithi:", result["tithi"])
    st.write("🌌 Nakshatra:", result["nakshatra"])
    st.write("🧮 Moon Longitude:", result["moon_long"])
    st.write("🔭 Sun Longitude:", result["sun_long"])
