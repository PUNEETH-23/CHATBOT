import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from typing import Optional

# Set page configurations for a better layout
st.set_page_config(
    page_title="Travel Chatbot",
    page_icon="✈️",
    layout="wide"
)

# Custom CSS for updated UI/UX with new color scheme and animations
st.markdown("""
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #F6F4F0;  /* Soft Off-White */
            color: #2E5077;  /* Deep Blue */
        }
        h1 {
            color: #2E5077;  /* Deep Blue */
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
        }
        .stButton>button {
            background-color: #79D7BE;  /* Soft Mint */
            color: #2E5077;  /* Deep Blue */
            border-radius: 1rem;
            padding: 1rem 2rem;
            font-size: 1.25rem;
            font-weight: 600;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #4DA1A9;  /* Teal Blue */
            transform: scale(1.05);
        }
        .stTextInput input, .stTextArea textarea {
            border: 1px solid #4DA1A9;  /* Teal Blue */
            border-radius: 1rem;
            padding: 1rem;
            font-size: 1.1rem;
            width: 100%;
            box-sizing: border-box;
        }
        .stTextInput input::placeholder, .stTextArea textarea::placeholder {
            color: #A6A6A6;  /* Lighter Grey */
            font-style: italic;
        }
        .chat-container {
            background-color: #F6F4F0;
            border-radius: 1rem;
            padding: 2rem;
            box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.1);
            margin-top: 2rem;
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
        }
        .chat-box {
            padding: 1rem;
            margin-bottom: 1.5rem;
            border-radius: 1rem;
            font-size: 1.1rem;
            line-height: 1.5;
            max-width: 80%;
        }
        .chat-box.bot {
            background-color: #2E5077;  /* Deep Blue */
            color: white;
            text-align: left;
        }
        .chat-box.user {
            background-color: #4DA1A9;  /* Teal Blue */
            color: #F6F4F0;  /* Soft Off-White */
            text-align: right;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for chat history and message counter
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.message_counter = 0

def get_chatbot_response(user_input: str, api_key: str) -> str:
    """
    Get response from Gemini AI for travel-related queries.
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        You are a friendly travel expert. Help the user with detailed travel advice.
        User question: {user_input}
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {type(e).__name__} - {str(e)}"

def transcribe_audio(audio_file):
    """
    Transcribe audio input using SpeechRecognition.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            return recognizer.recognize_google(audio_data)
    except Exception as e:
        return f"Audio Error: {str(e)}"

def main():
    st.title("✈️ Travel Chatbot")
    st.write("Hello! I'm your travel assistant. Ask me anything about destinations, planning, or travel tips!")

    # Get API key securely from environment or user input
    api_key = st.secrets.get("GENAI_API_KEY", "YOUR_API_KEY_HERE")
    if not api_key:
        st.warning("API key is not set in the environment.")
        api_key = st.text_input(
            "Enter your Gemini API Key:",
            type="password",
            key="api_key_input"
        )
        if not api_key:
            st.stop()

    # Text input for queries
    user_input = st.text_input(
        "Type your question:",
        placeholder="E.g., What are the best times to visit Japan?",
        key="user_question_input"
    )

    # Audio input for queries
    audio_file = st.file_uploader("Upload an audio question (WAV format):", type=["wav"])
    if audio_file is not None:
        with st.spinner("Transcribing audio..."):
            audio_input = transcribe_audio(audio_file)
            st.write(f"Transcribed Text: {audio_input}")
            user_input = audio_input

    # Submit button
    submit_button = st.button("Submit")
    
    if submit_button:
        if user_input:
            with st.spinner("Fetching your response..."):
                response = get_chatbot_response(user_input, api_key)
                st.session_state.message_counter += 1
                st.session_state.chat_history.append({
                    "id": st.session_state.message_counter,
                    "user": user_input,
                    "bot": response
                })
        else:
            st.warning("Please enter a question or upload an audio file before submitting.")

    # Display chat history
    if st.session_state.chat_history:
        st.write("### Chat History")
        for chat in reversed(st.session_state.chat_history):
            st.markdown(f"""
                <div class="chat-container">
                    <div class="chat-box user">
                        {chat['user']}
                    </div>
                    <div class="chat-box bot">
                        {chat['bot']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
