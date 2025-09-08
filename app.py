import streamlit as st
import openai
import os

# Page config
st.set_page_config(
    page_title="Travel Chatbot",
    page_icon="✈️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
/* same CSS you wrote */
</style>
""", unsafe_allow_html=True)

# Session state init
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.message_counter = 0

def get_chatbot_response(user_input: str, api_key: str) -> str:
    """
    Get response from OpenAI GPT for travel-related queries.
    """
    try:
        client = openai.OpenAI(api_key=api_key)

        messages = [
            {"role": "system", "content": "You are a friendly and knowledgeable travel assistant. Only answer travel-related questions and politely redirect if not travel-related."},
            {"role": "user", "content": user_input}
        ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"An error occurred: {type(e).__name__} - {str(e)}"

def main():
    st.title("✈️ Travel Chatbot")
    st.write("Hello! I'm your travel assistant. Ask me anything about destinations, planning, or travel tips!")

    # API key handling
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        api_key = st.text_input("Enter your OpenAI API Key:", type="password", key="api_key_input")
        if not api_key:
            st.warning("API key is required to use the chatbot.")
            st.stop()

    # Chat input
    user_input = st.text_input(
        "Question:",
        placeholder="E.g., What are the best times to visit Japan?",
        key="user_question_input"
    )

    if st.button("Submit") and user_input:
        with st.spinner("Fetching your response..."):
            response = get_chatbot_response(user_input, api_key)
            st.session_state.message_counter += 1
            st.session_state.chat_history.append({
                "id": st.session_state.message_counter,
                "user": user_input,
                "bot": response
            })

    # Display history
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
