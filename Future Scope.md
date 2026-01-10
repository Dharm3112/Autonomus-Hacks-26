## 🔮 Future Scope & Scalability

While the current MVP demonstrates the core autonomous loop, the vision for **Auto-Haggle** extends into a full-scale commerce automation platform.

### 1. 📱 True Platform Integration (The "Ghost" Layer)
* **Current:** User types text into the terminal.
* **Future:** Build a **Chrome Extension** or **Android Overlay** that injects the Agent directly into Facebook Marketplace and WhatsApp Web. The Agent will read incoming messages from the DOM and draft replies automatically, requiring only a "One-Click Approve" from the user.

### 2. 📸 Multimodal "Vision" Analysis
* **Current:** Text-only negotiation.
* **Future:** Integrate **Gemini 1.5 Pro Vision**. Users will upload a screenshot of the chat or a photo of the item. The Agent will detect:
    * **Item Condition:** "This scratch lowers value by 20%."
    * **Buyer Sentiment:** Analyze screenshots of profiles to detect potential scammers or serious buyers.

### 3. 🎙️ Real-Time Voice Negotiation
* **Current:** Text-based roasting.
* **Future:** Use **Gemini Live (Audio-to-Audio)** to handle phone calls. The Agent could screen calls from Craigslist buyers, negotiate the price verbally using a synthesized voice, and only forward the call to the human when the deal is closed.

### 4. 🧠 "Good Cop, Bad Cop" Multi-Agent Mode
* **Current:** Single Agent ("The Closer").
* **Future:** Deploy two agents simultaneously.
    * **Agent A (Manager):** Analyzes the deal stats and sets the floor price.
    * **Agent B (Negotiator):** Talks to the customer.
    * If Agent B gets stuck, it can "consult" Agent A ("Let me check with my manager...") to create artificial scarcity and pressure.

### 5. 🔌 Live Market APIs
* **Current:** Mock database for demonstration.
* **Future:** Integrate **eBay Sell API** and **Kelley Blue Book API**. The tool will pull the *exact* average sold price for the last 30 days in the user's specific zip code to ensure zero money is left on the table.

```
