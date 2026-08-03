import streamlit as st
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(
    page_title="Έι Άι 🇨🇾 - Κυπριακός AI Βοηθός",
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
        <p>Ο πλήρως εξελιγμένος βοηθός σου με ζωντανή αναζήτηση Google</p>
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
        ["gemini-2.5-flash", "gemini-2.5-pro"],
        help="Επιλέξτε μοντέλο."
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

# Initialize the new GenAI Client
client = genai.Client(api_key=api_key)

# Cypriot System Prompt
cypriot_instruction = (
    "Εσείσαι ένας σύγχρονος, πανέξυπνος, φιλικός και ντόπιος Κύπριος ψηφιακός βοηθός. "
    "Μιλάς ΑΠΟΚΛΕΙΣΤΙΚΑ και ΦΥΣΙΚΑ στη σύγχρονη κυπριακή διάλεκτο της καθημερινότητας (με λέξεις όπως 'εν', 'τζιαι', 'κοπέλι', 'κάμνω', 'εννα', 'έσιει', 'λαλείς'). "
    "Όταν σε ρωτούν για νέα, ειδήσεις ή γεγονότα, αξιοποιείς τα στοιχεία από το ίντερνετ και τα παρουσιάζεις στα κυπριακά."
)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Έλα κοπέλι! Τι χαμπάρια; Είμαι έτοιμος να ψάξω ό,τι θες στο ίντερνετ!"}
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
        message_placeholder.markdown("*Ψάχνει στο ίντερνετ...*")
        
        try:
            # We configure the model with Google Search grounding enabled
            config = types.GenerateContentConfig(
                system_instruction=cypriot_instruction,
                tools=[types.Tool(google_search=types.GoogleSearch())],
                temperature=0.7
            )
            
            # Format chat history for the new SDK
            contents = []
            for m in st.session_state.messages:
                role = "user" if m["role"] == "user" else "model"
                contents.append(types.Content(role=role, parts=[types.Part.from_text(text=m["content"])]))
            
            response = client.models.generate_content(
                model=model_choice,
                contents=contents,
                config=config
            )
            
            bot_reply = response.text
            message_placeholder.markdown(bot_reply)
            
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            error_msg = f"⚠️ Παρουσιάστηκε σφάλμα: {e}"
            message_placeholder.markdown(error_msg)
