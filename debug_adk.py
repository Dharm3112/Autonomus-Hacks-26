# debug_adk.py
import os
import sys

print("🔍 1. Checking File Existence...")
if not os.path.exists("agent.py"):
    print("❌ FATAL: agent.py not found in this folder!")
    sys.exit(1)
print("✅ agent.py found.")

print("\n🔍 2. Checking Variable Name...")
try:
    from agent import agent
    print("✅ Found variable 'agent' successfully!")
except ImportError:
    print("❌ FATAL: Could not import 'agent'. Did you name the variable 'agent = Agent(...)'?")
except Exception as e:
    print(f"❌ FATAL: Your code has a syntax error: {e}")
    sys.exit(1)

print("\n🔍 3. Attempting to Launch...")
print("Run this command exactly:")
print("python -m google.adk.cli web .")