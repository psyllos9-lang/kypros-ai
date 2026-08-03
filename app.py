import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Page Configuration
st.set_page_config(
    page_title="Έι Άι 🇨🇾 - Απεριόριστος Κυπριακός AI Βοηθός",
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
        <h1>Έι Άι 🇨🇾</h1>
        <p>Ανεξάρτητος, δωρεάν βοηθός χωρίς όρια χρήσης</p>
    </div>
""", unsafe_allow_html=True)

# Load Local Open-Source Model (Cached so it loads only once)
@st.cache_resource
def load_model():
    model_name = "Qwen/Qwen2.5-1.5B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True
    )
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=512)
    return pipe

with st.spinner("Φρτάρει το μοντέλο AI... (αυτό γίνεται μόνο στην πρώτη εκκίνηση)"):
    chatbot_pipeline = load_model()

# Sidebar for Controls
with st.sidebar:
    st.markdown("### ⚙️ Ρυθμίσεις Συστήματος")
    st.info("💡 Αυτή η εφαρμογή τρέχει με ανοιχτό κώδικα AI και **δεν έχει κανένα όριο (no rate limits)**!")
    
    st.markdown("---")
    if st.button("🗑️ Καθαρισμός Συνομιλίας", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #8b949e; font-size: 0.8rem;'>Powered by Open-Source & Streamlit</p>", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Έλα κοπέλι! Είμαι εντελώς ελεύθερος και έτοιμος για όσες ερωτήσεις θες, χωρίς περιορισμούς!"}
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
            # Build prompt keeping persona context
            system_prompt = (
                "Εσείσαι ένας σύγχρονος, πανέξυπνος, φιλικός και ντόπιος Κύπριος ψηφιακός βοηθός. "
                "Μιλάς ΑΠΟΚΛΕΙΣΤΙΚΑ και ΦΥΣΙΚΑ στη σύγχρονη κυπριακή διάλεκτο της καθημερινότητας "
                "(με λέξεις όπως 'εν', 'τζιαι', 'κοπέλι', 'κάμνω', 'εννα', 'έσιει', 'λαλείς').\n\n"
            )
            
            # Construct conversation history for Qwen format
            full_prompt = system_prompt
            for m in st.session_state.messages:
                role = "User" if m["role"] == "user" else "Assistant"
                full_prompt += f"{role}: {m['content']}\n"
            full_prompt += "Assistant: "

            # Generate response locally
            outputs = chatbot_pipeline(full_prompt, do_sample=True, temperature=0.7, top_p=0.9)
            raw_output = outputs[0]['generated_text']
            
            # Clean up output to isolate assistant reply
            if "Assistant: " in raw_output:
                bot_reply = raw_output.split("Assistant: ")[-1].strip()
            else:
                bot_reply = raw_output.replace(full_prompt, "").strip()

            message_placeholder.markdown(bot_reply)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            error_msg = f"⚠️ Παρουσιάστηκε σφάλμα: {e}"
            message_placeholder.markdown(error_msg)
