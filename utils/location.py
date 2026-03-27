import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")


def get_current_location():
    """
    MCP-safe location fetcher
    Returns:
        (lat, lng) OR raises controlled error via return
    """

    if not API_KEY:
        return None, None

    geo_url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={API_KEY}"

    try:
        # 🔹 Try Google Geolocation API
        response = requests.post(geo_url, json={}, timeout=10)
        data = response.json()

        if response.status_code == 200:
            location = data.get("location", {})
            lat = location.get("lat")
            lng = location.get("lng")

            if lat and lng:
                return lat, lng

        # 🔹 Fallback → IP-based location
        fallback = requests.get("https://ipapi.co/json/", timeout=5)
        fallback_data = fallback.json()

        lat = fallback_data.get("latitude")
        lng = fallback_data.get("longitude")

        if lat and lng:
            return lat, lng

        return None, None

    except Exception:
        return None, None