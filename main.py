from fastapi import FastAPI

from app.models import SMSRequest
from app.llm_classifier import (
    extract_transaction_with_llm
)
from app.form_submit import (
    submit_expense_form
)

app = FastAPI()


@app.get("/")
def home():
    return {
        "status": "ok",
        "message": "Welcome to the Expense Tracker API"
    }


@app.post("/sms")
def process_sms(
    sms_request: SMSRequest
):

    message = sms_request.message

    parsed = extract_transaction_with_llm(
        message
    )

    if not parsed:
        return {
            "status": "error",
            "message": "Failed to parse transaction"
        }

    submit_expense_form(
        expense_type=parsed["transaction_type"],
        category=parsed["category"],
        amount=parsed["amount"],
        payment_mode=parsed["payment_mode"],
        description=parsed['merchant'],
        remarks=f"Merchant: {parsed['merchant']}"
    )

    return {
        "status": "success",
        "parsed": parsed
    }

