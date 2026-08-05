import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ParkPulse Limassol // Precision Pin Drop",
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
        "subtitle": "Ακριβής Πινέζα με Κλικ στον Χάρτη",
        "tab1": "🗺️ Live Χάρτης Θέσεων",
        "tab2": "🚀 Καρφώστε Θέση στον Χάρτη",
        "map_title": "Ζωντανός Χάρτης Θέσεων Λεμεσού",
        "map_desc": "Δείτε τις ενεργές θέσεις και πλοηγηθείτε με Google Maps:",
        "nav_btn": "🧭 GPS Navigation (Google Maps)",
        "claim_btn": "🚗 Την πήρα! (Κατάργηση)",
        "success_claim": "Ευχαριστούμε! Η θέση αφαιρέθηκε.",
        "no_spots": "Δεν υπάρχουν ενεργές θέσεις αυτή τη στιγμή.",
        "form_title": "🚀 Επιλογή Ακριβούς Σημείου Parking",
        "form_desc": "Κάντε ζουμ και κλικ ακριβώς επάνω στο σημείο/parking που αφήνετε:",
        "publish_btn": "✅ ΔΗΜΟΣΙΕΥΣΗ ΠΙΝΕΖΑΣ ΣΤΟ ΣΗΜΕΙΟ",
        "success_publish": "Η ακριβής θέση μόλις δημοσιεύτηκε στον χάρτη!",
        "select_warn": "Παρακαλώ κάντε πρώτα κλικ επάνω στον χάρτη για να επιλέξετε σημείο."
    },
    "English": {
        "title": "🅿️ ParkPulse Limassol",
        "subtitle": "Precision Map Pin Drop",
        "tab1": "🗺️ Live Parking Map",
        "tab2": "🚀 Pin Spot on Map",
        "map_title": "Live Limassol Parking Map",
        "map_desc": "View active spots and navigate with Google Maps:",
        "nav_btn": "🧭 GPS Navigation (Google Maps)",
        "claim_btn": "🚗 Claimed! (Remove)",
        "success_claim": "Thanks! Spot removed.",
        "no_spots": "No active spots right now.",
        "form_title": "🚀 Pick Exact Parking Spot",
        "form_desc": "Zoom in and click directly on the exact spot or parking lot where you are leaving:",
        "publish_btn": "✅ PUBLISH PIN AT THIS LOCATION",
        "success_publish": "Your exact spot has been published live on the map!",
        "select_warn": "Please click on the map first to select your location."
    },
    "Русский": {
        "title": "🅿️ ParkPulse Лимассол",
        "subtitle": "Точная метка на карте",
        "tab1": "🗺️ Живая карта",
        "tab2": "🚀 Отметить на карте",
        "map_title": "Живая карта Лимассола",
        "map_desc": "Смотрите активные места и открывайте Google Maps:",
        "nav_btn": "🧭 GPS Навигация (Google Maps)",
        "claim_btn": "🚗 Занял! (Удалить)",
        "success_claim": "Спасибо! Место удалено.",
        "no_spots": "Нет активных мест.",
        "form_title": "🚀 Выбор точного места парковки",
        "form_desc": "Приблизьте карту и кликните прямо на то место, откуда вы уезжаете:",
        "publish_btn": "✅ ОПУБЛИКОВАТЬ МЕТКУ НА КАРТЕ",
        "success_publish": "Ваше место успешно опубликовано на карте!",
        "select_warn": "Пожалуйста, сначала кликните по карте."
    },
    "עברית": {
        "title": "🅿️ ParkPulse לימסול",
        "subtitle": "סיכה מדויקת במפה",
        "tab1": "🗺️ מפת חניה חיה",
        "tab2": "🚀 סמן חניה במפה",
        "map_title": "מפת חניה חיה בלימסול",
        "map_desc": "צפה במקומות פעילים ונווט באמצעות Google Maps:",
        "nav_btn": "🧭 ניווט GPS (Google Maps)",
        "claim_btn": "🚗 תפסתי! (הסרה)",
        "success_claim": "תודה! המקום הוסר.",
        "no_spots": "אין מקומות פעילים כרגע.",
        "form_title": "🚀 בחר את מיקום החניה המדויק",
        "form_desc": "התקרב ולחץ ישירות על המקום או החניון שבו אתה יוצא:",
        "publish_btn": "✅ פרסם סיכה במיקום זה",
        "success_publish": "המקום שלך פורסם בהצלחה למפה!",
        "select_warn": "אנא לחץ תחילה על המפה כדי לבחור מיקום."
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
            "Title": "📍 Κέντρο Λεμεσού (Ανεξαρτησίας)",
            "lat": 34.70654,
            "lon": 33.04351
        },
        {
            "Title": "📍 Παραλιακός Μώλος",
            "lat": 34.70212,
            "lon": 33.05124
        }
    ]

if "picker_lat" not in st.session_state:
    st.session_state.picker_lat = None
if "picker_lon" not in st.session_state:
    st.session_state.picker_lon = None

# --- TABS ---
tab1, tab2 = st.tabs([t['tab1'], t['tab2']])

with tab1:
    st.markdown(f"#### {t['map_title']}")
    st.write(t['map_desc'])

    # View map for active spots
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

    # Interactive picker map to drop a pin at the exact spot
    picker_map = folium.Map(location=[34.7063, 33.0461], zoom_start=15, tiles="CartoDB dark_matter")

    if st.session_state.picker_lat and st.session_state.picker_lon:
        folium.Marker(
            location=[st.session_state.picker_lat, st.session_state.picker_lon],
            icon=folium.Icon(color="red", icon="map-marker", prefix="fa"),
            tooltip="Επιλεγμένο Spot"
        ).add_to(picker_map)

    map_data = st_folium(picker_map, width=700, height=400, key="picker_map")

    if map_data and map_data.get("last_clicked"):
        st.session_state.picker_lat = map_data["last_clicked"]["lat"]
        st.session_state.picker_lon = map_data["last_clicked"]["lng"]

    if st.session_state.picker_lat:
        st.info(f"📍 Επιλεγμένες συντεταγμένες spot: {st.session_state.picker_lat:.5f}, {st.session_state.picker_lon:.5f}")

    if st.button(t['publish_btn'], key="publish_exact_pin"):
        if st.session_state.picker_lat and st.session_state.picker_lon:
            st.session_state.available_spots.insert(0, {
                "Title": f"📍 Spot Ακριβείας ({st.session_state.picker_lat:.4f}, {st.session_state.picker_lon:.4f})",
                "lat": st.session_state.picker_lat,
                "lon": st.session_state.picker_lon
            })
            st.session_state.picker_lat = None
            st.session_state.picker_lon = None
            st.success(t['success_publish'])
            st.rerun()
        else:
            st.warning(t['select_warn'])
