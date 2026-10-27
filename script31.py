import streamlit as st
import streamlit.components.v1 as components
import json
import os
import base64
from datetime import datetime

st.set_page_config(page_title="أكاديمية كابتن محسن", page_icon="⚽", layout="wide")

# ============================================================
# 🔥 إعدادات
# ============================================================
DATA_FILE = "data.json"
ADMIN_PASSWORD = "mohsen123"

COACH_PHOTO_URL = "https://i.postimg.cc/1XBwfr7M/Screenshot-20261017-210359-Google.jpg"
TRAINER_PHOTO_URL = "https://i.postimg.cc/1XBwfr7M/Screenshot-20261017-210359-Google.jpg"
AUDIO_URL = "https://github.com/bebo-12712/ya-wala/raw/refs/heads/main/WhatsApp%20Audio%202026-10-23%20at%208.49.32%20PM.mpeg"

# 👇 صور الخلفيات
LOGIN_BG_IMAGE = "https://i.postimg.cc/NMQ9rC6x/Screenshot-20261027-212455-Google.jpg"
HOME_BG_IMAGE = COACH_PHOTO_URL


# ============================================================
# دوال قاعدة البيانات (data.json)
# ============================================================
def get_default_data():
    return {
        "coach": {"name": "كابتن محسن", "photo": COACH_PHOTO_URL},
        "trainer": {"name": "المدرب المساعد", "photo": TRAINER_PHOTO_URL},
        "schedule": [
            {"day": "الإثنين", "time": "6:00 مساءً", "place": "الملعب", "session_type": "تدريب مجموعة", "booked_by": [],
             "video_url": ""},
        ],
        "users": {},
        "last_update_msg": "",
        "last_update_time": "",
        "motivation_msg": "مجهود عظيم = تدريبات كتير! استمر ولا تتوقف. 💪"
    }


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for s in data.get("schedule", []):
                    if "booked_by" not in s: s["booked_by"] = []
                    if "video_url" not in s: s["video_url"] = ""
                    if "session_type" not in s: s["session_type"] = "تدريب عام"
                if "motivation_msg" not in data:
                    data["motivation_msg"] = "مجهود عظيم = تدريبات كتير! استمر ولا تتوقف. 💪"
                return data
        except Exception:
            pass
    return get_default_data()


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if "data" not in st.session_state:
    st.session_state.data = load_data()

# ✅ حل مشكلة الريفريش
if "user" not in st.session_state:
    if "user" in st.query_params:
        saved_email = st.query_params["user"]
        if saved_email in st.session_state.data["users"]:
            st.session_state.user = {"email": saved_email, **st.session_state.data["users"][saved_email]}
        else:
            st.session_state.user = None
    else:
        st.session_state.user = None

if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = True if "admin" in st.query_params else False

if "editing_index" not in st.session_state:
    st.session_state.editing_index = None


# ============================================================
# دوال مساعدة
# ============================================================
def image_to_base64(uploaded_file):
    bytes_data = uploaded_file.getvalue()
    base64_str = base64.b64encode(bytes_data).decode()
    return f"data:image/jpeg;base64,{base64_str}"


# 👇 دالة الخلفية الجديدة (تغطي الشاشة وتركز على الجزء العلوي)
def set_bg_image(src):
    if not src: return
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: 
            linear-gradient(rgba(15,23,42,0.4), rgba(15,23,42,0.7)), 
            url("{src}");
        background-size: cover; 
        background-repeat: no-repeat;
        background-position: center 15%; /* التركيز على من السرة لفوق */
        background-attachment: fixed;
        direction: rtl;
    }}
    </style>
    """, unsafe_allow_html=True)


# ============================================================
# STYLING
# ============================================================
st.markdown("""
<style>
    .stApp { background-color: #0f172a; direction: rtl; text-align: right; }
    h1, h2, h3 { color: #38bdf8 !important; }

    .plan-card { background: rgba(30,41,59,0.95); border-right: 5px solid #38bdf8; border-left: none; border-radius: 12px; padding: 18px 22px; margin-bottom: 14px; }
    .plan-card .day { color: #38bdf8; font-weight: 700; font-size: 1.2rem; }
    .plan-card .meta { color: #cbd5e1; font-size: 0.95rem; }
    .plan-card .session-type { background: #f59e0b; color: #000; font-weight: bold; padding: 4px 8px; border-radius: 4px; display: inline-block; margin-top: 5px; font-size: 0.85rem; }

    .big-title { font-size: 2.2rem; font-weight: 800; color: #38bdf8; text-shadow: 2px 2px 4px #000; }
    .sub { color: #cbd5e1; font-weight: bold; text-shadow: 2px 2px 4px #000;}

    .profile-pic { width: 150px; height: 150px; border-radius: 50%; object-fit: cover; border: 4px solid #38bdf8; margin-bottom: 10px; }

    .tg-btn { display: inline-block; background-color: #0088cc; color: white !important; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold; margin-top: 10px; text-align: center; width: 100%; }
    .tg-btn:hover { background-color: #005f8f; }
    .video-btn { display: inline-block; background-color: #ef4444; color: white !important; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; text-align: center; margin-bottom: 10px; width: 100%; }
    .video-btn:hover { background-color: #dc2626; }

    .alert-box { background-color: #ef4444; color: white; padding: 15px; border-radius: 8px; font-weight: bold; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .booked-list { color: #10b981; font-weight: bold; font-size: 0.9rem; margin-top: 5px; }
    .motivation-quote { font-size: 2.5rem; font-weight: 900; color: #f59e0b; text-align: center; margin: 30px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.8); line-height: 1.3; }

    .review-card { background: rgba(30, 41, 59, 0.95); padding: 15px; border-radius: 10px; margin-bottom: 10px; border-right: 4px solid #10b981; }
    .review-stars { color: #fbbf24; font-size: 1.2rem; }
    .review-text { color: #e2e8f0; font-style: italic; margin: 5px 0; }
    .review-author { color: #94a3b8; font-size: 0.85rem; font-weight: bold; }

    .auth-box { background: rgba(15, 23, 42, 0.85); padding: 30px; border-radius: 15px; border: 2px solid #38bdf8; box-shadow: 0 10px 25px rgba(0,0,0,0.8); }

    .center-card { background: rgba(30,41,59,0.95); padding: 15px; border-radius: 10px; text-align: center; border-top: 3px solid #38bdf8; margin-bottom: 10px;}
    .news-card { background: rgba(30,41,59,0.95); padding: 15px; border-radius: 10px; margin-bottom: 10px; border-right: 4px solid #f59e0b; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# AUTH
# ============================================================
def show_auth_screen():
    set_bg_image(LOGIN_BG_IMAGE)
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown('<div class="auth-box">', unsafe_allow_html=True)
        st.markdown("<div class='big-title' style='text-align:center;'>⚽ كابتن محسن</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub' style='text-align:center;'>سجل دخولك أو أنشئ حساباً جديداً</div><br>",
                    unsafe_allow_html=True)

        role = st.radio("أنا...", ["لاعب", "أدمن (مسؤول)"], horizontal=True, key="role_select")
        tab_in, tab_up = st.tabs(["تسجيل الدخول", "حساب جديد"])

        with tab_in:
            login_input = st.text_input("البريد الإلكتروني أو رقم الموبايل", key="login_cred")
            pw = st.text_input("كلمة المرور", type="password", key="login_pw")
            if st.button("دخول", type="primary", use_container_width=True):
                if role == "أدمن (مسؤول)":
                    if pw == ADMIN_PASSWORD:
                        st.session_state.admin_logged = True
                        st.query_params["admin"] = "yes"
                        st.rerun()
                    else:
                        st.error("كلمة مرور الأدمن غير صحيحة.")
                else:
                    cred_key = login_input.lower()
                    if "@" not in cred_key: cred_key = f"{cred_key}@mobile.local"
                    u = st.session_state.data["users"].get(cred_key)
                    if not u:
                        st.error("لا يوجد حساب بهذه البيانات. يرجى إنشاء حساب.")
                    elif u["password"] != pw:
                        st.error("كلمة المرور غير صحيحة.")
                    else:
                        st.session_state.user = {"email": cred_key, **u}
                        st.query_params["user"] = cred_key
                        st.rerun()

        with tab_up:
            n = st.text_input("الاسم بالكامل", key="up_n")
            cred = st.text_input("البريد الإلكتروني أو رقم الموبايل", key="up_cred")
            p = st.text_input("كلمة المرور", type="password", key="up_p")
            if st.button("إنشاء الحساب", type="primary", use_container_width=True):
                if not (n and cred and p):
                    st.error("يرجى ملء جميع الحقول.")
                else:
                    cred_key = cred.lower()
                    if "@" not in cred_key: cred_key = f"{cred_key}@mobile.local"
                    if cred_key in st.session_state.data["users"]:
                        st.error("هذه البيانات مسجلة بالفعل. سجل دخولك.")
                    else:
                        st.session_state.data["users"][cred_key] = {
                            "name": n, "password": p, "phone": "", "age": "", "foot": "",
                            "info_complete": False, "profile_pic": "", "credential": cred
                        }
                        save_data(st.session_state.data)
                        st.session_state.user = {"email": cred_key, **st.session_state.data["users"][cred_key]}
                        st.query_params["user"] = cred_key
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# PERSONAL INFO
# ============================================================
def show_info_screen():
    set_bg_image(LOGIN_BG_IMAGE)
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown('<div class="auth-box">', unsafe_allow_html=True)
        st.markdown("<div class='big-title'>📋 بياناتك الشخصية</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub'>أخبر الكابتن محسن بمعلومات عنك</div><br>", unsafe_allow_html=True)

        phone = st.text_input("رقم الهاتف")
        age = st.number_input("العمر", 5, 99, 16)
        foot = st.radio("القدم المسيطرة", ["يمين", "شمال"], horizontal=True)

        if st.button("متابعة إلى التدريب ←", type="primary", use_container_width=True):
            em = st.session_state.user["email"]
            u = st.session_state.data["users"][em]
            u.update({"phone": phone.strip(), "age": str(age), "foot": foot, "info_complete": True})
            st.session_state.user = {"email": em, **u}
            save_data(st.session_state.data)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# DASHBOARD (شاشة اللاعب)
# ============================================================
def show_dashboard():
    data = st.session_state.data
    set_bg_image(HOME_BG_IMAGE)

    if data.get("last_update_msg"):
        st.markdown(f"""
        <div class="alert-box">
            📢 {data['last_update_msg']} <br>
            <span style="font-size: 0.8rem; font-weight: normal;">(بتاريخ: {data['last_update_time']})</span>
        </div>
        """, unsafe_allow_html=True)

    c1, c2 = st.columns([4, 1])
    with c1:
        st.markdown("<div class='big-title'>خطط التدريب</div>", unsafe_allow_html=True)
    with c2:
        if st.button("تسجيل خروج", use_container_width=True):
            st.session_state.user = None
            st.query_params.clear()
            st.rerun()

    st.markdown("---")

    u = st.session_state.user
    col_pic, col_info, col_tg = st.columns([1.5, 2, 2])

    with col_pic:
        if u.get("profile_pic"):
            st.markdown(f'<img src="{u["profile_pic"]}" class="profile-pic">', unsafe_allow_html=True)
        else:
            st.markdown(f'<img src="https://www.w3schools.com/howto/img_avatar.png" class="profile-pic">',
                        unsafe_allow_html=True)

    with col_info:
        st.markdown(f"<h3 style='text-shadow: 2px 2px 4px #000;'>{u['name']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='sub'>العمر: {u['age']} | القدم المسيطرة: {u['foot']}</div><br>",
                    unsafe_allow_html=True)

        uploaded_file = st.file_uploader("📷 غير صورتك الشخصية", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            if st.button("حفظ الصورة الجديدة", type="primary"):
                new_pic_b64 = image_to_base64(uploaded_file)
                st.session_state.data["users"][u["email"]]["profile_pic"] = new_pic_b64
                st.session_state.user["profile_pic"] = new_pic_b64
                save_data(st.session_state.data)
                st.success("تم حفظ صورتك بنجاح!")
                st.rerun()

    with col_tg:
        st.markdown("<h3 style='text-shadow: 2px 2px 4px #000;'>محتاج مساعدة؟</h3>", unsafe_allow_html=True)
        st.markdown("<div class='sub'>تواصل مع الكابتن محسن على تليجرام</div>", unsafe_allow_html=True)
        telegram_link = "https://t.me/Coashmaher1bot?start=hello"
        st.markdown(f'<a href="{telegram_link}" target="_blank" class="tg-btn">✈️ تواصل عبر تليجرام</a>',
                    unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f'<div class="motivation-quote">"{data.get("motivation_msg", "")}"</div>', unsafe_allow_html=True)

    st.subheader("📅 الخطط القادمة")
    if not data["schedule"]:
        st.info("لا توجد خطط تدريبية حالياً.")
    else:
        for i, s in enumerate(data["schedule"]):
            st.markdown(f"""
            <div class="plan-card">
                <div class="day">{s['day']}</div>
                <div class="session-type">📌 {s.get('session_type', 'تدريب عام')}</div>
                <div class="meta">🕒 {s['time']}<br>📍 {s['place']}</div>
            </div>""", unsafe_allow_html=True)

            if s.get("video_url"):
                st.markdown(f'<a href="{s["video_url"]}" target="_blank" class="video-btn">▶️ شاهد فيديو التمرين</a>',
                            unsafe_allow_html=True)

            has_booked = u["name"] in s.get("booked_by", [])
            if has_booked:
                st.success("✅ أنت محجوز في هذا التدريب!")
            else:
                html_button = f"""
                    <audio id="myAudio_{i}" src="{AUDIO_URL}"></audio>
                    <button onclick="playAndBook('{i}')" style="background-color: #38bdf8; color: #0f172a; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer; width: 100%; margin-bottom: 20px;">
                        احجز في {s.get('session_type', 'التدريب')}
                    </button>
                    <script>
                    function playAndBook(id) {{
                        var audio = document.getElementById('myAudio_' + id);
                        audio.play();
                        alert('تم الحجز بنجاح! استعد للتمرين 💪');
                    }}
                    </script>
                """
                components.html(html_button, height=80)

                if st.button(f"تأكيد الحجز في {s.get('session_type', 'التدريب')}", key=f"btn_book_{i}"):
                    if "booked_by" not in data["schedule"][i]: data["schedule"][i]["booked_by"] = []
                    if u["name"] not in data["schedule"][i]["booked_by"]:
                        data["schedule"][i]["booked_by"].append(u["name"])
                        save_data(data)
                        st.success("تم تسجيل حجزك بنجاح في قاعدة البيانات!")
                        st.rerun()

    st.markdown("---")

    # 👇 قسم المراكز
    st.subheader("📍 مراكز التدريب")
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        st.markdown('<div class="center-card"><h3>الملعب الرئيسي</h3><p class="sub">استاد المدينة الرياضي</p></div>',
                    unsafe_allow_html=True)
    with col_c2:
        st.markdown('<div class="center-card"><h3>ملعب التدريب ب</h3><p class="sub">أكاديمية النجوم</p></div>',
                    unsafe_allow_html=True)
    with col_c3:
        st.markdown('<div class="center-card"><h3>الملعب الصغير</h3><p class="sub">ميدان النادي الأهلي</p></div>',
                    unsafe_allow_html=True)

    st.markdown("---")

    # 👇 قسم الأخبار
    st.subheader("📰 أخبار الأكاديمية")
    st.markdown(
        '<div class="news-card"><h4>🔥 تدريبات مكثفة استعداداً للبطولة!</h4><p class="sub">يستعد فريقنا لبطولة الجمهورية بجدول تدريبي مكثف خلال الأيام القادمة.</p></div>',
        unsafe_allow_html=True)
    st.markdown(
        '<div class="news-card"><h4>⭐ انضمام لاعبين جدد</h4><p class="sub">نرحب باللاعبين الجدد في صفوف الأكاديمية، ونتمنى لهم مسيرة موفقة.</p></div>',
        unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("⭐ ماذا يقول اللاعبون؟")
    reviews = [
        {"name": "أحمد م.", "text": "أفضل تدريب جربته في حياتي!", "stars": "⭐⭐⭐⭐⭐"},
        {"name": "يوسف ع.", "text": "حجز البرايفت ساعدني أطور مستوايا بسرعة.", "stars": "⭐⭐⭐⭐⭐"}
    ]
    for r in reviews:
        st.markdown(
            f'<div class="review-card"><div class="review-stars">{r["stars"]}</div><div class="review-text">"{r["text"]}"</div><div class="review-author">- {r["name"]}</div></div>',
            unsafe_allow_html=True)


# ============================================================
# ADMIN
# ============================================================
def show_admin():
    data = st.session_state.data
    set_bg_image(LOGIN_BG_IMAGE)
    c1, c2 = st.columns([4, 1])
    with c1:
        st.markdown("<div class='big-title'>🔒 لوحة تحكم الأدمن</div>", unsafe_allow_html=True)
    with c2:
        if st.button("تسجيل خروج", use_container_width=True):
            st.session_state.admin_logged = False
            st.query_params.clear()
            st.rerun()

    st.subheader("✍️ تعديل الرسالة التحفيزية")
    with st.form("motivation_form"):
        new_motivation = st.text_input("الجملة التحفيزية", value=data.get("motivation_msg", ""))
        if st.form_submit_button("حفظ الجملة", type="primary"):
            data["motivation_msg"] = new_motivation
            save_data(data)
            st.success("تم حفظ الرسالة!")
            st.rerun()

    st.divider()
    st.subheader("📢 إرسال تنبيه للاعبين")
    with st.form("alert_form"):
        alert_msg = st.text_input("نص التنبيه")
        if st.form_submit_button("إرسال التنبيه", type="primary"):
            data["last_update_msg"] = alert_msg
            data["last_update_time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_data(data)
            st.success("تم إرسال التنبيه!")
            st.rerun()

    if data.get("last_update_msg"):
        if st.button("🗑️ مسح التنبيه"):
            data["last_update_msg"] = ""
            data["last_update_time"] = ""
            save_data(data)
            st.rerun()

    st.divider()
    st.subheader("➕ إضافة خطة تدريب")
    c1, c2, c3 = st.columns(3)
    with c1:
        day = st.selectbox("اليوم", ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"])
    with c2:
        time = st.text_input("الوقت")
    with c3:
        place = st.text_input("المكان")
    session_type = st.selectbox("نوع التدريب", ["تدريب مجموعة", "تدريب برايفت", "اختبارات ومباريات", "تدريب حراس مرمى"])
    video_url = st.text_input("رابط فيديو التمرين (اختياري)")

    if st.button("إضافة الخطة", type="primary"):
        if time.strip() and place.strip():
            data["schedule"].append(
                {"day": day, "time": time.strip(), "place": place.strip(), "session_type": session_type,
                 "booked_by": [], "video_url": video_url.strip()})
            save_data(data)
            st.rerun()
        else:
            st.error("أدخل الوقت والمكان.")

    st.divider()
    st.subheader("📝 إدارة الخطط والحجوزات")
    for i, s in enumerate(data["schedule"]):
        if st.session_state.editing_index == i:
            st.markdown(f"**تعديل: {s['day']}**")
            ec1, ec2, ec3 = st.columns(3)
            days_list = ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
            try:
                day_idx = days_list.index(s["day"])
            except:
                day_idx = 0
            with ec1:
                new_day = st.selectbox("اليوم", days_list, index=day_idx, key=f"edit_day_{i}")
            with ec2:
                new_time = st.text_input("الوقت", value=s["time"], key=f"edit_time_{i}")
            with ec3:
                new_place = st.text_input("المكان", value=s["place"], key=f"edit_place_{i}")
            types_list = ["تدريب مجموعة", "تدريب برايفت", "اختبارات ومباريات", "تدريب حراس مرمى"]
            try:
                type_idx = types_list.index(s.get("session_type", "تدريب مجموعة"))
            except:
                type_idx = 0
            new_type = st.selectbox("نوع التدريب", types_list, index=type_idx, key=f"edit_type_{i}")
            new_video = st.text_input("رابط الفيديو", value=s.get("video_url", ""), key=f"edit_vid_{i}")

            if st.button("حفظ", key=f"save_edit_{i}"):
                data["schedule"][i].update(
                    {"day": new_day, "time": new_time.strip(), "place": new_place.strip(), "session_type": new_type,
                     "video_url": new_video.strip()})
                save_data(data)
                st.session_state.editing_index = None
                st.rerun()
            if st.button("إلغاء", key=f"cancel_edit_{i}"):
                st.session_state.editing_index = None
                st.rerun()
            st.divider()
        else:
            cc1, cc2, cc3 = st.columns([4, 1, 1])
            with cc1:
                st.markdown(f"**{s['day']}** — {s['time']} — {s['place']}")
                st.markdown(
                    f"<span style='color:#f59e0b; font-weight:bold;'>📌 {s.get('session_type', 'تدريب عام')}</span>",
                    unsafe_allow_html=True)
                if s.get("video_url"): st.markdown(f"<span style='color:#ef4444;'>▶️ يوجد فيديو مرفق</span>",
                                                   unsafe_allow_html=True)
                booked_names = s.get("booked_by", [])
                if booked_names:
                    st.markdown(f"<div class='booked-list'>👥 الحجوزات: {', '.join(booked_names)}</div>",
                                unsafe_allow_html=True)
                else:
                    st.markdown("<div class='sub'>لا يوجد حجوزات حتى الآن.</div>", unsafe_allow_html=True)
            with cc2:
                if st.button("تعديل ✏️", key=f"edit_btn_{i}"):
                    st.session_state.editing_index = i
                    st.rerun()
            with cc3:
                if st.button("حذف 🗑️", key=f"del_{i}"):
                    data["schedule"].pop(i)
                    save_data(data)
                    st.session_state.editing_index = None
                    st.rerun()


# ============================================================
# ROUTER
# ============================================================
if st.session_state.admin_logged:
    show_admin()
elif st.session_state.user is None:
    show_auth_screen()
elif not st.session_state.user.get("info_complete"):
    show_info_screen()
else:
    show_dashboard()