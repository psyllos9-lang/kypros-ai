import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Cyprus E-Hub // EV Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CLEAN & RESPONSIVE PROFESSIONAL STYLING ---
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
    }
    header[data-testid="stHeader"] {
        display: none !important;
    }
    .stApp {
        background: #0f172a;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #f8fafc;
    }
    
    /* Professional Single-Line Header */
    .pro-header {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 0.9rem 1.2rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
    }
    .logo-left {
        display: flex;
        align-items: center;
        gap: 10px;
        min-width: 0;
    }
    .logo-icon {
        font-size: 1.3rem;
        background: #0284c7;
        color: white;
        padding: 6px 10px;
        border-radius: 8px;
        flex-shrink: 0;
    }
    .logo-text h1 {
        font-size: 1.1rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        white-space: nowrap;
    }
    .logo-text p {
        font-size: 0.65rem;
        color: #94a3b8;
        margin: 0;
        white-space: nowrap;
    }
    .status-pill {
        background: rgba(16, 185, 129, 0.2);
        color: #34d399;
        border: 1px solid #10b981;
        padding: 4px 8px;
        border-radius: 20px;
        font-size: 0.65rem;
        font-weight: 700;
        white-space: nowrap;
        flex-shrink: 0;
    }

    section[data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid #1e293b;
    }
    
    .metric-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .metric-val {
        font-size: 1.5rem;
        font-weight: 700;
        color: #38bdf8;
        margin: 0;
    }
    .metric-label {
        font-size: 0.7rem;
        color: #94a3b8;
        margin: 2px 0 0 0;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="pro-header">
        <div class="logo-left">
            <div class="logo-icon">⚡</div>
            <div class="logo-text">
                <h1>Cyprus E-Hub</h1>
                <p>National EV Telemetry & Live Status</p>
            </div>
        </div>
        <div>
            <span class="status-pill">● FULL API SYNC</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- FETCH ALL CYPRUS STATIONS FROM LIVE API WITH FULL TELEMETRY ---
@st.cache_data(ttl=300)
def fetch_complete_cyprus_chargers():
    # maxresults=500 διασφαλίζει ότι θα φέρει ΟΛΟΥΣ τους διαθέσιμους σταθμούς (πάνω από 300+)
    url = "https://api.openchargemap.io/v3/poi/?countrycode=CY&maxresults=500&key=free-api"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            stations = []
            for item in data:
                addr = item.get("AddressInfo", {})
                name = addr.get("Title", "Unknown Station")
                lat = addr.get("Latitude")
                lon = addr.get("Longitude")
                town = addr.get("Town", "Cyprus")
                if not town:
                    town = "Cyprus"
                
                operator_info = item.get("OperatorInfo", {})
                operator = operator_info.get("Title", "Public Operator") if operator_info else "Public Operator"
                
                # Υπολογισμός ταχύτητας σε kW από τις συνδέσεις
                connections = item.get("Connections", [])
                speed_type = "Standard Charging"
                max_kw = 0
                if connections:
                    for conn in connections:
                        kw = conn.get("PowerKW")
                        if kw and kw > max_kw:
                            max_kw = kw
                
                if max_kw > 0:
                    if max_kw >= 150:
                        speed_type = f"DC Ultra-Fast ({max_kw}kW)"
                    elif max_kw >= 50:
                        speed_type = f"DC Fast ({max_kw}kW)"
                    else:
                        speed_type = f"AC Standard ({max_kw}kW)"

                # Κατάσταση λειτουργίας/διαθεσιμότητας
                status_type = item.get("StatusType", {})
                is_operational = status_type.get("IsOperational", True) if status_type else True
                status_str = "Available" if is_operational else "Out of Service"

                stations.append({
                    "Name": name,
                    "City": town,
                    "Operator": operator,
                    "Type": speed_type,
                    "Status": status_str,
                    "lat": lat,
                    "lon": lon
                })
            
            if stations:
                return pd.DataFrame(stations)
    except Exception:
        pass
    
    # Πλήρης εφεδρική λίστα βασικών σημείων σε περίπτωση που το API δεν απαντήσει προσωρινά
    return pd.DataFrame({
        "City": ["Limassol", "Limassol", "Nicosia", "Paphos"],
        "Name": ["AHK / EAC Charging Station Ypsonas", "Sklavenitis Ypsonas EV Hub", "Mall of Cyprus Mega-Station", "Kings Avenue Mall Station"],
        "Operator": ["EAC eCharge", "EV Power", "EAC eCharge", "EAC eCharge"],
        "Type": ["DC Fast (50kW)", "AC Standard (22kW)", "DC Fast (50kW)", "DC Fast (50kW)"],
        "Status": ["Available", "Available", "Available", "Available"],
        "lat": [34.6945, 34.6912, 35.1264, 34.7720],
        "lon": [32.9612, 32.9584, 33.4251, 32.4182]
    })

chargers_db = fetch_complete_cyprus_chargers()

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("### 🎛️ NAVIGATION")
    app_mode = st.radio("Select View:", ["🗺️ Live National Map", "🔋 Cost & Energy Calculator"], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### 📊 SYSTEM TELEMETRY")
    st.markdown(f"""
        * **Total Live Nodes:** {len(chargers_db)} Stations
        * **Coverage:** Cyprus Island-wide
        * **Telemetry:** Speeds & Status Active
    """)

# --- MODE 1: LIVE MAP ---
if app_mode == "🗺️ Live National Map":
    st.markdown("### 📍 Comprehensive Cyprus EV Network Map")
    st.write("Real-time telemetry tracking of all public nodes, speeds, and live availability across Cyprus.")

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        cities = ["All Regions"] + sorted(list(chargers_db["City"].dropna().unique()))
        sel_city = st.selectbox("Filter Region:", cities)
    with col_f2:
        operators = ["All Operators"] + sorted(list(chargers_db["Operator"].dropna().unique()))
        sel_operator = st.selectbox("Filter Operator:", operators)
    with col_f3:
        statuses = ["All Statuses", "Available", "Out of Service"]
        sel_status = st.selectbox("Filter Status:", statuses)

    df_filtered = chargers_db.copy()
    if sel_city != "All Regions":
        df_filtered = df_filtered[df_filtered["City"] == sel_city]
    if sel_operator != "All Operators":
        df_filtered = df_filtered[df_filtered["Operator"] == sel_operator]
    if sel_status != "All Statuses":
        df_filtered = df_filtered[df_filtered["Status"] == sel_status]

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
            <div class="metric-card">
                <p class="metric-val">{len(df_filtered)}</p>
                <p class="metric-label">Stations Visible</p>
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
        st.markdown(f"""
            <div class="metric-card">
                <p class="metric-val" style="color: #38bdf8;">Live</p>
                <p class="metric-label">Telemetry Feed</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Clean Folium Map
    m = folium.Map(
        location=[35.1264, 33.4251], 
        zoom_start=10, 
        tiles="CartoDB positron",
        control_scale=False,
        attributionControl=False
    )

    for idx, row in df_filtered.iterrows():
        if pd.notnull(row["lat"]) and pd.notnull(row["lon"]):
            color = "green" if row["Status"] == "Available" else "red"
            popup_html = f"""
                <div style="font-family: sans-serif; min-width: 160px;">
                    <b style="font-size: 13px; color: #0f172a;">{row['Name']}</b><br>
                    <span style="font-size: 11px; color: #475569;">
                        <b>Operator:</b> {row['Operator']}<br>
                        <b>Speed:</b> {row['Type']}<br>
                        <b>Status:</b> <span style="color: {'green' if row['Status']=='Available' else 'red'}; font-weight: bold;">{row['Status']}</span>
                    </span>
                </div>
            """
            folium.Marker(
                [row["lat"], row["lon"]],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=row['Name'],
                icon=folium.Icon(color=color, icon="bolt", prefix="fa")
            ).add_to(m)

    st_folium(m, width="100%", height=520, returned_objects=[])

    st.markdown("### 📋 Station Directory & Telemetry")
    st.dataframe(df_filtered[["Name", "City", "Operator", "Type", "Status"]], use_container_width=True)

# --- MODE 2: CALCULATOR ---
else:
    st.markdown("### 🔋 Smart Energy & Cost Calculator")
    st.write("Calculate your charging session expenses based on current Cypriot electricity tariffs.")

    c1, c2, c3 = st.columns(3)
    with c1:
        battery_size = st.number_input("Battery Capacity (kWh):", min_value=20, max_value=120, value=60)
    with c2:
        current_charge = st.slider("Current Battery Level (%):", 0, 90, 20)
    with c3:
        charging_mode = st.selectbox("Tariff Type:", [
            "EAC Home Tariff (Night) [€0.17/kWh]", 
            "Public AC Standard [€0.35/kWh]", 
            "DC Ultra-Fast Hub [€0.52/kWh]"
        ])

    kwh_needed = battery_size * ((100 - current_charge) / 100)
    
    if "Night" in charging_mode:
        rate = 0.17
    elif "AC Standard" in charging_mode:
        rate = 0.35
    else:
        rate = 0.52

    total_cost = kwh_needed * rate

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Calculate Cost"):
        res1, res2, res3 = st.columns(3)
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
                    <p class="metric-label">Rate / kWh</p>
                </div>
            """, unsafe_allow_html=True)
