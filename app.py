import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ParkPulse Limassol // Direct Dashboard",
    page_icon="🅿️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CLEAN UI STYLING ---
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
        <div class="cyber-title">🅿️ ParkPulse Limassol - Live Dashboard</div>
        <span class="live-badge">⚡ DIRECT MUNICIPAL SYSTEM</span>
    </div>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if "community_reports" not in st.session_state:
    st.session_state.community_reports = {}

# --- OFFICIAL MUNICIPAL PARKING DATA (1-55 GRID) ---
parking_spots = [
    {"ID": 1, "Name": "Αρ. 1: Αγίας Φυλάξεως & Γλάδστωνος", "Area": "Κέντρο"},
    {"ID": 2, "Name": "Αρ. 2: Ανδρέα Βλάμη", "Area": "Κέντρο"},
    {"ID": 6, "Name": "Αρ. 6-7: Οδός Ηπείρου", "Area": "Κέντρο"},
    {"ID": 8, "Name": "Αρ. 8: Οθόνης και Αμαλίας", "Area": "Παραλία"},
    {"ID": 10, "Name": "Αρ. 9-10: Ρένου Πουγιούκκα", "Area": "Κέντρο"},
    {"ID": 21, "Name": "Αρ. 21: Χώρος Στάθμευσης ΤΕΠΑΚ", "Area": "ΤΕΠΑΚ"},
    {"ID": 37, "Name": "Αρ. 37: Σωκράτους", "Area": "Κέντρο"},
    {"ID": 39, "Name": "Αρ. 39: Αρχιεπισκόπου Κυπριανού", "Area": "Κέντρο"},
    {"ID": 48, "Name": "Αρ. 48: Κουμπουρολουζάντε", "Area": "Κάστρο"},
    {"ID": 50, "Name": "Αρ. 50: Σπύρου Αραούζου", "Area": "Μόλος"},
    {"ID": 54, "Name": "Αρ. 54: Σπύρου Αραούζου (Μόλος)", "Area": "Μόλος"},
    {"ID": 55, "Name": "Αρ. 55: Χριστόδουλου Χατζηπαύλου (Μόλος)", "Area": "Μόλος"}
]

df = pd.DataFrame(parking_spots)

# Evaluate probabilities & statuses
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
        statuses.append("🟢 Άφθονες Θέσεις (Available)")
    elif prob > 30:
        statuses.append("🟡 Γεμίζει Σιγά-Σιγά (Filling)")
    else:
        statuses.append("🔴 Συμφόρηση / Γεμάτο (Full)")

df["Probability"] = probabilities
df["Status"] = statuses

# --- APP INTERFACE ---
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

# --- DRIVER REPORT WIDGET ---
st.markdown("""
    <div class="interactive-card">
        <h3 style="color: #38bdf8; margin-top: 0; font-size: 1.1rem;">📍 Σύστημα Live Καταχώρησης Οδηγού</h3>
        <p style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 0.8rem;">
            Επίλεξε το σημείο που βρίσκεσαι και ενημέρωσε άμεσα τη διαθεσιμότητα για τους άλλους οδηγούς.
        </p>
    </div>
""", unsafe_allow_html=True)

with st.form("driver_report_form"):
    selected_spot = st.selectbox("Επιλογή Χώρου Στάθμευσης:", df["Name"].tolist())
    selected_status = st.selectbox("Κατάσταση:", [
        "🟢 Άφθονες θέσεις (85%)", 
        "🟡 Γεμίζει σιγά-σιγά (50%)", 
        "🔴 Γεμάτο / Ουρά (15%)"
    ])
    
    submit_btn = st.form_submit_button("🚀 Άμεση Καταχώρηση Αναφοράς")
    if submit_btn:
        if "85" in selected_status:
            st.session_state.community_reports[selected_spot] = 85
        elif "50" in selected_status:
            st.session_state.community_reports[selected_spot] = 50
        else:
            st.session_state.community_reports[selected_spot] = 15
        st.success(f"Η αναφορά για το σημείο '{selected_spot}' καταχωρήθηκε επιτυχώς!")
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 📋 Πίνακας Διαθεσιμότητας & Κατάστασης")
st.dataframe(df[["ID", "Name", "Area", "Probability", "Status"]], use_container_width=True, hide_index=True)
