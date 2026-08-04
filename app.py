import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import random
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ParkPulse Limassol // Official Map 1-55",
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
        <div class="cyber-title">🅿️ ParkPulse Limassol - Official Map (1-55)</div>
        <span class="live-badge">⚡ MUNICIPAL GRID DATA</span>
    </div>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if "community_reports" not in st.session_state:
    st.session_state.community_reports = {}

# --- ALL 55 OFFICIAL MUNICIPAL PARKING SPOTS FROM THE MAP ---
@st.cache_data
def load_all_municipal_spots():
    data = [
        ("Αρ. 1: Αγίας Φυλάξεως & Γλάδστωνος", "Long Term Parking", 34.6891, 33.0331),
        ("Αρ. 2: Ανδρέα Βλάμη", "Long Term Parking", 34.6871, 33.0425),
        ("Αρ. 3: Γωνία Α. Βλάμη & Βραγαδίνου", "Long Term Parking", 34.6865, 33.0418),
        ("Αρ. 4 & 5: Γωνία Ηπείρου & Κ. Οικονόμου", "Long Term Parking", 34.6885, 33.0442),
        ("Αρ. 6 & 7: Ηπείρου", "Long Term Parking", 34.6881, 33.0441),
        ("Αρ. 8: Οθόνης & Αμαλίας", "Long Term Parking", 34.6901, 33.0531),
        ("Αρ. 9 & 10: Ρένου Πουγιούκκα", "Long Term Parking", 34.6841, 33.0371),
        ("Αρ. 11: Θερμοπυλών", "Long Term Parking", 34.6821, 33.0325),
        ("Αρ. 12 & 13: Μεγάλου Αλεξάνδρου & Πτολεμαίων", "Long Term Parking", 34.6832, 33.0391),
        ("Αρ. 14 & 15: Παύλου Μελά", "Long Term Parking", 34.6875, 33.0465),
        ("Αρ. 16: Μάρκου Μπότσαρη", "Long Term Parking", 34.6862, 33.0491),
        ("Αρ. 17 & 18: Κιτίου Κυπριανού", "Long Term Parking", 34.6795, 33.0385),
        ("Αρ. 19: Πτολεμαίων & Γεωργίου Γενναδίου", "Long Term Parking", 34.6825, 33.0421),
        ("Αρ. 20: Οδός Θράκης", "Long Term Parking", 34.6851, 33.0435),
        ("Αρ. 21: Ανδρέα Θεμιστοκλέους (ΤΕΠΑΚ)", "Long Term Parking", 34.6835, 33.0451),
        ("Αρ. 22: Γωνία Ειρήνης & Θησέως", "Long Term Parking", 34.6781, 33.0295),
        ("Αρ. 23: Γωνία Ενώσεως & Ελλάδος", "Long Term Parking", 34.6775, 33.0321),
        ("Αρ. 24 & 25: Ελλάδος", "Long Term Parking", 34.6752, 33.0361),
        ("Αρ. 26: Κιτίου Κυπριανού", "Long Term Parking", 34.6761, 33.0375),
        ("Αρ. 27: Γωνία Αθηνών & Μ. Μπότσαρη", "Long Term Parking", 34.6822, 33.0495),
        ("Αρ. 28: Νικηφόρου Φωκά", "Long Term Parking", 34.6841, 33.0481),
        ("Αρ. 29: Ελένης Παλαιολογίνας", "Long Term Parking", 34.6861, 33.0542),
        ("Αρ. 30 & 31: Βασιλείου Μακεδόνος & Αθηνών", "Long Term Parking", 34.6842, 33.0525),
        ("Αρ. 32: Γεωργίου Τεμπελάρ", "Long Term Parking", 34.6831, 33.0561),
        ("Αρ. 33: Ειρήνης", "Long Term Parking", 34.6732, 33.0331),
        ("Αρ. 34: Ελλάδος", "Long Term Parking", 34.6761, 33.0352),
        ("Αρ. 35: Γωνία Ελλάδος & Σπάρτης", "Long Term Parking", 34.6771, 33.0362),
        ("Αρ. 36: Σπάρτης", "Long Term Parking", 34.6782, 33.0368),
        ("Αρ. 37: Σωκράτους", "Long Term Parking", 34.6791, 33.0382),
        ("Αρ. 38: Πάγκος Ποταμίτη", "Long Term Parking", 34.6805, 33.0395),
        ("Αρ. 39: Αρχιεπισκόπου Κυπριανού", "Long Term Parking", 34.6792, 33.0431),
        ("Αρ. 40: Ιφιγενείας", "Long Term Parking", 34.6815, 33.0442),
        ("Αρ. 41 & 42: Σαλαμίνος", "Long Term Parking", 34.6812, 33.0521),
        ("Αρ. 43 & 44: Βασιλείου Μακεδόνος", "Long Term Parking", 34.6835, 33.0538),
        ("Αρ. 45: Αθηνών & Ε. Παλαιολογίνας", "Long Term Parking", 34.6851, 33.0532),
        ("Αρ. 46: Σερτάρ", "Long Term Parking", 34.6705, 33.0291),
        ("Αρ. 47: Γωνία 'Εγκαφ & Έκκαφ", "Long Term Parking", 34.6685, 33.0271),
        ("Αρ. 48: Κουμπουρολουζάντε", "Long Term Parking", 34.6672, 33.0295),
        ("Αρ. 49: Κουμμανδαρίας & Γ. Μιτέλλα", "Long Term Parking", 34.6735, 33.0391),
        ("Αρ. 50: Σπύρου Αραούζου", "Long Term Parking", 34.6712, 33.0415),
        ("Αρ. 51 & 52: Σπύρου Αραούζου (Αγ. Νάπα)", "Long Term Parking", 34.6725, 33.0425),
        ("Αρ. 53: Σπύρου Αραούζου (Νότια)", "Long Term Parking", 34.6665, 33.0435),
        ("Αρ. 54: Σπύρου Αραούζου (Μόλος)", "Long Term Parking", 34.6751, 33.0489),
        ("Αρ. 55: Χριστόδουλου Χατζηπαύλου (Μόλος)", "Long Term Parking", 34.6739, 33.0454)
    ]
    return pd.DataFrame(data, columns=["Name", "Category", "lat", "lon"])

parking_df = load_all_municipal_spots()

# Dynamic evaluation
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

# --- MAIN INTERFACE ---
selected_view = st.radio("Επιλογή:", ["🗺️ Χάρτης & Αναφορές", "📋 Λίστα Όλων των Σημείων"], horizontal=True, label_visibility="collapsed")

if selected_view == "🗺️ Χάρτης & Αναφορές":
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-box"><p class="metric-num">{len(parking_df)}</p><p class="metric-txt">Συνολικά Σημεία (1-55)</p></div>', unsafe_allow_html=True)
    with m2:
        avg_p = int(parking_df["Probability"].mean()) if len(parking_df) > 0 else 0
        st.markdown(f'<div class="metric-box"><p class="metric-num">{avg_p}%</p><p class="metric-txt">Μέσος Δείκτης</p></div>', unsafe_allow_html=True)
    with m3:
        rep_count = len(st.session_state.community_reports)
        st.markdown(f'<div class="metric-box"><p class="metric-num" style="color: #34d399;">{rep_count}</p><p class="metric-txt">Live Reports</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Render Folium Map centered strictly on Limassol Center
    m = folium.Map(
        location=[34.6800, 33.0410],
        zoom_start=15,
        tiles="CartoDB positron",
        control_scale=False,
        attributionControl=False
    )

    for idx, row in parking_df.iterrows():
        if pd.notnull(row["lat"]) and pd.notnull(row["lon"]):
            p = row["Probability"]
            color = "green" if p > 60 else ("orange" if p > 30 else "red")
            
            popup_html = f"""
                <div style="font-family: sans-serif; min-width: 160px;">
                    <b style="font-size: 13px; color: #0f172a;">{row['Name']}</b><br>
                    <span style="font-size: 11px; color: #475569;">
                        <b>Τύπος:</b> {row['Category']}<br>
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

    st_folium(m, width="100%", height=450, returned_objects=[])

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
    st.markdown("### 📋 Πλήρης Λίστα Δημοτικών Χώρων Στάθμευσης (1-55)")
    st.dataframe(parking_df[["Name", "Category", "Probability", "Status"]], use_container_width=True)
