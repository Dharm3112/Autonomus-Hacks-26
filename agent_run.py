import os
import time
import google.generativeai as genai
from duckduckgo_search import DDGS
from dotenv import load_dotenv

# 1. Load your API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- THE UNIVERSAL SEARCH TOOL ---
def real_web_search(query: str):
    """
    Performs a real-time web search to get live data.
    """
    print(f"\n[🌐 WEB SEARCH] Googling: '{query}'...")
    try:
        results = DDGS().text(query, max_results=4)
        # We combine the top 4 search snippets into a single text block for the AI to read
        search_data = "\n\n".join([f"Title: {r['title']}\nSnippet: {r['body']}\nLink: {r['href']}" for r in results])
        return search_data
    except Exception as e:
        return f"Search Error: {str(e)}"

# --- TOOL 1: SELLER MODE (Check Value) ---
def check_market_price(item_name: str):
    """
    SELLER TOOL: Finds the average used price of an item.
    """
    # We search for "used price" specifically to avoid new retail prices
    search_query = f"current used price of {item_name} ebay facebook marketplace"
    raw_data = real_web_search(search_query)
    return raw_data

# --- TOOL 2: BUYER MODE (Recommendations) ---
def search_similar_products(product_query: str):
    """
    BUYER TOOL: Finds the best products and prices for a buyer.
    """
    # We search for "best [item] reviews price" to get comparisons
    search_query = f"best {product_query} review price comparison 2024"
    raw_data = real_web_search(search_query)
    return raw_data

# 3. Initialize the Autonomous Model
tools = [check_market_price, search_similar_products]

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=tools,
    system_instruction="""
    You are 'Auto-Haggle', an Intelligent Commerce Agent.
    You have access to Real-Time Web Search.

    MODE 1: SELLER ASSISTANT (Protecting the User)
    If the user is SELLING an item:
    1. Use 'check_market_price' to search for the REAL used market value.
    2. Read the search snippets to calculate an estimated average price.
    3. If the buyer's offer is < 80% of that average -> ROAST THEM.
    4. If the offer is fair -> Accept.
    
    MODE 2: BUYER ASSISTANT (Helping the User Buy)
    If the user wants to BUY something:
    1. Use 'search_similar_products' to find real options.
    2. Read the search snippets to identify 3 distinct options (Budget, Best Overall, Premium).
    3. Output a structured recommendation:
       - **Product Name** | **Approx Price** | **Why it's good**
    4. Recommend the best one for the user's specific needs.

    CRITICAL: The tool returns raw search text. YOU must parse it to find the dollar amounts.
    """
)

# 4. The Chat Loop
def start_agent():
    print("--------------------------------------------------")
    print("🤖 AUTO-HAGGLE AGENT (Connected to Internet)")
    print("--------------------------------------------------")
    
    # Enable automatic tool use (Agent Mode)
    chat = model.start_chat(enable_automatic_function_calling=True)
    
    while True:
        user_input = input("\n👤 YOU: ")
        if user_input.lower() in ["quit", "exit"]:
            break
            
        print("🤖 AGENT THINKING...", end="", flush=True)
        
        try:
            response = chat.send_message(user_input)
            print(f"\r🤖 AGENT: {response.text}")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    start_agent()