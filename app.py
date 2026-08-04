import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PadelPulse Limassol // Premium Hub",
    page_icon="🎾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- ULTRA-MODERN PREMIUM DESIGN ---
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        max-width: 700px !important;
    }
    header[data-testid="stHeader"] {
        display: none !important;
    }
    .stApp {
        background: #090d16;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #f1f5f9;
    }
    .hero-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    .hero-title {
        font-size: 1.6rem;
        font-weight: 900;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 0.8rem;
        color: #94a3b8;
        margin-top: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .custom-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }
    .stButton>button {
        background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%);
        color: white;
        border: none;
        border-radius: 14px;
        font-weight: 700;
        padding: 0.75rem 1rem;
        width: 100%;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.25);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.8);
        padding: 6px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        color: #94a3b8;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .stTabs [aria-selected="true"] {
        background: #0284c7 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER HERO ---
st.markdown("""
    <div class="hero-card">
        <div class="hero-title">🎾 PadelPulse Limassol</div>
        <div class="hero-subtitle">Smart Courts & Matchmaking Hub</div>
    </div>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if "bookings" not in st.session_state:
    st.session_state.bookings = {}

if "open_matches" not in st.session_state:
    st.session_state.open_matches = [
        {"Court": "Limassol Padel Club - Court 1", "Time": "19:00", "Level": "Intermediate (3.0-3.5)", "Player": "Μιχάλης", "Needed": "2 παίκτες"},
        {"Court": "PadelPro Arena - Court 2", "Time": "20:30", "Level": "Advanced (4.0+)", "Player": "Αλέξανδρος", "Needed": "1 παίκτης"}
    ]

# --- DATA ---
courts = [
    "Limassol Padel Club - Court 1 (Indoor)",
    "Limassol Padel Club - Court 2 (Outdoor)",
    "PadelPro Arena - Court 1 (Indoor)",
    "PadelPro Arena - Court 2 (Panoramic)"
]

time_slots = ["17:00", "18:00", "19:00", "20:00", "21:00", "22:00"]

# --- CLEAN TABS ---
tab1, tab2, tab3 = st.tabs(["📅 Κρατήσεις", "👥 Find Player", "⚡ Live Feed"])

with tab1:
    st.markdown("#### 🕒 Γρήγορη Κράτηση Γηπέδου")
    st.write("Διάλεξε γήπεδο και ώρα για άμεση δέσμευση.")
    
    with st.container():
        selected_court = st.selectbox("Επιλογή Γηπέδου:", courts, label_visibility="collapsed")
        selected_time = st.selectbox("Επιλογή Ώρας:", time_slots, label_visibility="collapsed")
        
        slot_key = f"{selected_court} @ {selected_time}"
        is_booked = slot_key in st.session_state.bookings
        
        player_name = st.text_input("Το όνομα σου:", placeholder="π.χ. Γιώργος", label_visibility="collapsed")
        
        if not is_booked:
            if st.button("✨ Κλείσε το Γήπεδο Τώρα"):
                if player_name.strip():
                    st.session_state.bookings[slot_key] = player_name.strip()
                    st.success(f"Επιτυχία! Το γήπεδο κλείστηκε για τις {selected_time}.")
                    st.rerun()
                else:
                    st.warning("Παρακαλώ γράψε το όνομα σου.")
        else:
            st.error(f"⚠️ Η Ώρα αυτή είναι κρατημένη από: **{st.session_state.bookings[slot_key]}**")

with tab2:
    st.markdown("#### 👥 Ανοιχτές Αγγελίες (Matchmaking)")
    st.write("Βρες παίκτες για να συμπληρώσεις τετράδα.")

    if st.session_state.open_matches:
        for match in st.session_state.open_matches:
            st.markdown(f"""
                <div class="custom-card">
                    <b>📍 {match['Court']}</b><br>
                    <span style="color: #38bdf8;">⏰ {match['Time']}</span> &nbsp;|&nbsp; <span style="color: #cbd5e1;">🎯 {match['Level']}</span><br>
                    <div style="margin-top: 8px; font-size: 0.85rem;">👤 Δημιουργός: <b>{match['Player']}</b> &nbsp;|&nbsp; Λείπουν: <b style="color: #34d399;">{match['Needed']}</b></div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Δεν υπάρχουν ενεργές αγγελίες.")

    st.markdown("---")
    st.markdown("#### ➕ Νέα Αγγελία Αγώνα")
    with st.form("match_form", border=False):
        m_court = st.selectbox("Γήπεδο:", courts)
        m_time = st.selectbox("Ώρα:", time_slots)
        m_level = st.selectbox("Επίπεδο:", ["Beginner (1.0-2.0)", "Intermediate (2.5-3.5)", "Advanced (4.0+)"])
        m_player = st.text_input("Όνομα σου:", placeholder="π.χ. Νίκος")
        m_needed = st.selectbox("Τι ψάχνεις;", ["1 παίκτης", "2 παίκτες", "3 παίκτες"])
        
        if st.form_submit_button("🚀 Δημοσίευση"):
            if m_player.strip():
                st.session_state.open_matches.append({
                    "Court": m_court,
                    "Time": m_time,
                    "Level": m_level,
                    "Player": m_player.strip(),
                    "Needed": m_needed
                })
                st.success("Η αγγελία ανέβηκε επιτυχώς!")
                st.rerun()
            else:
                st.warning("Συμπλήρωσε το όνομα σου.")

with tab3:
    st.markdown("#### 📊 Σύνοψη Δραστηριότητας")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Ενεργές Κρατήσεις", len(st.session_state.bookings))
    with col2:
        st.metric("Open Matches", len(st.session_state.open_matches))

    st.markdown("---")
    st.markdown("#### 📋 Τρέχουσες Κρατήσεις")
    if st.session_state.bookings:
        df_book = pd.DataFrame([{"Γήπεδο & Ώρα": k, "Παίκτης": v} for k, v in st.session_state.bookings.items()])
        st.dataframe(df_book, use_container_width=True, hide_index=True)
    else:
        st.write("Καμία κράτηση ακόμα για σήμερα.")
