"""
module_data_manager.py
=========================
โมดูลสำหรับจัดการไฟล์ข้อมูล .txt ที่ผู้ใช้อัปโหลด (อัปโหลด / ลบ / อ่านไฟล์)
และแปลงไฟล์ .txt ที่มีโครงสร้างแบบตาราง (คั่นด้วย tab, comma หรือช่องว่าง
หลายตัวที่มีความยาวคงที่) ให้อยู่ในรูปแบบ pandas DataFrame เพื่อนำไปกรอง
และแสดงผลบนแดชบอร์ด

หมายเหตุสำคัญ: โมดูลนี้เป็นเครื่องมือ "ทั่วไป" ไม่ได้ผูกติดกับโครงสร้าง
ข้อมูลเฉพาะเจาะจง (เช่น ข้อมูลพนักงาน/HR) จึงสามารถใช้กับไฟล์ .txt แบบตาราง
อื่น ๆ ได้เช่นกัน ตราบใดที่ไฟล์มีแถวหัวตาราง (header) อยู่บรรทัดแรก
และมีตัวคั่นคอลัมน์ที่สม่ำเสมอตลอดทั้งไฟล์

ไฟล์นี้ไม่มีโค้ดของ Streamlit หรือ UI ปะปนอยู่ (เป็นลอจิกล้วน ๆ)
"""

import os
import re
import pandas as pd

# โฟลเดอร์สำหรับเก็บไฟล์ .txt ที่ผู้ใช้อัปโหลด (จะถูกสร้างขึ้นอัตโนมัติถ้ายังไม่มี)
UPLOAD_DIR = "uploaded_txt_data"


# ----------------------------------------------------------------------------
# ส่วนจัดการไฟล์: อัปโหลด / แสดงรายการ / ลบ
# ----------------------------------------------------------------------------
def ensure_upload_dir():
    """สร้างโฟลเดอร์เก็บไฟล์อัปโหลด ถ้ายังไม่มีอยู่"""
    os.makedirs(UPLOAD_DIR, exist_ok=True)


def list_uploaded_files():
    """
    คืนรายชื่อไฟล์ .txt ทั้งหมดที่อยู่ในโฟลเดอร์อัปโหลด เรียงตามชื่อ

    Returns:
        list[str]: รายชื่อไฟล์ (เฉพาะนามสกุล .txt)
    """
    ensure_upload_dir()
    files = [f for f in os.listdir(UPLOAD_DIR) if f.lower().endswith(".txt")]
    return sorted(files)


def save_uploaded_file(filename, file_bytes):
    """
    บันทึกไฟล์ที่ผู้ใช้อัปโหลดลงในโฟลเดอร์อัปโหลด
    ถ้ามีชื่อไฟล์ซ้ำกับไฟล์ที่มีอยู่แล้ว จะต่อท้ายด้วยตัวเลขให้อัตโนมัติ
    เพื่อไม่ให้ไปทับไฟล์เดิมโดยไม่ตั้งใจ

    Args:
        filename (str): ชื่อไฟล์ต้นฉบับที่ผู้ใช้อัปโหลด
        file_bytes (bytes): เนื้อหาไฟล์ในรูปแบบ bytes

    Returns:
        str: ชื่อไฟล์จริงที่ถูกบันทึกไว้บนดิสก์
    """
    ensure_upload_dir()
    safe_name = os.path.basename(filename)
    if not safe_name.lower().endswith(".txt"):
        safe_name += ".txt"

    base, ext = os.path.splitext(safe_name)
    target_path = os.path.join(UPLOAD_DIR, safe_name)

    counter = 1
    while os.path.exists(target_path):
        safe_name = f"{base}_{counter}{ext}"
        target_path = os.path.join(UPLOAD_DIR, safe_name)
        counter += 1

    with open(target_path, "wb") as f:
        f.write(file_bytes)

    return safe_name


def delete_uploaded_file(filename):
    """
    ลบไฟล์ที่ระบุออกจากโฟลเดอร์อัปโหลด

    Args:
        filename (str): ชื่อไฟล์ที่ต้องการลบ

    Returns:
        bool: True ถ้าลบสำเร็จ, False ถ้าไม่พบไฟล์
    """
    ensure_upload_dir()
    target_path = os.path.join(UPLOAD_DIR, os.path.basename(filename))
    if os.path.exists(target_path):
        os.remove(target_path)
        return True
    return False


def get_file_path(filename):
    """คืน path เต็มของไฟล์ที่อยู่ในโฟลเดอร์อัปโหลด"""
    return os.path.join(UPLOAD_DIR, os.path.basename(filename))


# ----------------------------------------------------------------------------
# ส่วนแปลงไฟล์ .txt ให้เป็นตาราง (DataFrame)
# ----------------------------------------------------------------------------
def _detect_delimiter(header_line):
    """
    ตรวจจับตัวคั่นคอลัมน์จากบรรทัดหัวตาราง โดยเรียงลำดับความสำคัญดังนี้
    1. แท็บ (\\t)
    2. ช่องว่างหลายตัวติดกัน โดยนับความยาวชุดช่องว่างที่พบบ่อยที่สุด
       (ไฟล์ตารางหลายชนิดมักคั่นคอลัมน์ด้วยช่องว่างจำนวนคงที่ เช่น 8 ตัว)
    3. เครื่องหมายจุลภาค (,)
    4. เซมิโคลอน (;)

    Returns:
        str หรือ None: ตัวคั่นที่ตรวจพบ (None หมายถึงให้ fallback ไปแยกด้วย
        ช่องว่างเดี่ยวแบบทั่วไป)
    """
    if "\t" in header_line:
        return "\t"

    space_runs = re.findall(r" {2,}", header_line)
    if space_runs:
        lengths = [len(run) for run in space_runs]
        most_common_length = max(set(lengths), key=lengths.count)
        return " " * most_common_length

    if "," in header_line:
        return ","

    if ";" in header_line:
        return ";"

    return None


def load_txt_as_dataframe(filepath):
    """
    อ่านไฟล์ .txt ที่มีโครงสร้างแบบตาราง แล้วแปลงเป็น pandas DataFrame
    โดยตรวจจับตัวคั่นคอลัมน์ให้อัตโนมัติ และพยายามแปลงคอลัมน์ที่เป็นตัวเลข
    ให้อยู่ในชนิดข้อมูลตัวเลขจริง (ถ้าแปลงไม่ได้จะคงเป็นข้อความไว้เหมือนเดิม)

    Args:
        filepath (str): พาธของไฟล์ .txt ที่ต้องการอ่าน

    Returns:
        pandas.DataFrame หรือ None ถ้าไฟล์ว่างเปล่า หรืออ่านแล้วไม่ได้ข้อมูล
    """
    with open(filepath, "rb") as f:
        raw_bytes = f.read()

    try:
        text = raw_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw_bytes.decode("utf-8", errors="ignore")

    lines = [line for line in text.splitlines() if line.strip() != ""]
    if not lines:
        return None

    delimiter = _detect_delimiter(lines[0])

    def split_line(line):
        parts = line.split(delimiter) if delimiter else line.split()
        # ตัดช่องว่างหัวท้าย และเครื่องหมายคำพูดครอบที่อาจติดมากับค่า (เช่น "Somchai")
        return [p.strip().strip('"') for p in parts]

    header = split_line(lines[0])
    data_rows = [split_line(line) for line in lines[1:]]

    # เก็บเฉพาะแถวที่จำนวนคอลัมน์ตรงกับหัวตาราง เพื่อป้องกันข้อมูลเพี้ยนจาก
    # แถวที่ผิดรูปแบบ (เช่น บรรทัดว่างแปลก ๆ หรือบรรทัดที่ตัดขาด)
    n_cols = len(header)
    data_rows = [row for row in data_rows if len(row) == n_cols]

    if not data_rows:
        return None

    df = pd.DataFrame(data_rows, columns=header)

    # พยายามแปลงแต่ละคอลัมน์เป็นตัวเลข หากส่วนใหญ่ของค่าในคอลัมน์นั้นแปลงได้
    for col in df.columns:
        converted = pd.to_numeric(df[col], errors="coerce")
        if len(df) > 0 and converted.notna().sum() >= 0.8 * len(df):
            df[col] = converted

    return df


def get_column_categories(df):
    """
    แบ่งคอลัมน์ในตารางออกเป็น 2 กลุ่ม เพื่อให้เลือกวิธีกรอง/แสดงผลได้เหมาะสม

    Returns:
        tuple(list, list): (numeric_columns, text_columns)
    """
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    text_cols = [c for c in df.columns if c not in numeric_cols]
    return numeric_cols, text_cols


# ----------------------------------------------------------------------------
# ส่วนกรองข้อมูล
# ----------------------------------------------------------------------------
def filter_by_values(df, column, selected_values):
    """กรองแถวที่คอลัมน์ที่ระบุมีค่าตรงกับค่าที่เลือกไว้ (ใช้กับคอลัมน์ข้อความ)"""
    if not selected_values:
        return df
    return df[df[column].isin(selected_values)]


def filter_by_text_search(df, column, keyword):
    """กรองแถวด้วยการค้นหาคำที่ปรากฏในคอลัมน์ข้อความ (ไม่สนตัวพิมพ์เล็ก/ใหญ่)"""
    if not keyword:
        return df
    return df[df[column].astype(str).str.contains(keyword, case=False, na=False)]


def filter_by_range(df, column, min_value, max_value):
    """กรองแถวด้วยช่วงค่าตัวเลข (ใช้กับคอลัมน์ตัวเลข)"""
    return df[(df[column] >= min_value) & (df[column] <= max_value)]


def group_summary(df, group_col, value_col, agg="mean"):
    """
    สรุปข้อมูลแบบจัดกลุ่ม (Group By) เช่น หาค่าเฉลี่ยความพึงพอใจ/อารมณ์ของ
    พนักงาน แยกตามแผนก

    Args:
        df (pandas.DataFrame): ตารางข้อมูลต้นทาง
        group_col (str): คอลัมน์ที่จะใช้จัดกลุ่ม เช่น "Department"
        value_col (str): คอลัมน์ตัวเลขที่จะนำมาสรุปผล เช่น "EmpSatisfaction"
        agg (str): ฟังก์ชันสรุปผล ("mean", "sum", "count", "median")

    Returns:
        pandas.Series: index คือแต่ละกลุ่ม, ค่าคือผลสรุปตามฟังก์ชันที่เลือก
    """
    grouped = df.groupby(group_col)[value_col]

    if agg == "sum":
        result = grouped.sum()
    elif agg == "count":
        result = grouped.count()
    elif agg == "median":
        result = grouped.median()
    else:
        result = grouped.mean()

    return result.sort_values(ascending=False)
