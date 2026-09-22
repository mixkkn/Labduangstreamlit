"""
app.py
=======
หน้าเว็บหลักของแอปดูดวง สร้างด้วย Streamlit
ทำหน้าที่รับข้อมูลผู้ใช้ เรียกใช้ฟังก์ชันจากทั้ง 5 โมดูลลอจิก
(module_user, module_horoscope, module_tarot, module_lucky, module_report)
แล้วแสดงผลลัพธ์เป็น Bento Grid Layout พร้อมปุ่มดาวน์โหลดและรีเซ็ต

วิธีรัน: streamlit run app.py
"""

import streamlit as st

from module_user import (
    get_zodiac,
    get_element,
    calculate_name_number,
    get_numerology_meaning,
    validate_input,
)
from module_horoscope import (
    get_daily_score,
    get_work_horoscope,
    get_finance_horoscope,
    get_love_horoscope,
    summarize_horoscope,
)
from module_tarot import (
    create_deck,
    shuffle_deck,
    draw_three_cards,
    format_tarot_reading,
)
from module_lucky import (
    get_lucky_color,
    get_unlucky_color,
    get_lucky_numbers,
    get_lucky_direction,
    get_lucky_food,
)
from module_report import (
    generate_full_report,
    format_text_for_download,
    calculate_overall_percentage,
    get_daily_quote,
    clean_user_input,
)


# ----------------------------------------------------------------------------
# การตั้งค่าหน้าเพจ + Custom CSS สำหรับ Bento Grid
# ----------------------------------------------------------------------------
st.set_page_config(page_title="ดูดวงรายวัน ✨", page_icon="🔮", layout="wide")

st.markdown(
    """
    <style>
    .bento-box {
        background: linear-gradient(135deg, #2b2140 0%, #1a1330 100%);
        border-radius: 20px;
        padding: 22px 24px;
        margin-bottom: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.25);
        height: 100%;
    }
    .bento-box h3 {
        margin-top: 0;
        color: #f5c2e7;
    }
    .bento-box p, .bento-box li {
        color: #e6e6e6;
        font-size: 15px;
        line-height: 1.6;
    }
    .quote-box {
        background: linear-gradient(135deg, #3a2e5c 0%, #241a3d 100%);
        border-radius: 20px;
        padding: 20px 24px;
        text-align: center;
        font-style: italic;
        color: #ffe0f0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 8px;
    }
    .score-badge {
        font-size: 42px;
        font-weight: 700;
        color: #ffd166;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------------
# Session State เริ่มต้น
# ----------------------------------------------------------------------------
if "report_ready" not in st.session_state:
    st.session_state.report_ready = False
if "full_report" not in st.session_state:
    st.session_state.full_report = None
if "overall_percentage" not in st.session_state:
    st.session_state.overall_percentage = 0
if "daily_quote" not in st.session_state:
    st.session_state.daily_quote = ""
if "download_text" not in st.session_state:
    st.session_state.download_text = ""
if "clean_name" not in st.session_state:
    st.session_state.clean_name = ""


def run_prediction(raw_name, birth_month):
    """
    ประมวลผลข้อมูลผู้ใช้ทั้งหมด โดยเรียกใช้ฟังก์ชันจากทุกโมดูล
    แล้วเก็บผลลัพธ์สุดท้ายลงใน st.session_state
    """
    # 1. ตรวจสอบข้อมูลก่อน
    is_valid, message = validate_input(raw_name, birth_month)
    if not is_valid:
        st.error(f"⚠️ {message}")
        return

    # 2. กรองข้อความชื่อให้สะอาดก่อนนำไปใช้ต่อ
    clean_name = clean_user_input(raw_name)
    month = int(birth_month)

    # 3. โมดูลผู้ใช้
    zodiac = get_zodiac(month)
    element = get_element(zodiac)
    name_number = calculate_name_number(clean_name)
    number_meaning = get_numerology_meaning(name_number)

    user_dict = {
        "ชื่อ": clean_name,
        "ราศีเกิด": zodiac,
        "ธาตุประจำตัว": element,
        "เลขศาสตร์": name_number,
        "ความหมายเลขศาสตร์": number_meaning,
    }

    # 4. โมดูลดวงรายวัน
    daily_score = get_daily_score()
    horoscope_dict = {
        "คะแนนดวงวันนี้": f"{daily_score}/10",
        "ภาพรวม": summarize_horoscope(daily_score),
        "การงาน": get_work_horoscope(),
        "การเงิน": get_finance_horoscope(),
        "ความรัก": get_love_horoscope(),
    }

    # 5. โมดูลไพ่ยิปซี
    deck = shuffle_deck(create_deck())
    three_cards = draw_three_cards(deck)
    past_card, present_card, future_card = three_cards[0], three_cards[1], three_cards[2]
    tarot_dict = {
        "อดีต": f"{past_card['name']} — {past_card['meaning']}",
        "ปัจจุบัน": f"{present_card['name']} — {present_card['meaning']}",
        "อนาคต": f"{future_card['name']} — {future_card['meaning']}",
        "สรุปผลไพ่ทั้งหมด": format_tarot_reading(three_cards),
    }

    # 6. โมดูลของมงคล
    lucky_color = get_lucky_color()
    unlucky_color = get_unlucky_color(lucky_color)
    lucky_numbers = get_lucky_numbers()
    lucky_dict = {
        "สีมงคล": lucky_color,
        "สีกาลกิณี": unlucky_color,
        "เลขเด็ด 2 ตัว": lucky_numbers["two_digit"],
        "เลขเด็ด 3 ตัว": lucky_numbers["three_digit"],
        "ทิศมงคล": get_lucky_direction(),
        "เมนูเสริมดวง": get_lucky_food(),
    }

    # 7. รวมรายงานทั้งหมด
    full_report = generate_full_report(user_dict, horoscope_dict, tarot_dict, lucky_dict)

    # 8. คำนวณเปอร์เซ็นต์ความโชคดีรวม (ใช้คะแนนดวงรายวัน + เลขศาสตร์)
    overall_percentage = calculate_overall_percentage(daily_score, name_number)

    # 9. เก็บทุกอย่างลง session_state
    st.session_state.clean_name = clean_name
    st.session_state.full_report = full_report
    st.session_state.overall_percentage = overall_percentage
    st.session_state.daily_quote = get_daily_quote()
    st.session_state.download_text = format_text_for_download(full_report)
    st.session_state.report_ready = True


def reset_all():
    """ล้างข้อมูลทั้งหมดใน session_state เพื่อเริ่มทำนายใหม่"""
    st.session_state.report_ready = False
    st.session_state.full_report = None
    st.session_state.overall_percentage = 0
    st.session_state.daily_quote = ""
    st.session_state.download_text = ""
    st.session_state.clean_name = ""


# ----------------------------------------------------------------------------
# ส่วนหัวของหน้าเว็บ
# ----------------------------------------------------------------------------
st.title("🔮 ดูดวงรายวัน")
st.caption("กรอกชื่อและเดือนเกิด แล้วให้เราทำนายดวงให้คุณวันนี้")

# ----------------------------------------------------------------------------
# ส่วนรับข้อมูล (แสดงเฉพาะตอนที่ยังไม่มีผลลัพธ์)
# ----------------------------------------------------------------------------
if not st.session_state.report_ready:
    with st.form("user_input_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            name_input = st.text_input("ชื่อภาษาอังกฤษ", placeholder="เช่น Somchai")
        with col_b:
            month_input = st.selectbox(
                "เดือนเกิด",
                options=list(range(1, 13)),
                format_func=lambda m: [
                    "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน",
                    "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม",
                    "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม",
                ][m - 1],
            )

        submitted = st.form_submit_button("🔮 เริ่มทำนาย", use_container_width=True)
        if submitted:
            run_prediction(name_input, month_input)
            if st.session_state.report_ready:
                st.rerun()

# ----------------------------------------------------------------------------
# ส่วนแสดงผลลัพธ์ (Bento Grid)
# ----------------------------------------------------------------------------
else:
    report = st.session_state.full_report
    user = report["user"]
    horoscope = report["horoscope"]
    tarot = report["tarot"]
    lucky = report["lucky"]
    percentage = st.session_state.overall_percentage

    st.subheader(f"ผลการทำนายของคุณ {user['ชื่อ']} ✨")

    # -------------------------------------------------------------------
    # แถวสรุปด้านบน: เมตริกหลัก + แถบเปอร์เซ็นต์ความโชคดีรวม
    # -------------------------------------------------------------------
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("ราศีเกิด", user["ราศีเกิด"])
    m2.metric("ธาตุประจำตัว", user["ธาตุประจำตัว"])
    m3.metric("เลขศาสตร์", user["เลขศาสตร์"])
    m4.metric("คะแนนดวงวันนี้", horoscope["คะแนนดวงวันนี้"])

    st.markdown(f"**ระดับความโชคดีรวมวันนี้: {percentage:.0f}%** — {horoscope['ภาพรวม']}")
    st.progress(int(percentage) / 100)

    st.divider()

    # -------------------------------------------------------------------
    # แยกหมวดหมู่ด้วย Tabs ให้แต่ละเรื่องอยู่เป็นสัดส่วน
    # -------------------------------------------------------------------
    tab_basic, tab_daily, tab_tarot, tab_lucky = st.tabs(
        ["👤 ข้อมูลพื้นฐาน", "🌤️ ดวงรายวัน", "🃏 ไพ่ยิปซี", "🍀 มงคลประจำวัน"]
    )

    # --- แท็บที่ 1: ข้อมูลพื้นฐาน ---
    with tab_basic:
        st.markdown(
            f"""
            <div class="bento-box">
                <h3>🔢 เลขศาสตร์ของ {user['ชื่อ']}</h3>
                <p><b>ราศีเกิด:</b> {user['ราศีเกิด']} &nbsp;(ธาตุ{user['ธาตุประจำตัว']})</p>
                <p><b>เลขประจำตัว:</b> {user['เลขศาสตร์']}</p>
                <p><b>ความหมาย:</b> {user['ความหมายเลขศาสตร์']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --- แท็บที่ 2: ดวงรายวัน แยกเป็น 3 กล่องย่อยตามด้าน ---
    with tab_daily:
        d1, d2, d3 = st.columns(3)
        with d1:
            st.markdown(
                f"""
                <div class="bento-box">
                    <h3>💼 การงาน</h3>
                    <p>{horoscope['การงาน']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with d2:
            st.markdown(
                f"""
                <div class="bento-box">
                    <h3>💰 การเงิน</h3>
                    <p>{horoscope['การเงิน']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with d3:
            st.markdown(
                f"""
                <div class="bento-box">
                    <h3>❤️ ความรัก</h3>
                    <p>{horoscope['ความรัก']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # --- แท็บที่ 3: ไพ่ยิปซี แยกเป็น 3 กล่องย่อย อดีต/ปัจจุบัน/อนาคต ---
    with tab_tarot:
        t1, t2, t3 = st.columns(3)
        with t1:
            st.markdown(
                f"""
                <div class="bento-box">
                    <h3>🕰️ อดีต</h3>
                    <p>{tarot['อดีต']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with t2:
            st.markdown(
                f"""
                <div class="bento-box">
                    <h3>📍 ปัจจุบัน</h3>
                    <p>{tarot['ปัจจุบัน']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with t3:
            st.markdown(
                f"""
                <div class="bento-box">
                    <h3>🔭 อนาคต</h3>
                    <p>{tarot['อนาคต']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # --- แท็บที่ 4: มงคลประจำวัน แยกเป็น 4 กล่องย่อย ---
    with tab_lucky:
        l1, l2, l3, l4 = st.columns(4)
        with l1:
            st.markdown(
                f"""
                <div class="bento-box">
                    <h3>🎨 สีมงคล</h3>
                    <p><b>สีมงคล:</b> {lucky['สีมงคล']}</p>
                    <p><b>สีกาลกิณี:</b> {lucky['สีกาลกิณี']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with l2:
            st.markdown(
                f"""
                <div class="bento-box">
                    <h3>🔢 เลขเด็ด</h3>
                    <p><b>2 ตัว:</b> {lucky['เลขเด็ด 2 ตัว']}</p>
                    <p><b>3 ตัว:</b> {lucky['เลขเด็ด 3 ตัว']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with l3:
            st.markdown(
                f"""
                <div class="bento-box">
                    <h3>🧭 ทิศมงคล</h3>
                    <p>{lucky['ทิศมงคล']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with l4:
            st.markdown(
                f"""
                <div class="bento-box">
                    <h3>🍽️ เมนูเสริมดวง</h3>
                    <p>{lucky['เมนูเสริมดวง']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    # คำคมประจำวัน
    st.markdown(
        f"""
        <div class="quote-box">
            "{st.session_state.daily_quote}"
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    # ปุ่มดาวน์โหลด + ปุ่มรีเซ็ต
    col_dl, col_reset = st.columns(2)
    with col_dl:
        st.download_button(
            label="📥 ดาวน์โหลดผลดวง (.txt)",
            data=st.session_state.download_text,
            file_name=f"horoscope_{user['ชื่อ']}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with col_reset:
        if st.button("🔄 รีเซ็ตข้อมูล", use_container_width=True):
            reset_all()
            st.rerun()