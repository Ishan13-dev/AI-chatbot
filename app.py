import os
import streamlit as st
from google import genai
from google.genai import types

# Configure Streamlit page
st.set_page_config(page_title="Alan AI Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Alan AI Chatbot")

# Retrieve API key from environment variable or Streamlit secrets
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.info("Please provide your Gemini API Key to start chatting.", icon="🔑")
    api_key = st.text_input("AQ.Ab8RN6KTjz7puSAZVAcCgbPRFM-gDuWSGyljhFrYqdzU1U1zkw", type="password")
    if not api_key:
        st.stop()

# Initialize Gemini Client
client = genai.Client(api_key=api_key)

# Initialize chat session history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input field
if prompt := st.chat_input("Ask anything..."):
    # Render user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare chat history format for Gemini API
    gemini_contents = []
    for m in st.session_state.messages:
        role = "user" if m["role"] == "user" else "model"
        gemini_contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=m["content"])]
            )
        )

    # Generate and stream response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            response_stream = client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=gemini_contents,
            )

            for chunk in response_stream:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Error communicating with Gemini API: {e}")
