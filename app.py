# app.py

import streamlit as st
from datetime import datetime
from skyfield.api import load, Topos
import pytz
from streamlit_folium import st_folium
import folium

# Load ephemeris
eph = load('de421.bsp')
ts = load.timescale()

# Panchanga definitions
tithis = ["Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi",
          "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dwadashi",
          "Trayodashi", "Chaturdashi", "Purnima/Amavasya"]

nakshatras = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
              "Punarvasu", "Pushya", "Ashlesha", "Magha", "P. Phalguni", "U. Phalguni",
              "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
              "Mula", "P. Ashadha", "U. Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
              "P. Bhadrapada", "U. Bhadrapada", "Revati"]

# Panchanga calculator
def calculate_panchanga(lat, lon):
    timezone = pytz.timezone("Asia/Kolkata")
    now = datetime.now(timezone)
    t = ts.from_datetime(now)

    observer = Topos(latitude_degrees=lat, longitude_degrees=lon)
    obs = eph['earth'] + observer
    sun_pos = obs.at(t).observe(eph['sun']).apparent()
    moon_pos = obs.at(t).observe(eph['moon']).apparent()

    angle = moon_pos.separation_from(sun_pos).degrees
    tithi_index = int(angle // 12)  # 0–29
    tithi_number = tithi_index + 1  # 1–30
    tithi_name = tithis[tithi_index % 15]

    moon_long = moon_pos.ecliptic_latlon()[1].degrees
    nak_index = int(moon_long // (360 / 27))
    nakshatra = nakshatras[nak_index]

    weekday = now.strftime("%A")
    date = now.strftime("%Y-%m-%d %H:%M")

    return {
        "date": date,
        "vaara": weekday,
        "tithi": f"{tithi_name} ({tithi_number}/30)",
        "nakshatra": f"{nakshatra} ({nak_index + 1}/27)"
    }

# -----------------------------------------
# 🌍 Streamlit App with Map Input
# -----------------------------------------
st.set_page_config(page_title="🕉 Panchanga with Map", layout="centered")

st.title("🕉 Panchanga App – Click on Map to Get Panchang")

st.markdown("Click on any place on the map to get Panchanga for that location:")

# Default map centered at Mumbai
m = folium.Map(location=[19.0760, 72.8777], zoom_start=4)
m.add_child(folium.LatLngPopup())  # allows click-to-get coords

# Display map and get coordinates
map_data = st_folium(m, height=400, width=700)

lat = 19.0760
lon = 72.8777

if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    st.success(f"📍 Location selected: {lat:.4f}, {lon:.4f}")

if st.button("Get Panchanga"):
    p = calculate_panchanga(lat, lon)
    st.markdown(f"📅 **Date & Time**: {p['date']}")
    st.markdown(f"🌞 **Vaara**: {p['vaara']}")
    st.markdown(f"🌙 **Tithi**: {p['tithi']}")
    st.markdown(f"🌌 **Nakshatra**: {p['nakshatra']}")
else:
    st.info("Click the map and press the button to fetch Panchanga.")

st.markdown("---")
st.caption("Built with Skyfield, Streamlit, and Folium • Real-time astronomy")
