# import streamlit as st
# from app.pdf_utils import extract_text_from_pdf
# from app.summarizer import summarize_text

# st.title("🩺 Medical Report Summarizer")

# uploaded_file = st.file_uploader("Upload a medical report (PDF)", type="pdf")

# if uploaded_file:
#     with st.spinner("Extracting text..."):
#         text = extract_text_from_pdf(uploaded_file)
#         st.text_area("Extracted Text", text, height=300)

#     if st.button("Summarize"):
#         with st.spinner("Summarizing..."):
#             summary = summarize_text(text)
#             st.subheader("📄 Summary")
#             st.success(summary)





import streamlit as st
from app.pdf_utils import extract_text_from_pdf
from app.summarizer import summarize_text
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
else:
    gemini_model = None

def simplify_with_gemini(text):
    if not gemini_model:
        return "⚠️ Gemini API key not found. Please set it in your .env file."
    prompt = f"""
    Simplify this medical summary so that it’s easily understandable for a patient with no medical background.
    Avoid medical jargon and explain in everyday language:
    
    {text}
    """
    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Simplification failed: {e}"

# Streamlit App
st.set_page_config(page_title="Medical Report Summarizer", page_icon="🩺")
st.title("🩺 Medical Report Summarizer")

uploaded_file = st.file_uploader("Upload a medical report (PDF)", type="pdf")

if "summary" not in st.session_state:
    st.session_state.summary = ""
if "simplified" not in st.session_state:
    st.session_state.simplified = ""

if uploaded_file:
    with st.spinner("Extracting text..."):
        text = extract_text_from_pdf(uploaded_file)
        st.text_area("Extracted Text", text, height=250)

    if st.button("Summarize"):
        with st.spinner("Summarizing..."):
            st.session_state.summary = summarize_text(text)
            st.session_state.simplified = ""  # Reset simplified when new summary is generated

    if st.session_state.summary:
        st.subheader("Summary")
        st.success(st.session_state.summary)

        if st.button("Simplify for Patients"):
            with st.spinner("Simplifying..."):
                st.session_state.simplified = simplify_with_gemini(st.session_state.summary)

    if st.session_state.simplified:
        st.subheader("Simplified for Patients")
        st.info(st.session_state.simplified)
