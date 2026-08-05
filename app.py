import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ParkPulse Limassol // Real GPS Parking",
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
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    }
    .hero-title {
        font-size: 1.6rem;
        font-weight: 900;
        color: #ffffff;
        margin: 0;
    }
    .hero-subtitle {
        font-size: 0.75rem;
        color: #34d399;
        margin-top: 5px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
    }
    .legal-notice {
        background: rgba(30, 41, 59, 0.8);
        border-left: 4px solid #34d399;
        padding: 0.8rem;
        border-radius: 8px;
        font-size: 0.75rem;
        color: #94a3b8;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background: linear-gradient(90deg, #059669 0%, #34d399 100%);
        color: white;
        border: none;
        border-radius: 14px;
        font-weight: 700;
        padding: 0.75rem 1rem;
        width: 100%;
        box-shadow: 0 4px 12px rgba(52, 211, 153, 0.25);
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
        "subtitle": "Αυτόματο GPS & Live Κοινοτικό Parking",
        "legal": "<b>Νομική Σημείωση & GDPR:</b> Η εφαρμογή καταγράφει συντεταγμένες GPS κινητού αποκλειστικά κατόπιν συναίνεσης του χρήστη για τη στιγμή της απελευθέρωσης της θέσης. Μηδενική αποθήκευση προσωπικών δεδομένων.",
        "tab1": "🗺️ Live Χάρτης & GPS",
        "tab2": "📢 Αυτόματη Καταχώρηση (GPS)",
        "tab3": "⚖️ Όροι & GDPR",
        "map_title": "Ζωντανός Χάρτης Θέσεων GPS",
        "map_desc": "Πατήστε στις πινέζες για άμεση πλοήγηση βήμα-βήμα (Google Maps):",
        "list_title": "Ενεργές Θέσεις Οδηγών",
        "leave_time": "Αναχώρηση:",
        "driver": "Οδηγός:",
        "nav_btn": "🧭 GPS Navigation (Google Maps)",
        "claim_btn": "🚗 Την πήρα! (Αφαίρεση)",
        "success_claim": "Ευχαριστούμε! Η θέση απελευθερώθηκε.",
        "no_spots": "Δεν υπάρχουν ενεργές θέσεις στον χάρτη αυτή τη στιγμή.",
        "form_title": "Αυτόματη Απελευθέρωση Θέσης μέσω GPS",
        "form_desc": "Πατήστε παρακάτω για να εντοπίσει το κινητό σας την ακριβή σας τοποθεσία στον δρόμο:",
        "get_gps_btn": "📍 Εντοπισμός Τρέχουσας Θέσης GPS",
        "time_label": "Πότε φεύγετε?",
        "name_label": "Όνομα / Ψευδώνυμο:",
        "name_placeholder": "π.χ. Ανδρέας",
        "details_label": "Σημείο Αναφοράς / Λεπτομέρειες:",
        "details_placeholder": "π.χ. Δίπλα σε καφέ / φαρμακείο",
        "publish_btn": "🚀 Δημοσίευση Θέσης με GPS",
        "success_publish": "Η θέση σας προστέθηκε με απόλυτη ακρίβεια GPS!",
        "gps_warning": "Παρακαλώ πατήστε πρώτα το κουμπί εντοπισμού GPS ώστε να καταγραφεί η θέση σας.",
        "terms_title": "Όροι Χρήσης & GDPR",
        "terms_text": "1. <b>Σκοπός:</b> Αυτόματη κοινοτική κοινοποίηση θέσεων στάθμευσης.<br>2. <b>GPS:</b> Οι συντεταγμένες αντλούνται αποκλειστικά από τη συσκευή σας την ώρα της δημοσίευσης.<br>3. <b>GDPR:</b> Πλήρης προστασία, καμία μόνιμη αποθήκευση στοιχείων."
    },
    "English": {
        "title": "🅿️ ParkPulse Limassol",
        "subtitle": "Auto-GPS & Live Community Parking",
        "legal": "<b>Legal Notice & GDPR:</b> The app tracks mobile GPS coordinates strictly upon user consent at the moment of spot release. Fully GDPR compliant.",
        "tab1": "🗺️ Live Map & GPS",
        "tab2": "📢 Auto Publish (GPS)",
        "tab3": "⚖️ Terms & GDPR",
        "map_title": "Live GPS Parking Map",
        "map_desc": "Click pins for step-by-step Google Maps GPS navigation:",
        "list_title": "Active Driver Spots",
        "leave_time": "Leaving:",
        "driver": "Driver:",
        "nav_btn": "🧭 GPS Navigation (Google Maps)",
        "claim_btn": "🚗 Claimed! (Remove)",
        "success_claim": "Thanks! Spot cleared.",
        "no_spots": "No active spots on the map right now.",
        "form_title": "Auto-Release Spot via GPS",
        "form_desc": "Click below to let your phone detect your exact street location:",
        "get_gps_btn": "📍 Detect Current GPS Location",
        "time_label": "Leaving in:",
        "name_label": "Name / Nickname:",
        "name_placeholder": "e.g., Andrew",
        "details_label": "Landmark / Details:",
        "details_placeholder": "e.g., Next to a coffee shop",
        "publish_btn": "🚀 Publish Spot with GPS",
        "success_publish": "Spot successfully published with exact GPS accuracy!",
        "gps_warning": "Please click the GPS detection button first to capture your coordinates.",
        "terms_title": "Terms of Use & GDPR",
        "terms_text": "1. <b>Purpose:</b> Automated community parking helper.<br>2. <b>GPS:</b> Coordinates are fetched solely from your device upon publishing.<br>3. <b>GDPR:</b> Minimal data policy, fully purged."
    },
    "Русский": {
        "title": "🅿️ ParkPulse Лимассол",
        "subtitle": "Авто GPS и живая парковка",
        "legal": "<b>Правовое уведомление и GDPR:</b> Отслеживание координат GPS строго по согласию пользователя. Соответствует GDPR.",
        "tab1": "🗺️ Живая карта и GPS",
        "tab2": "📢 Авто публикация (GPS)",
        "tab3": "⚖️ Условия и GDPR",
        "map_title": "Карта парковки по GPS",
        "map_desc": "Нажмите на пины для навигации Google Maps:",
        "list_title": "Активные места водителей",
        "leave_time": "Уезжает:",
        "driver": "Водитель:",
        "nav_btn": "🧭 GPS Навигация (Google Maps)",
        "claim_btn": "🚗 Занял! (Удалить)",
        "success_claim": "Спасибо! Место освобождено.",
        "no_spots": "Нет активных мест.",
        "form_title": "Освобождение места через GPS",
        "form_desc": "Нажмите кнопку ниже для определения ваших координат:",
        "get_gps_btn": "📍 Определить текущие координаты GPS",
        "time_label": "Время ухода:",
        "name_label": "Имя:",
        "name_placeholder": "например, Алексей",
        "details_label": "Ориентир / Детали:",
        "details_placeholder": "например, возле кафе",
        "publish_btn": "🚀 Опубликовать по GPS",
        "success_publish": "Место успешно опубликовано с точным GPS!",
        "gps_warning": "Пожалуйста, сначала нажмите кнопку определения GPS.",
        "terms_title": "Условия и GDPR",
        "terms_text": "1. <b>Цель:</b> Автоматический обмен местами.<br>2. <b>GPS:</b> Координаты берутся с вашего устройства.<br>3. <b>GDPR:</b> Минимальный сбор данных."
    },
    "עברית": {
        "title": "🅿️ ParkPulse לימסול",
        "subtitle": "GPS אוטומטי וחניה חיה",
        "legal": "<b>הודעה משפטית ו-GDPR:</b> מעקב אחר קואורדינטות GPS בהסכמת המשתמש בלבד בעת שחרור החניה. תואם GDPR.",
        "tab1": "🗺️ מפה חיה ו-GPS",
        "tab2": "📢 פרסום אוטומטי (GPS)",
        "tab3": "⚖️ תנאים ו-GDPR",
        "map_title": "מפת חניה חיפאית לפי GPS",
        "map_desc": "לחץ על הסיכות לניווט GPS מדויק ב-Google Maps:",
        "list_title": "מקומות נהגים פעילים",
        "leave_time": "פינוי:",
        "driver": "נהג:",
        "nav_btn": "🧭 ניווט GPS (Google Maps)",
        "claim_btn": "🚗 תפסתי! (הסרה)",
        "success_claim": "תודה! המקום פונה.",
        "no_spots": "אין מקומות פעילים כרגע.",
        "form_title": "שחרור חניה אוטומטי באמצעות GPS",
        "form_desc": "לחץ למטה כדי שהטלפון יזהה את מיקומך המדויק ברחוב:",
        "get_gps_btn": "📍 איתור מיקום GPS נוכחי",
        "time_label": "מתי יוצא?",
        "name_label": "שם:",
        "name_placeholder": "לדוגמה, דוד",
        "details_label": "נקודת ציון / פרטים:",
        "details_placeholder": "לדוגמה, ליד בית הקפה",
        "publish_btn": "🚀 פרסם מקום עם GPS",
        "success_publish": "המקום פורסם בהצלחה עם דיוק GPS מלא!",
        "gps_warning": "אנא לחץ תחילה על כפתור איתור ה-GPS כדי לקלוט את הקואורדינטות שלך.",
        "terms_title": "תנאי שימוש ופרטיות (GDPR)",
        "terms_text": "1. <b>מטרה:</b> עזרה קהילתית אוטומטית לחניה.<br>2. <b>GPS:</b> הקואורדינטות נשלפות מהמכשיר שלך בעת הפרסום.<br>3. <b>GDPR:</b> שמירה מינימלית ומחיקה אוטומטית."
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

# --- LEGAL DISCLAIMER BANNER ---
st.markdown(f"""
    <div class="legal-notice">
        {t['legal']}
    </div>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if "available_spots" not in st.session_state:
    st.session_state.available_spots = [
        {
            "Title": "Οδός Ανεξαρτησίας",
            "Time": "Σε 5 λεπτά",
            "Driver": "Μάριος",
            "Details": "Έξω από κεντρικό κατάστημα",
            "lat": 34.70654,
            "lon": 33.04351
        },
        {
            "Title": "Περιοχή Μώλος",
            "Time": "Άμεσα / Τώρα",
            "Driver": "Έλενα",
            "Details": "Δίπλα στο πάρκο",
            "lat": 34.70212,
            "lon": 33.05124
        }
    ]

time_options = ["Άμεσα / Τώρα", "Σε 2 λεπτά", "Σε 5 λεπτά", "Σε 10 λεπτά"]

# --- TABS ---
tab1, tab2, tab3 = st.tabs([t['tab1'], t['tab2'], t['tab3']])

with tab1:
    st.markdown(f"#### {t['map_title']}")
    st.write(t['map_desc'])

    # Create Folium Map centered in Limassol
    limassol_map = folium.Map(location=[34.7063, 33.0461], zoom_start=15, tiles="CartoDB dark_matter")

    # Add dynamic markers
    for idx, spot in enumerate(st.session_state.available_spots):
        gmaps_url = f"https://www.google.com/maps/search/?api=1&query={spot['lat']},{spot['lon']}"
        
        popup_html = f"""
            <div style="font-family: sans-serif; color: #000; width: 220px;">
                <b>📍 {spot['Title']}</b><br>
                <b>⏰ {spot['Time']}</b><br>
                <small>{spot['Details']}</small><br>
                <b>👤 {spot['Driver']}</b><br><br>
                <a href="{gmaps_url}" target="_blank" style="background: #059669; color: white; padding: 5px 10px; text-decoration: none; border-radius: 4px; display: inline-block; font-size: 11px; font-weight: bold;">🧭 Google Maps GPS</a>
            </div>
        """
        folium.Marker(
            location=[spot['lat'], spot['lon']],
            popup=folium.Popup(popup_html, max_width=260),
            tooltip=f"{spot['Title']} ({spot['Time']})",
            icon=folium.Icon(color="green", icon="parking", prefix="fa")
        ).add_to(limassol_map)

    # Render interactive map
    st_folium(limassol_map, width=700, height=420)

    st.markdown("---")
    st.markdown(f"#### {t['list_title']}")

    if st.session_state.available_spots:
        for idx, spot in enumerate(st.session_state.available_spots):
            st.markdown(f"""
                <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(52, 211, 153, 0.25); border-radius: 14px; padding: 1rem; margin-bottom: 0.8rem;">
                    <b>📍 {spot['Title']}</b><br>
                    <span style="color: #34d399; font-weight: bold;">⏰ {t['leave_time']} {spot['Time']}</span><br>
                    <span style="color: #cbd5e1; font-size: 0.85rem;">📝 {spot['Details']}</span><br>
                    <div style="margin-top: 6px; font-size: 0.75rem; color: #94a3b8;">👤 {t['driver']} {spot['Driver']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            gmaps_link = f"https://www.google.com/maps/search/?api=1&query={spot['lat']},{spot['lon']}"
            st.markdown(f'<a href="{gmaps_link}" target="_blank"><button style="background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%); color: white; border: none; border-radius: 12px; font-weight: 700; padding: 0.5rem 1rem; width: 100%; text-align: center; margin-bottom: 0.5rem; cursor: pointer; text-decoration: none; display: block;">{t["nav_btn"]}</button></a>', unsafe_allow_html=True)

            if st.button(t['claim_btn'], key=f"claim_{idx}"):
                st.session_state.available_spots.pop(idx)
                st.success(t['success_claim'])
                st.rerun()
    else:
        st.info(t['no_spots'])

with tab2:
    st.markdown(f"#### {t['form_title']}")
    st.write(t['form_desc'])

    # Get live GPS location from user's device browser
    loc = streamlit_geolocation()

    with st.form("parking_form", border=False):
        time_leaving = st.selectbox(t['time_label'], time_options)
        driver_name = st.text_input(t['name_label'], placeholder=t['name_placeholder'])
        extra_details = st.text_input(t['details_label'], placeholder=t['details_placeholder'])
        
        submit_spot = st.form_submit_button(t['publish_btn'])
        
        if submit_spot:
            if loc and loc.get("latitude") and loc.get("longitude"):
                user_lat = loc["latitude"]
                user_lon = loc["longitude"]
                
                st.session_state.available_spots.insert(0, {
                    "Title": f"Σημείο GPS ({user_lat:.4f}, {user_lon:.4f})",
                    "Time": time_leaving,
                    "Driver": driver_name.strip() if driver_name.strip() else "Ανώνυμος Οδηγός",
                    "Details": extra_details.strip() if extra_details.strip() else "Χωρίς επιπλέον περιγραφή",
                    "lat": user_lat,
                    "lon": user_lon
                })
                st.success(t['success_publish'])
                st.rerun()
            else:
                st.warning(t['gps_warning'])

with tab3:
    st.markdown(f"#### {t['terms_title']}")
    st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.5); padding: 1.2rem; border-radius: 14px; line-height: 1.6; font-size: 0.9rem;">
            {t['terms_text']}
        </div>
    """, unsafe_allow_html=True)
