class OrderManager:
    def __init__(self, tax_rate=0.05):
        self.tax_rate = tax_rate  # 5% tax

    # 🔹 Create order
    def create_order(self, restaurant, items):
        """
        restaurant: dict (from RestaurantFinder)
        items: list (from MenuManager)
        """

        if not items:
            print("❌ No items selected")
            return None

        order = {
            "restaurant": restaurant,
            "items": items
        }

        return order

    # 🔹 Calculate bill
    def generate_bill(self, order):
        """
        Calculate subtotal, tax, total
        """

        items = order["items"]

        subtotal = sum(item["price"] for item in items)
        tax = subtotal * self.tax_rate
        total = subtotal + tax

        bill = {
            "subtotal": round(subtotal, 2),
            "tax": round(tax, 2),
            "total": round(total, 2)
        }

        return bill

    # 🔹 Full order summary (important)
    def summarize_order(self, order, bill):
        """
        Combine everything into one response
        """

        summary = {
            "restaurant_name": order["restaurant"]["name"],
            "address": order["restaurant"]["address"],
            "items": order["items"],
            "bill": bill
        }

        return summary

    # 🔹 Display nicely (CLI use)
    def display_order(self, summary):
        print("\n🧾 ORDER SUMMARY\n")

        print(f"🏬 Restaurant: {summary['restaurant_name']}")
        print(f"📍 Address: {summary['address']}\n")

        print("🍽️ Items:")
        for item in summary["items"]:
            print(f"- {item['name']} (₹{item['price']})")

        print("\n💰 BILL:")
        print(f"Subtotal: ₹{summary['bill']['subtotal']}")
        print(f"Tax: ₹{summary['bill']['tax']}")
        print(f"Total: ₹{summary['bill']['total']}")

if __name__ == "__main__":

    # 🔥 Fake restaurant (simulate RestaurantFinder)
    restaurant = {
        "name": "Pizza Hub",
        "address": "Delhi",
        "rating": 4.2
    }

    # 🔥 Fake items (simulate MenuManager)
    items = [
        {"name": "Cheese Pizza", "price": 250},
        {"name": "Cold Coffee", "price": 120}
    ]

    manager = OrderManager()

    # Create order
    order = manager.create_order(restaurant, items)

    # Generate bill
    bill = manager.generate_bill(order)

    # Summary
    summary = manager.summarize_order(order, bill)

    # Display
    manager.display_order(summary)