import sqlite3

DB_NAME = "calories.db"


def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS calories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        food_name TEXT UNIQUE,
        calories INTEGER
    )
    """)

    conn.commit()
    conn.close()


def seed_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    data = [
        ("paneer tikka", 250),
        ("chicken tikka", 320),
        ("spring rolls", 150),
        ("hara bhara kabab", 180),
        ("butter chicken", 350),
        ("paneer butter masala", 300),
        ("dal makhani", 320),
        ("chicken curry", 300),
        ("veg biryani", 280),
        ("chicken biryani", 350),
        ("veg burger", 250),
        ("chicken burger", 300),
        ("french fries", 320),
        ("cheese pizza", 285),
        ("pepperoni pizza", 350),
        ("gulab jamun", 150),
        ("ice cream", 200),
        ("brownie", 250),
        ("coke", 140),
        ("lassi", 220),
        ("cold coffee", 180)
    ]

    for item in data:
        try:
            cursor.execute(
                "INSERT INTO calories (food_name, calories) VALUES (?, ?)",
                item
            )
        except:
            pass

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_db()
    seed_data()
    print("✅ DB ready")