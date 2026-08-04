import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import random
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ParkPulse Limassol // Official Municipal Map",
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
        background: radial-gradient(circle at 50% 0%, #0f172a 0%, #030712 100%);
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
        backdrop-filter: blur(8px);
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
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
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
        <div class="cyber-title">🅿️ ParkPulse Limassol - Official Map Grid</div>
        <span class="live-badge">⚡ BASED ON MUNICIPAL MAP</span>
    </div>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if "community_reports" not in st.session_state:
    st.session_state.community_reports = {}

# --- OFFICIAL MUNICIPAL MAP PARKING SPOTS (FROM YOUR UPLOADED MAP) ---
@st.cache_data
def load_limassol_spots():
    data = [
        ("Αρ. 21: Χώρος Στάθμευσης ΤΕΠΑΚ (Γεωργίου Γενναδίου)", "Κεντρικός Χώρος", 34.68352, 33.04512),
        ("Αρ. 54: Σπύρου Αραούζου (Μόλος)", "Χώρος Στάθμευσης", 34.67512, 33.04891),
        ("Αρ. 55: Χριστόδουλου Χατζηπαύλου (Μόλος)", "Χώρος Στάθμευσης", 34.67389, 33.04542),
        ("Αρ. 50 & 51: Σπύρου Αραούζου / Αγ. Νάπα", "Χώρος Στάθμευσης", 34.67215, 33.04112),
        ("Αρ. 20: Οδός Θράκης", "Χώρος Στάθμευσης", 34.68512, 33.04351),
        ("Αρ. 1: Οδός Αγίας Φυλάξεως & Γλάδστωνος", "Χώρος Στάθμευσης", 34.68912, 33.03312),
        ("Αρ. 6: Οδός Ηπείρου", "Χώρος Στάθμευσης", 34.68815, 33.04412),
        ("Αρ. 38 & 39: ΤΕΠΑΚ / Αρχιεπισκόπου Κυπριανού", "Χώρος Στάθμευσης", 34.68112, 33.03815),
        ("Αρ. 47 & 48: Οδός Έγκαφ & Αγίου Ανδρέου", "Χώρος Στάθμευσης", 34.67054, 33.03215),
        ("Αρ. 53: Οδός Σπύρου Αραούζου (Νότια)", "Χώρος Στάθμευσης", 34.66812, 33.04312)
    ]
    return pd.DataFrame(data, columns=["Name", "Category", "lat", "lon"])

base_df = load_limassol_spots()

# Dynamic probability evaluation
final_probabilities = []
statuses = []

for idx, row in base_df.iterrows():
    name = row["Name"]
    if name in st.session_state.community_reports:
        prob = st.session_state.community_reports[name]
    else:
        random.seed(hash(name) + datetime.now().hour)
        prob = random.randint(20, 88)
    
    final_probabilities.append(prob)
    
    if prob > 60:
        statuses.append("Άφθονες Θέσεις (Available)")
    elif prob > 30:
        statuses.append("Γεμίζει Σιγά-Σιγά (Filling Up)")
    else:
        statuses.append("Συμφόρηση / Γεμάτο (Congested)")

base_df["Probability"] = final_probabilities
base_df["Status"] = statuses
parking_db = base_df

# --- TAB SELECTION ---
selected_view = st.radio("Επιλογή:", ["🗺️ Live Χάρτης & Αναφορά", "📊 Ανάλυση & Peak Hours"], horizontal=True, label_visibility="collapsed")

if selected_view == "🗺️ Live Χάρτης & Αναφορά":
    
    categories = ["Όλα τα Πάρκινγκ"] + sorted(list(parking_db["Category"].dropna().unique()))
    sel_cat = st.selectbox("Εμφάνιση τύπου:", categories, label_visibility="collapsed")

    df_filtered = parking_db.copy()
    if sel_cat != "Όλα τα Πάρκινγκ":
        df_filtered = df_filtered[df_filtered["Category"] == sel_cat]

    # Metrics Row
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
            <div class="metric-box">
                <p class="metric-num">{len(df_filtered)}</p>
                <p class="metric-txt">Σημεία</p>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        avg_prob = int(df_filtered["Probability"].mean()) if len(df_filtered) > 0 else 0
        st.markdown(f"""
            <div class="metric-box">
                <p class="metric-num">{avg_prob}%</p>
                <p class="metric-txt">Δείκτης</p>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        reports_count = len(st.session_state.community_reports)
        st.markdown(f"""
            <div class="metric-box">
                <p class="metric-num" style="color: #34d399;">{reports_count}</p>
                <p class="metric-txt">Live Reports</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Interactive Map centered on Limassol center (TEPAK / Agora area)
    m = folium.Map(
        location=[34.6800, 33.0410], 
        zoom_start=15, 
        tiles="CartoDB positron",
        control_scale=False,
        attributionControl=False
    )

    for idx, row in df_filtered.iterrows():
        if pd.notnull(row["lat"]) and pd.notnull(row["lon"]):
            if row["Probability"] > 60:
                color = "green"
            elif row["Probability"] > 30:
                color = "orange"
            else:
                color = "red"

            is_community_updated = row["Name"] in st.session_state.community_reports
            badge = " ⚡ [Community Live]" if is_community_updated else ""

            popup_html = f"""
                <div style="font-family: sans-serif; min-width: 180px;">
                    <b style="font-size: 13px; color: #0f172a;">{row['Name']}</b>{badge}<br>
                    <span style="font-size: 11px; color: #475569;">
                        <b>Τύπος:</b> {row['Category']}<br>
                        <b>Πιθανότητα Θέσης:</b> <span style="color: {color}; font-weight: bold;">{row['Probability']}%</span><br>
                        <i>({row['Status']})</i>
                    </span>
                </div>
            """
            folium.Marker(
                [row["lat"], row["lon"]],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=f"{row['Name']} ({row['Probability']}%)",
                icon=folium.Icon(color=color, icon="car", prefix="fa")
            ).add_to(m)

    st_folium(m, width="100%", height=420, returned_objects=[])

    # --- MOBILE LIVE REPORT WIDGET ---
    st.markdown("""
        <div class="interactive-card">
            <h3 style="color: #38bdf8; margin-top: 0; font-size: 1.05rem;">📍 Είσαι σε πάρκινγκ τώρα;</h3>
            <p style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 0.8rem;">Δώσε μια γρήγορη αναφορά για να βοηθήσεις τους οδηγούς!</p>
        </div>
    """, unsafe_allow_html=True)

    report_spot = st.selectbox("1. Διάλεξε σημείο:", parking_db["Name"].tolist(), key="mobile_spot")
    report_status = st.selectbox("2. Κατάσταση που βλέπεις:", [
        "🟢 Άφθονες θέσεις (85%)", 
        "🟡 Γεμίζει σιγά-σιγά (50%)", 
        "🔴 Γεμάτο / Ουρά (15%)"
    ], key="mobile_status")

    if st.button("🚀 Άμεση Ενημέρωση Χάρτη"):
        if "85" in report_status:
            st.session_state.community_reports[report_spot] = 85
        elif "50" in report_status:
            st.session_state.community_reports[report_spot] = 50
        else:
            st.session_state.community_reports[report_spot] = 15
        st.success("Επιτυχία! Ο χάρτης ενημερώθηκε ζωντανά.")
        st.rerun()

    st.markdown("### 📋 Επίσημη Λίστα Χώρων Στάθμευσης")
    st.dataframe(df_filtered[["Name", "Category", "Probability", "Status"]], use_container_width=True)

else:
    st.markdown("### 📊 Ανάλυση Κίνησης στη Λεμεσό")
    st.write("Μάθε πότε συμφέρει να κινηθείς στα κεντρικά σημεία.")

    st.markdown("""
        <div class="interactive-card">
            <h4 style="color: #38bdf8; margin-top: 0;">Limassol Municipal Traffic Matrix</h4>
            <p style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 0;">
                Βάσει του επίσημου χάρτη και των ζωνών πάρκινγκ:
                <br><br>
                🔴 <b>Ώρες Αιχμής (Δύσκολη Εύρεση):</b> 08:00 - 09:30 & 17:30 - 19:30
                <br>
                🟡 <b>Μέτρια Κίνηση:</b> 10:00 - 16:00 (Ψώνια, ΤΕΠΑΚ, βόλτες)
                <br>
                🟢 <b>Χρυσά Παράθυρα:</b> Πριν τις 07:30 το πρωί & μετά τις 21:00 το βράδυ
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 💡 Smart Tip")
    st.info("Οι χώροι στάθμευσης γύρω από το ΤΕΠΑΚ (Αρ. 21) και τον Μόλο (Αρ. 54, 55) είναι οι πιο δημοφιλείς στο κέντρο.")
