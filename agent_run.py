import os
import time
import google.generativeai as genai
from google.generativeai.types import content_types
from collections.abc import Iterable
from dotenv import load_dotenv

# 1. Load your API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# 2. Define the Tool (The "Hands")
# The SDK allows you to pass a simple Python function as a tool.
def check_market_price(item_name: str):
    """
    Look up the current market value of a used item.
    """
    print(f"\n[⚙️ TOOL USE] Checking database for: '{item_name}'...")
    time.sleep(1) # Simulate network delay for effect
    
    # Mock Database for the Demo
    db = {
        "ps5": 400,
        "monitor": 180,
        "macbook": 750,
        "iphone": 500
    }
    
    for key, price in db.items():
        if key in item_name.lower():
            return {"price": price, "currency": "USD", "demand": "High"}
            
    return {"price": 50, "currency": "USD", "demand": "Low (Unknown Item)"}

# 3. Initialize the Autonomous Model
# We explicitly enable 'automatic_function_calling' to make it an Agent.
tools = [check_market_price]

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    tools=tools,
    system_instruction="""
    You are 'The Closer', a ruthless negotiation agent.
    
    RULES:
    1. When a user mentions an item, YOU MUST FIRST use the 'check_market_price' tool to value it.
    2. Once you have the price, compare it to the user's offer.
    3. If Offer < 80% of Market Price -> Roast them and reject.
    4. If Offer >= 80% -> Accept.
    
    Keep responses short, punchy, and sarcastic.
    """
)

# 4. The Chat Loop
def start_agent():
    print("--------------------------------------------------")
    print("🤖 AUTO-HAGGLE AGENT ONLINE (Gemini 1.5 Flash)")
    print("--------------------------------------------------")
    
    # Enable automatic tool use (Agent Mode)
    chat = model.start_chat(enable_automatic_function_calling=True)
    
    while True:
        user_input = input("\n👤 BUYER: ")
        if user_input.lower() in ["quit", "exit"]:
            break
            
        print("🤖 AGENT THINKING...", end="", flush=True)
        
        try:
            # The SDK handles the Tool Call -> Output -> Final Response loop automatically
            response = chat.send_message(user_input)
            print(f"\r🤖 AGENT: {response.text}")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    start_agent()