KNOWN_MERCHANTS = { 
                   "SWIGGY": "Food Delivery",
                   "ZOMATO": "Food Delivery",
                   "UBER": "Cabs / Metro / Commute",
                   "OLA": "Cabs / Metro / Commute",
                   "BLINKIT": "Food Delivery",
                   "ZEPTO": "Food Delivery",
                   "AMAZON": "Other",
                   "FLIPKART": "Other",
                   "APOLLO": "Medical",
                   "NETFLIX": "Gadgets / Internet / Other subscriptions",
                   "SPOTIFY": "Gadgets / Internet / Other subscriptions",
                   "HOTSTAR": "Gadgets / Internet / Other subscriptions",
                   "PRIME VIDEO": "Gadgets / Internet / Other subscriptions",
                   "YOUTUBE": "Gadgets / Internet / Other subscriptions",
                   }

def classify_merchant(merchant_name):
    for known_merchant in KNOWN_MERCHANTS:
        if known_merchant in merchant_name.upper():
            return KNOWN_MERCHANTS[known_merchant]
    return "Gifts"

