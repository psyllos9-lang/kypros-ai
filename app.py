import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from PIL import Image
import requests
import io

# Page Configuration
st.set_page_config(
    page_title="Έι Άι // Unlimited Free Edition",
    page_icon="⚡",
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
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        font-weight: 700;
        color: #ffffff;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
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
            <p>100% Free & Unlimited Open Source</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sidebar Controls & Mode Selection
with st.sidebar:
    st.markdown("### ⚙️ ΠΙΝΑΚΑΣ ΕΛΕΓΧΟΥ")
    app_mode = st.radio("Λειτουργία:", ["💬 Έξυπνη Συνομιλία (Chat)", "🎨 Δημιουργία Εικόνας (Image Gen)"])
    
    st.info("💡 Χωρίς API keys, χωρίς χρεώσεις, εντελώς απεριόριστη χρήση (No Rate Limits).")
    
    st.markdown("---")
    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ", use_container_width=True):
        if "messages" in st.session_state:
            st.session_state.messages = []
        st.rerun()

# Load Local Open-Source Chat Model (Cached)
@st.cache_resource
def load_chat_model():
    model_name = "Qwen/Qwen2.5-1.5B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True
    )
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=512)
    return pipe

# Mode 1: Image Generation (Free & Unlimited via Pollinations)
if app_mode == "🎨 Δημιουργία Εικόνας (Image Gen)":
    st.markdown("### 🎨 Δημιουργία Φωτογραφίας μέσω AI")
    st.write("Γράψε τι εικόνα θέλεις να δημιουργήσεις:")
    
    img_prompt = st.text_input("Περιγραφή (π.χ., A futuristic cyberpunk car in Limassol):")
    
    if st.button("Δημιουργία", use_container_width=True):
        if img_prompt:
            with st.spinner("Δημιουργείται η εικόνα σου..."):
                try:
                    encoded_prompt = requests.utils.quote(img_prompt)
                    img_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
                    
                    response = requests.get(img_url)
                    if response.status_code == 200:
                        image = Image.open(io.BytesIO(response.content))
                        st.image(image, caption=img_prompt, use_container_width=True)
                    else:
                        st.error("⚠️ Αποτυχία φόρτωσης εικόνας.")
                except Exception as e:
                    st.error(f"Σφάλμα: {e}")
        else:
            st.warning("⚠️ Παρακαλώ γράψε μια περιγραφή.")

# Mode 2: Unlimited Local Chat Assistant
else:
    with st.spinner("Φόρτωση τοπικού μοντέλου AI... (γίνεται μόνο στην πρώτη εκκίνηση)"):
        chatbot_pipeline = load_chat_model()

    system_instruction = (
        "Εσείς είστε ένας σύγχρονος, έξυπνος και αξιόπιστος ψηφιακός βοηθός. "
        "Μιλάς όπως μιλάει ένας τυπικός Κύπριος ηλικίας 15 έως 50 ετών στην καθημερινότητά του (2026): "
        "φυσικά, χαλαρά, χρησιμοποιώντας στοιχεία της καθομιλουμένης (π.χ. 'τζιαι', 'εν', 'εννα', 'κάμνω', 'φάση', 'ρε φίλε'), "
        "αλλά χωρίς υπερβολές και χωρίς παλιές, βαριές εκφράσεις. "
        "Δίνεις σωστες, καθαρές και άμεσες απαντήσεις."
    )

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Έλα! Τι παίζει; Πώς μπορώ να σε βοηθήσω σήμερα;"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Γράψε ένα μήνυμα..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("*Σκεφτούμαι...*")
            
            try:
                full_prompt = f"System: {system_instruction}\n"
                for m in st.session_state.messages:
                    role = "User" if m["role"] == "user" else "Assistant"
                    full_prompt += f"{role}: {m['content']}\n"
                full_prompt += "Assistant: "

                outputs = chatbot_pipeline(full_prompt, do_sample=True, temperature=0.5, top_p=0.9)
                raw_output = outputs[0]['generated_text']
                
                if "Assistant: " in raw_output:
                    bot_reply = raw_output.split("Assistant: ")[-1].strip()
                else:
                    bot_reply = raw_output.replace(full_prompt, "").strip()

                message_placeholder.markdown(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                
            except Exception as e:
                message_placeholder.markdown(f"⚠️ Σφάλμα: {e}")
