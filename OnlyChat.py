import time
import streamlit as st
import speech_recognition as sr
import google.generativeai as ai

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            with col1:
                st.write("🎤 Listening...")
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio).lower()
            if "contact" in text:
                st.session_state.menu_option = "Contact"
                st.rerun()
            return text
        except sr.UnknownValueError:
            return False
        except sr.RequestError:
            return False

st.set_page_config(page_title="Cloned Voice ChatBot", page_icon="🎤", layout="wide")

# Configure Gemini model
API_KEY = st.secrets["GOOGLE_API_KEY"]
ai.configure(api_key=API_KEY)
model = ai.GenerativeModel(model_name="gemini-1.5-flash")

col1,clo2,clo3=st.columns([1,2,1])
with clo2:
    st.title("🤖 Cloned Voice ChatBot")

# if st.button("🗑️",help="Clear Chat History"):
#     st.session_state.messages = []
#     st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user messages
user_input = st.chat_input("Enter your message")
voice_query = None

# Voice input button
col1, col2 = st.columns([8, 1])
with col1:
    if st.button("🗑️", help="Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
with col2:
    if st.button("🎤 Speak",help="Ask with Voice"):
        voice_query = recognize_speech()
        if not voice_query:
            with col1:
                st.error("Please try again with a clear voice command.")
                time.sleep(2)
                st.rerun()

# Use voice input if available
if voice_query and not user_input:
    user_input = voice_query

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    if user_input.lower() in ["bye", "exit", "quit"]:
        response = "Goodbye! The application will now close."
    else:
        with st.spinner("Generating response..."):
            try:
                chat = model.start_chat()
                response = chat.send_message(user_input).text
            except Exception as e:
                response = "Sorry, I encountered an error. Please try again later."
                st.error(f"Error: {str(e)}")

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
