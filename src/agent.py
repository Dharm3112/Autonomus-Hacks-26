import os
from google.adk.agents import Agent
from google.adk.model import Model
from google.adk.types import ModelType
from dotenv import load_dotenv

load_dotenv()

# 1. Define Tool
def check_market_price(item_name: str) -> str:
    return f"Market Value for {item_name}: $200. Demand: High."

# 2. Define Agent (NAMED 'agent')
agent = Agent(
    name="Auto-Haggle-Bot",
    instruction="You are a ruthless negotiation agent.",
    model=Model(
        type=ModelType.GEMINI,
        name="gemini-1.5-flash"
    ),
    tools=[check_market_price]
)