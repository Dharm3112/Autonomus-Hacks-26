# 🤖 Auto-Haggle: The Autonomous Negotiation Agent
> **Hackathon 2026 Submission** | *Reclaiming your time from low-ballers.*

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Gemini](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-orange)
![Status](https://img.shields.io/badge/Status-Autonomous-green)

## 💡 The Problem
Selling used items online (Facebook Marketplace, Craigslist, eBay) is a nightmare.
* **Time Sink:** Answering "Is this available?" 50 times a day.
* **Emotional Tax:** Dealing with rude low-ballers and scammers.
* **Information Asymmetry:** Not knowing the real-time market value of what you are selling.

## 🚀 The Solution
**Auto-Haggle** is an autonomous AI agent that lives in your terminal. It doesn't just chat; it **thinks, researches, and negotiates** for you.

Instead of a standard chatbot, it uses an **Agentic Loop**:
1.  **Perceives** the buyer's offer.
2.  **Tools** used to check real-time market prices (mocked for demo).
3.  **Decides** if the offer is fair or an insult.
4.  **Acts** by accepting, rejecting, or roasting the buyer autonomously.

## ✨ Key Features

### 🧠 1. Autonomous Market Valuation (Tool Use)
The agent doesn't guess prices. When a buyer mentions an item (e.g., "PS5"), the agent triggers a custom Python tool `check_market_price()` to look up the real-time average value before responding.

### 🎭 2. Ruthless Persona Engine
Configured with a "The Closer" system prompt. It detects low-ball offers (<80% value) and generates sarcastic, high-context "roasts" to shut them down, or negotiates firmly if the price is close.

### 🔄 3. Auto-Negotiation Loop
The agent maintains context of the conversation. It handles the entire lifecycle:
* **Inquiry:** "Is this available?" -> "Yes, $200 firm."
* **Low-ball:** "I have $50." -> *[Checks Market: $200]* -> "Get real."
* **Close:** "Okay $190." -> "Deal."

## 🛠️ Tech Stack
* **Core Logic:** Python 3.11
* **AI Model:** Google Gemini 1.5 Flash (via `google-generativeai`)
* **Agent Framework:** Native Automatic Function Calling (Tool Use)
* **Environment:** Dotenv for secure key management

## ⚡ Quick Start

### 1. Clone & Install
```bash
git clone [https://github.com/yourusername/auto-haggle.git](https://github.com/yourusername/auto-haggle.git)
cd auto-haggle
pip install -r requirements.txt

```

### 2. Configure Keys

Create a `.env` file in the root directory:

```ini
GOOGLE_API_KEY=your_gemini_api_key_here

```

### 3. Run the Agent

```bash
python agent_run.py

```

## 🎮 Demo Scenarios

Try typing these inputs to see the Agent in action:

| User Input | Agent Action | Expected Result |
| --- | --- | --- |
| *"I'll give you $100 for that PS5."* | **Tool Call:** `check_market_price('ps5')` | Finds price is $450. **Roasts user.** |
| *"I can do $380 for the PS5."* | **Tool Call:** `check_market_price('ps5')` | Finds price is $450. **Negotiates.** |
| *"Is the iPhone still available?"* | **Tool Call:** `check_market_price('iphone')` | Finds price is $500. **Responds with stats.** |

---

*Built with ❤️ for Autonomous Hack 2026*

```

```
