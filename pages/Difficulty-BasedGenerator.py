import streamlit as st
import requests
import json
import fitz # PyMuPDF library for PDF text extraction

# --- Page Configuration ---
st.set_page_config(page_title="Difficulty-Based Test Generator", layout="wide")

st.title("🧠 Difficulty-Based Test Generator")
st.write("Choose your test level and let StudyMate create 5 questions for you from your document.")

# --- Session State Initialization ---
if 'document_content' not in st.session_state:
    st.session_state.document_content = None
if 'generated_questions' not in st.session_state:
    st.session_state.generated_questions = []

# --- Document Upload and Processing ---
st.subheader("1. Upload your Document")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    try:
        # Use PyMuPDF to read the PDF content
        pdf_bytes = uploaded_file.read()
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()

        if text:
            st.success("File uploaded and text extracted successfully!")
            st.session_state.document_content = text
        else:
            st.warning("The uploaded PDF appears to be empty or an image-based PDF (scanned document). "
                       "Please upload a text-based PDF.")
            st.session_state.document_content = None

    except Exception as e:
        st.error(f"An error occurred while processing the PDF: {e}")
        st.session_state.document_content = None
else:
    st.session_state.document_content = None
    st.session_state.generated_questions = []
    st.warning("Please upload a PDF to generate a quiz.")


# --- API Call Function ---
def call_gemini_api(document_content, difficulty):
    """
    Makes a call to the Gemini API to generate a list of questions in JSON format.
    """
    # Replace with your actual Gemini API key.
    # For a production app, use st.secrets or environment variables for security.
    api_key = "AIzaSyCC8s3-ZHZYWEtAhknKruPD6sCnVyaqBUs" 
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

    # Construct the full prompt based on the chosen difficulty
    prompt = (
        f"You are an AI quiz generator. Based on the following document content, "
        f"create a list of 5 questions that are appropriate for a '{difficulty}' difficulty level. "
        f"The output must be a valid JSON array of strings, where each string is a question.\n\n"
        f"Document Content:\n{document_content}"
    )

    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }

    try:
        response = requests.post(api_url, json=payload, timeout=30)
        response.raise_for_status()
        
        response_data = response.json()
        if "candidates" in response_data and response_data["candidates"]:
            json_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
            # The model might return a string with code block fences, so we strip them
            if json_text.startswith('json') and json_text.endswith(''):
                json_text = json_text.strip('` \njson')
            
            return json.loads(json_text)
        else:
            st.error("I'm sorry, I couldn't get a response from the API.")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while calling the Gemini API: {e}")
        return []
    except json.JSONDecodeError as e:
        st.error(f"Failed to parse JSON response from the API: {e}. Please try again.")
        return []
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return []


if st.session_state.get('document_content'):
    st.subheader("2. Choose Difficulty Level")
    difficulty = st.selectbox(
        "Select the difficulty for your test:",
        ("Easy", "Medium", "Hard")
    )

    if st.button("Generate Questions"):
        if not st.session_state.document_content:
            st.warning("Please upload a document first.")
        else:
            with st.spinner("Generating your test questions..."):
                questions = call_gemini_api(st.session_state.document_content, difficulty)
                if questions:
                    st.session_state.generated_questions = questions
                    st.success("Test questions generated!")

if st.session_state.generated_questions:
    st.subheader(f"Your Test Questions")
    for i, q in enumerate(st.session_state.generated_questions):
        st.markdown(f"{i+1}.** {q}")