# modules/email_manager.py

import os
from dotenv import load_dotenv
from utils.emails import EmailSender

load_dotenv()


class EmailManager:
    """
    Handles business logic for sending order-related emails
    """

    def __init__(self):
        self.sender = EmailSender(
            smtp_server="smtp.gmail.com",
            port=587,
            username=os.getenv("EMAIL"),
            password=os.getenv("EMAIL_PWD"),
            use_tls=True
        )

    def send_order_summary(self, order_summary: dict, user_stats: dict, user_email: str):
        """
        Send email with order + calorie + spending update
        """

        # 🔥 Validate email
        if not user_email or "@" not in user_email:
            return "Invalid or missing user email"

        subject = "🍽️ Your Vyanjanam Order Summary"
        body = self._format_email(order_summary, user_stats)

        try:
            self.sender.send_email(
                subject=subject,
                body=body,
                to_emails=user_email,
                html=False
            )
            return "Email sent successfully"

        except Exception as e:
            # 🔥 Important for debugging in MCP
            print("EMAIL ERROR:", str(e))
            return f"Email failed: {str(e)}"

    def _format_email(self, summary, stats):
        """
        Format email content
        """

        items_text = "\n".join(
            [f"- {item['name']} (₹{item['price']})" for item in summary["items"]]
        )

        calories_text = "\n".join(
            [f"- {item['item']}: {item['calories']} kcal"
             for item in summary["calories"]["breakdown"]]
        )

        return f"""
🍽️ Order Summary

Restaurant: {summary['restaurant']}

Items:
{items_text}

-----------------------
💰 BILL
Subtotal: ₹{summary['bill']['subtotal']}
Tax: ₹{summary['bill']['tax']}
Total: ₹{summary['bill']['total']}

-----------------------
🔥 CALORIES
{calories_text}

Total Calories: {summary['calories']['total_calories']}

-----------------------
📊 YOUR STATS
Total Calories Consumed: {stats['calories']}
Total Spending: ₹{stats['spending']}

-----------------------
⚠️ Feedback:
{summary['feedback']}

Thank you for using Vyanjanam AI 🚀
"""


# ==============================
# 🔥 TEST BLOCK
# ==============================
if __name__ == "__main__":

    email_manager = EmailManager()

    # Fake data for testing
    summary = {
        "restaurant": "Pizza Hub",
        "items": [
            {"name": "Cheese Pizza", "price": 250},
            {"name": "Cold Coffee", "price": 120}
        ],
        "bill": {
            "subtotal": 370,
            "tax": 18.5,
            "total": 388.5
        },
        "calories": {
            "total_calories": 500,
            "breakdown": [
                {"item": "Cheese Pizza", "calories": 285},
                {"item": "Cold Coffee", "calories": 180}
            ]
        },
        "feedback": "✅ Balanced meal"
    }

    stats = {
        "calories": 500,
        "spending": 388.5
    }

    result = email_manager.send_order_summary(
        summary,
        stats,
        user_email=os.getenv("EMAIL")  # send to yourself for testing
    )

    print(result)