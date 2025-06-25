# app.py

import streamlit as st
from datetime import datetime

# 🌞 Panchanga App – Basic Demo for Kids

def get_panchanga(lat, lon):
    today = datetime.now().strftime('%Y-%m-%d')
    weekday = datetime.now().strftime('%A')
    return {
        "date": today,
        "vaara": weekday,
        "tithi": "Shukla Pratipada → Dwitiya (~1:24 PM)",
        "nakshatra": "Ardra → Punarvasu",
        "moon_phase": "🌒 Waxing Crescent",
        "moonrise": "6:36 PM",
        "moonset": "5:48 AM"
    }

st.set_page_config(page_title="Panchanga for Today", page_icon="🕉", layout="centered")

st.title("🕉 Panchanga for Today")
st.markdown("Use your **latitude** and **longitude** to check Panchanga info for your region.")

lat = st.number_input("Enter Latitude", value=19.0760, format="%.4f")
lon = st.number_input("Enter Longitude", value=72.8777, format="%.4f")

if st.button("Get Panchanga"):
    data = get_panchanga(lat, lon)
    st.subheader("📅 Date:")
    st.write(data["date"])
    st.subheader("🌞 Vaara (Weekday):")
    st.write(data["vaara"])
    st.subheader("🌙 Tithi:")
    st.write(data["tithi"])
    st.subheader("🌌 Nakshatra:")
    st.write(data["nakshatra"])
    st.subheader("🌕 Moon Phase:")
    st.write(data["moon_phase"])
    st.subheader("🌝 Moonrise:")
    st.write(data["moonrise"])
    st.subheader("🌚 Moonset:")
    st.write(data["moonset"])
