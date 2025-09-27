import streamlit as st
import google.generativeai as genai
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Post-Surgery Adhesion Tracker",
    page_icon="🩺",
    layout="wide"
)

# --- Custom CSS for Chat Bubbles ---
st.markdown("""
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 20px;
}
.chat-box {
    padding: 12px;
    border-radius: 12px;
    max-width: 75%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    line-height: 1.6;
}
.user {
    background-color: #e1f5fe;
    align-self: flex-end;
    color: #333;
    border: 1px solid #b3e5fc;
}
.bot {
    background-color: #f1f8e9;
    align-self: flex-start;
    color: #333;
    border: 1px solid #dcedc8;
}
</style>
""", unsafe_allow_html=True)


# --- System Prompt for the Model ---
SYSTEM_PROMPT = (
    "You are a helpful and empathetic medical assistant specializing in post-surgery adhesion detection. "
    "Your primary role is to ask clarifying questions about symptoms and affected body regions "
    "and provide general post-surgery guidance. You must strictly adhere to the following rules:\n"
    "1. Only discuss symptoms, affected body regions, and related post-surgery topics.\n"
    "2. If the user asks for a diagnosis, medical advice, or prescription, you MUST refuse and advise them to consult a healthcare professional immediately. State that you are an AI assistant and cannot provide medical diagnoses.\n"
    "3. If the user's query is unrelated to post-surgery symptoms or care, politely redirect them back to the topic.\n"
    "4. Keep your responses concise, clear, and easy to understand for a non-medical person."
)


# --- Initialize Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# --- Function to call Gemini API ---
def get_gemini_response(user_input: str, api_key: str) -> str:
    """
    Calls the Gemini API to get a response based on user input.

    Args:
        user_input: The user's message.
        api_key: The Google AI API key.

    Returns:
        The model's response as a string.
    """
    try:
        # Configure the generative AI library with the API key
        genai.configure(api_key=api_key)

        # Initialize the model
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=SYSTEM_PROMPT
        )

        # Generate content
        response = model.generate_content(user_input)

        return response.text

    except Exception as e:
        st.error(f"An error occurred while contacting the AI model: {str(e)}")
        return "Sorry, I'm having trouble responding right now. Please check the API key and try again."


def main():
    """Main function to run the Streamlit app."""
    st.title("🩺 Post-Surgery Adhesion Tracker")
    st.markdown("This tool helps you track symptoms that might be related to post-surgical adhesions. This is not a diagnostic tool. **Always consult a healthcare professional for medical advice.**")

    # --- API Key Input ---
    # Using st.secrets is the recommended way for deployed apps.
    # For local development, you can use the text input.
    try:
        # Check for the API key in Streamlit secrets
        api_key = st.secrets["GEMINI_API_KEY"]
    except (FileNotFoundError, KeyError):
        # If not found, ask the user to input it
        st.info("Please provide your Google AI API Key to begin.", icon="🔑")
        api_key = st.text_input(
            "Enter your Google AI API Key:",
            type="password",
            key="api_key_input",
            help="You can get your key from Google AI Studio."
        )

    if not api_key:
        st.warning("An API key is required to use the tracker.")
        st.stop()


    # --- User Input Fields ---
    with st.form("symptom_form"):
        st.subheader("Describe Your Current Condition")
        col1, col2 = st.columns(2)
        with col1:
            symptom_input = st.text_area(
                "Describe your symptoms in detail:",
                placeholder="E.g., sharp pain in the lower abdomen, feeling bloated after eating, persistent nausea.",
                key="symptom_input",
                height=150
            )
        with col2:
            region_input = st.selectbox(
                "Select the primary affected region:",
                ["", "Abdomen", "Pelvis", "Chest", "Lower back", "Other"],
                key="region_input"
            )

        submit_button = st.form_submit_button("Submit Symptoms")

    if submit_button and symptom_input and region_input:
        user_question = f"My symptoms are: '{symptom_input}'. The primary affected region is: {region_input}."
        with st.spinner("Analyzing..."):
            response = get_gemini_response(user_question, api_key)
            st.session_state.chat_history.append({"user": user_question, "bot": response})
    elif submit_button:
        st.warning("Please describe your symptoms and select an affected region before submitting.")


    # --- Display Chat History ---
    if st.session_state.chat_history:
        st.subheader("Your Tracking History")
        for chat in reversed(st.session_state.chat_history):
            st.markdown(f"""
                <div class="chat-container">
                    <div class="chat-box user"><b>You:</b><br>{chat['user']}</div>
                    <div class="chat-box bot"><b>Assistant:</b><br>{chat['bot']}</div>
                </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
