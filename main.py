# main.py

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

from modules.restaurant_finder import RestaurantFinder
from modules.menu_manager import MenuManager
from modules.order_manager import OrderManager
from modules.calorie_manager import CalorieManager
from modules.user_manager import UserManager

# 🔥 Services
restaurant_finder = RestaurantFinder()
menu_manager = MenuManager()
order_manager = OrderManager()
calorie_manager = CalorieManager()
user_manager = UserManager()

mcp = FastMCP("vyanjanam-mcp")

# =========================================================
# STEP 1: FIND RESTAURANTS
# =========================================================
@mcp.tool()
def find_restaurants() -> list:
    """
    Step 1: Get nearby restaurants.
    """
    return restaurant_finder.find_restaurants()


# =========================================================
# STEP 2: SELECT RESTAURANT
# =========================================================
@mcp.tool()
def select_restaurant(restaurants: list, index: int) -> dict:
    """
    Step 2: User selects restaurant.
    """
    if index < 0 or index >= len(restaurants):
        raise ValueError("Invalid restaurant index")

    return restaurants[index]


# =========================================================
# STEP 3: SHOW MENU
# =========================================================
@mcp.tool()
def get_menu() -> dict:
    """
    Step 3: Show menu.
    """
    return menu_manager.get_menu()


# =========================================================
# STEP 4: SELECT ITEMS
# =========================================================
@mcp.tool()
def select_items(indices: list) -> list:
    """
    Step 4: User selects items.
    """
    return menu_manager.select_items(indices)


# =========================================================
# STEP 5: CREATE ORDER
# =========================================================
@mcp.tool()
def create_order(restaurant: dict, items: list) -> dict:
    """
    Step 5: Create order.
    """
    return order_manager.create_order(restaurant, items)


# =========================================================
# STEP 6: FINALIZE ORDER
# =========================================================
@mcp.tool()
def finalize_order(order: dict) -> dict:
    """
    Step 6: Generate bill + calories + update user.
    """

    bill = order_manager.generate_bill(order)
    calories = calorie_manager.calculate_order_calories(order["items"])

    feedback = user_manager.update_after_order(
        order,
        calories["total_calories"],
        bill
    )

    return {
        "restaurant": order["restaurant"]["name"],
        "items": order["items"],
        "bill": bill,
        "calories": calories,
        "feedback": feedback
    }


# =========================================================
# OPTIONAL: USER DATA
# =========================================================
@mcp.tool()
def get_user_stats() -> dict:
    return user_manager.get_totals()


@mcp.tool()
def get_order_history() -> list:
    return user_manager.get_order_history()


# =========================================================
# 🧠 PROMPT (GUIDES FLOW, DOES NOT AUTO-SKIP USER)
# =========================================================
@mcp.prompt("food_order_assistant")
def food_order_assistant():
    return """
You are a food ordering assistant.

STRICT FLOW:

1. Call find_restaurants
2. Ask user to choose restaurant (index)
3. Call select_restaurant

4. Call get_menu
5. Ask user to choose item indices

6. Call select_items
7. Call create_order

8. Call finalize_order

DO NOT skip steps.
DO NOT assume user choices.
Always ask user before next step.
"""


# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":
    mcp.run(transport="stdio")