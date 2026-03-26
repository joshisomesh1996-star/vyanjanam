import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")


def get_current_location():
    """
    Get user location using Google Geolocation API with fallback.
    """
    if not API_KEY:
        print("❌ GOOGLE_API_KEY not found")
        return None, None

    geo_url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={API_KEY}"

    try:
        response = requests.post(geo_url, json={}, timeout=10)

        try:
            data = response.json()
        except:
            print("❌ Invalid JSON from Google")
            return None, None

        if response.status_code == 200:
            location = data.get("location", {})
            lat, lng = location.get("lat"), location.get("lng")

            print(f"📍 Detected Location (Google): {lat}, {lng}")
            return lat, lng

        else:
            error_msg = data.get("error", {}).get("message", "Unknown Error")
            print(f"⚠️ Google Geolocation failed: {error_msg}")

            # 🔁 fallback
            print("🔄 Trying IP fallback...")
            fallback = requests.get("https://ipapi.co/json/", timeout=5).json()

            lat = fallback.get("latitude")
            lng = fallback.get("longitude")

            if lat and lng:
                print(f"📍 Detected Location (Fallback): {lat}, {lng}")
                return lat, lng

            return None, None

    except Exception as e:
        print(f"❌ Location error: {e}")
        return None, None