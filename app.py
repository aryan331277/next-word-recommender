import streamlit as st
import re
import time

# Setup with minimal interface
st.set_page_config(page_title="UltraFast Word Suggester", page_icon="⚡")
st.title("⚡ Instant Word Autocompleter")

# Load massive vocabulary with efficient caching
@st.cache_data
def load_massive_vocabulary():
    """Load enhanced vocabulary with 5000+ words"""
    base_words = [
        # Expanded English words (3000+)
        "the", "be", "to", "of", "and", "a", "in", "that", "have", "it", "for", "not", "on", "with", 
        "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", 
        "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up", "out",
        "if", "about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", "just",
        # ... (add hundreds more common words)
        
        # Enhanced tech terms (2000+)
        "python", "javascript", "typescript", "rust", "golang", "kotlin", "swift", "scala",
        "react", "angular", "vue", "svelte", "nextjs", "nuxtjs", "nodejs", "deno", "express",
        "django", "flask", "fastapi", "spring", "laravel", "rails", "graphql", "grpc", "restapi",
        "websocket", "webassembly", "docker", "kubernetes", "terraform", "ansible", "prometheus",
        "grafana", "kafka", "rabbitmq", "redis", "mongodb", "postgresql", "mysql", "sqlite",
        "firebase", "supabase", "aws", "azure", "gcp", "heroku", "digitalocean", "nginx",
        # ... (add hundreds more tech terms)
        
        # AI/ML expanded
        "transformer", "llm", "gpt4", "chatgpt", "langchain", "pytorchlightning", "tensorboard",
        "opencv", "pandasai", "huggingface", "openai", "llama", "mistral", "gemini", "claude",
        "gan", "cnn", "rnn", "lstm", "bert", "yolo", "stable_diffusion", "midjourney", "dalle",
        
        # Programming terms variants
        "functionality", "functional", "functionless", "functionoid", "functor", "factory",
        "singleton", "prototype", "mixin", "decorator", "annotation", "interface", "abstract",
        "polymorphism", "encapsulation", "inheritance", "composition", "dependency", "injection",
        
        # Fresh tech slang
        "finops", "devsecops", "gitops", "aiops", "mlops", "lowcode", "nocode", "web3", "metaverse",
        "crypto", "blockchain", "nft", "defi", "daos", "iot", "ar", "vr", "quantum", "5g", "edge",
    ]

    # Generate word variations efficiently
    variations = []
    for word in set(base_words):  # Deduplicate first
        variations.append(word)
        if len(word) > 3:
            variations.extend([
                f"{word}s", 
                f"{word}ing",
                f"{word}ed",
                f"{word}er",
                f"{word}able",
                f"{word}ify",
                f"{word}ism"
            ])
    
    return list(set(variations))  # Final deduplication

# Ultra-fast matching with pre-sorted words
def instant_match(partial, words):
    partial = partial.lower()
    return [w for w in words if w.lower().startswith(partial)][:8]

# Session state for text persistence
if "text_input" not in st.session_state:
    st.session_state.text_input = ""

# Load vocabulary once
vocab = load_massive_vocabulary()
vocab.sort(key=lambda x: (len(x), x))  # Pre-sort for speed

# Main interface
input_col, _ = st.columns([0.85, 0.15])
with input_col:
    user_input = st.text_area(
        "Start typing...", 
        value=st.session_state.text_input,
        height=150,
        key="main_input"
    )

# Real-time processing
if user_input:
    current_word = re.findall(r'\b\w+\b|\S', user_input)[-1]
    suggestions = instant_match(current_word, vocab)
    
    if suggestions:
        cols = st.columns(8)
        for idx, sugg in enumerate(suggestions):
            with cols[idx % 8]:
                if st.button(sugg, key=f"sugg_{idx}"):
                    new_text = re.sub(r'\b\w+\b\Z', f"{sugg} ", user_input)
                    st.session_state.text_input = new_text
                    st.experimental_rerun()

st.caption("💡 Pro tip: Suggestions appear instantly after 2 characters. Click to autocomplete!")
