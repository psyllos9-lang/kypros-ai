import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import random
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ParkPulse Limassol // True Interactive Map",
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
        <div class="cyber-title">🅿️ ParkPulse Limassol - Map Editor</div>
        <span class="live-badge">⚡ CLICK TO PIN ACCURATELY</span>
    </div>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE WITH A CLEAN BASE ---
if "limassol_spots" not in st.session_state:
    st.session_state.limassol_spots = [
        {"Name": "Χώρος Στάθμευσης ΤΕΠΑΚ", "Category": "Κέντρο", "lat": 34.6835, "lon": 33.0451},
        {"Name": "Δημοτικός Χώρος Μόλου", "Category": "Μόλος", "lat": 34.6739, "lon": 33.0454}
    ]

if "community_reports" not in st.session_state:
    st.session_state.community_reports = {}

# Build DataFrame dynamically from session state
data_list = []
for spot in st.session_state.limassol_spots:
    name = spot["Name"]
    cat = spot["Category"]
    lat = spot["lat"]
    lon = spot["lon"]
    
    if name in st.session_state.community_reports:
        prob = st.session_state.community_reports[name]
    else:
        random.seed(hash(name) + datetime.now().hour)
        prob = random.randint(20, 88)
        
    status = "Άφθονες Θέσεις (Available)" if prob > 60 else ("Γεμίζει Σιγά-Σιγά (Filling Up)" if prob > 30 else "Συμφόρηση / Γεμάτο (Congested)")
    data_list.append({"Name": name, "Category": cat, "lat": lat, "lon": lon, "Probability": prob, "Status": status})

parking_db = pd.DataFrame(data_list)

# --- MAP RENDERING WITH CLICK CAPTURE ---
m = folium.Map(
    location=[34.6800, 33.0410], 
    zoom_start=15, 
    tiles="CartoDB positron",
    control_scale=False,
    attributionControl=False
)

for idx, row in parking_db.iterrows():
    color = "green" if row["Probability"] > 60 else ("orange" if row["Probability"] > 30 else "red")
    popup_html = f"""
        <div style="font-family: sans-serif; min-width: 160px;">
            <b style="font-size: 13px; color: #0f172a;">{row['Name']}</b><br>
            <span style="font-size: 11px; color: #475569;">
                <b>Κατηγορία:</b> {row['Category']}<br>
                <b>Διαθεσιμότητα:</b> <span style="color: {color}; font-weight: bold;">{row['Probability']}%</span>
            </span>
        </div>
    """
    folium.Marker(
        [row["lat"], row["lon"]],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=row["Name"],
        icon=folium.Icon(color=color, icon="car", prefix="fa")
    ).add_to(m)

# Capture user clicks on the map
map_data = st_folium(m, width="100%", height=450, returned_objects=["last_clicked"])

# --- INTERACTIVE ADD / FIX FORM ---
st.markdown("""
    <div class="interactive-card">
        <h3 style="color: #38bdf8; margin-top: 0; font-size: 1rem;">📍 Προσθήκη / Διόρθωση Πάρκινγκ με 1 Κλικ</h3>
        <p style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 0.5rem;">
            1. Πάτησε πάνω στον χάρτη ακριβώς στο σημείο που βρίσκεται το πάρκινγκ.<br>
            2. Οι συντεταγμένες θα συμπληρωθούν αυτόματα παρακάτω. Δώσε όνομα και αποθήκευε!
        </p>
    </div>
""", unsafe_allow_html=True)

clicked_lat = 34.6800
clicked_lon = 33.0410

if map_data and map_data.get("last_clicked"):
    clicked_lat = map_data["last_clicked"]["lat"]
    clicked_lon = map_data["last_clicked"]["lng"]
    st.info(f"📍 Επιλεγμένες Συντεταγμένες από τον χάρτη: Lat: {clicked_lat:.5f}, Lon: {clicked_lon:.5f}")

with st.form("add_exact_spot"):
    new_name = st.text_input("Όνομα Πάρκινγκ:", placeholder="π.χ. Δημοτικός Χώρος Στάθμευσης ...")
    new_cat = st.selectbox("Κατηγορία:", ["Κέντρο", "Μόλος", "Μαρίνα", "Παλιό Λιμάνι", "Εναέριος", "Δικαστήρια"])
    
    col1, col2 = st.columns(2)
    with col1:
        lat_input = st.number_input("Latitude:", value=clicked_lat, format="%.5f")
    with col2:
        lon_input = st.number_input("Longitude:", value=clicked_lon, format="%.5f")
        
    submitted = st.form_submit_button("💾 Οριστική Αποθήκευση Σημείου στον Χάρτη")
    if submitted and new_name:
        st.session_state.limassol_spots.append({
            "Name": new_name,
            "Category": new_cat,
            "lat": lat_input,
            "lon": lon_input
        })
        st.success(f"Το σημείο '{new_name}' αποθηκεύτηκε επιτυχώς!")
        st.rerun()

st.markdown("### 📋 Λίστα Αποθηκευμένων Σημείων")
st.dataframe(parking_db[["Name", "Category", "lat", "lon", "Probability", "Status"]], use_container_width=True)
