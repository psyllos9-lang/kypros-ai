import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ParkPulse Limassol // Google Maps Engine",
    page_icon="🅿️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- STYLING ---
st.markdown("""
    <style>
    .block-container {
        padding-top: 0.6rem !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
    }
    header[data-testid="stHeader"] {
        display: none !important;
    }
    .stApp {
        background: #0f172a;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #f8fafc;
    }
    .cyber-header {
        background: rgba(30, 41, 59, 0.85);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 14px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .cyber-title {
        font-size: 1.3rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
    }
    .live-badge {
        background: rgba(52, 211, 153, 0.15);
        color: #34d399;
        border: 1px solid rgba(52, 211, 153, 0.4);
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.65rem;
        font-weight: 700;
        display: inline-block;
        margin-top: 6px;
    }
    .metric-box {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 0.7rem;
        text-align: center;
    }
    .metric-num {
        font-size: 1.3rem;
        font-weight: 800;
        color: #38bdf8;
        margin: 0;
    }
    .metric-txt {
        font-size: 0.6rem;
        color: #94a3b8;
        margin: 2px 0 0 0;
        text-transform: uppercase;
    }
    .interactive-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 14px;
        padding: 1.2rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 700;
        padding: 0.75rem 1rem;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="cyber-header">
        <div class="cyber-title">🅿️ ParkPulse Limassol</div>
        <span class="live-badge">⚡ GOOGLE MAPS INTEGRATION</span>
    </div>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "community_reports" not in st.session_state:
    st.session_state.community_reports = {}

# --- OFFICIAL MUNICIPAL SPOTS DATA ---
parking_data = [
    {"ID": 1, "Name": "Αρ. 1: Αγίας Φυλάξεως & Γλάδστωνος", "Category": "Long Term"},
    {"ID": 21, "Name": "Αρ. 21: Χώρος Στάθμευσης ΤΕΠΑΚ", "Category": "Long Term"},
    {"ID": 50, "Name": "Αρ. 50: Σπύρου Αραούζου (Κέντρο)", "Category": "Municipal"},
    {"ID": 54, "Name": "Αρ. 54: Σπύρου Αραούζου (Μόλος)", "Category": "Waterfront"},
    {"ID": 55, "Name": "Αρ. 55: Χριστόδουλου Χατζηπαύλου (Μόλος)", "Category": "Waterfront"},
    {"ID": 8, "Name": "Αρ. 8: Λεωφ. Μακαρίου ΙΙΙ (Εναέριος)", "Category": "Long Term"},
    {"ID": 7, "Name": "Αρ. 7: Εμ. Ροΐδη (Δικαστήρια)", "Category": "Long Term"},
    {"ID": 10, "Name": "Αρ. 10: Σπύρου Αραούζου (Παλιό Λιμάνι)", "Category": "Hub"}
]

df = pd.DataFrame(parking_data)

# Evaluate probabilities
probabilities = []
statuses = []

for idx, row in df.iterrows():
    name = row["Name"]
    if name in st.session_state.community_reports:
        prob = st.session_state.community_reports[name]
    else:
        random.seed(hash(name) + datetime.now().hour)
        prob = random.randint(20, 88)
    
    probabilities.append(prob)
    if prob > 60:
        statuses.append("🟢 Άφθονες Θέσεις")
    elif prob > 30:
        statuses.append("🟡 Γεμίζει Σιγά-Σιγά")
    else:
        statuses.append("🔴 Συμφόρηση / Γεμάτο")

df["Probability"] = probabilities
df["Status"] = statuses

# --- INTERFACE ---
selected_view = st.radio("Επιλογή:", ["🗺️ Google Maps Χάρτης", "📋 Λίστα & Live Αναφορές"], horizontal=True, label_visibility="collapsed")

if selected_view == "🗺️ Google Maps Χάρτης":
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-box"><p class="metric-num">{len(df)}</p><p class="metric-txt">Επίσημα Σημεία</p></div>', unsafe_allow_html=True)
    with m2:
        avg_p = int(df["Probability"].mean())
        st.markdown(f'<div class="metric-box"><p class="metric-num">{avg_p}%</p><p class="metric-txt">Μέσος Δείκτης</p></div>', unsafe_allow_html=True)
    with m3:
        rep_count = len(st.session_state.community_reports)
        st.markdown(f'<div class="metric-box"><p class="metric-num" style="color: #34d399;">{rep_count}</p><p class="metric-txt">Live Reports</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ΕΝΣΩΜΑΤΩΣΗ ΤΟΥ ΕΠΙΣΗΜΟΥ GOOGLE MAPS EMBED ΓΙΑ ΤΗ ΛΕΜΕΣΟ (ΚΕΝΤΡΟ / ΜΟΛΟΣ / ΤΕΠΑΚ)
    google_maps_html = """
    <iframe 
        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3272.035427189033!2d33.0390156!3d34.6800543!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x14e73307b22a6117%3A0x46c3b6d081f253ee!2sLimassol%2C%20Cyprus!5e0!3m2!1sen!2sgr!4v1700000000000!5m2!1sen!2sgr" 
        width="100%" 
        height="480" 
        style="border:0; border-radius: 14px;" 
        allowfullscreen="" 
        loading="lazy" 
        referrerpolicy="no-referrer-when-downgrade">
    ></iframe>
    """
    st.markdown(google_maps_html, unsafe_allow_html=True)
    
    st.info("💡 Ο χάρτης φορτώνει απευθείας από το Google Maps στο κέντρο της Λεμεσού με όλες τις οδούς και τα σημεία ενδιαφέροντος.")

else:
    st.markdown("### 📋 Κατάσταση Χώρων Στάθμευσης & Live Αναφορές")
    
    # Live Report Widget
    st.markdown("""
        <div class="interactive-card">
            <h3 style="color: #38bdf8; margin-top: 0; font-size: 1rem;">📍 Είσαι σε πάρκινγκ τώρα; Δώσε αναφορά!</h3>
        </div>
    """, unsafe_allow_html=True)

    spot_choice = st.selectbox("Επιλογή Σημείου:", df["Name"].tolist())
    status_choice = st.selectbox("Κατάσταση:", ["🟢 Άφθονες θέσεις (85%)", "🟡 Γεμίζει σιγά-σιγά (50%)", "🔴 Γεμάτο / Ουρά (15%)"])

    if st.button("🚀 Άμεση Καταχώρηση"):
        if "85" in status_choice:
            st.session_state.community_reports[spot_choice] = 85
        elif "50" in status_choice:
            st.session_state.community_reports[spot_choice] = 50
        else:
            st.session_state.community_reports[spot_choice] = 15
        st.success("Επιτυχία! Η κατάσταση ενημερώθηκε ζωντανά.")
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(df[["Name", "Category", "Probability", "Status"]], use_container_width=True)
