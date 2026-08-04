import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import random
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ParkPulse Limassol // Futuristic Radar",
    page_icon="🅿️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CLEAN & MOBILE-FIRST RESPONSIVE STYLING ---
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
    .cyber-subtitle {
        font-size: 0.65rem;
        color: #38bdf8;
        margin: 0 0 2px 0;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 700;
    }
    .cyber-title {
        font-size: 1.4rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 8px;
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
        box-shadow: 0 4px 20px rgba(2, 132, 199, 0.4);
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# --- CLEAN RESPONSIVE HEADER ---
st.markdown("""
    <div class="cyber-header">
        <p class="cyber-subtitle">Limassol Smart City Grid</p>
        <div class="cyber-title">
            <span>🅿️ ParkPulse AI</span>
        </div>
        <div>
            <span class="live-badge">⚡ LIVE HYBRID ENGINE</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if "community_reports" not in st.session_state:
    st.session_state.community_reports = {}

# --- EXACT LAND COORDINATES FOR LIMASSOL PARKING ---
@st.cache_data
def load_limassol_spots():
    data = [
        ("Molos Multi-Storey Parking (Chatzipavlou)", "Multi-story Structure", 34.6756, 33.0471),
        ("Molos Open Air Municipal Parking (East)", "Municipal Lot", 34.6768, 33.0514),
        ("Limassol Marina Official Car Park", "Covered / Structured", 34.6701, 33.0388),
        ("Limassol Old Port Parking Area", "Off-Street Hub", 34.6712, 33.0361),
        ("Anexartisias Commercial Street Zone", "On-Street Zones", 34.6824, 33.0413),
        ("Enaerios Open Air Municipal Lot", "Open Air Lot", 34.6879, 33.0519),
        ("Gladstonos Street Metered Spaces", "On-Street Zones", 34.6869, 33.0402),
        ("Pentadromos Commercial Centre Hub", "Multi-story / Off-Street", 34.6854, 33.0372),
        ("Municipal Library & Courts Parking", "Open Air Lot", 34.6901, 33.0441),
        ("Agios Athanasios Commercial Junction", "Commercial Lot", 34.7001, 33.0335),
        ("Agios Ioannis Municipal Area", "Open Air Lot", 34.6811, 33.0142),
        ("Linopetra Commercial Strip", "Open Air Lot", 34.7038, 33.0271)
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
    
    # Quick Filter
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

    # Interactive Map
    m = folium.Map(
        location=[34.6800, 33.0400], 
        zoom_start=14, 
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

    st.markdown("### 📋 Λίστα & Κατάσταση Σημείων")
    st.dataframe(df_filtered[["Name", "Category", "Probability", "Status"]], use_container_width=True)

else:
    st.markdown("### 📊 Ανάλυση Κίνησης στη Λεμεσό")
    st.write("Μάθε πότε συμφέρει να κινηθείς στα κεντρικά σημεία.")

    st.markdown("""
        <div class="interactive-card">
            <h4 style="color: #38bdf8; margin-top: 0;">Limassol Traffic & Parking Matrix</h4>
            <p style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 0;">
                Βάσει ωραρίων εμπορικών και γραφείων:
                <br><br>
                🔴 <b>Ώρες Αιχμής (Δύσκολη Εύρεση):</b> 08:00 - 09:30 & 17:30 - 19:30
                <br>
                🟡 <b>Μέτρια Κίνηση:</b> 10:00 - 16:00 (Ψώνια, καφέ, βόλτες)
                <br>
                🟢 <b>Χρυσά Παράθυρα:</b> Πριν τις 07:30 το πρωί & μετά τις 21:00 το βράδυ
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 💡 Smart Tip")
    st.info("Για κέντρο και Μόλο, οι πολυώροφοι χώροι στάθμευσης προσφέρουν σταθερά καλύτερη πιθανότητα εύρεσης θέσης.")
