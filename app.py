import streamlit as st
import google.generativeai as genai
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Post-Surgery Adhesion Tracker",
    page_icon="🩺",
    layout="centered"
)

# --- Gemini API Configuration ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except (KeyError, AttributeError):
    st.error("🚨 Gemini API Key not found. Please add it to your Streamlit secrets.", icon="🚨")
    st.stop()

# --- AI Model and System Prompt ---
SYSTEM_PROMPT = """
You are a highly specialized medical assistant for tracking post-surgery adhesion symptoms.
Your sole purpose is to help a user create a detailed log of their symptoms.

**Your Instructions:**
1.  **Analyze Initial Input**: The user will provide an affected body region and initial symptoms.
2.  **Ask ONE Question at a Time**: Based on their input, ask a single, targeted follow-up question to get more specific information.
3.  **Region-Specific Questions**: Tailor your questions to the affected region.
    -   **Abdomen/Pelvis**: Ask about bloating, bowel movement changes (constipation/diarrhea), sharp vs. dull pain, pain triggers (movement, eating), nausea, or vomiting.
    -   **Chest/Thoracic**: Ask about shortness of breath, pain during deep breaths, coughing, or a feeling of tightness.
    -   **Joints (Shoulder/Knee)**: Ask about range of motion, stiffness, popping/clicking sounds, or pain during specific movements.
4.  **Maintain Focus**: Do not deviate from symptom tracking. If the user asks for a diagnosis, medical advice, or an unrelated question, politely guide them back by stating your purpose is only for symptom logging.
5.  **Be Concise**: Keep your questions clear and to the point.

Start the conversation by asking the first logical follow-up question based on the user's initial details.
"""

# Function to initialize the Gemini chat model
def initialize_chat():
    """Initializes the Gemini Pro model and starts a chat session with the system prompt."""
    # Use the stable 'gemini-pro' model
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[
        {'role': 'user', 'parts': [SYSTEM_PROMPT]},
        {'role': 'model', 'parts': ["Understood. I am ready to assist with post-surgery adhesion symptom tracking. Please provide the affected region and initial symptoms."]}
    ])
    return chat

# --- Streamlit App UI and Logic ---

# Initialize session state variables
if "step" not in st.session_state:
    st.session_state.step = 0
if "chat" not in st.session_state:
    st.session_state.chat = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "region" not in st.session_state:
    st.session_state.region = None

st.title("🩺 Post-Surgery Adhesion Tracker")
st.markdown("This tool helps you create a detailed log of your symptoms after surgery by asking targeted questions. This is **not** medical advice.")

# --- Step 0: Confirm Surgery ---
if st.session_state.step == 0:
    st.subheader("Step 1: Confirm Surgery")
    st.write("Have you had a recent surgery?")
    
    col1, col2 = st.columns([1, 5]) # Make 'Yes' button smaller
    
    if col1.button("Yes", use_container_width=True):
        st.session_state.step = 1
        st.rerun()
        
    if col2.button("No", use_container_width=True):
        st.info("This tool is specifically designed for tracking symptoms after a surgical procedure. If you have health concerns, please consult a medical professional.", icon="ℹ️")
        st.session_state.step = -1 # A terminal state

# --- Step 1: Select Region ---
if st.session_state.step == 1:
    st.subheader("Step 2: Identify the Region")
    st.write("Please select the region where you had the surgery.")
    
    region_options = ["Abdomen", "Pelvis", "Chest/Thoracic", "Joint (e.g., Shoulder, Knee)"]
    st.session_state.region = st.selectbox("Select the affected body region:", region_options)
    
    if st.button("Confirm Region"):
        st.session_state.step = 2
        st.rerun()

# --- Step 2: Describe Symptoms ---
if st.session_state.step == 2:
    st.subheader(f"Step 3: Describe Symptoms for the **{st.session_state.region}** region")
    with st.form("symptom_form"):
        initial_symptoms = st.text_area(
            "Please describe your current symptoms:",
            placeholder="e.g., 'I have a sharp, pulling pain on my right side when I stand up straight.'",
            height=150
        )
        submitted = st.form_submit_button("Start AI Tracking")
        
        if submitted and initial_symptoms:
            st.session_state.chat = initialize_chat()
            st.session_state.messages = [] # Reset messages for a new log
            
            first_message = f"Region: {st.session_state.region}\n\nInitial Symptoms: {initial_symptoms}"
            st.session_state.messages.append({"role": "user", "content": first_message})
            
            with st.spinner("Analyzing..."):
                response = st.session_state.chat.send_message(first_message)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
            st.session_state.step = 3 # Move to the chat view
            st.rerun()

# --- Step 3: Chat Interface ---
if st.session_state.step == 3:
    st.info(f"You are now in a chat to detail your symptoms for the **{st.session_state.region}** region. Answer the assistant's questions below.", icon="💬")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input for user's response
    if prompt := st.chat_input("Your response..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.spinner("Thinking..."):
            response = st.session_state.chat.send_message(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            with st.chat_message("assistant"):
                st.markdown(response.text)
        st.rerun()

# --- Universal "Start Over" Button ---
# Placed in the sidebar for easy access from any step
if st.session_state.step > 0:
    if st.sidebar.button("Start Over"):
        # Reset all relevant session state variables
        st.session_state.step = 0
        st.session_state.messages = []
        st.session_state.chat = None
        st.session_state.region = None
        st.rerun()
