import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ParkPulse Limassol // Smart Street Parking",
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
        "subtitle": "Ζωντανός Χάρτης & Πλοήγηση Parking",
        "legal": "<b>Νομική Σημείωση & GDPR:</b> Η εφαρμογή λειτουργεί αποκλειστικά ως ενημερωτικός πίνακας κοινότητας. Η χρήση γίνεται με δική σας ευθύνη. Δεν αποθηκεύονται ευαίσθητα προσωπικά δεδομένα ή αριθμοί πινακίδων, σε πλήρη συμμόρφωση με τον Κανονισμό GDPR.",
        "tab1": "🗺️ Live Χάρτης & Οδηγίες",
        "tab2": "📢 Ελευθερώνω Θέση",
        "tab3": "⚖️ Όροι & GDPR",
        "map_title": "Διαδραστικός Χάρτης & GPS Navigation",
        "map_desc": "Επιλέξτε θέση και ανοίξτε αυτόματα τις οδηγίες οδήγησης (Google Maps):",
        "list_title": "Ενεργές Θέσεις σε Λίστα",
        "leave_time": "Αναχώρηση:",
        "driver": "Οδηγός:",
        "nav_btn": "🧭 Οδηγίες Πλοήγησης (Google Maps)",
        "claim_btn": "🚗 Την πήρα! (Αφαίρεση)",
        "success_claim": "Ευχαριστούμε! Η θέση ενημερώθηκε.",
        "no_spots": "Δεν υπάρχουν διαθέσιμες θέσεις στον χάρτη αυτή τη στιγμή.",
        "form_title": "Ελευθερώνεις θέση στο δρόμο?",
        "form_desc": "Καταχώρησε σημείο για να εμφανιστεί αυτόματα στον χάρτη.",
        "zone_label": "Επιλογή Περιοχής / Σημείου:",
        "time_label": "Πότε φεύγεις?",
        "name_label": "Ψευδώνυμο / Όνομα (Προαιρετικό):",
        "name_placeholder": "π.χ. Ανδρέας",
        "details_label": "Ακριβής Τοποθεσία / Οδός:",
        "details_placeholder": "π.χ. Αγίου Ανδρέου 42",
        "publish_btn": "🚀 Προσθήκη στον Χάρτη",
        "success_publish": "Η θέση προστέθηκε επιτυχώς!",
        "terms_title": "Όροι Χρήσης & Πολιτική Απορρήτου (GDPR)",
        "terms_text": "1. <b>Σκοπός:</b> Το ParkPulse Limassol είναι εργαλείο αλληλοβοήθειας πολιτών.<br>2. <b>Αποποίηση Ευθύνης:</b> Η διαθεσιμότητα των θέσεων δεν είναι εγγυημένη. Η πλατφόρμα δεν φέρει καμία νομική ευθύνη για τυχόν ζημιές ή διαφωνίες.<br>3. <b>Προστασία Δεδομένων (GDPR):</b> Τα στοιχεία που εισάγονται είναι προαιρετικά και διαγράφονται αυτόματα."
    },
    "English": {
        "title": "🅿️ ParkPulse Limassol",
        "subtitle": "Live Map & Parking Navigation",
        "legal": "<b>Legal Notice & GDPR:</b> This app acts solely as a community bulletin board. Use at your own risk. No sensitive personal data or license plates are stored, in full compliance with GDPR regulations.",
        "tab1": "🗺️ Live Map & Directions",
        "tab2": "📢 Release Spot",
        "tab3": "⚖️ Terms & GDPR",
        "map_title": "Interactive Map & GPS Navigation",
        "map_desc": "Select a spot and instantly launch driving directions (Google Maps):",
        "list_title": "Active Spots List",
        "leave_time": "Leaving:",
        "driver": "Driver:",
        "nav_btn": "🧭 Navigation Directions (Google Maps)",
        "claim_btn": "🚗 Claimed! (Remove)",
        "success_claim": "Thanks! Spot updated.",
        "no_spots": "No active spots on the map right now.",
        "form_title": "Releasing a Street Spot?",
        "form_desc": "Publish a location to instantly update the live map.",
        "zone_label": "Select Area / Hub:",
        "time_label": "Leaving in:",
        "name_label": "Nickname / Name (Optional):",
        "name_placeholder": "e.g., Andrew",
        "details_label": "Exact Location / Street:",
        "details_placeholder": "e.g., Agiou Andreou 42",
        "publish_btn": "🚀 Add to Map",
        "success_publish": "Spot successfully added!",
        "terms_title": "Terms of Use & Privacy Policy (GDPR)",
        "terms_text": "1. <b>Purpose:</b> ParkPulse Limassol is a peer-to-peer community tool.<br>2. <b>Disclaimer:</b> Spot availability is not guaranteed.<br>3. <b>GDPR Compliance:</b> Entered data is minimal, voluntary, and automatically purged."
    },
    "Русский": {
        "title": "🅿️ ParkPulse Лимассол",
        "subtitle": "Живая карта и навигация",
        "legal": "<b>Правовое уведомление и GDPR:</b> Приложение является информационной доской. Личные данные не сохраняются в соответствии с GDPR.",
        "tab1": "🗺️ Карта и маршрут",
        "tab2": "📢 Освободить место",
        "tab3": "⚖️ Условия и GDPR",
        "map_title": "Интерактивная карта и GPS навигация",
        "map_desc": "Выберите место и откройте маршрут (Google Maps):",
        "list_title": "Список активных мест",
        "leave_time": "Уезжает:",
        "driver": "Водитель:",
        "nav_btn": "🧭 Проложить маршрут (Google Maps)",
        "claim_btn": "🚗 Занял! (Удалить)",
        "success_claim": "Спасибо! Место обновлено.",
        "no_spots": "Нет активных мест на карте.",
        "form_title": "Освобождаете парковку?",
        "form_desc": "Добавьте место на живую карту.",
        "zone_label": "Выберите зону:",
        "time_label": "Время ухода:",
        "name_label": "Имя (необязательно):",
        "name_placeholder": "например, Алексей",
        "details_label": "Точный адрес:",
        "details_placeholder": "например, Агиу Андреу 42",
        "publish_btn": "🚀 Добавить на карту",
        "success_publish": "Место успешно добавлено!",
        "terms_title": "Условия использования и GDPR",
        "terms_text": "1. <b>Цель:</b> Инструмент взаимопомощи.<br>2. <b>Отказ от ответственности:</b> Доступность не гарантируется.<br>3. <b>GDPR:</b> Минимальный сбор данных."
    },
    "עברית": {
        "title": "🅿️ ParkPulse לימסול",
        "subtitle": "מפה חיה וניווט חניה",
        "legal": "<b>הודעה משפטית ו-GDPR:</b> אפליקציה זו משמשת כלוח מודעות קהילתי בלבד. אין שמירת נתונים אישיים רגישים בהתאם לתקנות GDPR.",
        "tab1": "🗺️ מפה והוראות הגעה",
        "tab2": "📢 פנוי חניה",
        "tab3": "⚖️ תנאים ו-GDPR",
        "map_title": "מפה אינטראקטיבית וניווט GPS",
        "map_desc": "בחר מקום ופתח מיד הוראות הגעה (Google Maps):",
        "list_title": "רשימת מקומות פעילים",
        "leave_time": "פינוי:",
        "driver": "נהג:",
        "nav_btn": "🧭 הוראות ניווט (Google Maps)",
        "claim_btn": "🚗 תפסתי! (הסרה)",
        "success_claim": "תודה! המקום עודכן.",
        "no_spots": "אין מקומות פעילים במפה כרגע.",
        "form_title": "מפנה חניה ברחוב?",
        "form_desc": "הוסף מיקום כדי לעדכן מיד את המפה החיה.",
        "zone_label": "בחר אזור:",
        "time_label": "מתי יוצא?",
        "name_label": "שם (אופציונלי):",
        "name_placeholder": "לדוגמה, דוד",
        "details_label": "כתובת מדויקת:",
        "details_placeholder": "לדוגמה, אגיו אנדראו 42",
        "publish_btn": "🚀 הוסף למפה",
        "success_publish": "המקום נוסף בהצלחה!",
        "terms_title": "תנאי שימוש ופרטיות (GDPR)",
        "terms_text": "1. <b>מטרה:</b> כלי עזרה הדדית לקהילה.<br>2. <b>כתב ויתור:</b> זמינות החניה אינה מובטחת.<br>3. <b>GDPR:</b> הנתונים מינימליים ונמחקים אוטומטית."
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

# --- INITIALIZE SESSION STATE WITH EXACT COORDINATES IN LIMASSOL ---
if "available_spots" not in st.session_state:
    st.session_state.available_spots = [
        {
            "Street": "Αγίου Ανδρέου (Κέντρο)", 
            "Time": "Σε 2 λεπτά", 
            "Driver": "Μάριος", 
            "Details": "Έξω από το ιστορικό καφέ",
            "lat": 34.7042, 
            "lon": 33.0461
        },
        {
            "Street": "Οδός Ανεξαρτησίας", 
            "Time": "Σε 5 λεπτά", 
            "Driver": "Έλενα", 
            "Details": "Κοντά στη συμβολή με Θ. Δέρβη",
            "lat": 34.7065, 
            "lon": 33.0435
        },
        {
            "Street": "Περιοχή Μώλος", 
            "Time": "Άμεσα / Τώρα", 
            "Driver": "Γιώργος", 
            "Details": "Κοντά στην αποβάθρα / παραλία",
            "lat": 34.7021, 
            "lon": 33.0512
        }
    ]

# Preset coordinates for Limassol zones
zone_coordinates = {
    "Αγίου Ανδρέου (Κέντρο)": {"lat": 34.7042, "lon": 33.0461},
    "Οδός Ανεξαρτησίας": {"lat": 34.7065, "lon": 33.0435},
    "Περιοχή Μώλος / Μαρίνα": {"lat": 34.7021, "lon": 33.0512},
    "Οδός Σαριπόλου": {"lat": 34.7080, "lon": 33.0430},
    "ΕΠΑΛ / Πλατεία Ηρώων": {"lat": 34.7095, "lon": 33.0450},
    "ΕΝΑΕΡΙΟΣ / Παραλιακή": {"lat": 34.6985, "lon": 33.0620},
    "Άγιος Αθανάσιος (Εμπορικό)": {"lat": 34.7190, "lon": 33.0580}
}

limassol_zones = list(zone_coordinates.keys())
time_options = ["Άμεσα / Τώρα", "Σε 2 λεπτά", "Σε 5 λεπτά", "Σε 10 λεπτά"]

# --- TABS ---
tab1, tab2, tab3 = st.tabs([t['tab1'], t['tab2'], t['tab3']])

with tab1:
    st.markdown(f"#### {t['map_title']}")
    st.write(t['map_desc'])

    # Create Folium Map centered in Limassol
    limassol_map = folium.Map(location=[34.7063, 33.0461], zoom_start=14, tiles="CartoDB dark_matter")

    # Add markers for each active parking spot
    for idx, spot in enumerate(st.session_state.available_spots):
        # Google Maps navigation link for the popup
        gmaps_url = f"https://www.google.com/maps/search/?api=1&query={spot['lat']},{spot['lon']}"
        
        popup_html = f"""
            <div style="font-family: sans-serif; color: #000; width: 200px;">
                <b>📍 {spot['Street']}</b><br>
                <b>⏰ {spot['Time']}</b><br>
                <small>{spot['Details']}</small><br>
                <b>👤 {spot['Driver']}</b><br><br>
                <a href="{gmaps_url}" target="_blank" style="background: #059669; color: white; padding: 4px 8px; text-decoration: none; border-radius: 4px; display: inline-block; font-size: 11px; font-weight: bold;">🧭 Google Maps Directions</a>
            </div>
        """
        folium.Marker(
            location=[spot['lat'], spot['lon']],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{spot['Street']} ({spot['Time']})",
            icon=folium.Icon(color="green", icon="parking", prefix="fa")
        ).add_to(limassol_map)

    # Render map in Streamlit
    st_folium(limassol_map, width=700, height=400)

    st.markdown("---")
    st.markdown(f"#### {t['list_title']}")

    if st.session_state.available_spots:
        for idx, spot in enumerate(st.session_state.available_spots):
            st.markdown(f"""
                <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(52, 211, 153, 0.25); border-radius: 14px; padding: 1rem; margin-bottom: 0.8rem;">
                    <b>📍 {spot['Street']}</b><br>
                    <span style="color: #34d399; font-weight: bold;">⏰ {t['leave_time']} {spot['Time']}</span><br>
                    <span style="color: #cbd5e1; font-size: 0.85rem;">📝 {spot['Details']}</span><br>
                    <div style="margin-top: 6px; font-size: 0.75rem; color: #94a3b8;">👤 {t['driver']} {spot['Driver']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Direct Navigation Link Button
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

    with st.form("parking_form", border=False):
        street_choice = st.selectbox(t['zone_label'], limassol_zones)
        time_leaving = st.selectbox(t['time_label'], time_options)
        driver_name = st.text_input(t['name_label'], placeholder=t['name_placeholder'])
        extra_details = st.text_input(t['details_label'], placeholder=t['details_placeholder'])
        
        submit_spot = st.form_submit_button(t['publish_btn'])
        
        if submit_spot:
            coords = zone_coordinates[street_choice]
            import random
            lat_offset = random.uniform(-0.0008, 0.0008)
            lon_offset = random.uniform(-0.0008, 0.0008)

            st.session_state.available_spots.insert(0, {
                "Street": street_choice,
                "Time": time_leaving,
                "Driver": driver_name.strip() if driver_name.strip() else "Ανώνυμος Οδηγός",
                "Details": extra_details.strip() if extra_details.strip() else "Χωρίς επιπλέον περιγραφή",
                "lat": coords["lat"] + lat_offset,
                "lon": coords["lon"] + lon_offset
            })
            st.success(t['success_publish'])
            st.rerun()

with tab3:
    st.markdown(f"#### {t['terms_title']}")
    st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.5); padding: 1.2rem; border-radius: 14px; line-height: 1.6; font-size: 0.9rem;">
            {t['terms_text']}
        </div>
    """, unsafe_allow_html=True)
