import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="AI Terminal | Cyber",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Futuristic Cyberpunk & Glassmorphism Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&display=swap');

    .stApp {
        background: radial-gradient(circle at 50% 0%, #0f172a 0%, #020617 100%);
        font-family: 'Space Grotesk', sans-serif;
        color: #f8fafc;
    }
    
    /* Logo / Brand Header */
    .brand-container {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 1rem 0 0.5rem 0;
        border-bottom: 1px solid rgba(56, 189, 248, 0.2);
        margin-bottom: 1.5rem;
    }
    .brand-logo {
        width: 42px;
        height: 42px;
        background: linear-gradient(135deg, #38bdf8 0%, #6366f1 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
    }
    .brand-title h2 {
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .brand-title p {
        font-size: 0.75rem;
        color: #94a3b8;
        margin: 0;
        letter-spacing: 1px;
    }

    /* Chat Input Styling */
    .stChatInputContainer input {
        background-color: rgba(15, 23, 42, 0.8) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 14px !important;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.5) !important;
    }
    .stChatInputContainer input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.3) !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #030712;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Logo & Branding Header (Εμφανίζεται στην κορυφή)
st.markdown("""
    <div class="brand-container">
        <div class="brand-logo">⚡</div>
        <div class="brand-title">
            <h2>NEXUS AI</h2>
            <p>CYBERNETIC ASSISTANT // 2026</p>
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
    st.markdown("### 🎛️ SYSTEM CONTROLS")
    st.info("⚡ System Online. Running on high-speed Groq inference without limits.")
    
    st.markdown("---")
    if st.button("🗑️ CLEAR MEMORY", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.75rem;'>SECURE PROTOCOL v4.2</p>", unsafe_allow_html=True)

if not api_key:
    st.error("⚠️ Error: GROQ_API_KEY missing in Streamlit Secrets.")
    st.stop()

# Initialize Groq Client
client = Groq(api_key=api_key)

# Modern Cypriot Style System Prompt
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
        message_placeholder.markdown("*Initializing response...*")
        
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
            error_msg = f"⚠️ System Error: {e}"
            message_placeholder.markdown(error_msg)
