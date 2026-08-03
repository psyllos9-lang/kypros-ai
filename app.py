import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="Έι Άι // Professional Intelligence",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Sleek, Professional & Futuristic Glassmorphism Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #111827 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f3f4f6;
    }
    
    /* Professional Logo Header */
    .brand-container {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 1rem 0 1.2rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 2rem;
    }
    .brand-logo-box {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        font-weight: 700;
        color: #ffffff;
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
        letter-spacing: -0.5px;
    }
    .brand-text h1 {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
        color: #ffffff;
        letter-spacing: -0.5px;
    }
    .brand-text p {
        font-size: 0.8rem;
        color: #9ca3af;
        margin: 0;
        font-weight: 400;
    }

    /* Chat Input Styling */
    .stChatInputContainer input {
        background-color: rgba(17, 24, 39, 0.9) !important;
        color: #f3f4f6 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
        padding: 0.8rem 1rem !important;
    }
    .stChatInputContainer input:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.2) !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Logo & Branding Header (Εμφανίζει το λογότυπο Έι Άι)
st.markdown("""
    <div class="brand-container">
        <div class="brand-logo-box">AI</div>
        <div class="brand-text">
            <h1>Έι Άι</h1>
            <p>Σύγχρονος Ψηφιακός Βοηθός // 2026</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Automatic API Key loading from Streamlit Secrets
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = ""

# Sidebar for Controls
with st.sidebar:
    st.markdown("### ⚙️ ΠΙΝΑΚΑΣ ΕΛΕΓΧΟΥ")
    st.info("✨ Η πλατφόρμα λειτουργεί με υψηλές ταχύτητες και χωρίς περιορισμούς.")
    
    st.markdown("---")
    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #4b5563; font-size: 0.75rem;'>SECURE ENTERPRISE LINK</p>", unsafe_allow_html=True)

if not api_key:
    st.error("⚠️ Σφάλμα: Δεν βρέθηκε το GROQ_API_KEY στα Secrets του Streamlit.")
    st.stop()

# Initialize Groq Client
client = Groq(api_key=api_key)

# Modern Style System Prompt (Η σύγχρονη καθημερινή γλώσσα 15-50 ετών)
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
if prompt := st.chat_input("Γράψε ένα μήνυμα..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("*Σκέφτομαι...*")
        
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
            error_msg = f"⚠️ Σφάλμα συστήματος: {e}"
            message_placeholder.markdown(error_msg)
