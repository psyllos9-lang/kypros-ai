import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Page Configuration
st.set_page_config(
    page_title="Cyprus EV Hub // Smart Mobility",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- STYLING & LOGO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #111827 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f3f4f6;
    }
    
    .brand-container {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 1.2rem 0;
        border-bottom: 1px solid rgba(56, 189, 248, 0.15);
        margin-bottom: 2rem;
        background: rgba(15, 23, 42, 0.6);
        border-radius: 16px;
        padding-left: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(8px);
    }
    .brand-logo-box {
        width: 52px;
        height: 52px;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        font-weight: 800;
        color: #0f172a;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.4);
    }
    .brand-text h1 {
        font-size: 1.6rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(90deg, #ffffff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .brand-text p {
        font-size: 0.75rem;
        color: #38bdf8;
        margin: 0;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .stButton button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #0f172a !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.2rem !important;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3) !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="brand-container">
        <div class="brand-logo-box">EV</div>
        <div class="brand-text">
            <h1>Cyprus EV Hub</h1>
            <p>Smart Charging & Route Intelligence // 2026</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sidebar Menu
with st.sidebar:
    st.markdown("### ⚙️ MENU")
    menu = st.radio("Επιλογή:", ["🗺️ Ζωντανός Χάρτης Φορτιστών", "🔋 Υπολογιστής Φόρτισης & Κόστους"])
    
    st.markdown("---")
    st.info("⚡ Η απόλυτη πλατφόρμα ηλεκτροκίνησης στην Κύπρο.")

# --- SECTION 1: MAP ---
if menu == "🗺️ Ζωντανός Χάρτης Φορτιστών":
    st.markdown("### 📍 Δίκτυο Ταχυφορτιστών Κύπρου")
    st.write("Βρες γρήγορα δημόσιους φορτιστές σε Λεμεσό, Λευκωσία, Λάρνακα, Πάφο και αυτοκινητόδρομους.")

    chargers_data = pd.DataFrame({
        "City": ["Λεμεσός", "Λεμεσός", "Λευκωσία", "Λευκωσία", "Λάρνακα", "Πάφος", "Αυτοκινητόδρομος"],
        "Name": ["MyMall EV Station", "Enaerios Fast Charger", "Mall of Cyprus Charger", "Athalassa Park Hub", "Finikoudes Station", "Kings Avenue Charger", "Governor's Beach Hub"],
        "lat": [34.6738, 34.6851, 35.1264, 35.1432, 34.9142, 34.7720, 34.7175],
        "lon": [33.0031, 33.0512, 33.4251, 33.3912, 33.6331, 32.4182, 33.2815],
        "Type": ["DC Ultra-Fast (150kW)", "AC Standard (22kW)", "DC Fast (50kW)", "DC Ultra-Fast (150kW)", "DC Fast (50kW)", "DC Fast (50kW)", "DC Ultra-Fast (300kW)"]
    })

    selected_city = st.selectbox("Φίλτρο ανά περιοχή:", ["Όλες οι περιοχές", "Λεμεσός", "Λευκωσία", "Λάρνακα", "Πάφος", "Αυτοκινητόδρομος"])
    
    if selected_city != "Όλες οι περιοχές":
        filtered_df = chargers_data[chargers_data["City"] == selected_city]
    else:
        filtered_df = chargers_data

    m = folium.Map(location=[35.0, 33.3], zoom_start=9, tiles="CartoDB dark_matter")

    for idx, row in filtered_df.iterrows():
        folium.Marker(
            [row["lat"], row["lon"]],
            popup=f"<b>{row['Name']}</b><br>Τύπος: {row['Type']}",
            tooltip=row["Name"],
            icon=folium.Icon(color="blue", icon="bolt", prefix="fa")
        ).add_to(m)

    st_folium(m, width=700, height=450)

    st.markdown("### 📝 Κατάσταση Σταθμών (Community Feed)")
    st.success("✅ Όλοι οι βασικοί σταθμοί λειτουργούν κανονικά σήμερα.")

# --- SECTION 2: CALCULATOR ---
else:
    st.markdown("### 🔋 Υπολογιστής Κόστους & Αυτονομίας")
    st.write("Υπολόγισε πόσο σου κοστίζει μια φόρτιση στην Κύπρο.")

    col1, col2 = st.columns(2)
    with col1:
        battery_size = st.number_input("Χωρητικότητα Μπαταρίας (kWh):", min_value=20, max_value=120, value=60)
    with col2:
        charging_type = st.selectbox("Τύπος Φόρτισης:", ["Οικιακή Φόρτιση (Night Tariff)", "Δημόσιος AC Φορτιστής", "Ταχυφορτιστής DC (High Power)"])

    rates = {
        "Οικιακή Φόρτιση (Night Tariff)": 0.18,
        "Δημόσιος AC Φορτιστής": 0.35,
        "Ταχυφορτιστής DC (High Power)": 0.50
    }

    rate = rates[charging_type]
    total_cost = battery_size * rate

    if st.button("Υπολογισμός Κόστους"):
        st.markdown(f"""
            <div style="background: rgba(56, 189, 248, 0.1); border: 1px solid #38bdf8; padding: 20px; border-radius: 12px; margin-top: 15px;">
                <h3 style="color: #38bdf8; margin: 0;">Αποτελέσματα Υπολογισμού:</h3>
                <p style="font-size: 1.1rem; margin: 10px 0 0 0;">💰 Εκτιμώμενο Κόστος Πλήρους Φόρτισης: <b>€{total_cost:.2f}</b></p>
                <p style="font-size: 0.9rem; color: #94a3b8; margin: 5px 0 0 0;">Χρέωση βάσει παρόχου: ~€{rate:.2f} ανά kWh</p>
            </div>
        """, unsafe_allow_html=True)
