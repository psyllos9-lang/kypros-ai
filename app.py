import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PadelPulse Limassol // Hybrid System",
    page_icon="🎾",
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
        <div class="cyber-title">🎾 PadelPulse Limassol</div>
        <span class="live-badge">⚡ HYBRID BOOKING & MATCHMAKING</span>
    </div>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if "bookings" not in st.session_state:
    st.session_state.bookings = {} # format: {"Court 1 - 18:00": "Booked"}

if "open_matches" not in st.session_state:
    st.session_state.open_matches = [
        {"Court": "Limassol Padel Club - Court 1", "Time": "19:00", "Level": "Intermediate (3.0-3.5)", "Needed": "2 παίκτες"},
        {"Court": "PadelPro Arena - Court 2", "Time": "20:30", "Level": "Advanced (4.0+)", "Needed": "1 παίκτης"}
    ]

# --- COURTS DATA ---
courts = [
    "Limassol Padel Club - Court 1 (Indoor)",
    "Limassol Padel Club - Court 2 (Outdoor)",
    "PadelPro Arena - Court 1 (Indoor)",
    "PadelPro Arena - Court 2 (Panoramic)"
]

time_slots = ["17:00", "18:00", "19:00", "20:00", "21:00", "22:00"]

# --- NAVIGATION TABS ---
tab1, tab2, tab3 = st.tabs(["📅 Κρατήσεις Γηπέδων", "👥 Find a Player (Matchmaking)", "📊 Κατάσταση & Στατιστικά"])

with tab1:
    st.markdown("### 🕒 Live Διαθεσιμότητα & Κράτηση Γηπέδου")
    st.write("Επίλεξε γήπεδο και ώρα για να κλείσεις τη θέση σου άμεσα.")
    
    selected_court = st.selectbox("Επιλογή Γηπέδου:", courts)
    selected_time = st.selectbox("Επιλογή Ώρας:", time_slots)
    
    slot_key = f"{selected_court} @ {selected_time}"
    is_booked = slot_key in st.session_state.bookings
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **Κατάσταση Θυρίδας:**  
        """ + ("🔴 Κρατημένο" if is_booked else "🟢 Ελεύθερο για Κράτηση"))
    with col2:
        player_name = st.text_input("Όνομα Παίκτη / Κρατήσεις:", placeholder="π.χ. Ανδρέας")

    if not is_booked:
        if st.button("🚀 Ολοκλήρωση Κράτησης"):
            if player_name:
                st.session_state.bookings[slot_key] = player_name
                st.success(f"Επιτυχία! Η κράτηση για το {selected_court} στις {selected_time} κατοχυρώθηκε.")
                st.rerun()
            else:
                st.warning("Παρακαλώ εισαγάγετε όνομα κράτησης.")
    else:
        st.warning(f"Η συγκεκριμένη ώρα είναι ήδη κρατημένη από τον χρήστη: **{st.session_state.bookings[slot_key]}**")

with tab2:
    st.markdown("### 👥 Ανοιχτοί Αγώνες (Matchmaking)")
    st.write("Σου λείπουν άτομα για να κλείσετε τετράδα; Δημιούργησε ανοιχτή πρόσκληση ή κάνε Join σε υπάρχοντα αγώνα!")

    # Display active open matches
    if st.session_state.open_matches:
        for idx, match in enumerate(st.session_state.open_matches):
            st.markdown(f"""
                <div class="interactive-card">
                    <b>📍 {match['Court']}</b><br>
                    ⏰ Ώρα: <b>{match['Time']}</b> | 🎯 Επίπεδο: <b>{match['Level']}</b><br>
                    👥 Αναζήτηση: <span style="color: #38bdf8; font-weight: bold;">{match['Needed']}</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.write("Δεν υπάρχουν ενεργές αγγελίες αυτή τη στιγμή.")

    st.markdown("---")
    st.markdown("#### ➕ Δημιουργία Νέου Open Match")
    with st.form("match_form"):
        m_court = st.selectbox("Γήπεδο:", courts, key="m_court")
        m_time = st.selectbox("Ώρα:", time_slots, key="m_time")
        m_level = st.selectbox("Επίπεδο παικτών:", ["Beginner (1.0-2.0)", "Intermediate (2.5-3.5)", "Advanced (4.0+)"])
        m_needed = st.selectbox("Τι χρειάζεσαι;", ["1 παίκτης", "2 παίκτες", "3 παίκτες"])
        
        m_submit = st.form_submit_button("📢 Δημοσίευση Αγγελίας")
        if m_submit:
            st.session_state.open_matches.append({
                "Court": m_court,
                "Time": m_time,
                "Level": m_level,
                "Needed": m_needed
            })
            st.success("Η αγγελία σου δημοσιεύτηκε επιτυχώς!")
            st.rerun()

with tab3:
    st.markdown("### 📊 Συνολική Εικόνα & Στατιστικά")
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-box"><p class="metric-num">{len(courts)}</p><p class="metric-txt">Ενεργά Γήπεδα</p></div>', unsafe_allow_html=True)
    with m2:
        total_bookings = len(st.session_state.bookings)
        st.markdown(f'<div class="metric-box"><p class="metric-num">{total_bookings}</p><p class="metric-txt">Active Bookings</p></div>', unsafe_allow_html=True)
    with m3:
        open_reqs = len(st.session_state.open_matches)
        st.markdown(f'<div class="metric-box"><p class="metric-num" style="color: #34d399;">{open_reqs}</p><p class="metric-txt">Open Matches</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📋 Λίστα Τρέχουσων Κρατήσεων")
    if st.session_state.bookings:
        booking_data = [{"Slot": k, "Player": v} for k, v in st.session_state.bookings.items()]
        st.dataframe(pd.DataFrame(booking_data), use_container_width=True, hide_index=True)
    else:
        st.info("Δεν υπάρχουν καταχωρισμένες κρατήσεις ακόμη.")
