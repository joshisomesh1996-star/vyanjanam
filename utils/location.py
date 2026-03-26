import requests

def get_user_coordinates():
    try:
        res = requests.get("https://ipinfo.io/json", timeout=5)
        data = res.json()

        loc = data.get("loc")  # format: "lat,lon"

        if loc:
            lat, lon = loc.split(",")
            return lat, lon

        return None, None

    except Exception as e:
        print("Location error:", e)
        return None, None


# 🔥 Demo runner
if __name__ == "__main__":
    lat, lon = get_user_coordinates()

    print("\n📍 Your Location Coordinates:\n")

    if lat and lon:
        print(f"Latitude: {lat}")
        print(f"Longitude: {lon}")
        print(f"LL Format: {lat},{lon}")  # useful for API
    else:
        print("❌ Could not fetch location.")