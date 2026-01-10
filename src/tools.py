import random

# The dictionary of valid market prices for the mock
MARKET_DB = {
    "monitor": 200,
    "airpods": 150,
    "macbook": 800,
    "chair": 100,
    "iphone": 999,
    "ps5": 500,
    "tesla": 45000,
    "coffee": 5,
    "t-shirt": 25,
    "camera": 600,
    "watch": 250,
    "headphones": 100
}

def check_market_price(item_name: str):
    """
    Look up the average market price of an item.
    Args:
        item_name: The name of the product.
    """
    print(f"\n[DEBUG] 🛠️ Tool Triggered: Searching price for '{item_name}'...")
    
    # Simple keyword matching for the mock
    found_price = None
    for key, price in MARKET_DB.items():
        if key in item_name.lower():
            found_price = price
            break
    
    if found_price:
        return {"average_price": found_price, "currency": "USD", "demand": "High"}
    else:
        return {"average_price": "Unknown", "note": "Item not found in database."}