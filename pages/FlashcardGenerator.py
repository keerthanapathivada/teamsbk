import streamlit as st
import requests
import json
import time
import fitz # Import the PyMuPDF library

# --- Page Configuration ---
st.set_page_config(page_title="Flashcard Generator", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f7f9fb;
        font-family: 'Inter', sans-serif;
    }
    .main-header {
        color: #1e3a8a;
        font-weight: 700;
        text-align: center;
        padding-bottom: 1rem;
    }
    .secondary-header {
        color: #1f2937;
        font-weight: 600;
        margin-top: 2rem;
    }
    .stButton>button {
        background-color: #4f46e5;
        color: white;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        font-weight: 600;
        border: none;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #4338ca;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .flashcard-expander .streamlit-expander-header {
        background-color: #eef2ff;
        border-radius: 0.5rem;
        padding: 1rem;
        font-weight: 600;
        font-size: 1.1rem;
        color: #374151;
        border: 1px solid #d1d5db;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }
    .flashcard-expander .streamlit-expanderContent {
        background-color: #f9fafb;
        border-left: 3px solid #6366f1;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="main-header">📝 Flashcard Generator</h1>', unsafe_allow_html=True)
st.write("Automatically convert key points from your document into interactive flashcards.")

# --- Session State Initialization ---
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = []
if 'flashcard_document' not in st.session_state:
    st.session_state.flashcard_document = None

# --- Document Upload and Processing ---
st.markdown('<h3 class="secondary-header">1. Upload your Document</h3>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="flashcard_uploader")

if uploaded_file is not None:
    # --- START OF MODIFICATION ---
    # Here we use PyMuPDF to extract text from the uploaded PDF.
    try:
        # Read the file as bytes
        pdf_bytes = uploaded_file.read()
        # Open the PDF file using PyMuPDF
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        
        # Check if text was successfully extracted
        if text:
            st.success("File uploaded and text extracted successfully!")
            st.session_state.flashcard_document = text
        else:
            st.warning("The uploaded PDF appears to be empty or an image-based PDF (scanned document). "
                       "Please upload a text-based PDF.")
            st.session_state.flashcard_document = None
            st.session_state.flashcards = []

    except Exception as e:
        st.error(f"An error occurred while processing the PDF: {e}")
        st.session_state.flashcard_document = None
        st.session_state.flashcards = []
    # --- END OF MODIFICATION ---

else:
    st.warning("Please upload a PDF to generate flashcards.")
    st.session_state.flashcard_document = None
    st.session_state.flashcards = []

# --- API Call Function ---
def call_gemini_api(document_content):
    """
    Makes a call to the Gemini API to generate flashcards in a structured JSON format.
    """
    # NOTE: Hardcoding your API key directly in the code is not a recommended security practice.
    # For production applications, consider using environment variables to store your key.
    api_key = "AIzaSyDkSLvT8jqu8Zi5kUWwDPHIvoxxqJznp3Y"
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"

    # Define the desired JSON schema for the response
    flashcard_schema = {
        "type": "ARRAY",
        "items": {
            "type": "OBJECT",
            "properties": {
                "question": {"type": "STRING"},
                "answer": {"type": "STRING"}
            },
            "propertyOrdering": ["question", "answer"]
        }
    }

    # Construct the full prompt for the model
    full_prompt = (
        f"You are an AI flashcard generator. Given the following document content, "
        f"create a list of 5-10 flashcards. Each flashcard should be an object "
        f"with a 'question' and an 'answer' property. The questions should be direct "
        f"and the answers should be concise. The output must be a valid JSON array.\n\n"
        f"Document Content:\n{document_content}"
    )

    payload = {
        "contents": [{"role": "user", "parts": [{"text": full_prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": flashcard_schema
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

# --- Flashcard Generation and Display ---
if st.session_state.get('flashcard_document'):
    if st.button("Generate Flashcards"):
        with st.spinner("Creating flashcards..."):
            # Call the API with the document content
            flashcards = call_gemini_api(st.session_state.flashcard_document)
            if flashcards:
                st.session_state.flashcards = flashcards
                st.success("Flashcards generated!")

if st.session_state.flashcards:
    st.markdown('<h3 class="secondary-header">Your Flashcards</h3>', unsafe_allow_html=True)
    for i, card in enumerate(st.session_state.flashcards):
        with st.expander(f"{i+1}.** {card['question']}", expanded=False):
            st.markdown(f"*Answer:* {card['answer']}")