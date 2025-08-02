import streamlit as st
import requests
import json
import fitz
import time

st.set_page_config(page_title="Summary & Highlights Extractor", layout="wide")

st.title("📖 Summary & Highlights Extractor")
st.write("Instantly get a concise summary and a list of key points from your document.")

# --- Session State Initialization ---
if 'summary_document_content' not in st.session_state:
    st.session_state.summary_document_content = None
if 'generated_summary' not in st.session_state:
    st.session_state.generated_summary = ""
if 'generated_highlights' not in st.session_state:
    st.session_state.generated_highlights = []

# --- Document Upload and Processing ---
st.subheader("1. Upload your Document")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="summary_uploader")

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
            st.session_state.summary_document_content = text
        else:
            st.warning("The uploaded PDF appears to be empty or an image-based PDF (scanned document). "
                       "Please upload a text-based PDF.")
            st.session_state.summary_document_content = None

    except Exception as e:
        st.error(f"An error occurred while processing the PDF: {e}")
        st.session_state.summary_document_content = None

else:
    st.session_state.summary_document_content = None
    st.session_state.generated_summary = ""
    st.session_state.generated_highlights = []
    st.warning("Please upload a PDF to generate a summary.")

# --- API Call Function ---
def generate_summary_and_highlights(document_content):
    """
    Makes a call to the Gemini API to generate a summary and highlights in a structured JSON format.
    """
    # --------------------------------------------------------------------------------------
    # YOUR API KEY IS ADDED HERE.
    # Replace "YOUR_GEMINI_API_KEY" with the actual key you obtained from Google AI Studio.
    api_key = "AIzaSyCC8s3-ZHZYWEtAhknKruPD6sCnVyaqBUs" 
    # --------------------------------------------------------------------------------------
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

    # Define the desired JSON schema for the response
    response_schema = {
        "type": "OBJECT",
        "properties": {
            "summary": {"type": "STRING"},
            "highlights": {
                "type": "ARRAY",
                "items": {"type": "STRING"}
            }
        }
    }

    # Construct the full prompt for the model
    full_prompt = (
        f"You are an AI assistant that summarizes documents and extracts key highlights. "
        f"Given the following document content, provide a concise summary and a list of 4-5 key highlights. "
        f"The output must be a valid JSON object with two properties: 'summary' (a string) and 'highlights' (an array of strings). "
        f"Format each highlight clearly. "
        f"Document Content:\n{document_content}"
    )

    payload = {
        "contents": [{"role": "user", "parts": [{"text": full_prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }

    try:
        response = requests.post(api_url, json=payload, timeout=60)
        response.raise_for_status()

        response_data = response.json()
        if "candidates" in response_data and response_data["candidates"]:
            json_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
            if json_text.startswith('json') and json_text.endswith(''):
                json_text = json_text.strip('` \njson')

            parsed_data = json.loads(json_text)
            return parsed_data.get('summary', ''), parsed_data.get('highlights', [])
        else:
            st.error("I'm sorry, I couldn't get a response from the API.")
            return "", []

    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while calling the Gemini API: {e}")
        return "", []
    except json.JSONDecodeError as e:
        st.error(f"Failed to parse JSON response from the API: {e}. Please try again.")
        return "", []
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return "", []

# --- Generation and Display ---
if st.session_state.get('summary_document_content'):
    if st.button("Generate Summary"):
        with st.spinner("Extracting summary and highlights..."):
            summary, highlights = generate_summary_and_highlights(st.session_state.summary_document_content)
            
            # Store the results in session state to display them
            st.session_state.generated_summary = summary
            st.session_state.generated_highlights = highlights

        if summary or highlights:
            st.success("Summary generated!")
        
if st.session_state.generated_summary or st.session_state.generated_highlights:
    st.subheader("Document Summary")
    st.markdown(st.session_state.generated_summary)
    
    if st.session_state.generated_highlights:
        st.subheader("Key Highlights & Extracted Information")
        for highlight in st.session_state.generated_highlights:
            st.markdown(f"• {highlight}")