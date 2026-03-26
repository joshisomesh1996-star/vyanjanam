# main.py

from modules.input_parser import parse_user_input
from modules.restaurant_finder import find_restaurants
from modules.menu_matcher import match_dishes
from modules.order_manager import create_order
from modules.billing import generate_bill
from modules.calorie_engine import calculate_calories
from modules.tracker import update_weekly_tracker
from modules.report import generate_report


def run_app():
    print("🍽️ Welcome to Vyanjanam AI")

    # 1. User Input
    user_input = input("What would you like to eat? ")

    # 2. Parse Input
    parsed_data = parse_user_input(user_input)

    # 3. Find Restaurants
    restaurants = find_restaurants(parsed_data)

    # 4. Match Dishes
    options = match_dishes(restaurants, parsed_data)

    print("\nAvailable options:")
    for i, opt in enumerate(options):
        print(f"{i+1}. {opt}")

    choice = int(input("Select option: ")) - 1
    selected_item = options[choice]

    # 5. Create Order
    order = create_order(selected_item)

    # 6. Generate Bill
    bill = generate_bill(order)

    # 7. Calculate Calories
    nutrition = calculate_calories(order)

    # 8. Update Tracker
    update_weekly_tracker(order, nutrition)

    # 9. Generate Report
    report = generate_report()

    print("\n🧾 Bill:", bill)
    print("🔥 Calories:", nutrition)
    print("📊 Weekly Report:", report)


if __name__ == "__main__":
    run_app()