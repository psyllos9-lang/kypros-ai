import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(
    page_title="Έι Άι 🇨🇾 - Κυπριακός AI Βοηθός",
    page_icon="🇨🇾",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom High-Tech Styling (ChatGPT / Claude Style)
st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }
    .chat-header {
        text-align: center;
        padding: 1.5rem 0;
        border-bottom: 1px solid #30363d;
        margin-bottom: 2rem;
    }
    .chat-header h1 {
        font-size: 2.2rem;
        font-weight: 700;
        color: #58a6ff;
        margin-bottom: 0.2rem;
    }
    .chat-header p {
        color: #8b949e;
        font-size: 1rem;
    }
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    .stChatInputContainer input {
        background-color: #161b22 !important;
        color: #e6edf3 !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
    <div class="chat-header">
        <h1>Έι Άι 🇨🇾</h1>
        <p>Ο σύγχρονος ψηφιακός βοηθός σου στην κυπριακή διάλεκτο</p>
    </div>
""", unsafe_allow_html=True)

# Automatic API Key loading from Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = ""

# Sidebar for Controls
with st.sidebar:
    st.markdown("### ⚙️ Ρυθμίσεις Συστήματος")
    model_choice = st.selectbox(
        "Επιλογή Μοντέλου AI:",
        ["gemini-3.5-flash", "gemini-2.5-pro"],
        help="Επιλέξτε ταχύτητα ή μέγιστη νοημοσύνη."
    )
    
    st.markdown("---")
    if st.button("🗑️ Καθαρισμός Συνομιλίας", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #8b949e; font-size: 0.8rem;'>Powered by Gemini & Streamlit</p>", unsafe_allow_html=True)

if not api_key:
    st.error("⚠️ Δεν έχει οριστεί το GEMINI_API_KEY στα Secrets του Streamlit.")
    st.stop()

# Configure GenAI
genai.configure(api_key=api_key)

# Strict Natural & Modern Cypriot System Prompt
CYPRIOT_SYSTEM_PROMPT = (
    "Εσείσαι ένας σύγχρονος, πανέξυπνος, φιλικός και ντόπιος Κύπριος ψηφιακός βοηθός. "
    "Μιλάς ΑΠΟΚΛΕΙΣΤΙΚΑ και ΦΥΣΙΚΑ στη σύγχρονη κυπριακή διάλεκτο της καθημερινότητας (με λέξεις όπως 'εν', 'τζιαι', 'κοπέλι', 'κάμνω', 'εννα', 'έσιει', 'λαλείς'). "
    "Απαγορεύεται αυστηρά να χρησιμοποιείς αρχαίες, λόγιες ή ψεύτικες εκφράσεις. "
    "Ο λόγος σου είναι απλός, άμεσος και καθαρός, ακριβώς όπως μιλάει ένας κανονικός Κύπριος σήμερα."
)

# Initialize Session State with a natural greeting
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Έλα κοπέλι! Τι χαμπάρια; Πώς μπορώ να σε βοηθήσω σήμερον;"}
    ]

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Λάλε μου κάτι..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("*Σκεφτούμαι...*")
        
        try:
            model = genai.GenerativeModel(
                model_name=model_choice,
                system_instruction=CYPRIOT_SYSTEM_PROMPT
            )
            
            chat_history = [
                {"role": m["role"] if m["role"] != "assistant" else "model", "parts": [m["content"]]}
                for m in st.session_state.messages[:-1]
            ]
            
            chat = model.start_chat(history=chat_history)
            response = chat.send_message(prompt)
            
            bot_reply = response.text
            message_placeholder.markdown(bot_reply)
            
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            error_msg = f"⚠️ Παρουσιάστηκε σφάλμα: {e}"
            message_placeholder.markdown(error_msg)
