import requests

from app.config import (
    GOOGLE_FORM_URL,
    FORM_FIELDS
)


def submit_expense_form(
    expense_type,
    category,
    amount,
    payment_mode,
    description="",
    remarks=""
):

    payload = {
        FORM_FIELDS['expense_type']: expense_type,

        FORM_FIELDS['amount']: str(amount),

        FORM_FIELDS['payment_mode']: payment_mode,

        FORM_FIELDS['description']: description,

        FORM_FIELDS['remarks']: remarks
    }

    # Expense Category
    if expense_type == 'Expense':

        payload[
            FORM_FIELDS['expense_category']
        ] = category

    # Income Category
    else:

        payload[
            FORM_FIELDS['income_category']
        ] = category

    print("\n========== PAYLOAD ==========")
    print(payload)

    try:

        response = requests.post(
            GOOGLE_FORM_URL,
            data=payload,
            timeout=15
        )

        print("\n========== STATUS ==========")
        print(response.status_code)

        print("\n========== RESPONSE ==========")
        print(response.text[:300])

        return response

    except Exception as e:

        print("\n========== FORM ERROR ==========")
        print(e)

        return None

