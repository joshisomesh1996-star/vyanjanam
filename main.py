# main.py

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

from modules.restaurant_finder import RestaurantFinder
from modules.menu_manager import MenuManager
from modules.order_manager import OrderManager
from modules.calorie_manager import CalorieManager
from modules.user_manager import UserManager
from modules.email_manager import EmailManager

# 🔥 Services
restaurant_finder = RestaurantFinder()
menu_manager = MenuManager()
order_manager = OrderManager()
calorie_manager = CalorieManager()
user_manager = UserManager()
email_manager = EmailManager()

mcp = FastMCP("vyanjanam-mcp")


# =========================================================
# 👤 SET USER
# =========================================================
@mcp.tool()
def set_user(name: str, email: str) -> str:
    if not email or "@" not in email:
        return "Invalid email format"

    user_manager.set_user(name, email)
    return f"User set: {name}"


# =========================================================
# STEP 1: FIND RESTAURANTS
# =========================================================
@mcp.tool()
def find_restaurants() -> list:
    try:
        result = restaurant_finder.find_restaurants()

        if not result:
            return [{"error": "No restaurants found"}]

        return result

    except Exception as e:
        return [{"error": str(e)}]


# =========================================================
# STEP 2: SELECT RESTAURANT
# =========================================================
@mcp.tool()
def select_restaurant(restaurants: list, index: int) -> dict:
    try:
        if not restaurants:
            return {"error": "No restaurants provided"}

        if index < 0 or index >= len(restaurants):
            return {"error": "Invalid restaurant index"}

        return restaurants[index]

    except Exception as e:
        return {"error": str(e)}


# =========================================================
# STEP 3: SHOW MENU
# =========================================================
@mcp.tool()
def get_menu() -> dict:
    try:
        return menu_manager.get_menu()
    except Exception as e:
        return {"error": str(e)}


# =========================================================
# STEP 4: SELECT ITEMS
# =========================================================
@mcp.tool()
def select_items(indices: list) -> list:
    try:
        items = menu_manager.select_items(indices)

        if not items:
            return [{"error": "No valid items selected"}]

        return items

    except Exception as e:
        return [{"error": str(e)}]


# =========================================================
# STEP 5: CREATE ORDER
# =========================================================
@mcp.tool()
def create_order(restaurant: dict, items: list) -> dict:
    try:
        if not restaurant:
            return {"error": "Restaurant not selected"}

        if not items:
            return {"error": "No items selected"}

        return order_manager.create_order(restaurant, items)

    except Exception as e:
        return {"error": str(e)}


# =========================================================
# STEP 6: FINALIZE ORDER
# =========================================================
@mcp.tool()
def finalize_order(order: dict) -> dict:
    """
    Generate bill + calories + update user + send email
    """

    try:
        if not order:
            return {"error": "Order is empty"}

        # 💰 Bill
        bill = order_manager.generate_bill(order)

        # 🔥 Calories
        calories = calorie_manager.calculate_order_calories(order["items"])

        # 👤 Update user
        feedback = user_manager.update_after_order(
            order,
            calories["total_calories"],
            bill
        )

        summary = {
            "restaurant": order["restaurant"]["name"],
            "items": order["items"],
            "bill": bill,
            "calories": calories,
            "feedback": feedback
        }

        # 📧 EMAIL CHECK (IMPORTANT FIX)
        user_email = user_manager.get_email()

        if not user_email or "@" not in user_email:
            summary["email_status"] = "User email not set. Please call set_user first."
            return summary

        # 📧 SEND EMAIL
        email_status = email_manager.send_order_summary(
            summary,
            user_manager.get_totals(),
            user_email
        )

        summary["email_status"] = email_status

        return summary

    except Exception as e:
        return {"error": str(e)}


# =========================================================
# 📊 USER DATA
# =========================================================
@mcp.tool()
def get_user_stats() -> dict:
    return user_manager.get_totals()


@mcp.tool()
def get_order_history() -> list:
    return user_manager.get_order_history()


# =========================================================
# 🧠 PROMPT
# =========================================================
@mcp.prompt("food_order_assistant")
def food_order_assistant():
    return """
You are a food ordering assistant.

STRICT FLOW:

1. Ask user name and email → call set_user

2. Call find_restaurants
3. Ask user to choose restaurant (index)
4. Call select_restaurant

5. Call get_menu
6. Ask user to choose item indices

7. Call select_items
8. Call create_order

9. Call finalize_order

DO NOT skip steps.
DO NOT assume user choices.
Always ask user before next step.
"""


# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":
    mcp.run(transport="stdio")