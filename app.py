import streamlit as st
import pyperclip
import asyncio
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.adk.types import ChatMessage
from src.agent import build_agent

# Load Environment
load_dotenv()

# Page Setup
st.set_page_config(page_title="Auto-Haggle (ADK)", layout="wide")
st.title("🤖 Auto-Haggle: Powered by ADK")

# Initialize ADK Agent in Session State
if "runner" not in st.session_state:
    with st.spinner("Initializing Agent Development Kit..."):
        agent = build_agent()
        # InMemoryRunner runs the agent locally within the Python process
        st.session_state.runner = InMemoryRunner(agent=agent)
        st.session_state.session_id = "hackathon-session-01"
        st.success("ADK Agent Online")

# Sidebar
with st.sidebar:
    st.header("ADK Controls")
    if st.button("Reset Session"):
        st.session_state.runner.reset_session(st.session_state.session_id)
        st.toast("Memory Wiped!")

# Helper: Async Wrapper for Streamlit
async def query_adk(user_text):
    """Sends text to the ADK Runner and awaits response."""
    response_text = ""
    # ADK runners are async
    async for event in st.session_state.runner.run(
        session_id=st.session_state.session_id,
        input=ChatMessage(role="user", content=user_text)
    ):
        # Capture the final text output from the agent
        if event.text:
            response_text += event.text
            
    return response_text

# UI Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Incoming Low-Ball")
    if st.button("Paste Clipboard"):
        st.session_state.user_input = pyperclip.paste()
    
    user_input = st.text_area("Buyer Message:", value=st.session_state.get("user_input", ""), height=200)

with col2:
    st.subheader("📤 ADK Response")
    if st.button("Generate Roast", type="primary"):
        if user_input:
            with st.spinner("ADK Agent Reasoning..."):
                # Run the Async loop
                reply = asyncio.run(query_adk(user_input))
                st.session_state.ai_reply = reply
        else:
            st.warning("Input required.")
            
    final_reply = st.text_area("Agent Output:", value=st.session_state.get("ai_reply", ""), height=200)
    
    if st.button("Copy Output"):
        pyperclip.copy(final_reply)
        st.toast("Copied!")