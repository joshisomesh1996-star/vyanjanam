import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("FOURSQUARE_API_KEY")


def find_restaurants(parsed_data):
    if not API_KEY:
        print("❌ API key not found. Check your .env file.")
        return []

    location = parsed_data.get("location", "Delhi")
    dish = parsed_data.get("dishes", ["restaurant"])[0]

    url = "https://places-api.foursquare.com/places/search"

    headers = {
        "accept": "application/json",
        "X-Places-Api-Version": "2025-06-17",
        "authorization": f"Bearer {API_KEY}"
    }

    params = {
        "query": f"{dish}",
        "near": location,
        "limit": 5,
        "sort": "DISTANCE"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)

        print("Status Code:", response.status_code)  # debug

        if response.status_code != 200:
            print("❌ API Error:", response.text)
            return []

        data = response.json()

        restaurants = []

        for place in data.get("results", []):
            restaurants.append({
                "name": place.get("name"),
                "address": place.get("location", {}).get("formatted_address"),
                "rating": place.get("rating", "N/A"),
                "fsq_id": place.get("fsq_id"),  # IMPORTANT for details API
                "lat": place.get("geocodes", {}).get("main", {}).get("latitude"),
                "lon": place.get("geocodes", {}).get("main", {}).get("longitude")
            })

        return restaurants

    except Exception as e:
        print("❌ Error fetching restaurants:", e)
        return []


# 🔥 Demo run
if __name__ == "__main__":

    print("API KEY:", API_KEY)

    sample_input = {
        "dishes": ["butter chicken"],
        "location": "Delhi"
    }

    results = find_restaurants(sample_input)

    print("\n🍽️ Nearby Restaurants:\n")

    if not results:
        print("No restaurants found.")
    else:
        for i, r in enumerate(results):
            print(f"{i+1}. {r['name']}")
            print(f"   📍 {r['address']}")
            print(f"   ⭐ {r['rating']}")
            print()