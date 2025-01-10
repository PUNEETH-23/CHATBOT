import streamlit as st
import google.generativeai as genai
from typing import Optional
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure page settings
st.set_page_config(
    page_title="Travel Chatbot",
    page_icon="✈️",
    layout="centered"
)

# Initialize session state for chat history and message counter
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.message_counter = 0


def get_chatbot_response(user_input: str, api_key: str) -> str:
    """
    Get response from Gemini AI for travel-related queries.
    
    Args:
        user_input: User's travel question
        api_key: Gemini API key
        
    Returns:
        str: Chatbot's response or error message
    """
    try:
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Initialize the model
        model = genai.GenerativeModel('gemini-pro')
        
        # Create the prompt
        prompt = f"""
        As a travel expert, provide a helpful and informative response to this query: {user_input}
        Focus on providing specific, practical advice and relevant travel tips.
        If the query isn't travel-related, politely redirect to travel topics.
        """
        
        # Generate the response
        response = model.generate_content(prompt)
        return response.text
        
    except genai.AuthenticationError:
        return "Invalid API key. Please check your credentials."
    except genai.ConnectionError:
        return "Unable to connect to the Gemini AI server. Please try again later."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


def main():
    st.title("✈️ Travel Chatbot")
    st.write("Hello! I'm your travel assistant. Ask me anything about destinations, planning, or travel tips!")

    # Get API key securely from environment or user input
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.warning("API key is not set in the environment.")
        api_key = st.text_input(
            "Enter your Gemini API Key:",
            type="password",  # Mask the input
            key="api_key_input"
        )
        if not api_key:
            st.stop()  # Stop the app until the API key is provided

    # Chat interface
    user_input = st.text_input(
        "Your travel question:",
        placeholder="E.g., What are the best times to visit Japan?",
        key="user_question_input"
    )
    
    # Submit button
    if st.button("Submit"):
        if user_input:
            with st.spinner("Fetching your response..."):
                response = get_chatbot_response(user_input, api_key)
                
                # Increment message counter
                st.session_state.message_counter += 1
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "id": st.session_state.message_counter,
                    "user": user_input,
                    "bot": response
                })
        else:
            st.warning("Please enter a question before submitting.")

    # Display chat history
    if st.session_state.chat_history:
        st.write("### Chat History")
        for chat in reversed(st.session_state.chat_history):
            st.text_area(
                f"You (Message {chat['id']}):",
                chat["user"],
                height=100,
                disabled=True,
                key=f"user_message_{chat['id']}"
            )
            st.text_area(
                f"Travel Assistant (Response {chat['id']}):",
                chat["bot"],
                height=200,
                disabled=True,
                key=f"bot_message_{chat['id']}"
            )
            st.markdown("---")


if __name__ == "__main__":
    main()
