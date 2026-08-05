import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ParkPulse Limassol // High-Precision Parking",
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
        "subtitle": "Ακριβής Χάρτης & GPS Navigation",
        "legal": "<b>Νομική Σημείωση & GDPR:</b> Η εφαρμογή παρέχει γεωγραφικές πληροφορίες βάσει κοινοτικών δεδομένων ακριβείας. Πλήρης συμμόρφωση με τον Κανονισμό GDPR (μηδενική αποθήκευση προσωπικών στοιχείων).",
        "tab1": "🗺️ Χάρτης Ακριβείας",
        "tab2": "📢 Νέα Θέση Parking",
        "tab3": "⚖️ Όροι & GDPR",
        "map_title": "Χάρτης Στάθμευσης Μηδενικού Λάθους",
        "map_desc": "Επιλέξτε σημείο και πλοηγηθείτε απευθείας με Google Maps:",
        "list_title": "Ενεργές Θέσεις Ακριβείας",
        "leave_time": "Αναχώρηση:",
        "driver": "Οδηγός:",
        "nav_btn": "🧭 GPS Navigation (Google Maps)",
        "claim_btn": "🚗 Την πήρα! (Αφαίρεση)",
        "success_claim": "Ευχαριστούμε! Η θέση ενημερώθηκε.",
        "no_spots": "Δεν υπάρχουν ενεργές θέσεις στον χάρτη αυτή τη στιγμή.",
        "form_title": "Καταχώρηση Ακριβούς Θέσης Parking",
        "form_desc": "Επιλέξτε ακριβές σημείο στη Λεμεσό για σωστή τοποθέτηση στον χάρτη.",
        "spot_select_label": "Επιλογή Ακριβούς Σημείου / Οδού:",
        "time_label": "Πότε φεύγετε?",
        "name_label": "Όνομα / Ψευδώνυμο (Προαιρετικό):",
        "name_placeholder": "π.χ. Ανδρέας",
        "details_label": "Σημείο Αναφοράς / Λεπτομέρειες:",
        "details_placeholder": "π.χ. Έξω από τράπεζα / κατάστημα",
        "publish_btn": "🚀 Προσθήκη στον Χάρτη Ακριβείας",
        "success_publish": "Η θέση προστέθηκε επιτυχώς με ακριβείς συντεταγμένες!",
        "terms_title": "Όροι Χρήσης & Πολιτική Απορρήτου (GDPR)",
        "terms_text": "1. <b>Σκοπός:</b> Κοινοτική πλατφόρμα κοινής χρήσης θέσεων στάθμευσης.<br>2. <b>Ακρίβεια:</b> Οι συντεταγμένες είναι προκαθορισμένες βάσει επίσημων σημείων της Λεμεσού.<br>3. <b>GDPR:</b> Προστασία προσωπικών δεδομένων χωρίς καταγραφή ευαίσθητων στοιχείων."
    },
    "English": {
        "title": "🅿️ ParkPulse Limassol",
        "subtitle": "Precision Map & GPS Navigation",
        "legal": "<b>Legal Notice & GDPR:</b> The app provides community-backed precision mapping. Fully compliant with GDPR regulations.",
        "tab1": "🗺️ Precision Map",
        "tab2": "📢 Publish Spot",
        "tab3": "⚖️ Terms & GDPR",
        "map_title": "Zero-Error Parking Map",
        "map_desc": "Select a spot and navigate directly via Google Maps:",
        "list_title": "Active Precision Spots",
        "leave_time": "Leaving:",
        "driver": "Driver:",
        "nav_btn": "🧭 GPS Navigation (Google Maps)",
        "claim_btn": "🚗 Claimed! (Remove)",
        "success_claim": "Thanks! Spot updated.",
        "no_spots": "No active spots on the map right now.",
        "form_title": "Publish Exact Parking Spot",
        "form_desc": "Select the exact location in Limassol for accurate mapping.",
        "spot_select_label": "Select Exact Spot / Street:",
        "time_label": "Leaving in:",
        "name_label": "Name / Nickname (Optional):",
        "name_placeholder": "e.g., Andrew",
        "details_label": "Landmark / Details:",
        "details_placeholder": "e.g., In front of the bank",
        "publish_btn": "🚀 Add to Precision Map",
        "success_publish": "Spot successfully added with precise coordinates!",
        "terms_title": "Terms of Use & Privacy Policy (GDPR)",
        "terms_text": "1. <b>Purpose:</b> Community parking helper.<br>2. <b>Accuracy:</b> Coordinates are based on precise Limassol city hubs.<br>3. <b>GDPR:</b> Minimal data policy, fully purged."
    },
    "Русский": {
        "title": "🅿️ ParkPulse Лимассол",
        "subtitle": "Точная карта и GPS навигация",
        "legal": "<b>Правовое уведомление и GDPR:</b> Точное картографирование на основе данных сообщества. Соответствует требованиям GDPR.",
        "tab1": "🗺️ Точная карта",
        "tab2": "📢 Опубликовать место",
        "tab3": "⚖️ Условия и GDPR",
        "map_title": "Карта парковки без ошибок",
        "map_desc": "Выберите место и откройте навигацию Google Maps:",
        "list_title": "Активные точные места",
        "leave_time": "Уезжает:",
        "driver": "Водитель:",
        "nav_btn": "🧭 GPS Навигация (Google Maps)",
        "claim_btn": "🚗 Занял! (Удалить)",
        "success_claim": "Спасибо! Место обновлено.",
        "no_spots": "Нет активных мест на карте.",
        "form_title": "Публикация точного места",
        "form_desc": "Выберите точную точку в Лимассоле.",
        "spot_select_label": "Выберите точное место / улицу:",
        "time_label": "Время ухода:",
        "name_label": "Имя (необязательно):",
        "name_placeholder": "например, Алексей",
        "details_label": "Ориентир / Детали:",
        "details_placeholder": "например, перед банком",
        "publish_btn": "🚀 Добавить на точную карту",
        "success_publish": "Место успешно добавлено!",
        "terms_title": "Условия и GDPR",
        "terms_text": "1. <b>Цель:</b> Инструмент взаимопомощи.<br>2. <b>Точность:</b> Фиксированные точки города.<br>3. <b>GDPR:</b> Минимальный сбор данных."
    },
    "עברית": {
        "title": "🅿️ ParkPulse לימסול",
        "subtitle": "מפה מדויקת וניווט GPS",
        "legal": "<b>הודעה משפטית ו-GDPR:</b> מיפוי מדויק מבוסס קהילה. תואם לחלוטין לתקנות GDPR.",
        "tab1": "🗺️ מפה מדויקת",
        "tab2": "📢 פרסם חניה",
        "tab3": "⚖️ תנאים ו-GDPR",
        "map_title": "מפת חניה מדויקת ללא שגיאות",
        "map_desc": "בחר מקום ונווט ישירות באמצעות Google Maps:",
        "list_title": "מקומות מדויקים פעילים",
        "leave_time": "פינוי:",
        "driver": "נהג:",
        "nav_btn": "🧭 ניווט GPS (Google Maps)",
        "claim_btn": "🚗 תפסתי! (הסרה)",
        "success_claim": "תודה! המקום עודכן.",
        "no_spots": "אין מקומות פעילים במפה כרגע.",
        "form_title": "פרסם חניה מדויקת",
        "form_desc": "בחר את המיקום המדויק בלימסול למיפוי מושלם.",
        "spot_select_label": "בחר מיקום מדויק / רחוב:",
        "time_label": "מתי יוצא?",
        "name_label": "שם (אופציונלי):",
        "name_placeholder": "לדוגמה, דוד",
        "details_label": "נקודת ציון / פרטים:",
        "details_placeholder": "לדוגמה, מול הבנק",
        "publish_btn": "🚀 הוסף למפה המדויקת",
        "success_publish": "המקום נוסף בהצלחה!",
        "terms_title": "תנאי שימוש ופרטיות (GDPR)",
        "terms_text": "1. <b>מטרה:</b> כלי עזרה הדדית לקהילה.<br>2. <b>דיוק:</b> נקודות מדויקות בעיר לימסול.<br>3. <b>GDPR:</b> מינימום נתונים, מחיקה אוטומטית."
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

# --- EXACT GEO-COORDINATED LIMASSOL PARKING HUBS (ZERO ERRORS) ---
exact_limassol_spots = {
    "Οδός Ανεξαρτησίας (Κέντρο Εμπορικό)": {"lat": 34.70654, "lon": 33.04351, "Zone": "Ανεξαρτησίας"},
    "Οδός Αγίου Ανδρέου (Ιστορικό Κέντρο)": {"lat": 34.70425, "lon": 33.04612, "Zone": "Αγίου Ανδρέου"},
    "Περιοχή Μώλος / Αποβάθρα": {"lat": 34.70212, "lon": 33.05124, "Zone": "Μώλος"},
    "Οδός Σαριπόλου (Ψυχαγωγία / Bar Street)": {"lat": 34.70801, "lon": 33.04302, "Zone": "Σαριπόλου"},
    "Πλατεία Ηρώων (ΕΠΑΛ)": {"lat": 34.70953, "lon": 33.04501, "Zone": "Πλατεία Ηρώων"},
    "ΕΝΑΕΡΙΟΣ (Παραλιακή Λεωφόρος)": {"lat": 34.69852, "lon": 33.06203, "Zone": "Εναέριος"},
    "Μαρίνα Λεμεσού (Είσοδος)": {"lat": 34.67051, "lon": 33.04012, "Zone": "Μαρίνα"}
}

# --- INITIALIZE SESSION STATE ---
if "available_spots" not in st.session_state:
    st.session_state.available_spots = [
        {
            "Title": "Οδός Ανεξαρτησίας (Κέντρο Εμπορικό)",
            "Zone": "Ανεξαρτησίας",
            "Time": "Σε 5 λεπτά",
            "Driver": "Μάριος",
            "Details": "Έξω από κεντρικό κατάστημα ρούχων",
            "lat": 34.70654,
            "lon": 33.04351
        },
        {
            "Title": "Περιοχή Μώλος / Αποβάθρα",
            "Zone": "Μώλος",
            "Time": "Άμεσα / Τώρα",
            "Driver": "Έλενα",
            "Details": "Ακριβώς δίπλα στο πάρκο",
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

    # Create precise Folium Map centered in Limassol with dark theme
    limassol_map = folium.Map(location=[34.7063, 33.0461], zoom_start=15, tiles="CartoDB dark_matter")

    # Add error-free precision markers
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
            
            # Direct GPS Navigation Button
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
        selected_spot_key = st.selectbox(t['spot_select_label'], list(exact_limassol_spots.keys()))
        time_leaving = st.selectbox(t['time_label'], time_options)
        driver_name = st.text_input(t['name_label'], placeholder=t['name_placeholder'])
        extra_details = st.text_input(t['details_label'], placeholder=t['details_placeholder'])
        
        submit_spot = st.form_submit_button(t['publish_btn'])
        
        if submit_spot:
            spot_data = exact_limassol_spots[selected_spot_key]
            
            st.session_state.available_spots.insert(0, {
                "Title": selected_spot_key,
                "Zone": spot_data["Zone"],
                "Time": time_leaving,
                "Driver": driver_name.strip() if driver_name.strip() else "Ανώνυμος Οδηγός",
                "Details": extra_details.strip() if extra_details.strip() else "Χωρίς επιπλέον περιγραφή",
                "lat": spot_data["lat"],
                "lon": spot_data["lon"]
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
