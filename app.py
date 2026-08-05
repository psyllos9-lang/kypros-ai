import streamlit as st
import pandas as pd

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
    .parking-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(52, 211, 153, 0.25);
        border-radius: 16px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
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
        "subtitle": "Ζωντανό Κοινοτικό Parking σε Πραγματικό Χρόνο",
        "tab1": "🟢 Live Θέσεις",
        "tab2": "📢 Ελευθερώνω Θέση",
        "tab3": "📊 Στατιστικά",
        "list_title": "Διαθέσιμες Θέσεις Αυτή τη Στιγμή",
        "list_desc": "Δες ποιοι οδηγοί ελευθερώνουν θέση στους δρόμους της Λεμεσού τώρα:",
        "leave_time": "Αναχώρηση:",
        "driver": "Οδηγός:",
        "claim_btn": "🚗 Την πήρα! (Κατάργηση)",
        "success_claim": "Ευχαριστούμε! Η θέση αφαιρέθηκε από τη λίστα.",
        "no_spots": "Δεν υπάρχουν διαθέσιμες θέσεις αυτή τη στιγμή. Γίνε ο πρώτος που θα βοηθήσει!",
        "form_title": "Ελευθερώνεις θέση στο δρόμο;",
        "form_desc": "Βοήθησε έναν γείτονα οδηγό ενημερώνοντας ότι φεύγεις από τη θέση σου.",
        "zone_label": "Επιλογή Περιοχής / Οδού:",
        "time_label": "Πότε φεύγεις;",
        "name_label": "Το όνομα σου:",
        "name_placeholder": "π.χ. Ανδρέας",
        "details_label": "Λεπτομέρειες / Σημείο αναφοράς:",
        "details_placeholder": "π.χ. Δίπλα στον πράσινο κάδο",
        "publish_btn": "🚀 Δημοσίευση Ελεύθερης Θέσης",
        "success_publish": "Η θέση σου δημοσιεύτηκε επιτυχώς και είναι ορατή σε όλους!",
        "name_warn": "Παρακαλώ βάλε το όνομα σου.",
        "stats_title": "Σύνοψη Κοινότητας",
        "active_spots_metric": "Ενεργές Θέσεις",
        "table_title": "Ιστορικό / Καταχωρήσεις"
    },
    "English": {
        "title": "🅿️ ParkPulse Limassol",
        "subtitle": "Live Crowdsourced Street Parking Hub",
        "tab1": "🟢 Live Spots",
        "tab2": "📢 Release Spot",
        "tab3": "📊 Statistics",
        "list_title": "Available Spots Right Now",
        "list_desc": "Check drivers releasing street parking in Limassol:",
        "leave_time": "Leaving:",
        "driver": "Driver:",
        "claim_btn": "🚗 Claimed! (Remove)",
        "success_claim": "Thanks! Spot removed from live feed.",
        "no_spots": "No available spots right now. Be the first to help!",
        "form_title": "Releasing a Street Spot?",
        "form_desc": "Help a fellow driver by sharing your spot as you leave.",
        "zone_label": "Select Area / Street:",
        "time_label": "When are you leaving?",
        "name_label": "Your Name:",
        "name_placeholder": "e.g., Andrew",
        "details_label": "Details / Landmark:",
        "details_placeholder": "e.g., Near the green bin",
        "publish_btn": "🚀 Publish Available Spot",
        "success_publish": "Your spot has been successfully published!",
        "name_warn": "Please enter your name.",
        "stats_title": "Community Summary",
        "active_spots_metric": "Active Spots",
        "table_title": "Current Live Feed"
    },
    "Русский": {
        "title": "🅿️ ParkPulse Лимассол",
        "subtitle": "Живой обмен парковочными местами",
        "tab1": "🟢 Свободные места",
        "tab2": "📢 Освобождаю место",
        "tab3": "📊 Статистика",
        "list_title": "Доступные места прямо сейчас",
        "list_desc": "Посмотрите, где водители освобождают места в Лимассоле:",
        "leave_time": "Уезжает через:",
        "driver": "Водитель:",
        "claim_btn": "🚗 Занял! (Удалить)",
        "success_claim": "Спасибо! Место удалено из списка.",
        "no_spots": "Нет доступных мест. Будьте первыми!",
        "form_title": "Освобождаете парковку?",
        "form_desc": "Помогите другому водителю, сообщив об уходе.",
        "zone_label": "Выберите район / улицу:",
        "time_label": "Когда уезжаете?",
        "name_label": "Ваше имя:",
        "name_placeholder": "например, Алексей",
        "details_label": "Детали / Ориентир:",
        "details_placeholder": "например, возле аптеки",
        "publish_btn": "🚀 Опубликовать место",
        "success_publish": "Ваше место успешно опубликовано!",
        "name_warn": "Пожалуйста, введите ваше имя.",
        "stats_title": "Сводка сообщества",
        "active_spots_metric": "Активные места",
        "table_title": "Текущий список"
    },
    "עברית": {
        "title": "🅿️ ParkPulse לימסול",
        "subtitle": "חניה חיה מבוססת קהילה בלימסול",
        "tab1": "🟢 מקומות פנויים",
        "tab2": "📢 פנוי מקום",
        "tab3": "📊 סטטיסטיקה",
        "list_title": "מקומות חניה פנויים כרגע",
        "list_desc": "ראה נהגים שמפנים חניה ברחובות לימסול עכשיו:",
        "leave_time": "פינוי:",
        "driver": "נהג:",
        "claim_btn": "🚗 תפסתי! (הסרה)",
        "success_claim": "תודה! המקום הוסר מהרשימה.",
        "no_spots": "אין מקומות פנויים כרגע.היה הראשון לעזור!",
        "form_title": "מפנה חניה ברחוב?",
        "form_desc": "עזור לנהג אחר ועדכן שאתה עוזב את החניה.",
        "zone_label": "בחר אזור / רחוב:",
        "time_label": "מתי אתה יוצא?",
        "name_label": "השם שלך:",
        "name_placeholder": "לדוגמה, דוד",
        "details_label": "פרטים / נקודת ציון:",
        "details_placeholder": "לדוגמה, ליד הפח הירוק",
        "publish_btn": "🚀 פרסם מקום פנוי",
        "success_publish": "המקום שלך פורסם בהצלחה!",
        "name_warn": "אנא הזן את שמך.",
        "stats_title": "סיכום קהילה",
        "active_spots_metric": "מקומות פעילים",
        "table_title": "רשימה חיה"
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

# --- INITIALIZE SESSION STATE (LIVE DATA) ---
if "available_spots" not in st.session_state:
    st.session_state.available_spots = [
        {"Street": "Αγίου Ανδρέου (Κέντρο)", "Time": "Σε 2 λεπτά", "Driver": "Μάριος", "Details": "Ακριβώς έξω από το καφέ"},
        {"Street": "Οδός Ανεξαρτησίας", "Time": "Σε 5 λεπτά", "Driver": "Έλενα", "Details": "Κοντά στη συμβολή με Θεμιστοκλή Δέρβη"},
        {"Street": "Περιοχή Μώλος", "Time": "Άμεσα / Τώρα", "Driver": "Γιώργος", "Details": "Κοντά στην αποβάθρα"}
    ]

# --- ZONES DATA IN LIMASSOL ---
limassol_zones = [
    "Αγίου Ανδρέου (Κέντρο)",
    "Οδός Ανεξαρτησίας",
    "Περιοχή Μώλος / Μαρίνα",
    "Οδός Σαριπόλου",
    "ΕΠΑΛ / Πλατεία Ηρώων",
    "ΕΝΑΕΡΙΟΣ / Παραλιακή",
    "Άγιος Αθανάσιος (Εμπορικό)"
]

time_options = ["Άμεσα / Τώρα", "Σε 2 λεπτά", "Σε 5 λεπτά", "Σε 10 λεπτά"]

# --- TABS ---
tab1, tab2, tab3 = st.tabs([t['tab1'], t['tab2'], t['tab3']])

with tab1:
    st.markdown(f"#### 🟢 {t['list_title']}")
    st.write(t['list_desc'])

    if st.session_state.available_spots:
        for idx, spot in enumerate(st.session_state.available_spots):
            st.markdown(f"""
                <div class="parking-card">
                    <b>📍 {spot['Street']}</b><br>
                    <span style="color: #34d399; font-weight: bold;">⏰ {t['leave_time']} {spot['Time']}</span><br>
                    <span style="color: #cbd5e1; font-size: 0.85rem;">📝 {spot['Details']}</span><br>
                    <div style="margin-top: 8px; font-size: 0.75rem; color: #94a3b8;">👤 {t['driver']} {spot['Driver']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(t['claim_btn'], key=f"claim_{idx}"):
                st.session_state.available_spots.pop(idx)
                st.success(t['success_claim'])
                st.rerun()
    else:
        st.info(t['no_spots'])

with tab2:
    st.markdown(f"#### 📢 {t['form_title']}")
    st.write(t['form_desc'])

    with st.form("parking_form", border=False):
        street_choice = st.selectbox(t['zone_label'], limassol_zones)
        time_leaving = st.selectbox(t['time_label'], time_options)
        driver_name = st.text_input(t['name_label'], placeholder=t['name_placeholder'])
        extra_details = st.text_input(t['details_label'], placeholder=t['details_placeholder'])
        
        submit_spot = st.form_submit_button(t['publish_btn'])
        
        if submit_spot:
            if not driver_name.strip():
                st.warning(t['name_warn'])
            else:
                st.session_state.available_spots.insert(0, {
                    "Street": street_choice,
                    "Time": time_leaving,
                    "Driver": driver_name.strip(),
                    "Details": extra_details.strip() if extra_details.strip() else "Χωρίς επιπλέον περιγραφή"
                })
                st.success(t['success_publish'])
                st.rerun()

with tab3:
    st.markdown(f"#### 📊 {t['stats_title']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(t['active_spots_metric'], len(st.session_state.available_spots))
    with col2:
        st.metric("City", "Limassol, CY")

    st.markdown("---")
    st.markdown(f"#### 📋 {t['table_title']}")
    if st.session_state.available_spots:
        df_spots = pd.DataFrame(st.session_state.available_spots)
        st.dataframe(df_spots, use_container_width=True, hide_index=True)
    else:
        st.info(t['no_spots'])
