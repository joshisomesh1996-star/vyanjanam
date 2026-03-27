class MenuManager:
    def __init__(self):
        self.menu = {
            "starters": [
                {"name": "Paneer Tikka", "price": 250},
                {"name": "Chicken Tikka", "price": 320},
                {"name": "Spring Rolls", "price": 150},
                {"name": "Hara Bhara Kabab", "price": 180}
            ],
            "main_course": [
                {"name": "Butter Chicken", "price": 350},
                {"name": "Paneer Butter Masala", "price": 280},
                {"name": "Dal Makhani", "price": 240},
                {"name": "Chicken Curry", "price": 300},
                {"name": "Veg Biryani", "price": 220},
                {"name": "Chicken Biryani", "price": 300}
            ],
            "fast_food": [
                {"name": "Veg Burger", "price": 120},
                {"name": "Chicken Burger", "price": 150},
                {"name": "French Fries", "price": 100},
                {"name": "Cheese Pizza", "price": 250},
                {"name": "Pepperoni Pizza", "price": 350}
            ],
            "desserts": [
                {"name": "Gulab Jamun", "price": 90},
                {"name": "Ice Cream", "price": 100},
                {"name": "Brownie", "price": 120}
            ],
            "drinks": [
                {"name": "Coke", "price": 50},
                {"name": "Lassi", "price": 80},
                {"name": "Cold Coffee", "price": 120}
            ]
        }

    def get_menu(self):
        return self.menu

    def flatten_menu(self):
        items = []
        for category in self.menu.values():
            items.extend(category)
        return items

    def display_menu(self):
        print("\n📜 MENU\n")
        count = 1
        for category, items in self.menu.items():
            print(f"\n🔹 {category.upper()}")
            for item in items:
                print(f"{count}. {item['name']} - ₹{item['price']}")
                count += 1

    def select_items(self, indices):
        flat = self.flatten_menu()
        selected = []

        for i in indices:
            if 0 <= i < len(flat):
                selected.append(flat[i])

        return selected

    def search_items(self, keyword):
        flat = self.flatten_menu()
        return [item for item in flat if keyword.lower() in item["name"].lower()]


# ==============================
# 🔥 TEST BLOCK
# ==============================

if __name__ == "__main__":

    menu_manager = MenuManager()

    # 1️⃣ Show full menu
    print("\n=== FULL MENU ===")
    menu_manager.display_menu()

    # 2️⃣ Search test
    print("\n=== SEARCH TEST (keyword: 'pizza') ===")
    search_results = menu_manager.search_items("pizza")

    if search_results:
        for item in search_results:
            print(f"{item['name']} - ₹{item['price']}")
    else:
        print("No items found.")

    # 3️⃣ Select items test
    print("\n=== SELECT ITEMS TEST (indices: 0, 3, 5) ===")
    selected_items = menu_manager.select_items([0, 3, 5])

    for item in selected_items:
        print(f"{item['name']} - ₹{item['price']}")

    # 4️⃣ Total price calculation (extra useful)
    total = sum(item["price"] for item in selected_items)
    print(f"\n💰 Total Price: ₹{total}")