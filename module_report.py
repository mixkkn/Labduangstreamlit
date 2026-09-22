"""
module_report.py
==================
โมดูลสำหรับจัดการข้อความและสรุปผลรวมของการดูดวง
รวมข้อมูลจากโมดูล user, horoscope, tarot, lucky เข้าด้วยกัน
จัดฟอร์แมตข้อความสำหรับดาวน์โหลด คำนวณเปอร์เซ็นต์ความโชคดี
สุ่มคำคมให้กำลังใจ และกรองข้อความนำเข้าจากผู้ใช้เบื้องต้น
(ไม่มีโค้ดของ Streamlit หรือ UI ปะปนอยู่ในไฟล์นี้)
"""

import random
import re


def generate_full_report(user_dict, horoscope_dict, tarot_dict, lucky_dict):
    """
    รวมข้อมูลจากทั้ง 4 โมดูล (user, horoscope, tarot, lucky) เข้าเป็น
    dictionary ก้อนใหญ่ก้อนเดียว เพื่อให้ง่ายต่อการส่งต่อไปแสดงผลบนหน้าเว็บ

    Args:
        user_dict (dict): ข้อมูลผู้ใช้ เช่น ชื่อ, ราศี, ธาตุ, เลขศาสตร์
        horoscope_dict (dict): ข้อมูลคำทำนายรายวัน เช่น คะแนน, งาน, การเงิน, ความรัก
        tarot_dict (dict): ข้อมูลผลไพ่ยิปซีที่จั่วได้
        lucky_dict (dict): ข้อมูลของมงคลประจำวัน เช่น สี, เลขเด็ด, ทิศ, อาหาร

    Returns:
        dict: รายงานฉบับเต็มในรูปแบบ dictionary เดียว มีโครงสร้างดังนี้
            {
                "user": user_dict,
                "horoscope": horoscope_dict,
                "tarot": tarot_dict,
                "lucky": lucky_dict,
            }
    """
    return {
        "user": user_dict or {},
        "horoscope": horoscope_dict or {},
        "tarot": tarot_dict or {},
        "lucky": lucky_dict or {},
    }


def format_text_for_download(report_dict):
    """
    จัดฟอร์แมต dictionary รายงานฉบับเต็ม (จาก generate_full_report) ให้เป็น
    ข้อความ (string) ที่อ่านง่าย มีการเว้นบรรทัดและสัญลักษณ์ตกแต่ง
    พร้อมสำหรับบันทึกเป็นไฟล์ .txt

    Args:
        report_dict (dict): รายงานฉบับเต็มที่ได้จาก generate_full_report

    Returns:
        str: ข้อความรายงานฉบับสมบูรณ์ พร้อมบันทึกเป็นไฟล์ .txt
    """
    user = report_dict.get("user", {})
    horoscope = report_dict.get("horoscope", {})
    tarot = report_dict.get("tarot", {})
    lucky = report_dict.get("lucky", {})

    lines = []
    lines.append("=" * 40)
    lines.append("      รายงานดวงประจำวันของคุณ")
    lines.append("=" * 40)
    lines.append("")

    if user:
        lines.append("👤 ข้อมูลส่วนตัว")
        lines.append("-" * 40)
        for key, value in user.items():
            lines.append(f"  • {key}: {value}")
        lines.append("")

    if horoscope:
        lines.append("🔮 คำทำนายรายวัน")
        lines.append("-" * 40)
        for key, value in horoscope.items():
            lines.append(f"  • {key}: {value}")
        lines.append("")

    if tarot:
        lines.append("🃏 ผลไพ่ยิปซี")
        lines.append("-" * 40)
        for key, value in tarot.items():
            lines.append(f"  • {key}: {value}")
        lines.append("")

    if lucky:
        lines.append("🍀 ของมงคลประจำวัน")
        lines.append("-" * 40)
        for key, value in lucky.items():
            lines.append(f"  • {key}: {value}")
        lines.append("")

    lines.append("=" * 40)
    lines.append("ขอให้เป็นวันที่ดีนะครับ/คะ ✨")
    lines.append("=" * 40)

    return "\n".join(lines)


def calculate_overall_percentage(score1, score2, max_score=10):
    """
    คำนวณเปอร์เซ็นต์ความโชคดีรวม จากคะแนนหลายส่วน (เช่น คะแนนดวงรายวัน
    และคะแนนจากไพ่ยิปซี) เพื่อนำไปใช้แสดงผลเป็นแถบพลังงาน (Progress bar)

    Args:
        score1 (float): คะแนนส่วนที่ 1 (เช่น คะแนนดวงประจำวัน)
        score2 (float): คะแนนส่วนที่ 2 (เช่น คะแนนที่แปลงมาจากไพ่ยิปซี)
        max_score (float, optional): คะแนนเต็มของแต่ละส่วน ค่าเริ่มต้นคือ 10

    Returns:
        float: เปอร์เซ็นต์ความโชคดีรวม อยู่ในช่วง 0-100
               (ถ้าข้อมูลนำเข้าไม่ถูกต้องจะคืนค่า 0.0)
    """
    try:
        score1 = float(score1)
        score2 = float(score2)
        max_score = float(max_score)
    except (ValueError, TypeError):
        return 0.0

    if max_score <= 0:
        return 0.0

    average_score = (score1 + score2) / 2
    percentage = (average_score / max_score) * 100

    # ป้องกันค่าหลุดขอบเขต 0-100
    percentage = max(0.0, min(100.0, percentage))

    return round(percentage, 2)


def get_daily_quote():
    """
    สุ่มคำคมให้กำลังใจประจำวัน จากลิสต์คำคมที่เตรียมไว้

    Returns:
        str: คำคมให้กำลังใจประจำวัน 1 ประโยค
    """
    quotes = [
        "ทุกวันคือโอกาสใหม่ที่จะเริ่มต้นสิ่งดีๆ ให้กับตัวเอง",
        "โชคชะตาช่วยคนที่ไม่หยุดพยายามเสมอ",
        "ความมืดมิดที่สุดของคืน คือช่วงเวลาก่อนที่แสงอรุณจะมาถึง",
        "เชื่อในตัวเอง แล้วทุกอย่างจะค่อยๆ ดีขึ้น",
        "แม้วันนี้จะไม่ง่าย แต่พรุ่งนี้อาจเป็นวันที่ดีที่สุดของคุณ",
    ]
    return random.choice(quotes)


def clean_user_input(text):
    """
    กรองข้อความนำเข้าจากผู้ใช้เบื้องต้น เช่น ช่องกรอกชื่อ
    โดยตัดอักขระพิเศษที่ไม่จำเป็นออก (คงไว้เฉพาะตัวอักษร ตัวเลข
    เว้นวรรค และอักขระภาษาไทย) พร้อมตัดช่องว่างส่วนเกินหัวท้าย

    Args:
        text (str): ข้อความดิบที่ผู้ใช้กรอกเข้ามา

    Returns:
        str: ข้อความที่ผ่านการกรองแล้ว หรือสตริงว่างถ้านำเข้าไม่ใช่ string
    """
    if not isinstance(text, str):
        return ""

    # เก็บเฉพาะตัวอักษรไทย, อังกฤษ, ตัวเลข, และเว้นวรรค
    cleaned = re.sub(r"[^ก-๙a-zA-Z0-9\s]", "", text)

    # ตัดช่องว่างซ้ำๆ ให้เหลือช่องว่างเดียว และตัดช่องว่างหัวท้าย
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned