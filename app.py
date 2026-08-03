import streamlit as st
import requests
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="Έι Άι // Voice & Vision Edition",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Professional Futuristic Styling
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
        background: linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        font-weight: 700;
        color: #ffffff;
        box-shadow: 0 8px 20px rgba(236, 72, 153, 0.3);
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
            <p>Voice & Vision Intelligence // 2026</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sidebar Controls & Mode Selection
with st.sidebar:
    st.markdown("### ⚙️ ΠΙΝΑΚΑΣ ΕΛΕΓΧΟΥ")
    app_mode = st.radio("Λειτουργία:", ["💬 Συνομιλία & Φωνή (Chat/Voice)", "🎨 Δημιουργία Εικόνας (Image Gen)"])
    
    st.info("🎙️ Tip: Κάθε απάντηση του AI συνοδεύεται από audio player για να την ακούς φωνητικά!")
    
    st.markdown("---")
    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ", use_container_width=True):
        if "messages" in st.session_state:
            st.session_state.messages = []
        st.rerun()

# Mode 1: Image Generation
if app_mode == "🎨 Δημιουργία Εικόνας (Image Gen)":
    st.markdown("### 🎨 Δημιουργία Φωτογραφίας")
    st.write("Γράψε τι εικόνα θέλεις να δημιουργήσει η τεχνητή νοημοσύνη:")
    
    img_prompt = st.text_input("Περιγραφή εικόνας (π.χ., A futuristic cyberpunk car in Limassol):")
    
    if st.button("Δημιουργία Εικόνας", use_container_width=True):
        if img_prompt:
            with st.spinner("Δημιουργείται η εικόνα σου..."):
                try:
                    encoded_prompt = requests.utils.quote(img_prompt)
                    img_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
                    
                    response = requests.get(img_url)
                    if response.status_code == 200:
                        st.image(img_url, caption=f"Prompt: {img_prompt}", use_container_width=True)
                    else:
                        st.error("⚠️ Αποτυχία φόρτωσης εικόνας.")
                except Exception as e:
                    st.error(f"Σφάλμα: {e}")
        else:
            st.warning("⚠️ Παρακαλώ γράψε μια περιγραφή.")

# Mode 2: Chat Assistant with Text & Voice Output
else:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        api_key = ""

    if not api_key:
        st.error("⚠️ Παρακαλώ προσθέστε το GROQ_API_KEY στα Secrets του Streamlit (από το console.groq.com).")
        st.stop()

    client = Groq(api_key=api_key)

    system_instruction = (
        "Εσείς είστε ένας σύγχρονος, έξυπνος και φιλικός ψηφιακός βοηθός. "
        "Μιλάς όπως μιλάει ένας τυπικός Κύπριος ηλικίας 15 έως 50 ετών στην καθημερινότητά του το 2026. "
        "Ο τρόπος σου είναι εντελώς φυσικός, χαλαρός και σύγχρονος, χρησιμοποιώντας στοιχεία της καθομιλουμένης (π.χ. 'τζιαι', 'εν', 'εννα', 'κάμνω', 'φάση', 'ρε φίλε'), "
        "αλλά χωρίς υπερβολές και χωρίς παλιές, βαριές εκφράσεις. "
        "Απαντάς άμεσα, έξυπνα και στην ουσία, σαν να μιλάς με έναν φίλο."
    )

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Έλα! Τι παίζει; Πώς μπορώ να σε βοηθήσω σήμερα;"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant":
                tts_html = f"""
                    <audio controls style="height: 30px; margin-top: 5px;">
                      <source src="https://translate.google.com/translate_tts?ie=UTF-8&q={requests.utils.quote(message['content'][:200])}&tl=el&client=tw-ob" type="audio/mpeg">
                    </audio>
                """
                st.markdown(tts_html, unsafe_allow_html=True)

    if prompt := st.chat_input("Γράψε ένα μήνυμα..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("*Σκεφτούμαι...*")
            
            try:
                formatted_messages = [{"role": "system", "content": system_instruction}]
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
                
                tts_html = f"""
                    <audio controls autoplay style="height: 30px; margin-top: 5px;">
                      <source src="https://translate.google.com/translate_tts?ie=UTF-8&q={requests.utils.quote(bot_reply[:200])}&tl=el&client=tw-ob" type="audio/mpeg">
                    </audio>
                """
                st.markdown(tts_html, unsafe_allow_html=True)
                
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                
            except Exception as e:
                message_placeholder.markdown(f"⚠️ Σφάλμα: {e}")
