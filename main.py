from fastapi import FastAPI

from app.models import SMSRequest

from app.sms_parser import (
    extract_amount,
    extract_merchant,
    extract_payment_mode,
    extract_transaction_type,
)

from app.merchant_classifier import classify_merchant
from app.llm_classifier import classify_with_llm
from app.form_submit import submit_expense_form


app = FastAPI()


@app.get("/")
def home():
    return {
        "status": "ok",
        "message": "Welcome to the Expense Tracker API"
    }


@app.post("/sms")
def process_sms(sms_request: SMSRequest):

    message = sms_request.message

    amount = extract_amount(message)

    merchant = extract_merchant(message)

    payment_mode = extract_payment_mode(message)

    transaction_type = extract_transaction_type(
        message
    )

    if not merchant:
        merchant = "Unknown"

    # First try rule-based classification
    category = classify_merchant(merchant)

    llm_used = False

    if category is None:

        try:

            category = classify_with_llm(
                message,
                merchant,
                transaction_type
            )

            llm_used = True

        except Exception as e:

            print("LLM ERROR:", e)

            category = "Other"

    submit_expense_form(
        expense_type=transaction_type,
        category=category,
        amount=amount,
        payment_mode=payment_mode,
        description=message,
        remarks=(
            f"Merchant: {merchant}, "
        )
    )

    return {
        "status": "success",
        "category": category,
        "amount": amount,
        "payment_mode": payment_mode,
        "merchant": merchant,
        "transaction_type": transaction_type,
        "llm_used": llm_used
    }

