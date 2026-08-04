import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PadelPulse Limassol // Multi-Language Hub",
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
    </style>
""", unsafe_allow_html=True)

# --- LANGUAGE DICTIONARIES ---
translations = {
    "Ελληνικά": {
        "title": "🎾 PadelPulse Λεμεσός",
        "subtitle": "Κρατήσεις & Matchmaking σε πραγματικό χρόνο",
        "tab1": "📅 Κρατήσεις",
        "tab2": "👥 Εύρεση Παικτη",
        "tab3": "⚡ Live Status",
        "book_title": "🕒 Κράτηση Γηπέδου",
        "book_desc": "Επίλεξε ημερομηνία, Club, γήπεδο και ώρα:",
        "date_label": "Επιλογή Ημερομηνίας:",
        "club_label": "Επιλογή Club:",
        "court_label": "Επιλογή Γηπέδου:",
        "time_label": "Επιλογή Ώρας:",
        "name_label": "Το όνομα σου:",
        "name_placeholder": "π.χ. Ανδρέας",
        "book_btn": "✨ Ολοκλήρωση Κράτησης",
        "success_book": "Επιτυχία! Το γήπεδο κλείστηκε.",
        "name_warn": "Παρακαλώ γράψε το όνομα σου.",
        "already_booked": "⚠️ Η Ημερομηνία και η Ώρα αυτή είναι κρατημένη από:",
        "match_title": "👥 Find a Player (Matchmaking)",
        "match_desc": "Βρες άτομα για να κλείσετε τετράδα.",
        "no_matches": "Δεν υπάρχουν ενεργές αγγελίες.",
        "create_match": "➕ Δημιουργία Αγγελίας",
        "level_label": "Επίπεδο:",
        "looking_for": "Τι ψάχνεις;",
        "publish_btn": "🚀 Δημοσίευση Αγγελίας",
        "match_success": "Η αγγελία σου ανέβηκε επιτυχώς!",
        "stats_title": "⚡ Live Κατάσταση & Σύνοψη",
        "active_bookings": "Ενεργές Κρατήσεις",
        "open_listings": "Open Matches",
        "table_title": "📋 Τρέχουσες Κρατήσεις στη Λεμεσό",
        "no_bookings": "Καμία ενεργή κράτηση αυτή τη στιγμή."
    },
    "English": {
        "title": "🎾 PadelPulse Limassol",
        "subtitle": "Real-time Courts & Matchmaking Hub",
        "tab1": "📅 Bookings",
        "tab2": "👥 Find Player",
        "tab3": "⚡ Live Status",
        "book_title": "🕒 Court Booking",
        "book_desc": "Select date, Club, court, and time slot:",
        "date_label": "Select Date:",
        "club_label": "Select Club:",
        "court_label": "Select Court:",
        "time_label": "Select Time:",
        "name_label": "Your Name:",
        "name_placeholder": "e.g., Andrew",
        "book_btn": "✨ Complete Booking",
        "success_book": "Success! Court has been booked.",
        "name_warn": "Please enter your name.",
        "already_booked": "⚠️ This date and slot are already booked by:",
        "match_title": "👥 Find a Player (Matchmaking)",
        "match_desc": "Find players to complete your match.",
        "no_matches": "No active listings found.",
        "create_match": "➕ Create Listing",
        "level_label": "Level:",
        "looking_for": "Looking for:",
        "publish_btn": "🚀 Publish Listing",
        "match_success": "Listing published successfully!",
        "stats_title": "⚡ Live Status & Summary",
        "active_bookings": "Active Bookings",
        "open_listings": "Open Matches",
        "table_title": "📋 Current Bookings in Limassol",
        "no_bookings": "No active bookings at the moment."
    },
    "Русский": {
        "title": "🎾 PadelPulse Лимассол",
        "subtitle": "Корты и поиск игроков в реальном времени",
        "tab1": "📅 Бронирование",
        "tab2": "👥 Найти игрока",
        "tab3": "⚡ Статус",
        "book_title": "🕒 Бронирование корта",
        "book_desc": "Выберите дату, клуб, корт и время:",
        "date_label": "Выберите дату:",
        "club_label": "Выберите клуб:",
        "court_label": "Выберите корт:",
        "time_label": "Выберите время:",
        "name_label": "Ваше имя:",
        "name_placeholder": "например, Алексей",
        "book_btn": "✨ Забронировать",
        "success_book": "Успешно! Корт забронирован.",
        "name_warn": "Пожалуйста, введите ваше имя.",
        "already_booked": "⚠️ Эта дата и время уже забронированы:",
        "match_title": "👥 Поиск игроков (Matchmaking)",
        "match_desc": "Найдите игроков для матча.",
        "no_matches": "Нет активных объявлений.",
        "create_match": "➕ Создать объявление",
        "level_label": "Уровень:",
        "looking_for": "Кто нужен:",
        "publish_btn": "🚀 Опубликовать",
        "match_success": "Объявление успешно опубликовано!",
        "stats_title": "⚡ Статус и сводка",
        "active_bookings": "Активные брони",
        "open_listings": "Открытые матчи",
        "table_title": "📋 Текущие бронирования в Лимассоле",
        "no_bookings": "В данный момент нет активных бронирований."
    },
    "עברית": {
        "title": "🎾 PadelPulse לימסול",
        "subtitle": "מרכז מגרשים ושידוך שחקנים בזמן אמת",
        "tab1": "📅 הזמנות",
        "tab2": "👥 מצא שחקן",
        "tab3": "⚡ סטטוס חי",
        "book_title": "🕒 הזמנת מגרש",
        "book_desc": "בחר תאריך, מועדון, מגרש ושעה:",
        "date_label": "בחר תאריך:",
        "club_label": "בחר מועדון:",
        "court_label": "בחר מגרש:",
        "time_label": "בחר שעה:",
        "name_label": "השם שלך:",
        "name_placeholder": "לדוגמה, דוד",
        "book_btn": "✨ בצע הזמנה",
        "success_book": "הצלחה! המגרש הוזמן.",
        "name_warn": "אנא הזן את שמך.",
        "already_booked": "⚠️ תאריך ושעה אלו כבר תפוסים על ידי:",
        "match_title": "👥 מציאת שחקנים (Matchmaking)",
        "match_desc": "מצא שחקנים להשלמת רביעייה.",
        "no_matches": "אין מודעות פעילות כרגע.",
        "create_match": "➕ פרסם מודעה",
        "level_label": "רמה:",
        "looking_for": "מה מחפש?",
        "publish_btn": "🚀 פרסם מודעה",
        "stats_title": "⚡ סטטוס וסיכום",
        "active_bookings": "הזמנות פעילות",
        "open_listings": "משחקים פתוחים",
        "table_title": "📋 הזמנות נוכחיות בלימסול",
        "no_bookings": "אין הזמנות פעילות כרגע."
    }
}

# --- TOP LANGUAGE SELECTOR BAR ---
selected_lang = st.selectbox(
    "🌐 Language / Γλώσσα / Язык / שפה",
    ["Ελληνικά", "English", "Русский", "עברית"],
    index=0,
    label_visibility="visible"
)

t = translations[selected_lang]

# --- HEADER HERO ---
st.markdown(f"""
    <div class="hero-card">
        <div class="hero-title">{t['title']}</div>
        <div class="hero-subtitle">{t['subtitle']}</div>
    </div>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if "bookings" not in st.session_state:
    st.session_state.bookings = {}

if "open_matches" not in st.session_state:
    st.session_state.open_matches = [
        {"Club": "PadelPro Limassol", "Court": "Court 1 (Indoor)", "Date": str(datetime.now().date()), "Time": "19:00", "Level": "Intermediate (3.0-3.5)", "Player": "Μιχάλης", "Needed": "2 παίκτες"},
        {"Club": "Limassol Padel Club", "Court": "Court 3 (Panoramic)", "Date": str(datetime.now().date()), "Time": "20:30", "Level": "Advanced (4.0+)", "Player": "Александр", "Needed": "1 player"}
    ]

# --- CLUBS & COURTS ---
clubs_data = {
    "PadelPro Limassol": [
        "Court 1 (Indoor)", 
        "Court 2 (Indoor)", 
        "Court 3 (Outdoor)"
    ],
    "Limassol Padel Club": [
        "Center Court (WPT Official)", 
        "Court 2 (Outdoor)", 
        "Court 3 (Panoramic)"
    ],
    "Padel House Limassol": [
        "Court 1 (Indoor Pro)", 
        "Court 2 (Indoor)"
    ]
}

time_slots = ["16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00"]

# --- TABS ---
tab1, tab2, tab3 = st.tabs([t['tab1'], t['tab2'], t['tab3']])

with tab1:
    st.markdown(f"#### {t['book_title']}")
    st.write(t['book_desc'])
    
    with st.form("booking_form", border=False):
        selected_date = st.date_input(t['date_label'], value=datetime.now())
        selected_club = st.selectbox(t['club_label'], list(clubs_data.keys()))
        selected_court = st.selectbox(t['court_label'], clubs_data[selected_club])
        selected_time = st.selectbox(t['time_label'], time_slots)
        player_name = st.text_input(t['name_label'], placeholder=t['name_placeholder'])
        
        submit_booking = st.form_submit_button(t['book_btn'])
        
        if submit_booking:
            slot_key = f"{selected_date} | {selected_club} - {selected_court} @ {selected_time}"
            if slot_key in st.session_state.bookings:
                st.error(f"{t['already_booked']} **{st.session_state.bookings[slot_key]}**")
            elif not player_name.strip():
                st.warning(t['name_warn'])
            else:
                st.session_state.bookings[slot_key] = player_name.strip()
                st.success(t['success_book'])
                st.rerun()

with tab2:
    st.markdown(f"#### {t['match_title']}")
    st.write(t['match_desc'])

    if st.session_state.open_matches:
        for match in st.session_state.open_matches:
            st.markdown(f"""
                <div class="custom-card">
                    <b>📍 {match['Club']}</b> ({match['Court']})<br>
                    <span style="color: #38bdf8;">📅 {match.get('Date', 'Today')} &nbsp;|&nbsp; ⏰ {match['Time']}</span><br>
                    <span style="color: #cbd5e1;">🎯 {match['Level']}</span><br>
                    <div style="margin-top: 8px; font-size: 0.85rem;">👤 Host: <b>{match['Player']}</b> &nbsp;|&nbsp; Wanted: <b style="color: #34d399;">{match['Needed']}</b></div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info(t['no_matches'])

    st.markdown("---")
    st.markdown(f"#### {t['create_match']}")
    with st.form("match_form", border=False):
        m_date = st.date_input(t['date_label'], value=datetime.now(), key="match_date")
        m_club = st.selectbox("Club:", list(clubs_data.keys()), key="match_club")
        m_court = st.selectbox(t['court_label'], clubs_data[m_club], key="match_court")
        m_time = st.selectbox(t['time_label'], time_slots, key="match_time")
        m_level = st.selectbox(t['level_label'], ["Beginner (1.0-2.0)", "Intermediate (2.5-3.5)", "Advanced (4.0+)"])
        m_player = st.text_input(t['name_label'], placeholder="π.χ. Νίκος", key="match_player")
        m_needed = st.selectbox(t['looking_for'], ["1 player / παίκτης", "2 players / παίκτες", "3 players / παίκτες"])
        
        if st.form_submit_button(t['publish_btn']):
            if m_player.strip():
                st.session_state.open_matches.append({
                    "Club": m_club,
                    "Court": m_court,
                    "Date": str(m_date),
                    "Time": m_time,
                    "Level": m_level,
                    "Player": m_player.strip(),
                    "Needed": m_needed
                })
                st.success(t['match_success'])
                st.rerun()
            else:
                st.warning(t['name_warn'])

with tab3:
    st.markdown(f"#### {t['stats_title']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(t['active_bookings'], len(st.session_state.bookings))
    with col2:
        st.metric(t['open_listings'], len(st.session_state.open_matches))

    st.markdown("---")
    st.markdown(f"#### {t['table_title']}")
    if st.session_state.bookings:
        df_book = pd.DataFrame([{"Date, Court & Slot": k, "Player": v} for k, v in st.session_state.bookings.items()])
        st.dataframe(df_book, use_container_width=True, hide_index=True)
    else:
        st.info(t['no_bookings'])
