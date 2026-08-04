import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import random
from datetime import datetime
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ParkPulse Limassol // OSM Detailed Map",
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
        <div class="cyber-title">🅿️ ParkPulse Limassol - Detailed OSM Map</div>
        <span class="live-badge">⚡ OPENSTREETMAP DETAILED GRID</span>
    </div>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "community_reports" not in st.session_state:
    st.session_state.community_reports = {}

# --- LOAD DATA FROM CSV ---
@st.cache_data
def load_data():
    csv_file = "parking.csv"
    if os.path.exists(csv_file):
        return pd.read_csv(csv_file)
    else:
        # Fallback δεδομένα αν δεν υπάρχει το CSV
        data = [
            [21, "Χώρος Στάθμευσης ΤΕΠΑΚ (Γεωργίου Γενναδίου)", "Long Term Parking", 34.68352, 33.04512],
            [54, "Σπύρου Αραούζου (Μόλος)", "Long Term Parking", 34.67512, 33.04891],
            [55, "Χριστόδουλου Χατζηπαύλου (Μόλος)", "Long Term Parking", 34.67389, 33.04542]
        ]
        return pd.DataFrame(data, columns=["ID", "Name", "Category", "lat", "lon"])

parking_df = load_data()

# Evaluate status & probabilities
probabilities = []
statuses = []

for idx, row in parking_df.iterrows():
    name = row["Name"]
    if name in st.session_state.community_reports:
        prob = st.session_state.community_reports[name]
    else:
        random.seed(hash(str(name)) + datetime.now().hour)
        prob = random.randint(20, 88)
    
    probabilities.append(prob)
    if prob > 60:
        statuses.append("Άφθονες Θέσεις (Available)")
    elif prob > 30:
        statuses.append("Γεμίζει Σιγά-Σιγά (Filling Up)")
    else:
        statuses.append("Συμφόρηση / Γεμάτο (Congested)")

parking_df["Probability"] = probabilities
parking_df["Status"] = statuses

# --- INTERFACE ---
selected_view = st.radio("Επιλογή:", ["🗺️ Λεπτομερής Χάρτης", "📋 Διαχείριση CSV"], horizontal=True, label_visibility="collapsed")

if selected_view == "🗺️ Λεπτομερής Χάρτης":
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-box"><p class="metric-num">{len(parking_df)}</p><p class="metric-txt">Ενεργά Σημεία</p></div>', unsafe_allow_html=True)
    with m2:
        avg_p = int(parking_df["Probability"].mean()) if len(parking_df) > 0 else 0
        st.markdown(f'<div class="metric-box"><p class="metric-num">{avg_p}%</p><p class="metric-txt">Μέσος Δείκτης</p></div>', unsafe_allow_html=True)
    with m3:
        rep_count = len(st.session_state.community_reports)
        st.markdown(f'<div class="metric-box"><p class="metric-num" style="color: #34d399;">{rep_count}</p><p class="metric-txt">Live Reports</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ΧΡΗΣΗ ΤΟΥ OPENSTREETMAP (openstreetmap tile) ΓΙΑ ΑΚΡΙΒΗ ΟΔΙΚΗ ΑΠΕΙΚΟΝΙΣΗ
    m = folium.Map(
        location=[34.6800, 33.0410],
        zoom_start=16,
        tiles="OpenStreetMap",
        control_scale=True
    )

    for idx, row in parking_df.iterrows():
        if pd.notnull(row["lat"]) and pd.notnull(row["lon"]):
            p = row["Probability"]
            color = "green" if p > 60 else ("orange" if p > 30 else "red")
            
            popup_html = f"""
                <div style="font-family: sans-serif; min-width: 160px;">
                    <b style="font-size: 13px; color: #0f172a;">{row['Name']}</b><br>
                    <span style="font-size: 11px; color: #475569;">
                        <b>Κατηγορία:</b> {row['Category']}<br>
                        <b>Διαθεσιμότητα:</b> <span style="color: {color}; font-weight: bold;">{p}%</span>
                    </span>
                </div>
            """
            folium.Marker(
                [row["lat"], row["lon"]],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=row["Name"],
                icon=folium.Icon(color=color, icon="car", prefix="fa")
            ).add_to(m)

    st_folium(m, width="100%", height=500, returned_objects=[])

    # Live Report Widget
    st.markdown("""
        <div class="interactive-card">
            <h3 style="color: #38bdf8; margin-top: 0; font-size: 1rem;">📍 Live Αναφορά Οδηγού</h3>
        </div>
    """, unsafe_allow_html=True)

    spot_choice = st.selectbox("Επιλογή Πάρκινγκ:", parking_df["Name"].tolist())
    status_choice = st.selectbox("Κατάσταση:", ["🟢 Άφθονες θέσεις (85%)", "🟡 Γεμίζει σιγά-σιγά (50%)", "🔴 Γεμάτο / Ουρά (15%)"])

    if st.button("🚀 Υποβολή Αναφοράς"):
        if "85" in status_choice:
            st.session_state.community_reports[spot_choice] = 85
        elif "50" in status_choice:
            st.session_state.community_reports[spot_choice] = 50
        else:
            st.session_state.community_reports[spot_choice] = 15
        st.success("Η αναφορά καταχωρήθηκε επιτυχώς!")
        st.rerun()

else:
    st.markdown("### 📋 Λίστα Δεδομένων (CSV)")
    st.write("Εδώ βλέπεις τα σημεία όπως διαβάζονται από το `parking.csv`.")
    st.dataframe(parking_df, use_container_width=True)
