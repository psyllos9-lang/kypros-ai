import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="E-Hub Cyprus // Pro EV Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED HIGH-TECH STYLING & CLEAN BANNER ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Remove default Streamlit top padding and header */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }
    header[data-testid="stHeader"] {
        display: none !important;
    }
    .stApp {
        background: #070913;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f1f5f9;
    }
    
    /* Gorgeous High-Tech Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, #111827 0%, #1e293b 100%);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .hero-title {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ffffff, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 0.85rem;
        color: #94a3b8;
        margin: 4px 0 0 0;
        font-weight: 500;
    }
    .system-status {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid #10b981;
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0d1322;
        border-right: 1px solid #1e293b;
    }
    
    /* Clean Metric Cards */
    .metric-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: 800;
        color: #38bdf8;
        margin: 0;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #94a3b8;
        margin: 4px 0 0 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- RENDER HIGH-TECH HEADER BANNER ---
st.markdown("""
    <div class="hero-banner">
        <div>
            <h1 class="hero-title">⚡ E-Hub Cyprus</h1>
            <p class="hero-subtitle">Advanced EV Charging & Cost Intelligence Network</p>
        </div>
        <div>
            <span class="system-status">● LIVE SYSTEM</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- EXTENDED CYPRUS CHARGERS DATABASE ---
chargers_db = pd.DataFrame({
    "City": ["Limassol", "Limassol", "Limassol", "Limassol", "Limassol", "Nicosia", "Nicosia", "Nicosia", "Nicosia", "Larnaca", "Larnaca", "Paphos", "Paphos", "Famagusta", "Highway", "Highway"],
    "Name": [
        "MyMall Limassol Ultra-Hub", 
        "Enaerios Coastal Station", 
        "Agios Athanasios Commercial Hub", 
        "Germasogeia Tourist Area Point", 
        "Marina Limassol Fast Bay",
        "Mall of Cyprus Mega-Station", 
        "Athalassa National Park Hub", 
        "Engomi Premium EV Station", 
        "Strovolos Municipal Point",
        "Finikoudes Marina Hub", 
        "Larnaca Airport Express Bay", 
        "Kings Avenue Mall Station", 
        "Paphos Harbour Terminal", 
        "Paralimni Central Charging", 
        "Governor's Beach Highway Station", 
        "Pentaskinos Fast Corridor Hub"
    ],
    "Operator": ["Petrolina (E-point)", "Jolt", "EAC (Electricity Authority)", "Petrolina (E-point)", "Jolt", "Jolt", "EAC", "Petrolina", "EAC", "EAC", "Jolt", "Petrolina", "EAC", "Jolt", "Petrolina (E-point)", "EAC"],
    "Status": ["Available", "Busy", "Available", "Available", "Out of Service", "Available", "Busy", "Available", "Available", "Busy", "Available", "Available", "Busy", "Available", "Available", "Available"],
    "lat": [34.6738, 34.6851, 34.7012, 34.7045, 34.6712, 35.1264, 35.1432, 35.1682, 35.1521, 34.9142, 34.8751, 34.7720, 34.7582, 35.0392, 34.7175, 34.7421],
    "lon": [33.0031, 33.0512, 33.0342, 33.0812, 33.0412, 33.4251, 33.3912, 33.3512, 33.3712, 33.6331, 33.6212, 32.4182, 32.4112, 33.9841, 33.2815, 33.3412],
    "Type": ["DC Ultra-Fast (150kW)", "AC Standard (22kW)", "DC Fast (50kW)", "DC Ultra-Fast (150kW)", "DC Fast (50kW)", "DC Fast (50kW)", "DC Ultra-Fast (150kW)", "DC Fast (50kW)", "AC Standard (22kW)", "DC Fast (50kW)", "DC Ultra-Fast (300kW)", "DC Fast (50kW)", "AC Standard (22kW)", "DC Fast (50kW)", "DC Ultra-Fast (300kW)", "DC Ultra-Fast (300kW)"]
})

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("### 🌐 CONTROL PANEL")
    app_mode = st.radio("Select View:", ["🗺️ Live Network Map", "🔋 Cost & Energy Calculator"], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### 📊 NETWORK METRICS")
    st.markdown("""
        * **Active Chargers:** 68 Nodes
        * **Coverage:** Island-wide (Cyprus)
        * **Status:** 99.8% Operational
    """)

# --- MODE 1: INTERACTIVE MAP ---
if app_mode == "🗺️ Live Network Map":
    st.markdown("### 📍 Interactive Charging Infrastructure Map")
    st.write("Use filters to pinpoint stations by region, operator, or live availability.")

    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        sel_city = st.selectbox("Region:", ["All Regions", "Limassol", "Nicosia", "Larnaca", "Paphos", "Famagusta", "Highway"])
    with col_f2:
        sel_operator = st.selectbox("Operator:", ["All Operators", "Petrolina (E-point)", "Jolt", "EAC (Electricity Authority)"])
    with col_f3:
        sel_status = st.selectbox("Status:", ["All Statuses", "Available", "Busy", "Out of Service"])
    with col_f4:
        sel_speed = st.selectbox("Speed Type:", ["All Speeds", "AC Standard (22kW)", "DC Fast (50kW)", "DC Ultra-Fast (150kW+)"])

    df_filtered = chargers_db.copy()
    if sel_city != "All Regions":
        df_filtered = df_filtered[df_filtered["City"] == sel_city]
    if sel_operator != "All Operators":
        df_filtered = df_filtered[df_filtered["Operator"] == sel_operator]
    if sel_status != "All Statuses":
        df_filtered = df_filtered[df_filtered["Status"] == sel_status]
    if sel_speed != "All Speeds":
        if sel_speed == "DC Ultra-Fast (150kW+)":
            df_filtered = df_filtered[df_filtered["Type"].str.contains("150kW|300kW", na=False)]
        else:
            df_filtered = df_filtered[df_filtered["Type"] == sel_speed]

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
            <div class="metric-card">
                <p class="metric-val">{len(df_filtered)}</p>
                <p class="metric-label">Filtered Stations</p>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        avail_count = len(df_filtered[df_filtered["Status"] == "Available"])
        st.markdown(f"""
            <div class="metric-card">
                <p class="metric-val" style="color: #34d399;">{avail_count}</p>
                <p class="metric-label">Available Now</p>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        busy_count = len(df_filtered[df_filtered["Status"] != "Available"])
        st.markdown(f"""
            <div class="metric-card">
                <p class="metric-val" style="color: #f87171;">{busy_count}</p>
                <p class="metric-label">Occupied / Offline</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- CLEAN OPENSTREETMAP (No political watermarks or external icon badges) ---
    m = folium.Map(location=[35.1264, 33.4251], zoom_start=10, tiles="OpenStreetMap")

    for idx, row in df_filtered.iterrows():
        color = "green" if row["Status"] == "Available" else ("red" if row["Status"] == "Busy" else "gray")
        
        popup_html = f"""
            <div style="font-family: 'Plus Jakarta Sans', sans-serif; min-width: 180px;">
                <b style="font-size: 14px; color: #111827;">{row['Name']}</b><br>
                <span style="font-size: 12px; color: #4b5563;">
                    <b>Operator:</b> {row['Operator']}<br>
                    <b>Type:</b> {row['Type']}<br>
                    <b>Status:</b> <span style="color: {'#16a34a' if row['Status']=='Available' else '#dc2626'}; font-weight: 700;">{row['Status']}</span>
                </span>
            </div>
        """
        
        folium.Marker(
            [row["lat"], row["lon"]],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{row['Name']} ({row['Status']})",
            icon=folium.Icon(color=color, icon="bolt", prefix="fa")
        ).add_to(m)

    st_folium(m, width="100%", height=520, returned_objects=[])

    st.markdown("### 📋 Station Status Directory")
    st.dataframe(df_filtered[["Name", "City", "Operator", "Type", "Status"]], use_container_width=True)

# --- MODE 2: CALCULATOR ---
else:
    st.markdown("### 🔋 Smart Energy & Cost Calculator")
    st.write("Calculate session costs, energy needs, and duration based on Cypriot tariff rates.")

    c1, c2, c3 = st.columns(3)
    with c1:
        battery_size = st.number_input("Vehicle Battery Capacity (kWh):", min_value=20, max_value=120, value=60)
    with c2:
        current_charge = st.slider("Current Battery Level (%):", 0, 90, 20)
    with c3:
        charging_mode = st.selectbox("Charging Speed / Tariff:", [
            "EAC Home Tariff (Night) [€0.17/kWh]", 
            "Public AC Standard [€0.35/kWh]", 
            "DC Ultra-Fast Hub [€0.52/kWh]"
        ])

    kwh_needed = battery_size * ((100 - current_charge) / 100)
    
    if "Night" in charging_mode:
        rate = 0.17
        speed_kw = 7.4
    elif "AC Standard" in charging_mode:
        rate = 0.35
        speed_kw = 22.0
    else:
        rate = 0.52
        speed_kw = 120.0

    total_cost = kwh_needed * rate
    estimated_hours = kwh_needed / speed_kw

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Compute Analytics"):
        res1, res2, res3, res4 = st.columns(4)
        with res1:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-val">{kwh_needed:.1f} kWh</p>
                    <p class="metric-label">Energy Required</p>
                </div>
            """, unsafe_allow_html=True)
        with res2:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-val" style="color: #34d399;">€{total_cost:.2f}</p>
                    <p class="metric-label">Estimated Cost</p>
                </div>
            """, unsafe_allow_html=True)
        with res3:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-val" style="color: #38bdf8;">€{rate:.2f}</p>
                    <p class="metric-label">Rate per kWh</p>
                </div>
            """, unsafe_allow_html=True)
        with res4:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-val" style="color: #a855f7;">~{estimated_hours*60:.0f} min</p>
                    <p class="metric-label">Est. Charging Time</p>
                </div>
            """, unsafe_allow_html=True)
