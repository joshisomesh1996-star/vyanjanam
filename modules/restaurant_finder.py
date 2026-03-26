import requests
import os
from dotenv import load_dotenv

from utils.location import get_current_location

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")


def find_restaurants():
    """
    Find nearby restaurants using Google Places API (no dish filtering)
    """
    if not API_KEY:
        print("❌ GOOGLE_API_KEY missing")
        return []

    # 🔥 Step 1: Get user location
    lat, lng = get_current_location()

    if lat is None or lng is None:
        print("❌ Could not determine location")
        return []

    # 🔥 Step 2: Google Places API call
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    params = {
        "location": f"{lat},{lng}",
        "rankby": "distance",   # closest restaurants first
        "type": "restaurant",
        "key": API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        try:
            data = response.json()
        except:
            print("❌ Invalid JSON from Places API")
            return []

        # Handle errors
        if data.get("status") == "ZERO_RESULTS":
            print("⚠️ No restaurants found nearby")
            return []

        if data.get("status") != "OK":
            print(f"❌ Places API Error: {data.get('status')}")
            return []

        # 🔥 Step 3: Parse results
        restaurants = []

        for place in data.get("results", [])[:5]:
            restaurants.append({
                "name": place.get("name"),
                "address": place.get("vicinity"),
                "rating": place.get("rating", "N/A"),
                "place_id": place.get("place_id"),
                "lat": place["geometry"]["location"]["lat"],
                "lon": place["geometry"]["location"]["lng"]
            })

        return restaurants

    except Exception as e:
        print(f"❌ Restaurant fetch error: {e}")
        return []


# 🔥 MAIN (for testing)
if __name__ == "__main__":

    print("🔍 Finding nearby restaurants...\n")

    results = find_restaurants()

    print("\n" + "=" * 30)
    print("🍽️ NEARBY RESTAURANTS")
    print("=" * 30 + "\n")

    if not results:
        print("No restaurants found.")
    else:
        for i, r in enumerate(results):
            print(f"{i + 1}. {r['name']}")
            print(f"   📍 {r['address']}")
            print(f"   ⭐ Rating: {r['rating']}")
            print("-" * 20)