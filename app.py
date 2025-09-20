import streamlit as st
from src.styles import CUSTOM_CSS
from src.session_state import initialize_session_state
from src.ui import render_sidebar, render_main_interface
from src.groq_client import summarize, get_title_for_chat
from src.config import MODEL_MAP
from utils.helpers import get_current_chat, create_new_chat

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Simplify",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLING ---
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# --- SESSION STATE ---
initialize_session_state()

# --- SIDEBAR ---
domain, tone, output_format, min_len, max_len, req_keywords_input, model_friendly_name, creativity = render_sidebar()

# --- MAIN INTERFACE ---
current_chat = get_current_chat()
render_main_interface(current_chat)

# --- CHAT INPUT AND SUMMARIZATION LOGIC ---
if prompt := st.chat_input("Simplify your text..."):
    if not current_chat:
        create_new_chat()
        current_chat = get_current_chat()
    
    current_chat["messages"].append({"role": "user", "content": prompt})
    
    summary_settings = {
        "domain": domain, 
        "tone": tone, 
        "format": output_format, 
        "min_len": min_len, 
        "max_len": max_len, 
        "keywords": [k.strip() for k in req_keywords_input.split(',') if k.strip()], 
        "model": MODEL_MAP[model_friendly_name], 
        "creativity": creativity
    }
    
    with st.spinner("✨ Simplifying..."):
        summary = summarize(prompt, summary_settings)
        if summary:
            if len(current_chat["messages"]) == 1:
                current_chat["title"] = get_title_for_chat(summary)
            
            current_chat["messages"].append({"role": "assistant", "content": summary})
            st.rerun()
