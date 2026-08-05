import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ParkPulse Limassol // Auto GPS",
    page_icon="🅿️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- MODERN DESIGN ---
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
        "subtitle": "Αυτόματος Εντοπισμός GPS",
        "tab1": "🗺️ Live Χάρτης Θέσεων",
        "tab2": "🚀 Αυτόματη Απελευθέρωση (GPS)",
        "map_title": "Ζωντανός Χάρτης Λεμεσού",
        "map_desc": "Δείτε τις διαθέσιμες θέσεις και πλοηγηθείτε με 1 κλικ (Google Maps):",
        "nav_btn": "🧭 GPS Navigation (Google Maps)",
        "claim_btn": "🚗 Την πήρα! (Κατάργηση)",
        "success_claim": "Ευχαριστούμε! Η θέση αφαιρέθηκε.",
        "no_spots": "Δεν υπάρχουν διαθέσιμες θέσεις στον χάρτη αυτή τη στιγμή.",
        "form_title": "🚀 Αυτόματος Εντοπισμός Θέσης",
        "form_desc": "Πατήστε το κουμπί παρακάτω για να διαβάσει το κινητό σας το GPS σας και να το δημοσιεύσει αυτόματα:",
        "success_publish": "Η θέση σας μόλις προστέθηκε αυτόματα στον χάρτη!"
    },
    "English": {
        "title": "🅿️ ParkPulse Limassol",
        "subtitle": "Auto GPS Tracking",
        "tab1": "🗺️ Live Parking Map",
        "tab2": "🚀 Auto Release (GPS)",
        "map_title": "Live Limassol Map",
        "map_desc": "View active spots and navigate instantly with Google Maps:",
        "nav_btn": "🧭 GPS Navigation (Google Maps)",
        "claim_btn": "🚗 Claimed! (Remove)",
        "success_claim": "Thanks! Spot removed.",
        "no_spots": "No active spots on the map right now.",
        "form_title": "🚀 Automatic Spot Detection",
        "form_desc": "Click the button below to let your phone read your GPS and publish it automatically:",
        "success_publish": "Your spot has been automatically published to the map!"
    },
    "Русский": {
        "title": "🅿️ ParkPulse Лимассол",
        "subtitle": "Автоматический GPS",
        "tab1": "🗺️ Живая карта",
        "tab2": "🚀 Авто публикация (GPS)",
        "map_title": "Живая карта Лимассола",
        "map_desc": "Смотрите места и открывайте навигацию Google Maps:",
        "nav_btn": "🧭 GPS Навигация (Google Maps)",
        "claim_btn": "🚗 Занял! (Удалить)",
        "success_claim": "Спасибо! Место удалено.",
        "no_spots": "Нет активных мест.",
        "form_title": "🚀 Автоматическое определение места",
        "form_desc": "Нажмите кнопку ниже, чтобы телефон определил ваш GPS:",
        "success_publish": "Ваше место успешно добавлено на карту!"
    },
    "עברית": {
        "title": "🅿️ ParkPulse לימסול",
        "subtitle": "איתור GPS אוטומטי",
        "tab1": "🗺️ מפת חניה חיה",
        "tab2": "🚀 שחרור אוטומטי (GPS)",
        "map_title": "מפת לימסול חיה",
        "map_desc": "צפה במקומות פעילים ונווט מיידית עם Google Maps:",
        "nav_btn": "🧭 ניווט GPS (Google Maps)",
        "claim_btn": "🚗 תפסתי! (הסרה)",
        "success_claim": "תודה! המקום הוסר.",
        "no_spots": "אין מקומות פעילים במפה כרגע.",
        "form_title": "🚀 זיהוי מיקום אוטומטי",
        "form_desc": "לחץ על הכפתור למטה כדי שהטלפון יזהה את ה-GPS שלך ויפרסם אותו אוטומטית:",
        "success_publish": "המקום שלך נוסף אוטומטית למפה!"
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
if "available_spots" not in st.session_state:
    st.session_state.available_spots = [
        {
            "Title": "📍 Οδός Ανεξαρτησίας (Κέντρο)",
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
    if st.session_state.available_spots:
        for idx, spot in enumerate(st.session_state.available_spots):
            gmaps_link = f"https://www.google.com/maps/search/?api=1&query={spot['lat']},{spot['lon']}"
            st.markdown(f"""
                <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(52, 211, 153, 0.25); border-radius: 12px; padding: 0.8rem; margin-bottom: 0.6rem;">
                    <b style="color: #34d399; font-size: 0.95rem;">{spot['Title']}</b>
                </div>
            """, unsafe_allow_html=True)
            
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

    # HTML5 Geolocation Widget via Streamlit Components
    geolocation_html = """
    <div style="text-align: center; padding: 20px;">
        <button onclick="getLocation()" style="background: linear-gradient(90deg, #059669 0%, #34d399 100%); color: white; border: none; border-radius: 14px; font-weight: 800; padding: 15px 25px; font-size: 1.1rem; cursor: pointer; box-shadow: 0 4px 15px rgba(52, 211, 153, 0.3); width: 100%;">
            📍 ΕΝΤΟΠΙΣΜΟΣ GPS & ΑΠΕΛΕΥΘΕΡΩΣΗ ΤΩΡΑ
        </button>
        <p id="status" style="color: #94a3b8; margin-top: 15px; font-size: 0.85rem;"></p>
    </div>

    <script>
    function getLocation() {
        const status = document.getElementById("status");
        if (!navigator.geolocation) {
            status.innerHTML = "❌ Ο browser σας δεν υποστηρίζει GPS.";
        } else {
            status.innerHTML = "⏳ Εντοπισμός ακριβούς τοποθεσίας...";
            navigator.geolocation.getCurrentPosition(success, error, {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            });
        }
    }

    function success(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        document.getElementById("status").innerHTML = "✅ Επιτυχής εντοπισμός! Συγχρονισμός...";
        
        // Send coordinates back to Streamlit via URL parameters reload or custom mechanism
        const url = new URL(window.parent.location.href);
        url.searchParams.set('lat', latitude);
        url.searchParams.set('lon', longitude);
        window.parent.location.href = url.href;
    }

    function error() {
        document.getElementById("status").innerHTML = "❌ Αποτυχία πρόσβασης στο GPS. Παρακαλώ επιτρέψτε την τοποθεσία.";
    }
    </script>
    """
    
    # Render the native JS GPS button
    components.html(geolocation_html, height=140)

    # Check if parameters were passed back from the JavaScript GPS trigger
    query_params = st.query_params
    if "lat" in query_params and "lon" in query_params:
        try:
            lat_val = float(query_params["lat"])
            lon_val = float(query_params["lon"])
            
            # Add spot automatically to session state
            new_spot_title = f"📍 Αυτόματο GPS ({lat_val:.4f}, {lon_val:.4f})"
            
            # Check if this exact spot wasn't just added
            if not any(s['lat'] == lat_val and s['lon'] == lon_val for s in st.session_state.available_spots):
                st.session_state.available_spots.insert(0, {
                    "Title": new_spot_title,
                    "lat": lat_val,
                    "lon": lon_val
                })
                st.success(t['success_publish'])
                # Clear query params to prevent re-adding on refresh
                st.query_params.clear()
                st.rerun()
        except ValueError:
            pass
