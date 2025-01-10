import streamlit as st
import google.generativeai as genai
from typing import Optional
import time

# Configure page settings
st.set_page_config(
    page_title="Travel Chatbot",
    page_icon="✈️"
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
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return "I apologize, but I'm having trouble processing your request. Please try again."

def main():
    st.title("✈️ Travel Chatbot")
    st.write("Hello! I'm your travel assistant. Ask me anything about destinations, planning, or travel tips!")
    
    # Simple API key input
    api_key ='AIzaSyCroupi2pzZ-oFzrEl2hLg8puCgchnJSqA'
    
    if not api_key:
        st.warning("Please enter your Gemini API key to continue.")
        return
    
    # Chat interface
    user_input = st.text_input(
        "Your travel question:",
        placeholder="E.g., What are the best times to visit Japan?",
        key="user_question_input"
    )
    
    if user_input:
        with st.spinner("Loading..."):
            response = get_chatbot_response(user_input, api_key)
            
            # Increment message counter
            st.session_state.message_counter += 1
            
            # Add to chat history with a unique ID
            st.session_state.chat_history.append({
                "id": st.session_state.message_counter,
                "user": user_input,
                "bot": response
            })
    
    # Display chat history
    if st.session_state.chat_history:
        st.write("### Chat History")
        for chat in reversed(st.session_state.chat_history):
            st.text_area(
                "You:",
                chat["user"],
                height=100,
                disabled=False,
                key=f"user_message_{chat['id']}"
            )
            st.text_area(
                "Travel Assistant:",
                chat["bot"],
                height=100,
                disabled=False,
                key=f"bot_message_{chat['id']}"
            )
            st.markdown("---")

if __name__ == "__main__":
    main()
