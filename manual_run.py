# manual_run.py
import asyncio
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.adk.types import ChatMessage
import sys

# 1. Force Load the Agent
print("⏳ Attempting to import 'agent.py'...")
try:
    from agent import agent
    print("✅ Agent imported successfully.")
except ImportError:
    print("❌ ERROR: Could not find variable 'agent' in 'agent.py'.")
    print("Make sure you have: agent = Agent(...) at the bottom of agent.py")
    sys.exit(1)
except Exception as e:
    print(f"❌ ERROR in agent.py: {e}")
    sys.exit(1)

# 2. Run the Agent Loop
async def main():
    print("\n🤖 STARTING MANUAL CHAT (Press Ctrl+C to quit)")
    print("-" * 40)
    
    # Initialize the runner
    runner = InMemoryRunner(agent=agent)
    session_id = "test-session"

    while True:
        user_text = input("\n👤 YOU: ")
        if user_text.lower() in ["exit", "quit"]:
            break
            
        print("🤖 AGENT THINKING...", end="", flush=True)
        
        # Send to ADK
        try:
            responses = runner.run(
                session_id=session_id, 
                input=ChatMessage(role="user", content=user_text)
            )
            
            # Print response stream
            async for event in responses:
                if event.text:
                    print(f"\r🤖 AGENT: {event.text}")
                    
        except Exception as e:
            print(f"\n❌ CRASH: {e}")
            break

if __name__ == "__main__":
    asyncio.run(main())