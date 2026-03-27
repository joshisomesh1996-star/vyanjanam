import sqlite3

DB_NAME = "calories.db"


class CalorieManager:

    def get_calories(self, food_name):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # normalize input
        food_name = food_name.lower().strip()

        cursor.execute(
            "SELECT calories FROM calories WHERE food_name = ?",
            (food_name,)
        )

        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]
        else:
            return 200  # fallback

    def calculate_order_calories(self, items):
        total = 0
        breakdown = []

        for item in items:
            name = item["name"]

            calories = self.get_calories(name)

            breakdown.append({
                "item": name,
                "calories": calories
            })

            total += calories

        return {
            "total_calories": total,
            "breakdown": breakdown
        }


# ==============================
# 🔥 TEST BLOCK
# ==============================

if __name__ == "__main__":

    manager = CalorieManager()

    # 🔥 Simulated items (from MenuManager)
    test_items = [
        {"name": "Cheese Pizza"},
        {"name": "Cold Coffee"},
        {"name": "Paneer Tikka"},
        {"name": "Unknown Dish"}  # should trigger fallback
    ]

    print("\n=== TESTING CALORIE MANAGER ===\n")

    result = manager.calculate_order_calories(test_items)

    print("🔥 TOTAL CALORIES:", result["total_calories"])
    print("\n📊 BREAKDOWN:\n")

    for item in result["breakdown"]:
        print(f"{item['item']} → {item['calories']} kcal")

    print("\n✅ Test completed")