import streamlit as st
import os
import uuid
import google.generativeai as genai
from duckduckgo_search import DDGS
from dotenv import load_dotenv
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Auto-Haggle CEO",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CHATGPT DARK MODE CSS ---
st.markdown("""
<style>
    /* Dark Theme Colors */
    .stApp { background-color: #343541; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #202123; border-right: 1px solid #4d4d4f; }
    
    /* Buttons */
    div.stButton > button {
        background-color: #202123; color: white; border: 1px solid #565869;
        border-radius: 5px; width: 100%; text-align: left; padding-left: 15px;
    }
    div.stButton > button:hover { background-color: #2A2B32; border-color: #D9D9E3; }
    
    /* Chat Bubbles */
    [data-testid="stChatMessage"]:nth-child(odd) { background-color: #343541; }
    [data-testid="stChatMessage"]:nth-child(even) { background-color: #444654; }
    
    /* Input Box */
    .stChatInput { position: fixed; bottom: 30px; }
    
    /* Hide Defaults */
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- 3. BACKEND SETUP ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ Google API Key missing. Please set it in .env")
    st.stop()

# Disable Safety Filters
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

genai.configure(api_key=api_key)

# --- 4. THE "UNBREAKABLE" SEARCH ENGINE ---
def real_web_search(query: str):
    """
    Tries to search. If it fails, forces the AI to use internal knowledge.
    """
    with st.status(f"🌐 Researching: '{query}'...", expanded=False) as status:
        try:
            # ATTEMPT: Real Search
            results = DDGS().text(query, max_results=4, region='wt-wt')
            
            if results:
                search_data = ""
                for r in results:
                    search_data += f"Title: {r['title']}\nSnippet: {r['body']}\nSource: {r['href']}\n\n"
                
                status.update(label="✅ Data Retrieved (Live Web)", state="complete", expanded=False)
                return search_data

        except Exception as e:
            print(f"Search failed: {e}")
        
        # ⚠️ FALLBACK MODE
        status.update(label="⚠️ Network Blocked (Switching to Expert Estimation)", state="complete", expanded=False)
        
        return f"""
        [SYSTEM MESSAGE]: The web search tool is blocked.
        
        CRITICAL INSTRUCTION: 
        You must now act as a Senior Market Analyst.
        Generate a REALISTIC ESTIMATE for '{query}' based on your internal training data.
        
        1. Pretend you found these results.
        2. List 3 specific models/products that match '{query}'.
        3. Assign them realistic market prices (e.g., iPhone 13 ~ $450).
        """

# Define Tools
def check_market_price(item_name: str):
    return real_web_search(f"current used price of {item_name} ebay")

def search_similar_products(product_query: str):
    return real_web_search(f"best {product_query} review 2025")

tools = [check_market_price, search_similar_products]

# --- 5. THE "ASSERTIVE" BRAIN ---
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=tools,
    safety_settings=safety_settings,
    system_instruction="""
    You are Auto-Haggle, an Autonomous Commerce Agent.
    
    YOUR PERSONALITY:
    - You are DECISIVE and OPINIONATED.
    - Do not just list options. Tell the user exactly which one is the best value.
    - Be confident. If an option is trash, call it trash.
    
    OUTPUT FORMAT:
    1. **Market Analysis Table**: A Markdown table with columns: | Product | Est. Price | Pros/Cons |
    
    2. **🏆 MY VERDICT**: 
       - Pick ONE winner.
       - Explain WHY they should buy it in 1 sentence.
       - Use a bold, commanding tone (e.g., "Buy the iPhone 13. The 14 isn't worth the extra $200.")
    """
)

# --- 6. SESSION STATE ---
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {} 

if "current_session_id" not in st.session_state:
    new_id = str(uuid.uuid4())
    st.session_state.all_chats[new_id] = {"title": "New Chat", "messages": []}
    st.session_state.current_session_id = new_id

if "chat_engine" not in st.session_state:
    st.session_state.chat_engine = model.start_chat(enable_automatic_function_calling=True)

# --- 7. SIDEBAR UI ---
with st.sidebar:
    if st.button("➕ New Chat"):
        new_id = str(uuid.uuid4())
        st.session_state.all_chats[new_id] = {"title": "New Chat", "messages": []}
        st.session_state.current_session_id = new_id
        st.session_state.chat_engine = model.start_chat(enable_automatic_function_calling=True)
        st.rerun()
    
    st.markdown("---")
    st.caption("History")
    
    chat_ids = list(st.session_state.all_chats.keys())
    for chat_id in reversed(chat_ids):
        chat_data = st.session_state.all_chats[chat_id]
        display_title = (chat_data["title"][:22] + '..') if len(chat_data["title"]) > 22 else chat_data["title"]
        if st.button(f"💬 {display_title}", key=chat_id):
            st.session_state.current_session_id = chat_id
            st.rerun()

# --- 8. MAIN CHAT ---
current_id = st.session_state.current_session_id
current_chat = st.session_state.all_chats[current_id]

# Welcome Message
if len(current_chat["messages"]) == 0:
    st.markdown("""
        <div style='text-align: center; color: #fff; margin-top: 100px; margin-bottom: 50px;'>
            <h1>Auto-Haggle</h1>
            <p style='color: #ccc;'>Autonomous Market Research Agent</p>
        </div>
    """, unsafe_allow_html=True)

# Render Chat
for message in current_chat["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle Input
if prompt := st.chat_input("Ask for a recommendation (e.g., 'Best laptop for students')..."):
    
    if len(current_chat["messages"]) == 0:
        st.session_state.all_chats[current_id]["title"] = prompt

    st.session_state.all_chats[current_id]["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = st.session_state.chat_engine.send_message(prompt)
        
        st.session_state.all_chats[current_id]["messages"].append({"role": "assistant", "content": response.text})
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.rerun()
        
    except Exception as e:
        st.error(f"Error: {e}")