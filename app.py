import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ParkPulse Limassol // 1-Click Community Parking",
    page_icon="🅿️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- PROFESSIONAL DESIGN ---
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        max-width: 750px !important;
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
        background: linear-gradient(135deg, #064e3b 0%, #022c22 100%);
        border: 1px solid rgba(52, 211, 153, 0.3);
        border-radius: 20px;
        padding: 1.2rem;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    }
    .hero-title {
        font-size: 1.5rem;
        font-weight: 900;
        color: #ffffff;
        margin: 0;
    }
    .hero-subtitle {
        font-size: 0.7rem;
        color: #34d399;
        margin-top: 4px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
    }
    .stButton>button {
        background: linear-gradient(90deg, #059669 0%, #34d399 100%);
        color: white;
        border: none;
        border-radius: 14px;
        font-weight: 800;
        padding: 0.85rem 1rem;
        width: 100%;
        font-size: 1.05rem;
        box-shadow: 0 4px 15px rgba(52, 211, 153, 0.3);
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
        background: #059669 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- LANGUAGE DICTIONARIES ---
translations = {
    "Ελληνικά": {
        "title": "🅿️ ParkPulse Λεμεσός",
        "subtitle": "Σύστημα Άμεσης Απελευθέρωσης με 1 Κλικ",
        "tab1": "🗺️ Live Χάρτης Θέσεων",
        "tab2": "🚀 Ελευθερώνω Τώρα",
        "map_title": "Ζωντανός Χάρτης Λεμεσού",
        "map_desc": "Δείτε τις διαθέσιμες θέσεις και πλοηγηθείτε απευθείας με Google Maps:",
        "nav_btn": "🧭 GPS Navigation (Google Maps)",
        "claim_btn": "🚗 Την πήρα! (Κατάργηση)",
        "success_claim": "Ευχαριστούμε! Η θέση αφαιρέθηκε από τον χάρτη.",
        "no_spots": "Δεν υπάρχουν διαθέσιμες θέσεις στον χάρτη αυτή τη στιγμή.",
        "form_title": "🚀 Άμεση Δημοσίευση Ελεύθερης Θέσης",
        "form_desc": "Επιλέξτε τη ζώνη/οδό που βρίσκεστε και πατήστε το κουμπί για να ενημερωθούν αμέσως οι οδηγοί:",
        "spot_label": "Επιλέξτε Περιοχή / Οδό στη Λεμεσό:",
        "publish_btn": "✅ ΕΛΕΥΘΕΡΩΝΩ ΘΕΣΗ ΤΩΡΑ",
        "success_publish": "Η θέση σας δημοσιεύτηκε επιτυχώς και είναι ορατή στον χάρτη!"
    },
    "English": {
        "title": "🅿️ ParkPulse Limassol",
        "subtitle": "1-Click Instant Spot Release",
        "tab1": "🗺️ Live Parking Map",
        "tab2": "🚀 Release Now",
        "map_title": "Live Limassol Map",
        "map_desc": "View active spots and navigate instantly with Google Maps:",
        "nav_btn": "🧭 GPS Navigation (Google Maps)",
        "claim_btn": "🚗 Claimed! (Remove)",
        "success_claim": "Thanks! Spot removed from map.",
        "no_spots": "No active spots on the map right now.",
        "form_title": "🚀 Instant Spot Release",
        "form_desc": "Select your street zone and hit release to notify nearby drivers instantly:",
        "spot_label": "Select Area / Street in Limassol:",
        "publish_btn": "✅ RELEASE SPOT NOW",
        "success_publish": "Your spot has been successfully published live on the map!"
    },
    "Русский": {
        "title": "🅿️ ParkPulse Лимассол",
        "subtitle": "Быстрое освобождение места",
        "tab1": "🗺️ Живая карта",
        "tab2": "🚀 Освободить",
        "map_title": "Живая карта Лимассола",
        "map_desc": "Смотрите места и открывайте навигацию Google Maps:",
        "nav_btn": "🧭 GPS Навигация (Google Maps)",
        "claim_btn": "🚗 Занял! (Удалить)",
        "success_claim": "Спасибо! Место удалено с карты.",
        "no_spots": "Нет активных мест на карте.",
        "form_title": "🚀 Мгновенная публикация местоположения",
        "form_desc": "Выберите зону и нажмите кнопку для мгновенного оповещения водителей:",
        "spot_label": "Выберите улицу / зону в Лимассоле:",
        "publish_btn": "✅ ОСВОБОДИТЬ МЕСТО СЕЙЧАС",
        "success_publish": "Ваше место успешно опубликовано на карте!"
    },
    "עברית": {
        "title": "🅿️ ParkPulse לימסול",
        "subtitle": "שחרור חניה מהיר בקליק אחד",
        "tab1": "🗺️ מפת חניה חיה",
        "tab2": "🚀 שחרר עכשיו",
        "map_title": "מפת לימסול חיה",
        "map_desc": "צפה במקומות פעילים ונווט מיידית עם Google Maps:",
        "nav_btn": "🧭 ניווט GPS (Google Maps)",
        "claim_btn": "🚗 תפסתי! (הסרה)",
        "success_claim": "תודה! המקום הוסר מהמפה.",
        "no_spots": "אין מקומות פעילים במפה כרגע.",
        "form_title": "🚀 שחרור חניה מיידי",
        "form_desc": "בחר את האזור שלך ולחץ שחרור כדי לעדכן מיד את הנהגים הסמוכים:",
        "spot_label": "בחר אזור / רחוב בלימסול:",
        "publish_btn": "✅ שחרר חניה עכשיו",
        "success_publish": "המקום שלך פורסם בהצלחה למפה החיה!"
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

# --- EXACT LIMASSOL PARKING HUBS & COORDINATES ---
limassol_parking_spots = {
    "📍 Οδός Ανεξαρτησίας (Κέντρο Εμπορικό)": {"lat": 34.70654, "lon": 33.04351},
    "📍 Οδός Αγίου Ανδρέου (Ιστορικό Κέντρο)": {"lat": 34.70425, "lon": 33.04612},
    "📍 Περιοχή Μώλος / Αποβάθρα": {"lat": 34.70212, "lon": 33.05124},
    "📍 Οδός Σαριπόλου (Bar Street)": {"lat": 34.70801, "lon": 33.04302},
    "📍 Πλατεία Ηρώων (ΕΠΑΛ)": {"lat": 34.70953, "lon": 33.04501},
    "📍 ΕΝΑΕΡΙΟΣ (Παραλιακή Λεωφόρος)": {"lat": 34.69852, "lon": 33.06203},
    "📍 Μαρίνα Λεμεσού (Είσοδος)": {"lat": 34.67051, "lon": 33.04012}
}

# --- INITIALIZE SESSION STATE ---
if "available_spots" not in st.session_state:
    st.session_state.available_spots = [
        {
            "Title": "📍 Οδός Ανεξαρτησίας (Κέντρο Εμπορικό)",
            "lat": 34.70654,
            "lon": 33.04351
        },
        {
            "Title": "📍 Περιοχή Μώλος / Αποβάθρα",
            "lat": 34.70212,
            "lon": 33.05124
        }
    ]

# --- TABS ---
tab1, tab2 = st.tabs([t['tab1'], t['tab2']])

with tab1:
    st.markdown(f"#### {t['map_title']}")
    st.write(t['map_desc'])

    limassol_map = folium.Map(location=[34.7063, 33.0461], zoom_start=15, tiles="CartoDB dark_matter")

    for idx, spot in enumerate(st.session_state.available_spots):
        gmaps_url = f"https://www.google.com/maps/search/?api=1&query={spot['lat']},{spot['lon']}"
        
        popup_html = f"""
            <div style="font-family: sans-serif; color: #000; width: 180px;">
                <b>{spot['Title']}</b><br><br>
                <a href="{gmaps_url}" target="_blank" style="background: #059669; color: white; padding: 5px 10px; text-decoration: none; border-radius: 4px; display: inline-block; font-size: 11px; font-weight: bold;">🧭 Google Maps GPS</a>
            </div>
        """
        folium.Marker(
            location=[spot['lat'], spot['lon']],
            popup=folium.Popup(popup_html, max_width=220),
            tooltip=spot['Title'],
            icon=folium.Icon(color="green", icon="parking", prefix="fa")
        ).add_to(limassol_map)

    st_folium(limassol_map, width=700, height=400, key="view_map")

    st.markdown("---")
    st.markdown(f"#### {selected_lang == 'Ελληνικά' and 'Διαθέσιμες Θέσεις Αυτή τη Στιγμή' or 'Active Spots'}")

    if st.session_state.available_spots:
        for idx, spot in enumerate(st.session_state.available_spots):
            st.markdown(f"""
                <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(52, 211, 153, 0.25); border-radius: 12px; padding: 0.8rem; margin-bottom: 0.6rem;">
                    <b style="color: #34d399; font-size: 0.95rem;">{spot['Title']}</b>
                </div>
            """, unsafe_allow_html=True)
            
            gmaps_link = f"https://www.google.com/maps/search/?api=1&query={spot['lat']},{spot['lon']}"
            st.markdown(f'<a href="{gmaps_link}" target="_blank"><button style="background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%); color: white; border: none; border-radius: 10px; font-weight: 700; padding: 0.4rem 1rem; width: 100%; text-align: center; margin-bottom: 0.4rem; cursor: pointer; text-decoration: none; display: block;">{t["nav_btn"]}</button></a>', unsafe_allow_html=True)

            if st.button(t['claim_btn'], key=f"claim_{idx}"):
                st.session_state.available_spots.pop(idx)
                st.success(t['success_claim'])
                st.rerun()
    else:
        st.info(t['no_spots'])

with tab2:
    st.markdown(f"#### {t['form_title']}")
    st.write(t['form_desc'])

    with st.form("instant_release_form", border=False):
        selected_spot = st.selectbox(t['spot_label'], list(limassol_parking_spots.keys()))
        
        submit_btn = st.form_submit_button(t['publish_btn'])
        
        if submit_btn:
            coords = limassol_parking_spots[selected_spot]
            
            # Insert spot instantly at the top of the live list
            st.session_state.available_spots.insert(0, {
                "Title": selected_spot,
                "lat": coords["lat"],
                "lon": coords["lon"]
            })
            st.success(t['success_publish'])
            st.rerun()
