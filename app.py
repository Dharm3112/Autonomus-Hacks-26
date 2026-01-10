import streamlit as st
import pyperclip
import asyncio
from dotenv import load_dotenv
from src.agent import build_agent
import time

# Load Environment
load_dotenv()

# Page Setup
st.set_page_config(page_title="Auto-Haggle Ultra", page_icon="🤖", layout="wide")

# Custom CSS for Premium Feel
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FF914D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);
    }
    
    /* Text Areas */
    .stTextArea > div > div > textarea {
        background-color: #262730;
        border: 1px solid #4B4B4B;
        border-radius: 8px;
        color: #FAFAFA;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: #FF4B4B;
        box-shadow: 0 0 0 1px #FF4B4B;
    }
    
    /* Metric Cards (fake) */
    .metric-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF4B4B;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Main Title with Animation
st.title("🤖 Auto-Haggle Ultra")
st.caption("The AI-Powered Lowball Annihilation Tool")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Persona Selector
    current_persona = st.session_state.get("persona", "The Closer")
    selected_persona = st.selectbox(
        "Negotiator Persona", 
        ["The Closer", "The Diplomat", "The Roastmaster"],
        index=["The Closer", "The Diplomat", "The Roastmaster"].index(current_persona)
    )
    
    # Check if persona changed to rebuild agent
    if selected_persona != st.session_state.get("persona", ""):
        st.session_state.persona = selected_persona
        # Force agent rebuild
        if "chat_session" in st.session_state:
            del st.session_state.chat_session
    
    st.divider()
    
    st.info(f"**Current Mode:** {selected_persona}")
    if selected_persona == "The Closer":
        st.markdown("*Ruthless. Efficient. Takes no prisoners.*")
    elif selected_persona == "The Diplomat":
        st.markdown("*Polite. Professional. Disappointed parent energy.*")
    elif selected_persona == "The Roastmaster":
        st.markdown("*Chaos. Memes. Emotional damage.*")

    st.divider()
    if st.button("Reset Memory", type="secondary"):
        st.session_state.pop("chat_session", None)
        st.session_state.pop("messages", None)
        st.toast("Brain scrubbed clean!", icon="🧠")

# Initialize Gemini Agent
if "chat_session" not in st.session_state:
    with st.spinner(f"Summoning {selected_persona}..."):
        try:
            agent = build_agent(persona=selected_persona)
            st.session_state.chat_session = agent.start_chat(enable_automatic_function_calling=True)
            st.session_state.messages = [] # Store chat history
            st.toast(f"{selected_persona} is Online", icon="🟢")
        except Exception as e:
            st.error(f"Failed to initialize agent: {e}")
            st.stop()

# Helper: Async Wrapper
async def query_agent(user_text):
    try:
        response = await st.session_state.chat_session.send_message_async(user_text)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Main UI Layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📥 The Low-Ball")
    
    # Clipboard Action
    if st.button("📋 Paste from Clipboard"):
        try:
            st.session_state.user_input = pyperclip.paste()
            st.toast("Pasted from clipboard")
        except:
            st.error("Clipboard access denied.")

    # Input Area
    user_input = st.text_area(
        "What did the buyer say?", 
        value=st.session_state.get("user_input", ""), 
        height=250,
        placeholder="e.g., 'Bro, cash in hand, $50 for the PS5 right now.'"
    )

with col2:
    st.markdown("### 📤 The Rebuttal")
    
    # Output Area placeholder
    output_container = st.empty()
    
    # Action Button
    start_btn = st.button("🚀 Generate Response", type="primary", use_container_width=True)
    
    if start_btn and user_input:
        with st.spinner("Analyzing market value... Constructing emotional damage..."):
            # Progress bar effect
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.005)
                progress_bar.progress(i + 1)
            progress_bar.empty()
            
            # Run Agent
            reply = asyncio.run(query_agent(user_input))
            
            # Save to history
            st.session_state.messages.append({"role": "user", "text": user_input})
            st.session_state.messages.append({"role": "agent", "text": reply})
            
            # Display
            output_container.markdown(f"""
            <div style="background-color: #262730; padding: 20px; border-radius: 10px; border: 1px solid #4B4B4B;">
                {reply}
            </div>
            """, unsafe_allow_html=True)
            
            # Update session state for copy button
            st.session_state.latest_reply = reply
    
    elif st.session_state.get("latest_reply"):
        # Show previous reply if exists and no new generation
        output_container.markdown(f"""
        <div style="background-color: #262730; padding: 20px; border-radius: 10px; border: 1px solid #4B4B4B;">
            {st.session_state.latest_reply}
        </div>
        """, unsafe_allow_html=True)

    # Copy Button
    if st.session_state.get("latest_reply"):
        if st.button("📋 Copy Response"):
            try:
                pyperclip.copy(st.session_state.latest_reply)
                st.toast("Response copied to clipboard!", icon="✅")
            except:
                st.warning("Clipboard write failed.")

# History Section
if st.session_state.get("messages"):
    with st.expander("📜 Negotiation History"):
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"**Buyer:** {msg['text']}")
            else:
                st.markdown(f"**You:** {msg['text']}")
                st.divider()