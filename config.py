from dotenv import load_dotenv
import os
load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_FORM_URL = os.getenv("GOOGLE_FORM_URL")

FORM_FIELDS = {
    "expense_type": os.getenv("FORM_EXPENSE_TYPE"),

    "expense_category": os.getenv(
        "FORM_EXPENSE_CATEGORY"
    ),

    "income_category": os.getenv(
        "FORM_INCOME_CATEGORY"
    ),

    "amount": os.getenv("FORM_AMOUNT"),

    "payment_mode": os.getenv(
        "FORM_PAYMENT_MODE"
    ),

    "description": os.getenv(
        "FORM_DESCRIPTION"
    ),

    "remarks": os.getenv(
        "FORM_REMARKS"
    )
}



