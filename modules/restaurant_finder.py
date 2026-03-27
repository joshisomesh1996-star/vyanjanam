import requests
import os
from dotenv import load_dotenv

from utils.location import get_current_location

load_dotenv()


class RestaurantFinder:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")

    # 🔹 Get nearby restaurants
    def find_restaurants(self, limit=5):
        """
        Find nearby restaurants using Google Places API
        """

        if not self.api_key:
            print("❌ GOOGLE_API_KEY missing")
            return []

        # 🔥 Step 1: Get user location
        lat, lng = get_current_location()

        if lat is None or lng is None:
            print("❌ Could not determine location")
            return []

        # 🔥 Step 2: API call
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

        params = {
            "location": f"{lat},{lng}",
            "rankby": "distance",
            "type": "restaurant",
            "key": self.api_key
        }

        try:
            response = requests.get(url, params=params, timeout=10)

            try:
                data = response.json()
            except:
                print("❌ Invalid JSON from Places API")
                return []

            # 🔴 Handle errors
            status = data.get("status")

            if status == "ZERO_RESULTS":
                print("⚠️ No restaurants found nearby")
                return []

            if status != "OK":
                print(f"❌ Places API Error: {status}")
                return []

            # 🔥 Step 3: Parse
            return self._parse_results(data, limit)

        except Exception as e:
            print(f"❌ Restaurant fetch error: {e}")
            return []

    # 🔹 Internal parser (clean design)
    def _parse_results(self, data, limit):
        restaurants = []

        for place in data.get("results", [])[:limit]:
            restaurants.append({
                "name": place.get("name"),
                "address": place.get("vicinity"),
                "rating": place.get("rating", "N/A"),
                "place_id": place.get("place_id"),
                "lat": place["geometry"]["location"]["lat"],
                "lon": place["geometry"]["location"]["lng"]
            })

        return restaurants

    # 🔹 Display nicely
    def display_restaurants(self, restaurants):
        print("\n🍽️ NEARBY RESTAURANTS\n")

        if not restaurants:
            print("No restaurants found.")
            return

        for i, r in enumerate(restaurants):
            print(f"{i + 1}. {r['name']}")
            print(f"   📍 {r['address']}")
            print(f"   ⭐ Rating: {r['rating']}")
            print("-" * 20)


# 🔥 TEST
if __name__ == "__main__":
    finder = RestaurantFinder()

    print("🔍 Finding nearby restaurants...\n")

    results = finder.find_restaurants()

    finder.display_restaurants(results)