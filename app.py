import streamlit as st
from skyfield.api import load, Topos
from datetime import datetime
import pytz
from geopy.geocoders import Nominatim

# Load ephemeris data
eph = load('de421.bsp')  # Only needs to be downloaded once
ts = load.timescale()

# Nakshatra list (27)
nakshatras = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
    "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
    "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

# Tithi names (30 total)
tithis = [
    "Shukla Pratipada", "Shukla Dwitiya", "Shukla Tritiya", "Shukla Chaturthi", "Shukla Panchami",
    "Shukla Shashti", "Shukla Saptami", "Shukla Ashtami", "Shukla Navami", "Shukla Dashami",
    "Shukla Ekadashi", "Shukla Dwadashi", "Shukla Trayodashi", "Shukla Chaturdashi", "Purnima",
    "Krishna Pratipada", "Krishna Dwitiya", "Krishna Tritiya", "Krishna Chaturthi", "Krishna Panchami",
    "Krishna Shashti", "Krishna Saptami", "Krishna Ashtami", "Krishna Navami", "Krishna Dashami",
    "Krishna Ekadashi", "Krishna Dwadashi", "Krishna Trayodashi", "Krishna Chaturdashi", "Amavasya"
]

# Get user location and date
st.title("🌞 Real-Time Panchang Demo")
city = st.text_input("Enter your location (e.g., Varanasi, Delhi)", value="Delhi")
date = st.date_input("Choose a date", value=datetime.now().date())

# Use geopy to convert city name to lat/lon
geolocator = Nominatim(user_agent="panchang-app")
location = geolocator.geocode(city)

if location:
    lat, lon = location.latitude, location.longitude
    st.success(f"📍 Location: {location.address}")
    st.write(f"🧭 Coordinates: {lat:.4f}, {lon:.4f}")

    # Skyfield observer
    observer = Topos(latitude_degrees=lat, longitude_degrees=lon)
    time = ts.utc(date.year, date.month, date.day, datetime.now().hour)

    # Planet positions
    sun = eph['sun']
    moon = eph['moon']
    earth = eph['earth']
    observer = earth + observer

    sun_pos = observer.at(time).observe(sun).apparent().ecliptic_latlon()
    moon_pos = observer.at(time).observe(moon).apparent().ecliptic_latlon()

    sun_long = sun_pos[1].degrees
    moon_long = moon_pos[1].degrees

    # Calculate Tithi
    angle = (moon_long - sun_long) % 360
    tithi_index = int(angle / 12)
    tithi = tithis[tithi_index]

    # Calculate Nakshatra
    nakshatra_index = int(moon_long / (360 / 27))
    nakshatra = nakshatras[nakshatra_index]

    # Calculate Vaara (weekday)
    weekday = date.strftime("%A")

    # Display output
    st.subheader("🕉️ Panchang Elements")
    st.write(f"**Vaara (Day)**: {weekday}")
    st.write(f"**Tithi**: {tithi}")
    st.write(f"**Nakshatra**: {nakshatra}")
    st.write(f"**Moon Longitude**: {moon_long:.2f}°")
    st.write(f"**Sun Longitude**: {sun_long:.2f}°")

else:
    st.error("Could not find the location. Please check the name and try again.")
