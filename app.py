import streamlit as st
from openai import Gemini
import os

# Page config
st.set_page_config(
    page_title="Post-Surgery Adhesion Tracker",
    page_icon="🩺",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.chat-box {
    padding: 10px;
    border-radius: 8px;
    max-width: 80%;
}
.user {
    background-color: #d1f0ff;
    align-self: flex-end;
}
.bot {
    background-color: #f0f0f0;
    align-self: flex-start;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.message_counter = 0

# Function to call Gemini chat API
def get_tracker_response(user_input: str, api_key: str) -> str:
    try:
        client = Gemini(api_key=api_key)

        messages = [
            {"role": "system", "content": "You are a medical assistant specialized in post-surgery adhesion detection. Only ask or provide information about symptoms, affected body regions, and related post-surgery guidance. Politely redirect if the query is unrelated."},
            {"role": "user", "content": user_input}
        ]

        response = client.chat.completions.create(
            model="gemini-1.5",
            messages=messages,
            temperature=0.7,
            max_output_tokens=300
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"An error occurred: {type(e).__name__} - {str(e)}"

def main():
    st.title("🩺 Post-Surgery Adhesion Tracker")
    st.write("Track post-surgery adhesion symptoms and affected regions. Answer the questions based on your condition.")

    # API key input
    api_key = "AIzaSyAhnRkBFUKzEiQeyZ038yw0zjo92xFUcrM"
    if not api_key:
        api_key = st.text_input("Enter your Gemini API Key:", type="password", key="api_key_input")
        if not api_key:
            st.warning("API key is required to use the tracker.")
            st.stop()

    # Symptom input
    symptom_input = st.text_input(
        "Describe your symptoms:",
        placeholder="E.g., abdominal pain, bloating, nausea",
        key="symptom_input"
    )

    # Region input
    region_input = st.selectbox(
        "Select affected region:",
        ["Abdomen", "Pelvis", "Lower back", "Other"],
        key="region_input"
    )

    if st.button("Submit") and symptom_input:
        user_question = f"Symptoms: {symptom_input}. Affected region: {region_input}."
        with st.spinner("Analyzing symptoms..."):
            response = get_tracker_response(user_question, api_key)
            st.session_state.message_counter += 1
            st.session_state.chat_history.append({
                "id": st.session_state.message_counter,
                "user": user_question,
                "bot": response
            })

    # Display chat history
    if st.session_state.chat_history:
        st.write("### Patient Tracking History")
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
