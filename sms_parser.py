import re


def extract_amount(text: str):

    patterns = [
        r'Rs\.?\s?(\d+(?:\.\d+)?)',
        r'by\s(\d+(?:\.\d+)?)',
        r'INR\s?(\d+(?:\.\d+)?)',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return float(match.group(1))

    return None


def extract_transaction_type(text: str):

    text_lower = text.lower()

    if "debited" in text_lower:
        return "Expense"

    if "credited" in text_lower:
        return "Income"

    return "Expense"


def extract_merchant(text: str):

    patterns = [
        r'trf to\s(.+?)\sRefno',
        r'transfer from\s(.+?)\sRef',
        r'at\s([A-Z0-9\s\-_\.]+)',
        r'to\s([A-Z0-9\s\-_\.]+)',
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            merchant = match.group(1).strip()

            merchant = re.sub(
                r'\s+',
                ' ',
                merchant
            )

            merchant = merchant.replace(
                "If not u?",
                ""
            ).strip()

            return merchant

    return "Unknown"


def extract_reference_number(text: str):

    patterns = [
        r'Refno\s(\d+)',
        r'Ref No\s(\d+)',
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1)

    return None


def extract_payment_mode(text: str):

    text_upper = text.upper()

    if "X8819" in text_upper:
        return "Debit Card - SBI"

    if "HDFC" in text_upper:
        return "Credit Card - HDFC"

    return "Other:"


def parse_sms(text: str):

    return {
        "transaction_type": extract_transaction_type(text),
        "amount": extract_amount(text),
        "merchant": extract_merchant(text),
        "reference_number": extract_reference_number(text),
        "payment_mode": extract_payment_mode(text),
    }


if __name__ == "__main__":

    sms1 = (
        "Dear UPI user A/C X8819 debited by 30.00 "
        "on date 27May26 trf to SHUSANTA KUMAR S "
        "Refno 614768435330 If not u?"
    )

    sms2 = (
        "Dear SBI User, your A/c X8819-credited by Rs.40 "
        "on 26May26 transfer from PREETI THAPLIYAL "
        "Ref No 614631826010 -SBI"
    )

    print(parse_sms(sms1))
    print(parse_sms(sms2))

