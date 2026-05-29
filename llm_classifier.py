from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

CATEGORIES = [
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
    "Other",
    "Salary",
    "Interest",
    "Cashback / Refunds",
]


def clean_response(text):

    return (
        text
        .replace("*", "")
        .replace("\n", "")
        .strip()
    )


def classify_with_llm(
    message: str,
    merchant: str,
    transaction_type: str
):

    prompt = f"""
You are a financial transaction classifier.

Transaction SMS:
{message}

Merchant:
{merchant}

Transaction Type:
{transaction_type}

Choose EXACTLY ONE category
from this list:

{", ".join(CATEGORIES)}

Rules:
- Return ONLY category name
- No markdown
- No explanation
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

    category = clean_response(
        response.text
    )

    if category not in CATEGORIES:
        return "Other"

    return category

