# 💼 Negotio.ai
### The Autonomous Commerce & Negotiation Engine
**"Don't leave money on the table. Let AI handle the deal."**

---

## 📖 Project Overview
**Negotio.ai** is an intelligent autonomous agent built for the **Autonomous Hack 2026**. It solves the "Dead Capital" crisis—where millions of dollars in used goods sit in closets because selling them is too stressful and time-consuming.

Unlike standard chatbots, Negotio.ai is **goal-oriented**. It doesn't just chat; it actively performs work. It scouts the live web to find real-time market valuations and acts as a ruthless negotiation coach, generating data-backed counter-offers to maximize seller profit.

### 🌟 Why It's Unique
1.  **Dual-Mode Brain:** Instantly switches between "Market Researcher" (finding data) and "Negotiation Coach" (closing deals).
2.  **Live Internet Access:** Uses `duckduckgo-search` to find *actual* 2025 pricing, not outdated training data.
3.  **Self-Healing Architecture:** Features a "Silent Failover" system that ensures the demo never crashes, even if the search API is rate-limited.
4.  **Assertive Persona:** Engineered to be opinionated and decisive, acting like a Senior Consultant rather than a passive assistant.

---

## 🚀 Key Features

### 🕵️‍♂️ Mode 1: The Researcher
* **Real-Time Valuation:** Scrapes eBay and forums to find the true "sold" price of any item.
* **Comparison Tables:** Automatically generates Markdown tables comparing models, prices, and features.
* **Verdict Engine:** Doesn't just list options; picks a "Winner" and tells you why.

### 💼 Mode 2: The Negotiator
* **Lowball Detection:** Instantly flags offers that are under market value.
* **Script Generation:** Writes professional, firm, and data-backed replies for you to copy-paste to buyers.
* **Psychological Edge:** Uses price anchoring tactics to protect your profit margins.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (Custom CSS for Dark "SaaS" UI)
* **Core Intelligence:** [Google Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/) (Low latency, High reasoning)
* **Tools:** `duckduckgo-search` (Live Web Access)
* **Backend:** Pure Python 3.13
* **State Management:** `st.session_state` (Persistent Chat History)

---

## ⚙️ Installation & Setup

Follow these steps to run Negotio.ai locally.

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/negotio-ai.git](https://github.com/yourusername/negotio-ai.git)
cd negotio-ai

```

### 2. Install Dependencies

```bash
pip install streamlit google-generativeai duckduckgo-search python-dotenv

```

### 3. Configure API Key

Create a `.env` file in the root directory and add your Google Gemini API key:

```env
GOOGLE_API_KEY=your_api_key_here

```

### 4. Run the Application

```bash
streamlit run app.py

```

---

## 💡 How to Use

### Scene 1: Buying (Research)

**User:** *"What is the best laptop for coding under $800?"*
**Negotio:** Scours the web for 2025 reviews, creates a comparison table of the MacBook Air M1 vs. Dell XPS, and gives a final recommendation.

### Scene 2: Selling (Negotiation)

**User:** *"I am selling my iPhone 13. Someone offered me $300."*
**Negotio:** > "⚠️ **Stop.** Do not accept that.

> Real Market Value: **$450 - $500**
> Offer Received: **$300** (Lowball)
> **Suggested Reply:**
> 'Hi, thanks for the offer. I checked current sales and these are going for $450+. I can meet you at $425, but $300 is too low.'"

---

## 🧩 System Architecture

    A[User Input] --> B{Intent Detection}
    B -->|Research| C[DuckDuckGo Search Tool]
    B -->|Negotiate| D[Market Price Check]
    C --> E[Raw HTML/Snippets]
    D --> E
    E --> F[Gemini 1.5 Flash (Analysis)]
    F --> G[Structured Response (Table/Script)]
    G --> H[Streamlit UI]


---

## 🔮 Future Roadmap

* **WhatsApp Integration:** Allow Negotio to reply to buyers directly on your behalf.
* **Image Vision:** Upload a photo of a garage sale item, and Negotio identifies it and prices it instantly.
* **sniper Mode:** Automatically find underpriced items on eBay for arbitrage.

---

## 🏆 Hackathon Status

**Submission for:** Autonomous Hacks 2026
**Status:** MVP Complete (v1.0)

---

**Made with ❤️ by Pair Programmers**

```
