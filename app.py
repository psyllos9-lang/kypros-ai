import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Έι Άι - Ο Κύπριος Βοηθός", page_icon="🇨🇾", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    h1 {
        text-align: center;
        color: #38bdf8;
        font-family: sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>Έι Άι 🇨🇾</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Ο προσωπικός σου ψηφιακός βοηθός στην κυπριακή διάλεκτο</p>", unsafe_allow_html=True)

st.sidebar.header("Ρυθμίσεις")
api_key = st.sidebar.text_input("Βάλτε το Google Gemini API Key σας:", type="password")

if not api_key:
    st.warning("⚠️ Παρακαλώ εισάγετε το API Key σας στην αριστερή μπάρα για να ξεκινήσετε.")
else:
    genai.configure(api_key=api_key)
    
    cyprus_system_instruction = """
    Είσαι το "Έι Άι", ένας ψηφιακός βοηθός φτιαγμένος στην Κύπρο. 
    Μιλάς πάντοτε και αποκλειστικά τη σύγχρονη κυπριακή διάλεκτο (χρησιμοποιείς φυσικές εκφράσεις όπως "τζιαι", "εν", "κοπέλι", "λάλε μου", "εν έσιει πρόβλημα", κ.λπ.). 
    Αν κάποιος σε ρωτήσει στα αγγλικά ή στα ελληνικά της Ελλάδας, εσύ απάντησε του μεταφέροντας το νόημα στα κυπριακά. 
    Μην φύγεις ποτέ από τον ρόλο σου ως Κύπριος βοηθός.
    """

    generation_config = {
        "temperature": 0.7,
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=cyprus_system_instruction,
        generation_config=generation_config
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Λάλε μου κάτι..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                chat_history = [
                    {"role": m["role"] if m["role"] == "user" else "model", "parts": [m["content"]]} 
                    for m in st.session_state.messages[:-1]
                ]
                chat = model.start_chat(history=chat_history)
                response = chat.send_message(prompt)
                
                bot_reply = response.text
                st.markdown(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            except Exception as e:
                st.error(f"Εγίνεν λάθος: {e}")
