import streamlit as st
import google.generativeai as genai
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
            margin: 0;
            padding: 0;
        }
        h1 {
            color: #2E5077;  /* Deep Blue */
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
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
            transition: border-color 0.3s ease;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #79D7BE;  /* Soft Mint */
            box-shadow: 0 0 0 3px rgba(121, 215, 190, 0.2);
        }
        .chat-container {
            background-color: #F6F4F0;  /* Soft Off-White */
            border-radius: 1rem;
            padding: 2rem;
            box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.1);
            margin-top: 2rem;
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
            animation: fadeIn 0.5s ease-out;
        }
        .chat-box {
            padding: 1rem;
            margin-bottom: 1.5rem;
            border-radius: 1rem;
            font-size: 1.1rem;
            line-height: 1.5;
            max-width: 80%;
            margin-left: auto;
            margin-right: auto;
        }
        .chat-box.bot {
            background-color: #2E5077;  /* Deep Blue */
            color: white;
            text-align: left;
            border-bottom-left-radius: 0;
            border-top-right-radius: 0;
        }
        .chat-box.user {
            background-color: #4DA1A9;  /* Teal Blue */
            color: #F6F4F0;  /* Soft Off-White */
            text-align: right;
            border-bottom-right-radius: 0;
            border-top-left-radius: 0;
        }
        /* Animation for smooth transition */
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        .stTextInput input, .stTextArea textarea {
            padding-left: 1.5rem;
        }
        .stTextInput input::placeholder, .stTextArea textarea::placeholder {
            color: #A6A6A6;  /* Lighter Grey */
            font-style: italic;
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
You are a friendly and knowledgeable travel expert, here to provide helpful, informative, and practical responses to travel-related queries. When answering, focus on offering specific advice, travel tips, and recommendations that can guide the user in planning their trip. Be clear, concise, and aim to create an engaging, pleasant experience for the user.

If the question isn't travel-related, politely redirect the conversation by suggesting topics that are related to travel, such as destinations, packing tips, and travel planning. Keep the tone positive and friendly, and encourage further travel inquiries.

User question: {user_input}
"""
        
        # Generate the response
        response = model.generate_content(prompt)
        return response.text

    except ValueError as ve:
        return "There was an issue with the input or response. Please try again."
    except RuntimeError as re:
        return "There was a runtime error. Please check your API connection and try again."
    except Exception as e:
        return f"An unexpected error occurred: {type(e).__name__} - {str(e)}"

def main():
    st.title("✈️ Travel Chatbot")
    st.write("Hello! I'm your travel assistant. Ask me anything about destinations, planning, or travel tips!")

    # Get API key securely from environment or user input
    api_key = 'AIzaSyCroupi2pzZ-oFzrEl2hLg8puCgchnJSqA'
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
        "Question:",
        placeholder="E.g., What are the best times to visit Japan?",
        key="user_question_input"
    )
    
    # Submit button with better interaction
    submit_button = st.button("Submit")
    
    if submit_button:
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
    
    # Display chat history with improved UI
    if st.session_state.chat_history:
        st.write("### Chat History")
        chat_container = st.container()
        with chat_container:
            for chat in reversed(st.session_state.chat_history):
                st.markdown(f"""
                    <div class="chat-container">
                        <div class="chat-box user">
                            <strong></strong> {chat['user']}
                        </div>
                        <div class="chat-box bot">
                            <strong></strong> {chat['bot']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
ADD a audio input also for this
