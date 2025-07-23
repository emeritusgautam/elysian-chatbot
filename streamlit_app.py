import streamlit as st
import PyPDF2
import google.generativeai as genai
import os

st.set_page_config(page_title="📄 Prestige Elysian Chatbot")

st.title("💬 Prestige Elysian Chatbot")

# 🔒 Hardcoded Gemini API Key and PDF Path
api_key = "AIzaSyDgqfPNnyTTtrt20jghCFFHzhsvoosSFck"
pdf_path = "/Users/gautamkumarsingh/Downloads/final_gemini_pdf_qa_bot/ror.pdf"  # ← replace with full path to your PDF

# Configure Gemini API and read PDF
if os.path.exists(pdf_path):
    try:
        genai.configure(api_key=api_key)

        # Load model and start chat session
        model = genai.GenerativeModel("gemini-1.5-flash")  # or gemini-2.5-flash if supported
        if "chat" not in st.session_state:
            st.session_state.chat = model.start_chat(history=[])

        # Load PDF content
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            full_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text.strip() + "\n"

        #st.success(f"PDF loaded from: {pdf_path}")

        # ChatGPT-style user input
        user_input = st.text_input("💬 Ask a question about your prestige elysian:", key="chat_input")
        if st.button("Send") and user_input:
            prompt = f"Here is the PDF content:\n{full_text}\n\nAnswer the question:\n{user_input}"
            with st.spinner("Hold tight! ElysianChatbot is fetching the insights...."):
                response = st.session_state.chat.send_message(prompt)
                st.session_state.last_response = response.text
                st.session_state.chat_history = st.session_state.get("chat_history", []) + [
                    ("You", user_input),
                    ("ElysianChatbot", response.text)
                ]

        # Display full conversation
        if "chat_history" in st.session_state:
            st.subheader("🧠 Chat History")
            for sender, msg in st.session_state.chat_history:
                st.markdown(f"**{sender}:** {msg}")

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.error(f"🚫 PDF path not found: {pdf_path}")
