"""
pages/1_📊_Data_Dashboard.py
==============================
หน้าแดชบอร์ดสำหรับ "อัปโหลด / ลบ / ดูข้อมูล" จากไฟล์ .txt ทั่วไป
(ไม่เกี่ยวข้องกับเนื้อหาเว็บดูดวงเลย เป็นเครื่องมือแยกต่างหากสำหรับ
เรียกดูข้อมูลจากไฟล์ตาราง เช่น ไฟล์ข้อมูลพนักงาน HR_DATA.txt)

ไฟล์นี้เป็นหน้าเพิ่มเติมของ Streamlit multipage app โดยวางไว้ในโฟลเดอร์
`pages/` ตามธรรมเนียมของ Streamlit ทำให้ระบบเมนูด้านซ้ายจะมีหน้านี้เพิ่ม
เข้ามาโดยอัตโนมัติ โดย "ไม่ต้องแก้ไขไฟล์ app.py เดิมแม้แต่บรรทัดเดียว"

วิธีรัน: streamlit run app.py  (แล้วเลือกหน้า "Data Dashboard" จากเมนูซ้าย)

หมายเหตุ: หน้านี้ใช้คอมโพเนนต์ของ Streamlit ล้วน ๆ (ไม่มีการฝัง HTML/CSS เอง)
"""

import streamlit as st

import module_data_manager as dm


st.set_page_config(page_title="Data Dashboard", page_icon="📊", layout="wide")

st.title("📊 ระบบจัดการไฟล์ข้อมูล (.txt) และแดชบอร์ดแสดงผล")
st.caption(
    "อัปโหลดไฟล์ .txt แบบตาราง (เช่น ข้อมูลพนักงาน) เพื่อดู ลบ กรอง และ "
    "สรุปผลข้อมูลได้ตามต้องการ — เครื่องมือนี้ไม่เกี่ยวข้องกับเว็บดูดวงแต่อย่างใด"
)

dm.ensure_upload_dir()


# ==============================================================================
# ส่วนที่ 1: อัปโหลดไฟล์ .txt
# ==============================================================================
st.header("1️⃣ อัปโหลดไฟล์ข้อมูล (.txt)")

uploaded_file = st.file_uploader(
    "เลือกไฟล์ .txt ที่ต้องการอัปโหลด", type=["txt"], key="txt_uploader"
)

col_upload_btn, _ = st.columns([1, 3])
with col_upload_btn:
    if st.button("📤 อัปโหลดไฟล์นี้", use_container_width=True, disabled=uploaded_file is None):
        saved_name = dm.save_uploaded_file(uploaded_file.name, uploaded_file.getvalue())
        st.success(f"อัปโหลดไฟล์สำเร็จ: {saved_name}")
        st.rerun()

st.divider()


# ==============================================================================
# ส่วนที่ 2: จัดการรายการไฟล์ที่อัปโหลดไว้ (เลือกไฟล์ / ลบไฟล์)
# ==============================================================================
st.header("2️⃣ ไฟล์ข้อมูลที่มีอยู่ในระบบ")

file_list = dm.list_uploaded_files()

if not file_list:
    st.info("ยังไม่มีไฟล์ .txt ในระบบ กรุณาอัปโหลดไฟล์ก่อนในขั้นตอนที่ 1")
    st.stop()

col_select, col_delete = st.columns([3, 1])
with col_select:
    selected_file = st.selectbox("เลือกไฟล์ที่ต้องการดูข้อมูล", options=file_list)
with col_delete:
    st.write("")
    st.write("")
    if st.button("🗑️ ลบไฟล์นี้", use_container_width=True):
        dm.delete_uploaded_file(selected_file)
        st.success(f"ลบไฟล์ {selected_file} เรียบร้อยแล้ว")
        st.rerun()

st.divider()


# ==============================================================================
# ส่วนที่ 3: อ่านไฟล์ที่เลือกให้เป็นตาราง (พร้อม cache เพื่อความเร็ว)
# ==============================================================================
@st.cache_data(show_spinner="กำลังอ่านและประมวลผลไฟล์ข้อมูล ...")
def _load_cached(filepath, _cache_buster):
    return dm.load_txt_as_dataframe(filepath)


filepath = dm.get_file_path(selected_file)
file_mtime = None
try:
    import os

    file_mtime = os.path.getmtime(filepath)
except OSError:
    pass

df = _load_cached(filepath, file_mtime)

if df is None or df.empty:
    st.error(
        "ไม่สามารถอ่านไฟล์นี้เป็นตารางข้อมูลได้ กรุณาตรวจสอบว่าไฟล์มีแถวหัวตาราง "
        "และมีตัวคั่นคอลัมน์ที่สม่ำเสมอ (เช่น tab, comma หรือช่องว่างหลายตัว)"
    )
    st.stop()

numeric_cols, text_cols = dm.get_column_categories(df)

st.header("3️⃣ แดชบอร์ดแสดงผลข้อมูล")
st.caption(f"ไฟล์ที่กำลังแสดง: **{selected_file}**")

tab_overview, tab_filter, tab_group = st.tabs(
    ["📋 ภาพรวมข้อมูล", "🔍 กรอง/ค้นหาข้อมูล", "📈 สรุปแบบจัดกลุ่ม"]
)

# ------------------------------------------------------------------------
# แท็บที่ 1: ภาพรวมข้อมูลทั้งหมด
# ------------------------------------------------------------------------
with tab_overview:
    m1, m2, m3 = st.columns(3)
    m1.metric("จำนวนแถวข้อมูล", f"{len(df):,}")
    m2.metric("จำนวนคอลัมน์", len(df.columns))
    m3.metric("คอลัมน์ตัวเลข", len(numeric_cols))

    st.subheader("ตัวอย่างข้อมูล")
    st.dataframe(df, use_container_width=True, height=420)

    if numeric_cols:
        st.subheader("สถิติเบื้องต้นของคอลัมน์ตัวเลข")
        st.dataframe(df[numeric_cols].describe(), use_container_width=True)

# ------------------------------------------------------------------------
# แท็บที่ 2: กรอง/ค้นหาข้อมูลตามต้องการ (เรียกดูอะไรจากไฟล์ก็ได้)
# ------------------------------------------------------------------------
with tab_filter:
    st.subheader("เลือกคอลัมน์ที่ต้องการแสดง")
    display_columns = st.multiselect(
        "คอลัมน์ที่จะแสดงผล (ไม่เลือก = แสดงทุกคอลัมน์)",
        options=df.columns.tolist(),
        default=[],
    )
    columns_to_show = display_columns if display_columns else df.columns.tolist()

    st.subheader("ตัวกรองข้อมูล (เลือกได้สูงสุด 3 เงื่อนไข)")
    filtered_df = df.copy()

    filter_slots = st.columns(3)
    no_filter_label = "— ไม่ใช้ตัวกรองนี้ —"

    for i, slot in enumerate(filter_slots):
        with slot:
            filter_col = st.selectbox(
                f"เงื่อนไขที่ {i + 1}: เลือกคอลัมน์",
                options=[no_filter_label] + df.columns.tolist(),
                key=f"filter_col_{i}",
            )

            if filter_col == no_filter_label:
                continue

            if filter_col in numeric_cols:
                col_min = float(df[filter_col].min())
                col_max = float(df[filter_col].max())
                if col_min == col_max:
                    st.caption(f"คอลัมน์นี้มีค่าเดียว: {col_min}")
                    continue
                selected_range = st.slider(
                    f"ช่วงค่าของ {filter_col}",
                    min_value=col_min,
                    max_value=col_max,
                    value=(col_min, col_max),
                    key=f"filter_range_{i}",
                )
                filtered_df = dm.filter_by_range(
                    filtered_df, filter_col, selected_range[0], selected_range[1]
                )
            else:
                unique_vals = df[filter_col].dropna().unique().tolist()
                if len(unique_vals) <= 50:
                    selected_vals = st.multiselect(
                        f"เลือกค่าของ {filter_col}",
                        options=sorted(unique_vals, key=str),
                        key=f"filter_multiselect_{i}",
                    )
                    filtered_df = dm.filter_by_values(filtered_df, filter_col, selected_vals)
                else:
                    keyword = st.text_input(
                        f"ค้นหาคำในคอลัมน์ {filter_col}", key=f"filter_text_{i}"
                    )
                    filtered_df = dm.filter_by_text_search(filtered_df, filter_col, keyword)

    st.divider()
    st.subheader(f"ผลลัพธ์ ({len(filtered_df):,} แถว)")
    result_df = filtered_df[columns_to_show]
    st.dataframe(result_df, use_container_width=True, height=420)

    st.download_button(
        label="📥 ดาวน์โหลดผลลัพธ์นี้เป็น CSV",
        data=result_df.to_csv(index=False).encode("utf-8-sig"),
        file_name="filtered_result.csv",
        mime="text/csv",
    )

# ------------------------------------------------------------------------
# แท็บที่ 3: สรุปแบบจัดกลุ่ม เช่น "อารมณ์/ความพึงพอใจของพนักงานแต่ละแผนก"
# ------------------------------------------------------------------------
with tab_group:
    st.subheader("สรุปข้อมูลแบบจัดกลุ่ม (Group By)")
    st.caption(
        "เช่น ต้องการดูค่าเฉลี่ยความพึงพอใจ (อารมณ์) ของพนักงานแยกตามแผนก "
        "ให้เลือกคอลัมน์จัดกลุ่มเป็นแผนก และคอลัมน์ค่าเป็นคะแนนความพึงพอใจ"
    )

    if not text_cols or not numeric_cols:
        st.warning("ไฟล์นี้ต้องมีทั้งคอลัมน์ข้อความ (สำหรับจัดกลุ่ม) และคอลัมน์ตัวเลข (สำหรับสรุปผล)")
    else:
        col_g1, col_g2, col_g3 = st.columns(3)
        with col_g1:
            group_col = st.selectbox("จัดกลุ่มตามคอลัมน์", options=text_cols)
        with col_g2:
            value_col = st.selectbox("สรุปผลจากคอลัมน์ตัวเลข", options=numeric_cols)
        with col_g3:
            agg_func = st.selectbox(
                "วิธีสรุปผล",
                options=["mean", "sum", "count", "median"],
                format_func=lambda x: {
                    "mean": "ค่าเฉลี่ย",
                    "sum": "ผลรวม",
                    "count": "จำนวนนับ",
                    "median": "ค่ามัธยฐาน",
                }[x],
            )

        summary_series = dm.group_summary(df, group_col, value_col, agg_func)

        st.subheader(f"ผลสรุป: {value_col} ({agg_func}) แยกตาม {group_col}")
        st.dataframe(summary_series.rename(value_col), use_container_width=True)
        st.bar_chart(summary_series)
