import streamlit as st
import re
from collections import defaultdict, Counter
import pandas as pd

# Setup
st.set_page_config(page_title="Real-Time Word Suggester", page_icon="⌨️")
st.title("Real-Time Word Suggester")

# Dictionary-based approach
@st.cache_resource
def load_english_words():
    # Common English words with their frequency
    words = {
        "the": 1, "be": 2, "to": 3, "of": 4, "and": 5, "a": 6, "in": 7, "that": 8, "have": 9, "I": 10,
        "it": 11, "for": 12, "not": 13, "on": 14, "with": 15, "as": 16, "you": 17, "do": 18, "at": 19, "this": 20,
        "but": 21, "his": 22, "by": 23, "from": 24, "they": 25, "we": 26, "say": 27, "her": 28, "she": 29, "or": 30,
        "create": 50, "creative": 51, "creation": 52, "creativity": 53, "creator": 54, "creating": 55,
        "created": 56, "creatively": 57, "python": 100, "program": 101, "programming": 102,
        "programmer": 103, "code": 104, "coding": 105, "algorithm": 106, "data": 107, "science": 108,
        "develop": 120, "developer": 121, "development": 122, "software": 123, "hardware": 124,
        "computer": 125, "machine": 126, "learning": 127, "artificial": 128, "intelligence": 129,
        "streamlit": 130, "web": 131, "app": 132, "application": 133, "interface": 134,
        "user": 135, "experience": 136, "design": 137, "frontend": 138, "backend": 139
    }
    # Add more tech and programming related words
    return words

# User dictionary management
if 'user_dictionary' not in st.session_state:
    st.session_state.user_dictionary = {}

# Load dictionaries
english_words = load_english_words()
user_words = st.session_state.user_dictionary

# Combine dictionaries
def get_combined_dictionary():
    combined = english_words.copy()
    combined.update(user_words)
    return combined

# Find matching words for partial input
def find_matching_words(partial_word, dictionary, max_suggestions=5):
    if not partial_word:
        return []
    
    partial_word = partial_word.lower()
    
    # Find all words that start with the partial word
    matching = [(word, freq) for word, freq in dictionary.items() 
                if word.lower().startswith(partial_word)]
    
    # Sort by frequency (higher frequency first)
    matching.sort(key=lambda x: x[1], reverse=True)
    
    # Return just the words, limited to max_suggestions
    return [word for word, _ in matching[:max_suggestions]]

# Real-time word prediction
def update_suggestions():
    text = st.session_state.input_text
    
    # If empty, clear suggestions
    if not text:
        st.session_state.suggestions = []
        return
    
    # Split the text to get the last word being typed
    words = re.findall(r'\b\w+\b|\S', text)
    
    if not words:
        st.session_state.suggestions = []
        return
    
    last_word = words[-1]
    
    # Get suggestions for the last word
    combined_dict = get_combined_dictionary()
    suggestions = find_matching_words(last_word, combined_dict)
    
    st.session_state.suggestions = suggestions
    st.session_state.current_word = last_word

# Initialize session state
if 'suggestions' not in st.session_state:
    st.session_state.suggestions = []
if 'current_word' not in st.session_state:
    st.session_state.current_word = ""
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

# Add to user dictionary
st.sidebar.title("Add Words to Dictionary")
new_word = st.sidebar.text_input("New Word:")
if st.sidebar.button("Add to Dictionary") and new_word:
    st.session_state.user_dictionary[new_word] = 1000  # High frequency for user-added words
    st.sidebar.success(f"Added '{new_word}' to dictionary!")

# Show user dictionary
if st.session_state.user_dictionary:
    st.sidebar.subheader("Your Custom Words")
    user_words_df = pd.DataFrame(
        {"Word": list(st.session_state.user_dictionary.keys())}
    )
    st.sidebar.dataframe(user_words_df)

# Main text input with live update
st.text_area(
    "Type here:", 
    key="input_text",
    height=150,
    on_change=update_suggestions
)

# Display suggestions in real-time
if st.session_state.suggestions:
    st.subheader("Suggestions:")
    cols = st.columns(min(len(st.session_state.suggestions), 5))
    
    for i, suggestion in enumerate(st.session_state.suggestions):
        if i < len(cols):
            if cols[i].button(suggestion, key=f"sugg_{i}"):
                # Replace the last partial word with the selected suggestion
                words = re.findall(r'\b\w+\b|\S', st.session_state.input_text)
                if words:
                    words[-1] = suggestion
                    st.session_state.input_text = ' '.join(words)
                    # Add a space after the selected suggestion
                    st.session_state.input_text += ' '
                    st.experimental_rerun()

# Explanation
st.markdown("---")
st.markdown("""
### How it works:
- As you type, the app suggests completions for the current word
- Click on a suggestion to complete the current word
- Add custom words to your dictionary using the sidebar
""")

# Footer
st.markdown("---")
st.markdown("Real-Time Word Suggester - Built with Streamlit")
