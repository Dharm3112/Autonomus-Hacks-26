import streamlit as st
from PIL import Image
from agent import HaggleAgent
import pyperclip

# Page Setup
st.set_page_config(page_title="Auto-Haggle 2.0", page_icon="💸", layout="centered")
st.title("💸 Auto-Haggle 2.0")
st.caption("Upload a screenshot. Let AI negotiate the deal.")

# Initialize Agent
if "agent" not in st.session_state:
    st.session_state.agent = HaggleAgent()

# --- SIDEBAR: CONTROLS ---
with st.sidebar:
    st.header("🧠 Strategy")
    persona = st.radio("Negotiator Personality:", 
        ["The Closer (Ruthless)", "Grandma Sue (Polite)", "Desperate Seller (Quick Sale)"])
    
    st.divider()
    
    st.header("📝 Secret Context")
    secret_note = st.text_area("Tell the bot something...", 
        placeholder="e.g., 'The screen is cracked' or 'I need cash tonight'")

# --- MAIN UI ---
st.subheader("1. Upload Chat Screenshot 📸")
uploaded_file = st.file_uploader("Drop your Facebook Marketplace chat here", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    # Open and display image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Chat", use_column_width=True)
    
    st.subheader("2. Generate Response 🚀")
    
    if st.button("Analyze & Reply", type="primary"):
        # THE THINKING UI (The "Trust" Builder)
        with st.status("🤖 AI is thinking...", expanded=True) as status:
            st.write("👀 Reading text from screenshot...")
            st.write("🔎 Googling current market prices...")
            st.write(f"🎭 Adopting persona: {persona}...")
            
            # Call the Backend
            reply, sources = st.session_state.agent.analyze_negotiation(
                image, secret_note, persona
            )
            
            status.update(label="✅ Strategy Found!", state="complete", expanded=False)
            
        # Display Result
        st.success("Draft Reply Generated:")
        st.text_area("Copy this:", value=reply, height=150, key="final_output")
        
        if sources:
            st.caption(sources[0])

        if st.button("📋 Copy to Clipboard"):
            pyperclip.copy(reply)
            st.toast("Copied! Go get that money!")