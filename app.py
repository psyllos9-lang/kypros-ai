import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Page Configuration
st.set_page_config(
    page_title="VoltCy // Cyprus EV Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN CLEAN & HIGH-TECH STYLING ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #f1f5f9;
    }

    /* Clean Header */
    .app-header {
        background: #111827;
        border-bottom: 1px solid #1f2937;
        padding: 1.5rem 2rem;
        margin: -6rem -4rem 2rem -4rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .app-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
    }
    .app-subtitle {
        font-size: 0.85rem;
        color: #9ca3af;
        margin: 2px 0 0 0;
    }
    
    /* Metric Cards */
    .metric-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #38bdf8;
        margin: 0;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #9ca3af;
        text-transform: uppercase;
        margin-top: 4px;
    }

    /* Sidebar Clean Look */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="app-header">
        <div>
            <h1 class="app-title">⚡ VoltCy Hub</h1>
            <p class="app-subtitle">Cyprus Electric Vehicle Charging & Route Intelligence</p>
        </div>
        <div>
            <span style="background: rgba(16, 185, 129, 0.15); color: #34d399; padding: 6px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; border: 1px solid #10b981;">● Online</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### Menu")
    app_mode = st.radio("Select View:", ["🗺️ Interactive Map & Status", "⚡ Cost & Time Calculator"])
    
    st.markdown("---")
    st.markdown("### Network Stats")
    st.markdown("""
        * **Active Chargers:** 68 Nodes
        * **Coverage:** Island-wide (Cyprus)
        * **Operators:** EAC, Petrolina, Jolt
    """)

# --- CYPRUS CHARGERS DATABASE ---
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

# --- MODE 1: INTERACTIVE MAP ---
if app_mode == "🗺️ Interactive Map & Status":
    st.markdown("### Interactive Charging Map")
    st.write("Easily navigate stations across Cyprus. Filter by region, operator, or live availability.")

    # Filters
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        sel_city = st.selectbox("Region:", ["All Regions", "Limassol", "Nicosia", "Larnaca", "Paphos", "Famagusta", "Highway"])
    with col_f2:
        sel_operator = st.selectbox("Operator:", ["All Operators", "Petrolina (E-point)", "Jolt", "EAC (Electricity Authority)"])
    with col_f3:
        sel_status = st.selectbox("Status:", ["All Statuses", "Available", "Busy", "Out of Service"])

    df_filtered = chargers_db.copy()
    if sel_city != "All Regions":
        df_filtered = df_filtered[df_filtered["City"] == sel_city]
    if sel_operator != "All Operators":
        df_filtered = df_filtered[df_filtered["Operator"] == sel_operator]
    if sel_status != "All Statuses":
        df_filtered = df_filtered[df_filtered["Status"] == sel_status]

    # Metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value">{len(df_filtered)}</p>
                <p class="metric-label">Matching Stations</p>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        avail_count = len(df_filtered[df_filtered["Status"] == "Available"])
        st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value" style="color: #34d399;">{avail_count}</p>
                <p class="metric-label">Available Now</p>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        busy_count = len(df_filtered[df_filtered["Status"] != "Available"])
        st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value" style="color: #f87171;">{busy_count}</p>
                <p class="metric-label">Busy / Offline</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Enhanced & Smooth Map (Centered precisely on Cyprus with optimal zoom)
    m = folium.Map(location=[35.1264, 33.4251], zoom_start=10, tiles="CartoDB dark_matter")

    for idx, row in df_filtered.iterrows():
        color = "green" if row["Status"] == "Available" else ("red" if row["Status"] == "Busy" else "gray")
        
        popup_content = f"""
            <div style="font-family: sans-serif; padding: 5px; min-width: 160px;">
                <b style="font-size: 13px; color: #38bdf8;">{row['Name']}</b><br>
                <b>Operator:</b> {row['Operator']}<br>
                <b>Type:</b> {row['Type']}<br>
                <b>Status:</b> <span style="color: {'#34d399' if row['Status']=='Available' else '#f87171'}; font-weight: bold;">{row['Status']}</span>
            </div>
        """
        
        folium.Marker(
            [row["lat"], row["lon"]],
            popup=folium.Popup(popup_content, max_width=250),
            tooltip=f"{row['Name']} ({row['Status']})",
            icon=folium.Icon(color=color, icon="bolt", prefix="fa")
        ).add_to(m)

    st_folium(m, width="100%", height=520)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Station Directory Matrix")
    st.dataframe(df_filtered[["Name", "City", "Operator", "Type", "Status"]], use_container_width=True)

# --- MODE 2: CALCULATOR ---
else:
    st.markdown("### Smart EV Cost & Time Calculator")
    st.write("Accurately calculate your charging session expenses and duration based on Cyprus tariffs.")

    c1, c2, c3 = st.columns(3)
    with c1:
        battery_size = st.number_input("Battery Capacity (kWh):", min_value=20, max_value=120, value=60)
    with c2:
        current_charge = st.slider("Current Battery Level (%):", 0, 90, 20)
    with c3:
        charging_mode = st.selectbox("Tariff & Speed Type:", [
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

    if st.button("Calculate Analytics"):
        res1, res2, res3, res4 = st.columns(4)
        with res1:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-value">{kwh_needed:.1f} kWh</p>
                    <p class="metric-label">Energy Required</p>
                </div>
            """, unsafe_allow_html=True)
        with res2:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-value" style="color: #34d399;">€{total_cost:.2f}</p>
                    <p class="metric-label">Total Cost</p>
                </div>
            """, unsafe_allow_html=True)
        with res3:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-value" style="color: #38bdf8;">€{rate:.2f}</p>
                    <p class="metric-label">Rate / kWh</p>
                </div>
            """, unsafe_allow_html=True)
        with res4:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-value" style="color: #a855f7;">~{estimated_hours*60:.0f} min</p>
                    <p class="metric-label">Est. Charging Time</p>
                </div>
            """, unsafe_allow_html=True)
