import streamlit as st
from mistralai import Mistral
import os

# Set your API Key
api_key = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=api_key)

st.title("🤖 Mistral Customer Support")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        # Simplified call to your mistral function
        chat_response = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        full_response = chat_response.choices[0].message.content
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})