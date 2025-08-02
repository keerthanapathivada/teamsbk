import streamlit as st
import requests

# --- Page Configuration ---
st.set_page_config(page_title="Chat with StudyMate", layout="wide")

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! I'm StudyMate, your AI learning assistant. What would you like to learn about today?"
        }
    ]

# --- Main App Interface ---
st.title("💬 Chat with StudyMate")
st.write("Have a conversation with your AI assistant. Ask questions, request explanations, or generate practice content.")

st.markdown("---")

# --- AI Response Function ---
def generate_ai_response(prompt):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except KeyError:
        st.error("API key not found. Please add your GEMINI_API_KEY to your .streamlit/secrets.toml file.")
        return "I can't connect to the AI without a valid API key."

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

    full_prompt = (
        f"You are StudyMate, an AI assistant. Your goal is to provide helpful, detailed, and conversational answers "
        f"to user questions. Respond based on your general knowledge without referencing any document content.\n\n"
        f"*User Question:*\n{prompt}"
    )

    payload = {
        "contents": [{"role": "user", "parts": [{"text": full_prompt}]}],
        "generationConfig": {
            "responseMimeType": "text/plain"
        }
    }

    try:
        response = requests.post(api_url, json=payload, timeout=60)
        response.raise_for_status()  # Raise an error for 4xx and 5xx responses
        response_data = response.json()
        return response_data["candidates"][0]["content"]["parts"][0]["text"]
    except requests.exceptions.HTTPError as e:
        return f"An API error occurred: {e.response.status_code} - {e.response.text}"
    except requests.exceptions.RequestException as e:
        return f"An unexpected error occurred: {e}"

st.markdown("---")

# --- Chat Interface ---

def reset_chat_history():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! I'm StudyMate, your AI learning assistant. What would you like to learn about today?"
        }
    ]
    st.experimental_rerun()

st.button("Clear Chat", on_click=reset_chat_history)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("StudyMate is typing..."):
        ai_response = generate_ai_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        with st.chat_message("assistant"):
            st.markdown(ai_response)