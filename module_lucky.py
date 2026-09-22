"""
module_lucky.py
=================
โมดูลสำหรับสุ่มของมงคลประจำวัน (Mock Data) โดยใช้โมดูล random ของ Python
ครอบคลุมสีเสื้อมงคล, สีกาลกิณี, เลขเด็ด, ทิศมงคล และเมนูอาหารเสริมดวง
"""

import random

# รายการสีทั้งหมดที่ใช้ร่วมกันระหว่างสีมงคลและสีกาลกิณี
_ALL_COLORS = [
    "แดง", "ส้ม", "เหลือง", "เขียว", "ฟ้า",
    "น้ำเงิน", "ม่วง", "ชมพู", "เทา", "ดำ", "ขาว", "น้ำตาล",
]


def get_lucky_color():
    """
    สุ่มสีเสื้อมงคลประจำวันจากลิสต์สีทั้งหมด

    Returns:
        str: ชื่อสีมงคลประจำวัน
    """
    return random.choice(_ALL_COLORS)


def get_unlucky_color(lucky_color=None):
    """
    สุ่มสีกาลกิณีประจำวัน โดยตรวจสอบให้แน่ใจว่าไม่ซ้ำกับสีมงคลที่สุ่มได้

    Args:
        lucky_color (str, optional): สีมงคลที่สุ่มได้แล้ว (จาก get_lucky_color)
            หากไม่ระบุ ฟังก์ชันจะสุ่มสีมงคลขึ้นมาเองเพื่อใช้เปรียบเทียบ

    Returns:
        str: ชื่อสีกาลกิณีประจำวัน ซึ่งรับประกันว่าไม่ซ้ำกับสีมงคล
    """
    if lucky_color is None:
        lucky_color = get_lucky_color()

    unlucky_candidates = [color for color in _ALL_COLORS if color != lucky_color]
    return random.choice(unlucky_candidates)


def get_lucky_numbers():
    """
    สุ่มเลขเด็ดประจำวัน ทั้งแบบ 2 ตัว (00-99) และ 3 ตัว (000-999)

    Returns:
        dict: ตัวอย่าง {"two_digit": "07", "three_digit": "142"}
    """
    two_digit = random.randint(0, 99)
    three_digit = random.randint(0, 999)

    return {
        "two_digit": f"{two_digit:02d}",
        "three_digit": f"{three_digit:03d}",
    }


def get_lucky_direction():
    """
    สุ่มทิศมงคลที่ควรหันหน้าไปทำงานหรือทำกิจกรรมสำคัญในวันนี้

    Returns:
        str: ชื่อทิศมงคลประจำวัน
    """
    directions = [
        "ทิศเหนือ", "ทิศใต้", "ทิศตะวันออก", "ทิศตะวันตก",
        "ทิศตะวันออกเฉียงเหนือ", "ทิศตะวันออกเฉียงใต้",
        "ทิศตะวันตกเฉียงเหนือ", "ทิศตะวันตกเฉียงใต้",
    ]
    return random.choice(directions)


def get_lucky_food():
    """
    สุ่มเมนูอาหารเสริมดวงประจำวันจากลิสต์เมนูง่ายๆ

    Returns:
        str: ชื่อเมนูอาหารเสริมดวงประจำวัน
    """
    foods = [
        "ข้าวผัดกุ้ง", "ต้มยำกุ้ง", "แกงเขียวหวานไก่", "ส้มตำไทย",
        "ผัดไทยกุ้งสด", "ข้าวมันไก่", "ก๋วยเตี๋ยวเรือ", "ยำวุ้นเส้น",
        "ข้าวหน้าปลาแซลมอน", "สุกี้น้ำ",
    ]
    return random.choice(foods)