class UserManager:
    def __init__(self):
        self.user = {
            "user_id": 1,
            "name": "Guest",
            "total_calories": 0,
            "total_spending": 0,
            "order_history": []
        }

    # 🔹 Update after each order
    def update_after_order(self, order, calories, bill):
        """
        Update user stats per order
        """

        # Update totals
        self.user["total_calories"] += calories
        self.user["total_spending"] += bill["total"]

        # Store order
        order_record = {
            "restaurant": order["restaurant"]["name"],
            "items": order["items"],
            "calories": calories,
            "cost": bill["total"]
        }

        self.user["order_history"].append(order_record)

        # 🔥 Return instant feedback
        return self._generate_feedback(order_record)

    # 🔹 Instant feedback
    def _generate_feedback(self, order_record):
        calories = order_record["calories"]

        if calories > 800:
            return "⚠️ High calorie meal"
        elif calories < 300:
            return "⚠️ Very low calorie meal"
        else:
            return "✅ Balanced meal"

    # 🔹 Get totals
    def get_totals(self):
        return {
            "calories": self.user["total_calories"],
            "spending": self.user["total_spending"]
        }

    # 🔹 Get history
    def get_order_history(self):
        return self.user["order_history"]

    # 🔹 Show last order (very useful)
    def get_last_order(self):
        if not self.user["order_history"]:
            return None
        return self.user["order_history"][-1]

if __name__ == "__main__":

    user_manager = UserManager()

    # 🔥 Fake order
    order = {
        "restaurant": {"name": "Pizza Hub"},
        "items": [
            {"name": "Cheese Pizza", "price": 250},
            {"name": "Cold Coffee", "price": 120}
        ]
    }

    calories = 500

    bill = {
        "subtotal": 370,
        "tax": 18.5,
        "total": 388.5
    }

    # Update user
    feedback = user_manager.update_after_order(order, calories, bill)

    print("\n=== FEEDBACK ===")
    print(feedback)

    print("\n=== TOTALS ===")
    print(user_manager.get_totals())

    print("\n=== LAST ORDER ===")
    print(user_manager.get_last_order())