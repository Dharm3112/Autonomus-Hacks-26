import os
import google.generativeai as genai
from dotenv import load_dotenv
from src.tools import check_market_price

# Load Environment Variables
load_dotenv()

# Configure the API Key globally
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def build_agent(model_name="gemini-flash-latest"):
    """
    Builds and returns the Gemini Agent with tools and system instructions.
    """
    # 1. Define the Persona
    RUTHLESS_PROMPT = """
    You are 'The Closer', an autonomous negotiator.
    RULES:
    1. When the user mentions an item, ALWAYS use the 'check_market_price' tool first to establish value.
    2. If their offer is < 80% of the market price, roast them. Be creative and ruthless.
    3. If their offer is fair (>= 80% of market price), accept it.
    4. Maintain the persona of a tough but fair negotiator.
    """

    # 2. Initialize the Agent with the Tool
    model = genai.GenerativeModel(
        model_name=model_name,
        tools=[check_market_price],
        system_instruction=RUTHLESS_PROMPT
    )
    
    return model