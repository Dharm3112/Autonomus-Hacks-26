import streamlit as st
import os
import google.generativeai as genai
from duckduckgo_search import DDGS
from dotenv import load_dotenv
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Auto-Haggle (Live)",
    page_icon="⚡",
    layout="centered"
)

# --- SETUP ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ Google API Key missing. Please check .env")
    st.stop()

# ⚠️ DISABLE SAFETY FILTERS (To allow all search results)
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

genai.configure(api_key=api_key)

# --- 🌐 THE REAL SEARCH TOOL (No Mock Data) ---
def real_web_search(query: str):
    """
    Performs a 100% REAL web search. 
    No hardcoded fallbacks. No fake data.
    """
    print(f"\n🔎 EXECUTION: Searching Internet for: '{query}'")
    
    with st.status(f"🌐 Searching live web for: '{query}'...", expanded=False) as status:
        try:
            # 1. We ask DuckDuckGo for real results
            # max_results=5 gives us a good breadth of live data
            results = DDGS().text(query, max_results=5)
            
            # 2. Check if we actually got data
            if not results:
                status.update(label="❌ No results found online.", state="error")
                return "SEARCH_RESULT: No data found on the web for this specific query."
            
            # 3. Format the raw data for the AI
            # We include the Link so the AI can prove it's real
            formatted_results = ""
            for r in results:
                formatted_results += f"Title: {r['title']}\nSnippet: {r['body']}\nSource: {r['href']}\n\n"
            
            status.update(label="✅ Found Live Data!", state="complete", expanded=False)
            return formatted_results

        except Exception as e:
            status.update(label="❌ Connection Error", state="error")
            return f"SEARCH_ERROR: Could not connect to search engine. Error: {str(e)}"

# --- TOOL DEFINITIONS ---
def check_market_price(item_name: str):
    # Search for the specific used item
    return real_web_search(f"current used price of {item_name} ebay")

def search_similar_products(product_query: str):
    # Search for exactly what the user asked + "review price"
    return real_web_search(f"best {product_query} price review 2025")

tools = [check_market_price, search_similar_products]

# --- MODEL ---
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=tools,
    safety_settings=safety_settings,
    system_instruction="""
    You are Auto-Haggle. You have access to a LIVE web search tool.
    
    CRITICAL INSTRUCTIONS:
    1. USE THE TOOL DATA. The text provided by the tool is the TRUTH.
    2. Do not use your internal training knowledge if the tool gives you data.
    3. If the tool finds a "weird" item, talk about that weird item.
    4. Provide the EXACT prices found in the snippets.
    
    OUTPUT FORMAT FOR RECOMMENDATIONS:
    Create a markdown table:
    | Product Name | Price Found | Key Feature |
    |--------------|-------------|-------------|
    """
)

# --- UI ---
st.title("⚡ Auto-Haggle: Live Search")
st.caption("Searching the real internet. No pre-canned answers.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(enable_automatic_function_calling=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Search for ANYTHING (e.g. 'Pink Gaming Chair')..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = st.session_state.chat_session.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")