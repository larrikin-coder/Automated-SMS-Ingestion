import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

ALLOWED_CATEGORIES = [
    "Utilities - Water / Gas",
    "Rent / Other Maintenance",
    "Dining out",
    "Food Delivery",
    "Cabs / Metro / Commute",
    "Gadgets / Internet / Other subscriptions",
    "Gifts",
    "Insurance / Legal",
    "Medical",
    "Travel",
    "Clothes / Accessories / Haircut",
    "Electricity",
    "Other:",
    "Salary",
    "Interest",
    "Cashback / Refunds",
]

ALLOWED_PAYMENT_MODES = [
    "Debit Card - SBI",
    "Credit Card - HDFC",
    "Other:"
]


def extract_transaction_with_llm(
    message: str
):

    prompt = f"""
You are an expert financial transaction parser.

Analyze the transaction message and extract structured information.

MESSAGE:
{message}

Return ONLY valid JSON.

Schema:

{{
    "transaction_type": "Expense or Income",
    "amount": 0,
    "merchant": "",
    "category": "",
    "payment_mode": ""
}}

Allowed categories:

{ALLOWED_CATEGORIES}

Allowed payment modes:

{ALLOWED_PAYMENT_MODES}

Rules:

1. If money leaves the account:
   transaction_type = Expense

2. If money enters the account:
   transaction_type = Income

3. Personal transfers:
   - received money -> Gifts
   - sent money -> Gifts

4. Salary payments -> Salary

5. Interest payments -> Interest

6. Refunds and cashback -> Cashback / Refunds

7. Food ordering apps -> Food Delivery

8. Ride sharing apps -> Cabs / Metro / Commute

9. Medical stores/hospitals -> Medical

10. Streaming subscriptions:
    Netflix
    Spotify
    Prime Video
    Hotstar
    YouTube Premium

    -> Gadgets / Internet / Other subscriptions

11. payment_mode MUST be one of:

    if the card number is X8819 then - Debit Card - SBI
    Credit Card - HDFC

12. category MUST be one of the allowed categories.

13. Return ONLY JSON.

14. No markdown.

15. No explanation.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        text = (
            text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        data = json.loads(text)

        if data.get("category") not in ALLOWED_CATEGORIES:
            data["category"] = "Other:"

        if (
            data.get("payment_mode")
            not in ALLOWED_PAYMENT_MODES
        ):
            data["payment_mode"] = "Other:"

        return data

    except Exception as e:

        print(
            "GEMINI EXTRACTION ERROR:",
            e
        )

        return {
            "transaction_type": "Expense",
            "amount": 0,
            "merchant": "Unknown",
            "category": "Other:",
            "payment_mode": "Other:"
        }

