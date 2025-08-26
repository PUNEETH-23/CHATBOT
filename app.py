import streamlit as st
import openai
import os

# Set page configurations
st.set_page_config(
    page_title="Travel Chatbot",
    page_icon="✈️",
    layout="wide"
)

# Custom CSS (same as your original)
st.markdown("""<style> body { font-family: 'Inter', sans-serif; background-color: #F6F4F0; /* Soft Off-White */ color: #2E5077; /* Deep Blue */ margin: 0; padding: 0; } h1 { color: #2E5077; /* Deep Blue */ text-align: center; font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem; } .stButton>button { background-color: #79D7BE; /* Soft Mint */ color: #2E5077; /* Deep Blue */ border-radius: 1rem; padding: 1rem 2rem; font-size: 1.25rem; font-weight: 600; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); transition: all 0.3s ease; } .stButton>button:hover { background-color: #4DA1A9; /* Teal Blue */ transform: scale(1.05); } .stTextInput input, .stTextArea textarea { border: 1px solid #4DA1A9; /* Teal Blue */ border-radius: 1rem; padding: 1rem; font-size: 1.1rem; width: 100%; box-sizing: border-box; transition: border-color 0.3s ease; } .stTextInput input:focus, .stTextArea textarea:focus { border-color: #79D7BE; /* Soft Mint */ box-shadow: 0 0 0 3px rgba(121, 215, 190, 0.2); } .chat-container { background-color: #F6F4F0; /* Soft Off-White */ border-radius: 1rem; padding: 2rem; box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.1); margin-top: 2rem; max-width: 900px; margin-left: auto; margin-right: auto; animation: fadeIn 0.5s ease-out; } .chat-box { padding: 1rem; margin-bottom: 1.5rem; border-radius: 1rem; font-size: 1.1rem; line-height: 1.5; max-width: 80%; margin-left: auto; margin-right: auto; } .chat-box.bot { background-color: #2E5077; /* Deep Blue */ color: white; text-align: left; border-bottom-left-radius: 0; border-top-right-radius: 0; } .chat-box.user { background-color: #4DA1A9; /* Teal Blue */ color: #F6F4F0; /* Soft Off-White */ text-align: right; border-bottom-right-radius: 0; border-top-left-radius: 0; } /* Animation for smooth transition */ @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } } .stTextInput input, .stTextArea textarea { padding-left: 1.5rem; } .stTextInput input::placeholder, .stTextArea textarea::placeholder { color: #A6A6A6; /* Lighter Grey */ font-style: italic; } </style> """, unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.message_counter = 0

def get_chatbot_response(user_input: str, api_key: str) -> str:
    """
    Get response from OpenAI GPT for travel-related queries.
    """
    try:
        openai.api_key = api_key

        prompt = f"""
You are a friendly and knowledgeable travel expert. Answer travel-related questions, give practical tips, and suggest destinations.
If the question isn't travel-related, politely redirect to travel topics.

User question: {user_input}
"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-4 if you have access
            messages=[
                {"role": "system", "content": "You are a helpful travel assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=300,
            temperature=0.7,
        )

        return response['choices'][0]['message']['content']

    except Exception as e:
        return f"An error occurred: {type(e).__name__} - {str(e)}"

def main():
    st.title("✈️ Travel Chatbot")
    st.write("Hello! I'm your travel assistant. Ask me anything about destinations, planning, or travel tips!")

    # Get API key securely from environment or user input
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        api_key = st.text_input(
            "Enter your OpenAI API Key:",
            type="password",
            key="api_key_input"
        )
        if not api_key:
            st.warning("API key is required to use the chatbot.")
            st.stop()

    # Chat interface
    user_input = st.text_input(
        "Question:",
        placeholder="E.g., What are the best times to visit Japan?",
        key="user_question_input"
    )

    submit_button = st.button("Submit")
    
    if submit_button and user_input:
        with st.spinner("Fetching your response..."):
            response = get_chatbot_response(user_input, api_key)
            st.session_state.message_counter += 1
            st.session_state.chat_history.append({
                "id": st.session_state.message_counter,
                "user": user_input,
                "bot": response
            })

    # Display chat history
    if st.session_state.chat_history:
        st.write("### Chat History")
        for chat in reversed(st.session_state.chat_history):
            st.markdown(f"""
                <div class="chat-container">
                    <div class="chat-box user">{chat['user']}</div>
                    <div class="chat-box bot">{chat['bot']}</div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
