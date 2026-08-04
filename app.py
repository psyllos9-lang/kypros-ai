import streamlit as st
import pandas as pd
import pydeck as pdk
import random
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ParkPulse Limassol // 3D Deck Engine",
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
        <div class="cyber-title">🅿️ ParkPulse Limassol - Live 3D Grid</div>
        <span class="live-badge">⚡ ACCURATE PINS & LIVE REPORTS</span>
    </div>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if "community_reports" not in st.session_state:
    st.session_state.community_reports = {}

if "parking_spots" not in st.session_state:
    # Ακριβή σημεία κέντρου Λεμεσού / ΤΕΠΑΚ / Μόλου / Εναερίου
    st.session_state.parking_spots = [
        {"Name": "Αρ. 21: Χώρος Στάθμευσης ΤΕΠΑΚ", "Category": "TEPAK / Κέντρο", "lat": 34.68352, "lon": 33.04512},
        {"Name": "Αρ. 54: Σπύρου Αραούζου (Μόλος)", "Category": "Μόλος", "lat": 34.67512, "lon": 33.04891},
        {"Name": "Αρ. 55: Χριστόδουλου Χατζηπαύλου (Μόλος)", "Category": "Μόλος", "lat": 34.67389, "lon": 33.04542},
        {"Name": "Αρ. 10: Παλιό Λιμάνι", "Category": "Μαρίνα", "lat": 34.67105, "lon": 33.03712},
        {"Name": "Αρ. 8: Εναέριος (Μακαρίου)", "Category": "Εναέριος", "lat": 34.68692, "lon": 33.05185},
        {"Name": "Αρ. 1: Αγίας Φυλάξεως & Γλάδστωνος", "Category": "Κέντρο", "lat": 34.68912, "lon": 33.03312},
        {"Name": "Αρ. 7: Πλησίον Δικαστηρίων (Εμ. Ροΐδη)", "Category": "Δικαστήρια", "lat": 34.69124, "lon": 33.04512}
    ]

# Build DataFrame dynamically
data_list = []
for spot in st.session_state.parking_spots:
    name = spot["Name"]
    cat = spot["Category"]
    lat = spot["lat"]
    lon = spot["lon"]
    
    if name in st.session_state.community_reports:
        prob = st.session_state.community_reports[name]
    else:
        random.seed(hash(name) + datetime.now().hour)
        prob = random.randint(20, 88)
        
    if prob > 60:
        status = "🟢 Άφθονες Θέσεις"
        color = [0, 200, 100, 200]  # Πράσινο
    elif prob > 30:
        status = "🟡 Γεμίζει Σιγά-Σιγά"
        color = [255, 165, 0, 200]  # Πορτοκαλί
    else:
        status = "🔴 Συμφόρηση / Γεμάτο"
        color = [255, 50, 50, 200]  # Kokkino

    data_list.append({
        "Name": name, 
        "Category": cat, 
        "lat": lat, 
        "lon": lon, 
        "Probability": prob, 
        "Status": status,
        "color": color
    })

df = pd.DataFrame(data_list)

# --- INTERFACE TABS ---
selected_view = st.radio("Επιλογή:", ["🗺️ 3D Χάρτης & Pins", "📋 Live Αναφορές Οδηγών"], horizontal=True, label_visibility="collapsed")

if selected_view == "🗺️ 3D Χάρτης & Pins":
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-box"><p class="metric-num">{len(df)}</p><p class="metric-txt">Ενεργά Σημεία</p></div>', unsafe_allow_html=True)
    with m2:
        avg_p = int(df["Probability"].mean())
        st.markdown(f'<div class="metric-box"><p class="metric-num">{avg_p}%</p><p class="metric-txt">Μέσος Δείκτης</p></div>', unsafe_allow_html=True)
    with m3:
        rep_count = len(st.session_state.community_reports)
        st.markdown(f'<div class="metric-box"><p class="metric-num" style="color: #34d399;">{rep_count}</p><p class="metric-txt">Live Reports</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Pydeck 3D Map Layer (Ακριβή pins με χρωματικές κωδικοποιήσεις)
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_color="color",
        get_radius=120,
        pickable=True,
        auto_highlight=True,
    )

    view_state = pdk.ViewState(
        latitude=34.6800,
        longitude=33.0410,
        zoom=14.5,
        pitch=30,
        bearing=0
    )

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            "html": "<b>{Name}</b><br>Περιοχή: {Category}<br>Διαθεσιμότητα: <b>{Probability}%</b> ({Status})",
            "style": {"backgroundColor": "#0f172a", "color": "white", "padding": "10px", "borderRadius": "8px"}
        },
        map_style="mapbox://styles/mapbox/dark-v10"
    )

    st.pydeck_chart(r, use_container_width=True)
    st.info("💡 Κάνε hover ή κλικ πάνω στα pins στον χάρτη για να δεις το όνομα του πάρκινγκ και τη ζωντανή διαθεσιμότητα.")

else:
    st.markdown("### 📍 Σύστημα Live Καταχώρησης από Οδηγούς")
    st.write("Βλέπεις ένα πάρκινγκ γεμάτο ή άδειο τώρα; Ενημέρωσε αμέσως την κοινότητα!")

    with st.form("report_form"):
        spot_choice = st.selectbox("Επιλογή Χώρου Στάθμευσης:", df["Name"].tolist())
        status_choice = st.selectbox("Κατάσταση που βλέπεις:", [
            "🟢 Άφθονες θέσεις (85%)", 
            "🟡 Γεμίζει σιγά-σιγά (50%)", 
            "🔴 Γεμάτο / Ουρά (15%)"
        ])
        
        submitted = st.form_submit_button("🚀 Άμεση Υποβολή Αναφοράς")
        if submitted:
            if "85" in status_choice:
                st.session_state.community_reports[spot_choice] = 85
            elif "50" in status_choice:
                st.session_state.community_reports[spot_choice] = 50
            else:
                st.session_state.community_reports[spot_choice] = 15
            st.success(f"Επιτυχία! Το σημείο '{spot_choice}' ενημερώθηκε ζωντανά.")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📋 Τρέχουσα Κατάσταση Σημείων")
    st.dataframe(df[["Name", "Category", "Probability", "Status"]], use_container_width=True)
