import streamlit as st
import ollama
import time
import json
import os
from datetime import datetime

HISTORY_FILE = "debate_history.json"

# --- Configuration & Styles ---
st.set_page_config(
    page_title="Clash of Minds [Local]",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Force Dark Mode and Custom Styles
st.markdown(
    """
    <style>
    /* Force black background */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* Chat bubbles */
    .chat-bubble {
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        display: inline-block;
        max-width: 85%;
    }
    
    .idealist-bubble {
        background-color: #004d40; /* Dark Cyan/Teal */
        border: 1px solid #00bfa5;
        color: #e0f2f1;
        float: left;
        clear: both;
    }
    
    .skeptic-bubble {
        background-color: #3e2723; /* Dark Brown/Red */
        border: 1px solid #ff5722;
        color: #fbe9e7;
        float: right;
        clear: both;
        text-align: right;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background-color: #1e1e1e;
        color: #ffffff;
        border: 1px solid #333;
    }
    
    /* Button */
    .stButton > button {
        width: 100%;
        background-color: #6200ea;
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px;
    }
    .stButton > button:hover {
        background-color: #3700b3;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Logic & Helper Functions ---

def check_ollama_status():
    """Checks if Ollama is reachable."""
    try:
        # Simple list call to check connectivity
        ollama.list()
        return True
    except Exception:
        return False

def get_system_prompt(persona_type, style):
    """Returns the system prompt for the given persona and style."""
    
    style_instruction = ""
    if style == "Bullet Points":
        style_instruction = "Structure your response using clear bullet points. Keep it organized."
    else:
        style_instruction = "Use natural paragraphs and a conversational flow. Don't use bullet points."

    if persona_type == "Optimist":
        return (
            f"You are Alex. You are an optimist. Speak like a normal human in casual, easy language. "
            f"Keep sentences short and punchy. You believe everything will work out great. "
            f"Don't sound like a robot or an essay. Just chat naturally. "
            f"Support your arguments with real-life examples and logical proofs where possible. "
            f"{style_instruction} "
            f"Debate the given topic with Sam (the skeptic)."
        )
    elif persona_type == "Skeptic":
        return (
            f"You are Sam. You are a realist and a bit of a skeptic. Speak like a normal human in casual, easy language. "
            f"Keep sentences short. You are doubtful and look at the risks or history. "
            f"Don't sound like a robot or an essay. Just chat naturally. "
            f"Support your arguments with real-life examples and logical proofs where possible. "
            f"{style_instruction} "
            f"Debate the given topic with Alex (the optimist)."
        )
    elif persona_type == "Autonomous":
        return (
            f"You are a participant in a debate. You have your own free will and opinions. "
            f"Do not act like a specific character unless you want to. "
            f"Act as a neutral, unbiased human. Think critically but speak naturally. "
            f"Keep your responses short and concise. "
            f"Support your arguments with real-life examples and logical proofs where possible. "
            f"{style_instruction}"
        )
    return ""

def load_history():
    """Loads debate history from JSON file."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_debate(topic, transcript):
    """Saves the debate transcript to history."""
    history = load_history()
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "topic": topic,
        "transcript": transcript
    }
    history.append(entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def stream_response(model_name, messages, placeholder, persona_name, avatar):
    """
    Streams the response from Ollama to a Streamlit placeholder.
    Returns the full response text.
    """
    full_response = ""
    
    # Display initial loading state or header
    with placeholder.container():
        st.markdown(f"**{avatar} {persona_name}:**")
        text_area = st.empty()
    
    try:
        stream = ollama.chat(model=model_name, messages=messages, stream=True)
        
        for chunk in stream:
            content = chunk['message']['content']
            full_response += content
            text_area.markdown(full_response + "▌")
            
        text_area.markdown(full_response)
        return full_response
        
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# --- UI Layout ---

# Sidebar
with st.sidebar:
    st.header("Configuration")
    model_name = st.text_input("Model Name", value="llama3.2")
    debate_style = st.radio(
        "Debate Style",
        ("Natural Conversation", "Bullet Points"),
        index=0
    )
    persona_mode = st.radio(
        "Persona Mode",
        ("Fixed (Alex vs Sam)", "Autonomous (No Bias)"),
        index=0
    )
    
    st.divider()
    
    # History Viewer
    with st.expander("📜 Debate History"):
        history_data = load_history()
        if not history_data:
            st.info("No debates saved yet.")
        else:
            for i, entry in enumerate(reversed(history_data)):
                if st.button(f"{entry['timestamp']} - {entry['topic']}", key=f"hist_{i}"):
                    st.session_state.selected_debate = entry

    is_online = check_ollama_status()
    if is_online:
        st.success("🟢 Ollama Online")
    else:
        st.error("🔴 Ollama Offline")
        st.warning("Is Ollama running? Try `ollama serve` in your terminal.")

# Main Screen
st.title("⚡ Clash of Minds [Local]")
st.caption("A casual debate between two AI personalities.")

# Session State for Topic
if "topic" not in st.session_state:
    st.session_state.topic = ""

# Show History if selected
if "selected_debate" in st.session_state and st.session_state.selected_debate:
    entry = st.session_state.selected_debate
    st.info(f"Viewing Past Debate: {entry['topic']} ({entry['timestamp']})")
    st.markdown(entry['transcript'])
    if st.button("Close History"):
        del st.session_state.selected_debate
        st.rerun()
    st.stop() # Stop execution here to just show history

# New Debate Button
col1, col2 = st.columns([3, 1])
with col1:
    topic = st.text_input("Debate Topic", key="topic_input", placeholder="e.g., Is AI dangerous?")
with col2:
    if st.button("Start New Debate"):
        st.session_state.topic_input = "" # Clear input
        st.rerun()

if st.button("Ignite Debate"):
    if not is_online:
        st.error("Cannot start debate. Ollama is offline.")
    elif not topic:
        st.warning("Please enter a debate topic.")
    else:
        # Initialize Debate State
        full_transcript = ""
        last_response = ""
        
        st.divider()
        
        # 5 Rounds Loop
        for round_num in range(1, 6):
            st.subheader(f"Round {round_num}")
            
            # Determine Names and Prompts based on Mode
            if "Fixed" in persona_mode:
                name_a = "Alex (Optimist)"
                avatar_a = "🚀"
                prompt_a = get_system_prompt("Optimist", debate_style)
                
                name_b = "Sam (Skeptic)"
                avatar_b = "🛡️"
                prompt_b = get_system_prompt("Skeptic", debate_style)
            else:
                name_a = "Debater 1"
                avatar_a = "🗣️"
                prompt_a = get_system_prompt("Autonomous", debate_style)
                
                name_b = "Debater 2"
                avatar_b = "🤔"
                prompt_b = get_system_prompt("Autonomous", debate_style)

            # Create two columns for side-by-side debate
            col_a, col_b = st.columns(2)

            # --- Agent A ---
            msgs_a = [{'role': 'system', 'content': prompt_a}]
            
            if round_num == 1:
                msgs_a.append({'role': 'user', 'content': f"Topic: {topic}. Start the conversation. What do you think?"})
            else:
                msgs_a.append({'role': 'user', 'content': f"Topic: {topic}. {name_b} just said: '{last_response}'. Respond to {name_b}."})
            
            with col_a:
                ph_a = st.empty()
                resp_a = stream_response(model_name, msgs_a, ph_a, name_a, avatar_a)
            
            if resp_a:
                last_response = resp_a
                full_transcript += f"**{avatar_a} {name_a}:** {resp_a}\n\n"
            
            # --- Agent B ---
            msgs_b = [{'role': 'system', 'content': prompt_b}]
            msgs_b.append({'role': 'user', 'content': f"Topic: {topic}. {name_a} just said: '{last_response}'. Respond to {name_a}."})
            
            with col_b:
                ph_b = st.empty()
                resp_b = stream_response(model_name, msgs_b, ph_b, name_b, avatar_b)
            
            if resp_b:
                last_response = resp_b
                full_transcript += f"**{avatar_b} {name_b}:** {resp_b}\n\n"
            
            st.divider()

        st.success("Debate Concluded!")
        save_debate(topic, full_transcript)
        st.toast("Debate saved to history!")
