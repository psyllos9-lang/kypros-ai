import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="Σύγχρονος Κυπριακός Βοηθός",
    page_icon="🇨🇾",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom High-Tech Styling
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
        <h1>Chat 🇨🇾</h1>
        <p>Ο ρυθμός και η φάση όπως μιλάμε σήμερα στην Κύπρο</p>
    </div>
""", unsafe_allow_html=True)

# Automatic API Key loading from Streamlit Secrets
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = ""

# Sidebar for Controls
with st.sidebar:
    st.markdown("### ⚙️ Ρυθμίσεις Συστήματος")
    st.info("💡 Τρέχει με Groq AI, εντελώς ελεύθερα και γρήγορα!")
    
    st.markdown("---")
    if st.button("🗑️ Καθαρισμός Συνομιλίας", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #8b949e; font-size: 0.8rem;'>Powered by Groq & Streamlit</p>", unsafe_allow_html=True)

if not api_key:
    st.error("⚠️ Πρόσθεσε το GROQ_API_KEY στα Secrets του Streamlit.")
    st.stop()

# Initialize Groq Client
client = Groq(api_key=api_key)

# Modern Cypriot Style System Prompt (Η σύγχρονη καθημερινή γλώσσα 15-50 ετών)
modern_cypriot_instruction = (
    "Μιλάς όπως μιλάει ένας τυπικός Κύπριος ηλικίας 15 έως 50 ετών στην καθημερινότητά του το 2026. "
    "Ο τρόπος σου είναι εντελώς φυσικός, χαλαρός και σύγχρονος. "
    "Χρησιμοποιείς φυσικά στοιχεία της καθομιλουμένης (π.χ. 'τζιαι', 'εν', 'εννα', 'κάμνω', 'πκάλα', 'ρε φίλε', 'τζιεκ', 'φάση'), "
    "αλλά χωρίς υπερβολές και χωρίς να το παρακάνεις με παλιές, βαριές εκφράσεις που δεν χρησιμοποιεί ο κόσμος σήμερα. "
    "Απαντάς άμεσα, έξυπνα και στην ουσία, σαν να μιλάς με έναν φίλο σου."
)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Έλα! Τι παίζει; Πώς μπορώ να σε βοηθήσω σήμερα;"}
    ]

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Γράψε κάτι..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("*Για δες...*")
        
        try:
            formatted_messages = [{"role": "system", "content": modern_cypriot_instruction}]
            for m in st.session_state.messages:
                formatted_messages.append({"role": m["role"], "content": m["content"]})
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=formatted_messages,
                temperature=0.75,
                max_tokens=1024,
            )
            
            bot_reply = completion.choices[0].message.content
            message_placeholder.markdown(bot_reply)
            
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            error_msg = f"⚠️ Παρουσιάστηκε σφάλμα: {e}"
            message_placeholder.markdown(error_msg)
