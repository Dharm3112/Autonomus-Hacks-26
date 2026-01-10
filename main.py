import asyncio
import sys
from google.adk.runners import InMemoryRunner
from google.adk.types import ChatMessage
from src.agent import build_agent

async def main():
    # Fix for Windows encoding issues
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    print("🤖 AGENT ONLINE (ADK Powered). Type 'quit' to exit.")
    
    # Initialize the agent and runner
    agent = build_agent()
    runner = InMemoryRunner(agent=agent)
    session_id = "cli_session_01"

    while True:
        # Get user input
        try:
            user_in = input("\n👤 YOU: ")
        except EOFError:
            break
            
        if user_in.lower() in ["quit", "exit"]:
            break
        
        print("🤖 AGENT: ", end="", flush=True)
        
        # Run the agent via ADK runner
        async for event in runner.run(
            session_id=session_id,
            input=ChatMessage(role="user", content=user_in)
        ):
            if event.text:
                print(event.text, end="", flush=True)
        
        print() # Newline after response

if __name__ == "__main__":
    # Windows SelectorEventLoop policy fix for some environments if needed, 
    # but usually standard run works.
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(main())