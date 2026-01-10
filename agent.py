import os
from google.adk.agents import Agent, Tool
from google.adk.types import ModelType
from dotenv import load_dotenv

# 1. Load Keys
load_dotenv()

# 2. Define Tools (The ADK way)
def check_market_price(item_name: str) -> str:
    """
    Searches market databases to find the average used price of an item.
    Use this to determine if a buyer's offer is fair.
    """
    # Mock database for the Hackathon demo
    prices = {
        "ps5": 450,
        "monitor": 200,
        "iphone": 600,
        "chair": 100
    }
    
    # Simple fuzzy match
    for key, price in prices.items():
        if key in item_name.lower():
            return f"Market Value: ${price}. Demand: High."
            
    return "Market Value: Unknown. Assume $100 for generic items."

# 3. Initialize the ADK Agent
# The 'Agent' class automatically creates the web server endpoints
haggle_bot = Agent(
    name="Auto-Haggle-Bot",
    model="gemini-1.5-flash",  # Use the standard model string
    instruction="""
    You are 'The Closer', a ruthless negotiation agent on Facebook Marketplace.
    
    YOUR PROCESS:
    1. Receive a message from a buyer.
    2. Check if the item has a known price using 'check_market_price'.
    3. If the offer is < 80% of market value, ROAST THEM.
    4. If the offer is fair, accept cautiously.
    
    TONE: Short, text-message style, slightly aggressive.
    """,
    tools=[check_market_price] # Register the function directly
)

# 4. (Optional) Hooks for the ADK Runner
# This tells the 'adk' CLI where to find your entry point
def entry_point():
    return haggle_bot