import streamlit as st
from modules.medqa import load_medquad_data, get_medical_answer
from modules import analytics, sentiment
from modules.llm import get_llm_response  # 🆕 Added

# App setup
st.set_page_config(page_title="Medical Chatbot", page_icon="🩺")
st.title("MedQuAD-Powered Medical Chatbot")

# Load MedQuAD data and embeddings once
if "medquad_data" not in st.session_state:
    with st.spinner("Loading MedQuAD data..."):
        data, embeddings = load_medquad_data()
        st.session_state.medquad_data = data
        st.session_state.medquad_embeddings = embeddings

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input
user_input = st.chat_input("Ask a medical question...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    # Try MedQuAD first
    response = get_medical_answer(
        user_input,
        st.session_state.medquad_data,
        st.session_state.medquad_embeddings
    )

    # If MedQuAD has no match, use LLaMA
    if response.startswith("❌"):
        st.info("🤖 MedQuAD has no match. Generating answer with LLaMA 3...")
        response = get_llm_response(user_input)

    # Sentiment + analytics
    sentiment_result = sentiment.get_sentiment(user_input)
    analytics.log_interaction(user_input, response, sentiment_result)

    # Show bot response
    st.session_state.chat_history.append(("bot", response))

# Display chat history
for sender, message in st.session_state.chat_history:
    st.chat_message("user" if sender == "user" else "assistant").markdown(message)
