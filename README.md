========================================================================
                       CLASH OF MINDS [LOCAL]
                 Vibe Coded in Antigravity for the Win
========================================================================

## ⚡ OVERVIEW
Clash of Minds is a local, AI-powered debate arena designed to simulate 
intense philosophical and logical battles between opposing viewpoints. 

Built specifically to prep for high-stakes debate competitions, this tool 
allows you to spectate as two AI personalities tear apart and reconstruct 
arguments in real-time. 

No cloud. No lag. Just pure local compute and dialectics.

## 🚀 FEATURES
* **Dual Personas:**
    * **Alex (The Optimist 🚀):** Sees the potential, the growth, and the light.
    * **Sam (The Skeptic 🛡️):** Sees the risks, the history, and the flaws.
* **Autonomous Mode:** Let the AI choose its own stance without bias.
* **Local Privacy:** Runs entirely on your machine using Ollama.
* **Debate History:** Automatically saves transcripts to JSON for review.
* **Dark Mode UI:** "Vibe coded" aesthetic with custom CSS for maximum focus.

## 🛠️ PREREQUISITES
To run this antigravity engine, you need:

1.  **Python 3.8+** installed.
2.  **Ollama** installed and running locally.
    * Download at: https://ollama.com/
    * You must pull a model first. The app defaults to `llama3.2`.
    * Run this in your terminal: `ollama pull llama3.2`

## 📦 INSTALLATION

1.  **Unzip/Clone the project.**

2.  **Install Python Dependencies:**
    Open your terminal in the project folder and run:
    pip install -r requirements.txt

    (Note: This installs 'streamlit' and 'ollama')

## 🎮 HOW TO RUN

1.  **Start Ollama:**
    Ensure Ollama is running in the background (usually `ollama serve` in a 
    separate terminal, or via the desktop app).

2.  **Ignite the App:**
    Run the following command:
    streamlit run app.py

3.  **Debate:**
    * Enter a topic (e.g., "Is AI dangerous?", "Universal Basic Income").
    * Choose your style (Natural vs. Bullet Points).
    * Click "Ignite Debate" and watch the sparks fly.

## 📂 FILE STRUCTURE
* `app.py` - The brain of the operation (Streamlit UI + Logic).
* `requirements.txt` - The fuel (Dependencies).
* `debate_history.json` - The archives (Past debates are stored here).

## 💡 PRO TIPS FOR THE COMPETITION
* **Review the Transcripts:** Use the "Debate History" sidebar to read 
    past arguments. The AI often brings up obscure counter-points you 
    might miss.
* **Switch Models:** You can change the model name in the sidebar if 
    you want to test against `mistral`, `gemma`, or `llama3`.
* **Style Toggle:** Use "Bullet Points" mode if you need to quickly 
    extract arguments for your own notes.

========================================================================
                "If you can't code it, you can't debate it."
========================================================================
