import streamlit as st
import re

# Setup
st.set_page_config(page_title="Fast Word Suggester", page_icon="⌨️")
st.title("Fast Word Suggester")

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
    "creamy", "creaky", "creak", "cream", "creamy", "creampuff", "creampie", "creamsicle",

    # Words starting with common prefixes
    "program", "programmer", "programming", "programmatic", "programmatically",
    "develop", "developer", "development", "developing", "developed",
    "implement", "implementation", "implementing", "implemented", "implementer",
    "design", "designer", "designing", "designed", "designate",
    "build", "builder", "building", "built", "buildable",
    "algorithm", "algorithmic", "algorithmically",
    "data", "database", "datatype", "dataset", "datapoint", "datamine",

    # Streamlit specific
    "streamlit", "st", "sidebar", "button", "text", "input", "slider", "checkbox", "radio",
    "selectbox", "multiselect", "number", "text_input", "text_area", "date_input", "time_input",
    "file_uploader", "color_picker", "progress", "spinner", "balloons", "error", "warning", "info",
    "success", "exception", "markdown", "latex", "code", "echo", "container", "columns", "expander",
    "beta_columns", "beta_container", "beta_expander", "header", "subheader", "title", "write",

    # Additional programming concepts
    "machine", "learning", "artificial", "intelligence", "neural", "network", "deep", "learning",
    "tensorflow", "pytorch", "keras", "scikit", "numpy", "pandas", "matplotlib", "seaborn", "plotly",
    "visualization", "analysis", "analytics", "statistic", "statistical", "regression", "classification",
    "clustering", "dimensionality", "reduction", "feature", "extraction", "selection", "engineering",
    "preprocessing", "postprocessing", "training", "validation", "testing", "inference", "prediction",
    "accuracy", "precision", "recall", "f1", "score", "loss", "function", "gradient", "descent",
    "backpropagation", "optimization", "optimizer", "momentum", "learning", "rate", "epoch", "batch",
    "normalization", "regularization", "dropout", "activation", "function", "sigmoid", "tanh", "relu",

    # Business & Entrepreneurship
    "entrepreneur", "startup", "founder", "business", "enterprise", "venture", "funding", "investment",
    "capital", "revenue", "profit", "loss", "scalability", "market", "branding", "advertising",
    "sales", "customer", "negotiation", "pitch", "valuation", "equity", "synergy", "networking",
    "strategy", "growth", "disruption", "innovation", "leadership", "management", "B2B", "B2C",
    "subscription", "ecommerce", "retail", "supply", "logistics", "franchise", "monopoly", "merger",
    "acquisition", "partnership", "stakeholder", "angel", "venture", "bootstrapping", "ROI", "scalable",
    "marketing", "conversion", "customer", "retention", "incubator", "accelerator", "crowdfunding",
    "benchmark", "blueprint", "competitive", "consumer", "pricing", "brand", "loyalty", "product",
    "services", "outsourcing", "consulting", "freelance", "gig", "influencer", "affiliate", "BPM", "KPI",
    "lean", "MVP", "SaaS", "IPO", "monetization",

    # Entertainment & Culture
    "cinema", "film", "screenplay", "director", "producer", "acting", "cast", "theater", "script",
    "blockbuster", "indie", "festival", "documentary", "animation", "VFX", "soundtrack", "binge",
    "streaming", "remix", "concert", "performance", "lyric", "album", "composition", "orchestra",
    "symphony", "choreography", "dance", "art", "exhibition", "museum", "mythology", "folklore",
    "narrative", "character", "plot", "twist", "climax", "sequel", "prequel", "trilogy", "franchise",
    "cinematography", "editing", "CGI", "voiceover", "dubbing", "genre", "satire",

    # Science & Technology
    "physics", "chemistry", "biology", "genetics", "biotechnology", "nanotechnology", "robotics",
    "quantum", "neuroscience", "hypothesis", "theory", "experiment", "observation", "ecosystem",
    "evolution", "dark matter", "astrophysics", "singularity", "exoplanet",

    # Health & Wellness
    "nutrition", "diet", "fitness", "exercise", "calories", "macronutrients", "metabolism",
    "endurance", "immunity", "epidemiology", "pandemic", "prognosis", "therapy", "cognition",
    "mental health", "well-being", "resilience", "self-care", "wellness", "mindfulness",
    "vaccination", "microbiome", "pathology", "cardiology", "neurology", "oncology",
]
    
    # Add more word variations
    more_words = []
    for word in words:
        if len(word) > 4:
            more_words.append(word + "s")  # Plural
            more_words.append(word + "ing")  # Gerund
            if word[-1] not in ['e', 'y']:
                more_words.append(word + "ed")  # Past tense
    
    words.extend(more_words)
    return list(set(words))  # Remove duplicates

# Find matching words
def find_matching_words(partial_word, word_list, max_suggestions=5):
    """Find words that start with the given partial word"""
    if not partial_word or len(partial_word) < 2:
        return []
    
    partial_word = partial_word.lower()
    matching = [word for word in word_list if word.lower().startswith(partial_word)]
    
    # Sort by length (shorter words first) for better user experience
    matching.sort(key=len)
    
    return matching[:max_suggestions]

# Initialize vocabulary
vocabulary = load_large_vocabulary()

# Main text input
st.text_area("Type here:", height=150, key="user_input")

# Get current input and update suggestions
user_input = st.session_state.get("user_input", "")

# Split text to get the last word being typed
words = re.findall(r'\b\w+\b|\S', user_input)
current_word = words[-1] if words else ""

# Get suggestions
suggestions = find_matching_words(current_word, vocabulary)

# Display suggestions
if suggestions:
    st.subheader("Suggestions:")
    cols = st.columns(min(len(suggestions), 5))
    
    for i, suggestion in enumerate(suggestions):
        if cols[i].button(suggestion, key=f"sugg_{i}"):
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

  
