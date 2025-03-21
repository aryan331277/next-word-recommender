import streamlit as st
import re
import time

# Setup chatbot interface
st.set_page_config(page_title="Chatbot with Autocomplete", page_icon="💬", layout="wide")
st.title("Chatbot with Real-Time Autocomplete")

# Load vocabulary (cached for performance)
@st.cache_data
def load_vocabulary():
    words = [
        "python", "java", "javascript", "html", "css", "code", "function", "variable",
        "string", "integer", "list", "dictionary", "loop", "class", "object", "api",
        "database", "web", "app", "mobile", "cloud", "debug", "error", "exception",
        "create", "creating", "created", "creation", "creative", "creator", "streamlit",
        "machine", "learning", "neural", "network", "tensorflow", "pytorch", "keras",
        "algorithm", "async", "authentication", "blockchain", "compiler", "docker",
        "framework", "microservice", "database", "kubernetes", "lambda", "middleware"
    ]
    return list(set(words))

# Find matching words
def get_suggestions(partial_word, word_list):
    if not partial_word:
        return []
    partial_word = partial_word.lower()
    return [word for word in word_list if word.lower().startswith(partial_word)][:5]

# Initialize chat and vocabulary
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vocab" not in st.session_state:
    st.session_state.vocab = load_vocabulary()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input with autocomplete
user_input = st.chat_input("Type your message...")
current_word = ""

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Simulate bot response
    with st.chat_message("assistant"):
        st.markdown(f"Echo: {user_input}")
    st.session_state.messages.append({"role": "assistant", "content": f"Echo: {user_input}"})

# Autocomplete suggestions (run on every render)
if st.session_state.get('messages'):
    last_message = st.session_state.messages[-1]["content"]
    if last_message.startswith("Echo: "):
        last_message = last_message[6:]
    current_word = re.findall(r'\b\w+\b|\S', last_message)[-1] if last_message else ""

suggestions = get_suggestions(current_word, st.session_state.vocab)

# Show suggestions as buttons above input
if suggestions:
    cols = st.columns(5)
    for idx, sugg in enumerate(suggestions):
        with cols[idx]:
            if st.button(sugg, key=f"sugg_{idx}"):
                # Update the last message with suggestion
                if st.session_state.messages:
                    last_msg = st.session_state.messages[-1]["content"]
                    if "Echo: " in last_msg:
                        original = last_msg[6:]
                        words = re.findall(r'\b\w+\b|\S', original)
                        if words:
                            words[-1] = sugg
                            new_msg = " ".join(words)
                            st.session_state.messages[-1]["content"] = f"Echo: {new_msg}"
                            st.experimental_rerun()
