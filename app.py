# app.py

import streamlit as st
from datetime import datetime
from skyfield.api import load, Topos
import pytz

# Load ephemeris
eph = load('de421.bsp')
ts = load.timescale()

# List of Panchanga items
tithis = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi",
    "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dwadashi",
    "Trayodashi", "Chaturdashi", "Purnima/Amavasya"
]

nakshatras = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "P. Phalguni", "U. Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "P. Ashadha", "U. Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "P. Bhadrapada", "U. Bhadrapada", "Revati"
]

# Panchanga calculator
def calculate_panchanga(lat, lon):
    timezone = pytz.timezone("Asia/Kolkata")
    now = datetime.now(timezone)
    t = ts.from_datetime(now)

    observer = Topos(latitude_degrees=lat, longitude_degrees=lon)
    obs = eph['earth'] + observer

    sun = eph['sun']
    moon = eph['moon']

    sun_pos = obs.at(t).observe(sun).apparent()
    moon_pos = obs.at(t).observe(moon).apparent()

    # Tithi
    angle = moon_pos.separation_from(sun_pos).degrees
    tithi_number = int(angle // 12) + 1
    tithi_name = tithis[tithi_number % 15]

    # Nakshatra
    moon_long = moon_pos.ecliptic_latlon()[1].degrees
    nakshatra_index = int(moon_long // (360 / 27))
    nakshatra_name = nakshatras[nakshatra_index]

    # Weekday
    weekday = now.strftime("%A")
    date = now.strftime("%Y-%m-%d %H:%M")

    return {
        "date": date,
        "vaara": weekday,
        "tithi": f"{tithi_name} ({tithi_number}/30)",
        "nakshatra": f"{nakshatra_name} ({nakshatra_index + 1}/27)"
    }

# ----------------------------
# Streamlit App UI
# ----------------------------
st.set_page_config(page_title="🕉 Real Panchanga", layout="centered")

st.title("🕉 Real Panchanga App using NASA Skyfield")
st.markdown("Enter your location to get accurate Tithi, Nakshatra, and Vaara.")

# Input
lat = st.number_input("🌍 Latitude", value=19.0760, format="%.4f")
lon = st.number_input("🌍 Longitude", value=72.8777, format="%.4f")

if st.button("Get Today's Panchanga"):
    data = calculate_panchanga(lat, lon)
    st.success("🔍 Panchanga Calculated!")
    st.markdown(f"📅 **Date & Time**: {data['date']}")
    st.markdown(f"🌞 **Vaara (Weekday)**: {data['vaara']}")
    st.markdown(f"🌙 **Tithi**: {data['tithi']}")
    st.markdown(f"🌌 **Nakshatra**: {data['nakshatra']}")
else:
    st.info("Click the button to see today's Panchanga.")

st.markdown("---")
st.caption("Built with NASA Skyfield • Accurate • Educational")
