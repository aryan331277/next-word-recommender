import streamlit as st
import re
import time

# Setup with better performance
st.set_page_config(page_title="Fast Word Suggester", page_icon="⌨️", layout="wide")
st.title("Real-Time Word Suggester")

# Load large English vocabulary with common programming terms
@st.cache_data
def load_large_vocabulary():
    """Load a large vocabulary of English and programming terms"""
    words = [
        # Common English words
        "the", "be", "to", "of", "and", "a", "in", "that", "have", "it", "for", "not", "on", "with", 
        "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", 
        "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up", "out",
        "if", "about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", "just",
        "him", "know", "take", "people", "into", "year", "your", "good", "some", "could", "them", "see",
        "other", "than", "then", "now", "look", "only", "come", "its", "over", "think", "also", "back",
        "after", "use", "two", "how", "our", "work", "first", "well", "way", "even", "new", "want",
        
        # Programming terms
        "python", "java", "javascript", "html", "css", "code", "programming", "develop", "software",
        "function", "method", "class", "object", "variable", "string", "integer", "float", "boolean",
        "array", "list", "dictionary", "tuple", "set", "loop", "if", "else", "while", "for", "return",
        "import", "export", "require", "module", "package", "library", "framework", "api", "json", "xml",
        "database", "sql", "nosql", "query", "server", "client", "frontend", "backend", "fullstack",
        "web", "app", "mobile", "desktop", "cloud", "deploy", "development", "production", "testing",
        "debug", "error", "exception", "try", "catch", "finally", "async", "await", "promise", "callback",
        
        # Words starting with "crea"
        "create", "creating", "created", "creation", "creative", "creativity", "creator", "creature",
        "creamy", "creaky", "creak", "cream", "creamy", "creampuff", "creamsicle",
        
        # Streamlit specific
        "streamlit", "st", "sidebar", "button", "text", "input", "slider", "checkbox", "radio",
        "selectbox", "multiselect", "number", "text_input", "text_area", "date_input", "time_input",
        "file_uploader", "color_picker", "progress", "spinner", "balloons", "error", "warning", "info",
        "success", "exception", "markdown", "latex", "code", "echo", "container", "columns", "expander",
        "header", "subheader", "title", "write", "metric", "dataframe", "table", "image", "audio", "video",
        
        # AI and ML terms
        "machine", "learning", "artificial", "intelligence", "neural", "network", "deep", "learning",
        "tensorflow", "pytorch", "keras", "scikit", "numpy", "pandas", "matplotlib", "seaborn", "plotly",
        "visualization", "analysis", "analytics", "statistic", "statistical", "regression", "classification",
        "clustering", "dimensionality", "reduction", "feature", "extraction", "selection", "engineering",
        "preprocessing", "postprocessing", "training", "validation", "testing", "inference", "prediction",
        "accuracy", "precision", "recall", "f1", "score", "loss", "gradient", "descent", "backpropagation",
        "optimization", "optimizer", "momentum", "learning", "rate", "epoch", "batch", "normalization",
        "regularization", "dropout", "activation", "sigmoid", "tanh", "relu", "transformer", "attention",
        "bert", "gpt", "nlp", "natural", "language", "processing", "computer", "vision", "reinforcement",
        
        # Additional tech terms
        "algorithm", "api", "architecture", "async", "authentication", "automation", "bandwidth", "binary",
        "blockchain", "browser", "buffer", "bug", "cache", "cloud", "cluster", "compiler", "component",
        "concurrent", "configuration", "container", "cookie", "cpu", "dashboard", "data", "database",
        "debug", "deployment", "design", "developer", "devops", "distributed", "docker", "documentation",
        "dom", "encryption", "endpoint", "engine", "environment", "event", "exception", "execution",
        "expression", "extension", "firewall", "framework", "frontend", "function", "gateway", "git",
        "github", "gradle", "graph", "hardware", "hash", "header", "heap", "hosting", "http", "https",
        "ide", "image", "index", "inheritance", "integration", "interface", "interpreter", "iteration",
        "jenkins", "json", "kernel", "key", "kubernetes", "lambda", "latency", "library", "lifecycle",
        "load", "localhost", "logger", "logic", "loop", "maven", "memory", "message", "metadata",
        "method", "microservice", "middleware", "model", "module", "monitoring", "multithreading",
        "namespace", "native", "network", "node", "npm", "object", "oriented", "parameter", "parser",
        "pattern", "pipeline", "platform", "plugin", "pointer", "polymorphism", "port", "process", 
        "protocol", "prototype", "proxy", "query", "queue", "react", "recursion", "redis", "regex",
        "repository", "request", "response", "rest", "router", "runtime", "schema", "scope", "script",
        "sdk", "security", "serialization", "server", "service", "session", "socket", "software", "source",
        "spring", "sql", "stack", "standard", "storage", "stream", "string", "struct", "syntax", "system",
        "template", "terminal", "test", "thread", "token", "transaction", "type", "ui", "update", "url",
        "user", "validation", "value", "variable", "vector", "version", "view", "virtual", "web", "webpack",
        "webhook", "websocket", "workflow", "xml", "yaml"
    ]
    
    # Add more word variations
    more_words = []
    for word in words:
        if len(word) > 4:
            if not word.endswith('s'):
                more_words.append(word + "s")  # Plural
            if not word.endswith('ing'):
                if word.endswith('e'):
                    more_words.append(word[:-1] + "ing")  # Gerund for words ending in 'e'
                else:
                    more_words.append(word + "ing")  # Gerund
            if not word.endswith('ed'):
                if word.endswith('e'):
                    more_words.append(word + "d")  # Past tense for words ending in 'e'
                elif word[-1] not in ['y']:
                    more_words.append(word + "ed")  # Past tense
    
    words.extend(more_words)
    return list(set(words))  # Remove duplicates

# Find matching words with frequency ranking
def find_matching_words(partial_word, word_list, max_suggestions=5):
    """Find words that start with the given partial word"""
    if not partial_word or len(partial_word) < 1:  # Reduced to 1 character for faster suggestions
        return []
    
    partial_word = partial_word.lower()
    
    # Primary exact matches (case insensitive)
    primary_matches = [word for word in word_list if word.lower().startswith(partial_word)]
    
    # Sort by length and then alphabetically for better user experience
    primary_matches.sort(key=lambda x: (len(x), x))
    
    return primary_matches[:max_suggestions]

# Performance metrics tracking
if 'suggestion_times' not in st.session_state:
    st.session_state.suggestion_times = []

# Layout with two columns for better use of space
col1, col2 = st.columns([3, 1])

with col1:
    # Initialize vocabulary
    start_time = time.time()
    vocabulary = load_large_vocabulary()
    load_time = time.time() - start_time
    
    # Main text input with key events handling
    st.markdown("### Start typing to see word suggestions")
    user_input = st.text_area("", height=200, key="user_input")
    
    # Get current input and update suggestions
    if user_input:
        # Split text to get the last word being typed
        words = re.findall(r'\b\w+\b|\S', user_input)
        current_word = words[-1] if words else ""
        
        # Get suggestions with timing
        start_time = time.time()
        suggestions = find_matching_words(current_word, vocabulary, max_suggestions=8)
        suggestion_time = time.time() - start_time
        
        if suggestion_time > 0:  # Only track non-zero times
            st.session_state.suggestion_times.append(suggestion_time)
        
        # Display suggestions
        if suggestions:
            st.subheader("Suggestions:")
            # Create a more compact UI for suggestions
            buttons_per_row = 4
            for i in range(0, len(suggestions), buttons_per_row):
                cols = st.columns(buttons_per_row)
                for j, col in enumerate(cols):
                    idx = i + j
                    if idx < len(suggestions):
                        suggestion = suggestions[idx]
                        if col.button(suggestion, key=f"sugg_{idx}"):
                            # Create a new text with the suggestion
                            if words:
                                new_words = words[:-1] + [suggestion]
                                new_text = " ".join(new_words) + " "  # Add space at the end
                                # Use JavaScript to update the text area
                                js = f"""
                                <script>
                                    var textareas = window.parent.document.querySelectorAll('textarea');
                                    for (var i = 0; i < textareas.length; i++) {{
                                        if (textareas[i].value.includes("{user_input}")) {{
                                            textareas[i].value = "{new_text}";
                                            var event = new Event('input', {{ bubbles: true }});
                                            textareas[i].dispatchEvent(event);
                                        }}
                                    }}
                                </script>
                                """
                                st.components.v1.html(js, height=0)

with col2:
    # Instructions
    st.markdown("### How to use")
    st.markdown("""
    1. Type text in the text area
    2. As you type, suggestions appear below
    3. Click on a suggestion to complete the word
    4. Continue typing your text
    """)
    
    # Performance metrics
    st.markdown("### Performance")
    st.markdown(f"**Dictionary size:** {len(vocabulary)} words")
    st.markdown(f"**Dictionary load time:** {load_time:.4f} seconds")
    
    if st.session_state.suggestion_times:
        avg_time = sum(st.session_state.suggestion_times) / len(st.session_state.suggestion_times)
        st.markdown(f"**Average suggestion time:** {avg_time:.4f} seconds")
    
    # Settings
    st.markdown("### Settings")
    max_suggestions = st.slider("Max suggestions to show", 3, 12, 8)

# Footer
st.markdown("---")
st.markdown("Real-Time Word Suggester - Fast typing assistance for programmers and writers")
