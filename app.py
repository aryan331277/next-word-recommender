import streamlit as st
import re

# Setup
st.set_page_config(page_title="Word Suggester", page_icon="⌨️")
st.title("Fast Word Suggester")

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
    
    # Create proper word forms following English spelling rules
    # Define irregular words and words that don't need certain forms
    irregular_plurals = {
        "man": "men", "woman": "women", "child": "children", "foot": "feet", "tooth": "teeth",
        "goose": "geese", "mouse": "mice", "ox": "oxen", "person": "people", "leaf": "leaves",
        "life": "lives", "wife": "wives", "wolf": "wolves", "elf": "elves", "loaf": "loaves",
        "potato": "potatoes", "tomato": "tomatoes", "echo": "echoes", "hero": "heroes", 
        "torpedo": "torpedoes", "veto": "vetoes", "criterion": "criteria", "datum": "data",
        "analysis": "analyses", "crisis": "crises", "thesis": "theses", "phenomenon": "phenomena", 
        "index": "indices", "matrix": "matrices", "vertex": "vertices", "medium": "media",
        "formula": "formulae", "cactus": "cacti", "focus": "foci", "nucleus": "nuclei",
        "syllabus": "syllabi", "fungus": "fungi", "radius": "radii"
    }
    
    # Words that don't follow standard rules for past tense
    irregular_verbs = {
        "be": ["am", "is", "are", "was", "were", "been", "being"],
        "have": ["has", "had", "having"],
        "do": ["does", "did", "done", "doing"],
        "say": ["says", "said", "saying"],
        "make": ["makes", "made", "making"],
        "go": ["goes", "went", "gone", "going"],
        "take": ["takes", "took", "taken", "taking"],
        "come": ["comes", "came", "coming"],
        "see": ["sees", "saw", "seen", "seeing"],
        "know": ["knows", "knew", "known", "knowing"],
        "get": ["gets", "got", "gotten", "getting"],
        "give": ["gives", "gave", "given", "giving"],
        "find": ["finds", "found", "finding"],
        "think": ["thinks", "thought", "thinking"],
        "tell": ["tells", "told", "telling"],
        "run": ["runs", "ran", "running"],
        "bring": ["brings", "brought", "bringing"],
        "buy": ["buys", "bought", "buying"],
        "catch": ["catches", "caught", "catching"],
        "teach": ["teaches", "taught", "teaching"],
        "eat": ["eats", "ate", "eaten", "eating"],
        "put": ["puts", "putting"],
        "read": ["reads", "reading"],  # Same spelling for present and past
        "begin": ["begins", "began", "begun", "beginning"],
        "write": ["writes", "wrote", "written", "writing"],
        "sing": ["sings", "sang", "sung", "singing"],
        "speak": ["speaks", "spoke", "spoken", "speaking"],
        "swim": ["swims", "swam", "swum", "swimming"],
        "stand": ["stands", "stood", "standing"]
    }
    
    # Words that are already plural or don't have a typical plural form
    non_plurals = {
        "physics", "mathematics", "economics", "news", "politics", "statistics", "ethics",
        "series", "species", "deer", "sheep", "fish", "means", "offspring", "scissors", 
        "pants", "trousers", "glasses", "binoculars", "clothes", "thanks", "jeans", 
        "pliers", "shears", "shorts", "information", "knowledge", "furniture", "luggage",
        "equipment", "traffic", "advice", "progress", "research", "evidence", "music",
        "homework", "money", "cash", "happiness", "anger", "love", "courage", "honesty",
        "water", "air", "oil", "electricity", "software", "hardware", "data", "media","chemistry"
    }
    
    more_words = []
    for word in words:
        if len(word) > 3:  # Only process words of reasonable length
            # Handle plurals
            if word.lower() in non_plurals:
                # Don't add plural forms for these words
                pass
            elif word.lower() in irregular_plurals:
                more_words.append(irregular_plurals[word.lower()])
            elif word.endswith(('ch', 'sh', 's', 'x', 'z', 'o')):
                more_words.append(word + "es")
            elif word.endswith('y') and word[-2] not in 'aeiou':
                more_words.append(word[:-1] + "ies")
            elif word.endswith('f'):
                more_words.append(word[:-1] + "ves")
            elif word.endswith('fe'):
                more_words.append(word[:-2] + "ves")
            else:
                more_words.append(word + "s")
            
            # Handle verb forms (ing, ed, etc.)
            if word.lower() in irregular_verbs:
                more_words.extend(irregular_verbs[word.lower()])
            else:
                # Handle -ing form (gerund/present participle)
                if word.endswith('ie'):
                    more_words.append(word[:-2] + "ying")
                elif word.endswith('e') and not word.endswith(('ee', 'oe', 'ye')):
                    more_words.append(word[:-1] + "ing")
                # Double final consonant in certain cases
                elif (len(word) > 2 and 
                      word[-1] not in 'wy' and 
                      word[-1] in 'bcdfghjklmnpqrstvxz' and 
                      word[-2] in 'aeiou' and 
                      word[-3] not in 'aeiou'):
                    more_words.append(word + word[-1] + "ing")
                else:
                    more_words.append(word + "ing")
                
                # Handle -ed form (past tense/past participle)
                if word.endswith('e'):
                    more_words.append(word + "d")
                elif word.endswith('y') and word[-2] not in 'aeiou':
                    more_words.append(word[:-1] + "ied")
                # Double final consonant in certain cases
                elif (len(word) > 2 and 
                      word[-1] not in 'wy' and 
                      word[-1] in 'bcdfghjklmnpqrstvxz' and 
                      word[-2] in 'aeiou' and 
                      word[-3] not in 'aeiou'):
                    more_words.append(word + word[-1] + "ed")
                else:
                    more_words.append(word + "ed")
    
    # Add all words to the vocabulary and ensure uniqueness
    words.extend(more_words)
    unique_words = list(set(words))
    
    # Remove incorrect word forms for words we explicitly know about
    words_to_remove = []
    for word in unique_words:
        # Remove incorrect forms like "physicss", "physicsed", "physicsing"
        for non_plural in non_plurals:
            if word.startswith(non_plural + "s") or word.startswith(non_plural + "ed") or word.startswith(non_plural + "ing"):
                words_to_remove.append(word)
    
    return [w for w in unique_words if w not in words_to_remove]

def find_matching_words(partial_word, word_list, max_suggestions=5):
    """Find words that start with the given partial word"""
    if not partial_word or len(partial_word) < 2:
        return []
    
    partial_word = partial_word.lower()
    matching = [word for word in word_list if word.lower().startswith(partial_word)]
    
    matching.sort(key=len)
    
    return matching[:max_suggestions]

vocabulary = load_large_vocabulary()

st.text_area("Type here:", height=150, key="user_input")

user_input = st.session_state.get("user_input", "")

words = re.findall(r'\b\w+\b|\S', user_input)
current_word = words[-1] if words else ""

suggestions = find_matching_words(current_word, vocabulary)

if suggestions:
    st.subheader("Suggestions:")
    cols = st.columns(min(len(suggestions), 5))
    
    for i, suggestion in enumerate(suggestions):
        if cols[i].button(suggestion, key=f"sugg_{i}"):
            if words:
                new_words = words[:-1] + [suggestion]
                new_text = " ".join(new_words) + " "  
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
