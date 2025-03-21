import streamlit as st
import numpy as np
import re
from collections import defaultdict, Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

# Setup
st.set_page_config(page_title="Next Word Recommender", page_icon="📝")
st.title("Next Word Recommender")

# Download required NLTK data
@st.cache_resource
def download_nltk_data():
    nltk.download('punkt')
    nltk.download('brown')
    nltk.download('gutenberg')
    from nltk.corpus import brown, gutenberg
    # Combine texts from Brown and Gutenberg corpus
    all_texts = []
    for file_id in brown.fileids():
        all_texts.extend(brown.words(file_id))
    for file_id in gutenberg.fileids():
        all_texts.extend(gutenberg.words(file_id))
    return ' '.join(all_texts).lower()

# Build n-gram model
@st.cache_resource
def build_ngram_model(text):
    # Tokenize text
    tokens = word_tokenize(text)
    
    # Build n-gram models (bigram and trigram)
    bigrams = list(ngrams(tokens, 2))
    trigrams = list(ngrams(tokens, 3))
    
    # Create frequency dictionaries
    bigram_freq = defaultdict(Counter)
    trigram_freq = defaultdict(Counter)
    
    for w1, w2 in bigrams:
        bigram_freq[w1][w2] += 1
    
    for w1, w2, w3 in trigrams:
        trigram_freq[(w1, w2)][w3] += 1
    
    return bigram_freq, trigram_freq

# Get recommendations based on input text
def get_recommendations(input_text, bigram_freq, trigram_freq, top_n=5):
    input_text = input_text.lower().strip()
    
    if not input_text:
        return ["Start typing to get recommendations..."]
    
    words = word_tokenize(input_text)
    
    # Use trigram model if we have at least 2 words
    if len(words) >= 2:
        last_two = (words[-2], words[-1])
        if last_two in trigram_freq:
            return [word for word, _ in trigram_freq[last_two].most_common(top_n)]
    
    # Fall back to bigram model
    if words[-1] in bigram_freq:
        return [word for word, _ in bigram_freq[words[-1]].most_common(top_n)]
    
    # If no match found
    return ["No recommendations found"]

# Main app logic
corpus_text = download_nltk_data()
bigram_freq, trigram_freq = build_ngram_model(corpus_text)

# User input
user_input = st.text_area("Type your text here:", height=150)

# Button for recommendations
if st.button("Get Recommendations") or user_input:
    recommendations = get_recommendations(user_input, bigram_freq, trigram_freq)
    
    st.subheader("Recommended next words:")
    
    # Create buttons for each recommendation
    cols = st.columns(len(recommendations))
    for i, rec in enumerate(recommendations):
        if cols[i].button(rec, key=f"rec_{i}"):
            user_input = user_input + " " + rec
            st.experimental_rerun()

# Advanced settings expander
with st.expander("Advanced Settings"):
    st.subheader("Model Settings")
    n_recommendations = st.slider("Number of recommendations", 1, 10, 5)
    
    if st.button("Upload Custom Training Text"):
        st.warning("This feature would allow users to upload their own text corpus to train the model with domain-specific vocabulary.")

# Real-time recommendations
st.subheader("Real-time suggestions")
rt_input = st.text_input("Try real-time suggestions (type and wait):")
if rt_input:
    rt_recommendations = get_recommendations(rt_input, bigram_freq, trigram_freq)
    rt_cols = st.columns(len(rt_recommendations))
    for i, rec in enumerate(rt_recommendations):
        rt_cols[i].markdown(f"**{rec}**")

# About section
st.sidebar.title("About")
st.sidebar.info(
    """
    This app recommends the next word based on what you've typed, using n-gram language models 
    trained on a corpus of English text. The model learns patterns from existing text to predict 
    likely continuations of your writing.
    
    The app uses:
    - NLTK for language processing
    - N-gram model for predictions
    - Streamlit for the web interface
    """
)

# Footer
st.markdown("---")
st.markdown("Next Word Recommender - Built with Streamlit and NLTK")
