import asyncio
import sys
from src.agent import build_agent

async def main():
    # Fix for Windows encoding issues
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    print("🤖 AGENT ONLINE (Standard Mode). Type 'quit' to exit.")
    
    # Initialize the agent
    agent = build_agent()
    # Start a chat session (history is preserved automatically)
    chat = agent.start_chat(enable_automatic_function_calling=True)

    while True:
        # Get user input
        try:
            user_in = input("\n👤 YOU: ")
        except EOFError:
            break
            
        if user_in.lower() in ["quit", "exit"]:
            break
        
        print("🤖 AGENT: ", end="", flush=True)
        
        try:
            # Send message asynchronously
            response = await chat.send_message_async(user_in)
            if response.text:
                print(response.text)
        except Exception as e:
            print(f"\n[Error] {e}")
        
        print() 

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(main())