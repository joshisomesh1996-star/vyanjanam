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
        MCP-safe restaurant finder
        """

        if not self.api_key:
            return [{"error": "GOOGLE_API_KEY missing"}]

        # 🔥 Step 1: Get location
        lat, lng = get_current_location()

        if lat is None or lng is None:
            return [{"error": "Could not determine location"}]

        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

        params = {
            "location": f"{lat},{lng}",
            "rankby": "distance",
            "type": "restaurant",
            "key": self.api_key
        }

        try:
            response = requests.get(url, params=params, timeout=10)

            data = response.json()

            status = data.get("status")

            if status == "ZERO_RESULTS":
                return [{"message": "No restaurants found nearby"}]

            if status != "OK":
                return [{"error": f"Places API Error: {status}"}]

            return self._parse_results(data, limit)

        except Exception as e:
            return [{"error": str(e)}]

    # 🔹 Internal parser
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


# 🔥 TEST (safe for CLI only)
if __name__ == "__main__":
    finder = RestaurantFinder()
    results = finder.find_restaurants()

    print("\n🍽️ TEST OUTPUT:\n")
    print(results)