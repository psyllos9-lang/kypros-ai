import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="Έι Άι // Accurate Assistant",
    page_icon="⚡",
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

    section[data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Logo & Branding Header
st.markdown("""
    <div class="brand-container">
        <div class="brand-logo-box">AI</div>
        <div class="brand-text">
            <h1>Έι Άι</h1>
            <p>High-Accuracy Assistant // 2026</p>
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
    st.info("⚡ Λειτουργία Υψηλής Ακρίβειας (Strict & Accurate Mode).")
    
    st.markdown("---")
    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #4b5563; font-size: 0.75rem;'>SECURE ENGINE</p>", unsafe_allow_html=True)

if not api_key:
    st.error("⚠️ Σφάλμα: Δεν βρέθηκε το GROQ_API_KEY στα Secrets του Streamlit.")
    st.stop()

# Initialize Groq Client
client = Groq(api_key=api_key)

# Strict & Accurate System Prompt (Αποφυγή ψευδών πληροφοριών / Hallucinations)
accurate_instruction = (
    "Είσαι ένας εξαιρετικά ακριβής, σοβαρός και αποτελεσματικός ψηφιακός βοηθός, σχεδιασμένος να δίνει τεκμηριωμένες, σωστές και ξεκάθαρες απαντήσεις, ακριβώς όπως το ChatGPT. "
    "Κανόνας 1: Μην εφευρίσκεις γεγονότα, στατιστικά ή πληροφορίες. Αν δεν γνωρίζεις κάτι με ακρίβεια, πες το ευθέως. "
    "Κανόνας 2: Απάντησε στη γλώσσα που σε ρωτά ο χρήστης (ελληνικά). "
    "Κανόνας 3: Μιλάς φυσικά, σύγχρονα, χωρίς υπερβολές, χωρίς περιττές τυπικότητες και χωρίς στημένες αργκό. "
    "Κανόνας 4: Δίνε άμεσες, δομημένες και ακριβείς απαντήσεις στην ουσία του ερωτήματος."
)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Γεια σου! Είμαι έτοιμος. Ποιο είναι το θέμα που θέλεις να δούμε;"}
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
        message_placeholder.markdown("*Αναζήτηση απάντησης...*")
        
        try:
            formatted_messages = [{"role": "system", "content": accurate_instruction}]
            for m in st.session_state.messages:
                formatted_messages.append({"role": m["role"], "content": m["content"]})
            
            # Χρήση του llama-3.1-8b-instant για μέγιστη ταχύτητα και ακρίβεια χωρίς ασυναρτησίες
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=formatted_messages,
                temperature=0.2,  # Χαμηλή θερμοκρασία για να είναι απόλυτα συγκεντρωμένο και ακριβές
                max_tokens=1500,
            )
            
            bot_reply = completion.choices[0].message.content
            message_placeholder.markdown(bot_reply)
            
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            error_msg = f"⚠️ Σφάλμα συστήματος: {e}"
            message_placeholder.markdown(error_msg)
