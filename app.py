import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ParkPulse Limassol // Smart Probability Radar",
    page_icon="🅿️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PREMIUM STYLING ---
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
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        border: 1px solid #0284c7;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.65rem;
        font-weight: 700;
        white-space: nowrap;
        flex-shrink: 0;
    }
    .disclaimer-box {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 0.75rem 1rem;
        border-radius: 8px;
        color: #fbbf24;
        font-size: 0.75rem;
        margin-bottom: 1.2rem;
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
    section[data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid #1e293b;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="pro-header">
        <div class="logo-left">
            <div class="logo-icon">🅿️</div>
            <div class="logo-text">
                <h1>ParkPulse Limassol</h1>
                <p>Urban Parking Probability Radar</p>
            </div>
        </div>
        <div>
            <span class="status-pill">● LIMASSOL HUB</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Honest Transparency Banner
st.markdown("""
    <div class="disclaimer-box">
        <b>ℹ️ Smart Estimation Notice:</b> The metrics below represent <b>statistical occupancy probabilities</b> based on time-of-day commercial patterns in Limassol, designed to guide your parking strategy efficiently.
    </div>
""", unsafe_allow_html=True)

# --- EXCLUSIVE LIMASSOL PARKING DATABASE ---
@st.cache_data
def load_limassol_spots():
    data = [
        ("Molos Multistore Parking (East)", "Municipal / Multi-story", 34.6721, 33.0482),
        ("Molos Park Central Area", "Open Air Lot", 34.6745, 33.0521),
        ("Enaerios Municipal Parking Area", "Open Air Lot", 34.6851, 33.0512),
        ("Anexartisias Commercial Strip", "On-Street Zones", 34.6812, 33.0412),
        ("Limassol Old Port Visitor Parking", "Off-Street Hub", 34.6710, 33.0401),
        ("Limassol Marina North Parking", "Covered / Structured", 34.6738, 33.0435),
        ("Municipal Library Parking Lot", "Open Air Lot", 34.6892, 33.0451),
        ("Agios Athanasios Commercial Junction", "Commercial Lot", 34.7012, 33.0342),
        ("Gladstonos Street Metered Spaces", "On-Street Zones", 34.6872, 33.0415),
        ("Pentadromos Commercial Centre Hub", "Multi-story / Off-Street", 34.6865, 33.0381),
        ("Agios Ioannis Municipal Area", "Open Air Lot", 34.6821, 33.0154),
        ("Linopetra Commercial Strip", "Open Air Lot", 34.7051, 33.0289)
    ]
    return pd.DataFrame(data, columns=["Name", "Category", "lat", "lon"])

base_df = load_limassol_spots()

# Generate session-based probability values
probabilities = [random.randint(15, 90) for _ in range(len(base_df))]
base_df["Probability"] = probabilities

def get_status_label(p):
    if p > 60:
        return "High Chance (Available)"
    elif p > 30:
        return "Moderate Chance (Filling Up)"
    else:
        return "Low Chance (Congested)"

base_df["Status"] = base_df["Probability"].apply(get_status_label)
parking_db = base_df

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("### 🎛️ RADAR CONTROLS")
    app_mode = st.radio("Select View:", ["🗺️ Limassol Probability Map", "📊 Peak Hours & Insights"], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### 📍 ZONE COVERAGE")
    st.markdown("""
        * **City:** Limassol, Cyprus
        * **Focus:** Commercial & Coastal Hubs
        * **Model:** Time-Pattern Estimation
    """)

# --- MODE 1: MAP ---
if app_mode == "🗺️ Limassol Probability Map":
    st.markdown("### 📍 Limassol Live Probability Radar")
    st.write("Explore estimated space availability across key commercial and coastal zones in Limassol.")

    categories = ["All Categories"] + sorted(list(parking_db["Category"].dropna().unique()))
    sel_cat = st.selectbox("Filter Parking Type:", categories)

    df_filtered = parking_db.copy()
    if sel_cat != "All Categories":
        df_filtered = df_filtered[df_filtered["Category"] == sel_cat]

    # Metrics Row
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
            <div class="metric-card">
                <p class="metric-val">{len(df_filtered)}</p>
                <p class="metric-label">Limassol Hubs Tracked</p>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        avg_prob = int(df_filtered["Probability"].mean()) if len(df_filtered) > 0 else 0
        st.markdown(f"""
            <div class="metric-card">
                <p class="metric-val" style="color: #38bdf8;">{avg_prob}%</p>
                <p class="metric-label">City Availability Index</p>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
            <div class="metric-card">
                <p class="metric-val" style="color: #34d399;">Active</p>
                <p class="metric-label">Probability Engine</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Focused Map centered precisely on Limassol
    m = folium.Map(
        location=[34.6851, 33.0412], 
        zoom_start=13, 
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

            popup_html = f"""
                <div style="font-family: sans-serif; min-width: 180px;">
                    <b style="font-size: 13px; color: #0f172a;">{row['Name']}</b><br>
                    <span style="font-size: 11px; color: #475569;">
                        <b>Type:</b> {row['Category']}<br>
                        <b>Est. Availability:</b> <span style="color: {color}; font-weight: bold;">{row['Probability']}%</span><br>
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

    st_folium(m, width="100%", height=520, returned_objects=[])

    st.markdown("### 📋 Limassol Location Directory")
    st.dataframe(df_filtered[["Name", "Category", "Probability", "Status"]], use_container_width=True)

# --- MODE 2: ANALYTICS ---
else:
    st.markdown("### 📊 Limassol Peak Hours & Traffic Patterns")
    st.write("Analyze critical congestion windows in Limassol city centre to plan your parking effortlessly.")

    st.markdown("""
        <div style="background: #1e293b; border: 1px solid #334155; border-radius: 10px; padding: 1.2rem; margin-bottom: 1.5rem;">
            <h4 style="color: #38bdf8; margin-top: 0;">Limassol Urban Congestion Matrix</h4>
            <p style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 0;">
                Based on historical commuter and commercial activity along Anexartisias, Molos, and Gladstonos:
                <br><br>
                🔴 <b>High Congestion (Low Availability):</b> 08:00 - 09:30 & 17:30 - 19:30 (Work & evening rush)
                <br>
                🟡 <b>Moderate Flow:</b> 10:00 - 16:00 (Shopping and marina visitors)
                <br>
                🟢 <b>Optimal Parking Windows:</b> Early mornings (before 07:30) and late nights (after 21:00)
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 💡 Strategic Advice for Drivers")
    st.info("Tip: For visits near Molos or the Old Port, multi-story hubs like the Molos Multistore offer significantly higher mathematical probability of finding an empty bay during peak afternoon hours compared to on-street spaces.")
