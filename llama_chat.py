# chatbot_app/llama_chat.py

import streamlit as st
import requests

# --- LLaMA 3 Helper ---
def get_llama_response(prompt):
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        })
        return response.json()["response"].strip()
    except Exception as e:
        return f"⚠️ Error calling LLaMA 3: {e}"

# --- Streamlit App ---
st.set_page_config(page_title="LLaMA Chat", page_icon="🦙")
st.title("🦙 LLaMA 3 Local Chatbot (via Ollama)")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask anything...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.spinner("Thinking..."):
        bot_response = get_llama_response(user_input)
    st.session_state.chat_history.append(("bot", bot_response))

# Display chat history
for sender, msg in st.session_state.chat_history:
    st.chat_message("user" if sender == "user" else "assistant").write(msg)
