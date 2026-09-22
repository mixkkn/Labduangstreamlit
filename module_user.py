"""
module_user.py
================
โมดูลสำหรับจัดการข้อมูลผู้ใช้ในเว็บแอปดูดวง
ประกอบด้วยฟังก์ชันเกี่ยวกับราศี, ธาตุประจำตัว, เลขศาสตร์จากชื่อ
และการตรวจสอบความถูกต้องของข้อมูลนำเข้า (ลอจิกทั้งหมดจำลองขึ้นเอง ไม่พึ่ง API ภายนอก)
"""


def get_zodiac(month):
    """
    รับค่าเดือนเกิด (1-12) แล้วคืนค่าชื่อราศีที่สอดคล้องกัน
    ใช้เงื่อนไข if-elif ธรรมดาแบบง่าย โดยอิงจากเดือนเกิด (ไม่ใช้วันที่ละเอียด)

    Args:
        month (int): เดือนเกิด (1 = มกราคม ... 12 = ธันวาคม)

    Returns:
        str: ชื่อราศี หรือ "ไม่ทราบ" ถ้าเดือนไม่ถูกต้อง
    """
    if month == 1:
        return "มังกร"
    elif month == 2:
        return "กุมภ์"
    elif month == 3:
        return "มีน"
    elif month == 4:
        return "เมษ"
    elif month == 5:
        return "พฤษภ"
    elif month == 6:
        return "เมถุน"
    elif month == 7:
        return "กรกฎ"
    elif month == 8:
        return "สิงห์"
    elif month == 9:
        return "กันย์"
    elif month == 10:
        return "ตุลย์"
    elif month == 11:
        return "พิจิก"
    elif month == 12:
        return "ธนู"
    else:
        return "ไม่ทราบ"


def get_element(zodiac):
    """
    รับชื่อราศี แล้วคืนค่าธาตุประจำตัว (ดิน, น้ำ, ลม, ไฟ)
    เป็นการจับกลุ่มราศีตามความเชื่อโหราศาสตร์ทั่วไป

    Args:
        zodiac (str): ชื่อราศี เช่น "เมษ", "พฤษภ" เป็นต้น

    Returns:
        str: ชื่อธาตุ ("ไฟ", "ดิน", "ลม", "น้ำ") หรือ "ไม่ทราบ" ถ้าไม่พบราศีนี้
    """
    fire_signs = ["เมษ", "สิงห์", "ธนู"]
    earth_signs = ["พฤษภ", "กันย์", "มังกร"]
    air_signs = ["เมถุน", "ตุลย์", "กุมภ์"]
    water_signs = ["กรกฎ", "พิจิก", "มีน"]

    if zodiac in fire_signs:
        return "ไฟ"
    elif zodiac in earth_signs:
        return "ดิน"
    elif zodiac in air_signs:
        return "ลม"
    elif zodiac in water_signs:
        return "น้ำ"
    else:
        return "ไม่ทราบ"


def calculate_name_number(name):
    """
    คำนวณ "เลขศาสตร์" จากชื่อภาษาอังกฤษ โดยแปลงตัวอักษรแต่ละตัวเป็นตัวเลข
    (a=1, b=2, ..., z=26) นำมาบวกกันทั้งหมด แล้วบวกเลขซ้ำไปเรื่อยๆ
    จนเหลือเลขหลักเดียว (1-9)

    Args:
        name (str): ชื่อภาษาอังกฤษ (ไม่สนตัวพิมพ์เล็ก/ใหญ่ ตัดอักขระอื่นทิ้ง)

    Returns:
        int: เลขศาสตร์ผลลัพธ์ (1-9) หรือ 0 ถ้าไม่มีตัวอักษรที่คำนวณได้เลย
    """
    name = name.lower()
    total = 0
    for ch in name:
        if ch.isalpha() and ch.isascii():
            total += ord(ch) - ord('a') + 1

    if total == 0:
        return 0

    while total > 9:
        total = sum(int(digit) for digit in str(total))

    return total


def get_numerology_meaning(number):
    """
    รับตัวเลขศาสตร์ (1-9) ที่ได้จาก calculate_name_number แล้วคืนค่า
    ความหมายสั้นๆ ที่สื่อถึงบุคลิกหรือลักษณะนิสัยของเลขนั้น

    Args:
        number (int): เลขศาสตร์ (1-9)

    Returns:
        str: คำอธิบายความหมายของเลขนั้นๆ หรือข้อความแจ้งว่าไม่พบข้อมูล
    """
    meanings = {
        1: "ผู้นำ มีความมั่นใจในตัวเอง ชอบความเป็นอิสระ",
        2: "อ่อนโยน ประนีประนอม เก่งเรื่องความสัมพันธ์",
        3: "ร่าเริง มีความคิดสร้างสรรค์ ชอบการแสดงออก",
        4: "มั่นคง ขยัน รอบคอบ ทำงานเป็นระบบ",
        5: "รักอิสระ ชอบการผจญภัยและการเปลี่ยนแปลง",
        6: "รักความสมดุล ใส่ใจครอบครัวและคนรอบข้าง",
        7: "ชอบคิดวิเคราะห์ รักความสงบ สนใจเรื่องลึกซึ้ง",
        8: "มีความทะเยอทะยาน เก่งเรื่องธุรกิจและการเงิน",
        9: "ใจบุญ เห็นอกเห็นใจผู้อื่น มีอุดมคติสูง",
    }
    return meanings.get(number, "ไม่พบความหมายสำหรับตัวเลขนี้")


def validate_input(name, birth_month):
    """
    ตรวจสอบความถูกต้องของข้อมูลที่ผู้ใช้กรอก ได้แก่ ชื่อและเดือนเกิด
    ว่ากรอกครบถ้วนและอยู่ในรูปแบบที่ถูกต้องหรือไม่

    Args:
        name (str): ชื่อที่ผู้ใช้กรอก
        birth_month: เดือนเกิดที่ผู้ใช้กรอก (คาดว่าเป็น int หรือ str ตัวเลข)

    Returns:
        tuple: (is_valid: bool, message: str)
            - is_valid: True ถ้าข้อมูลถูกต้องครบถ้วน, False ถ้าไม่ถูกต้อง
            - message: ข้อความแจ้งเตือน หรือข้อความยืนยันว่าข้อมูลถูกต้อง
    """
    if not name or not str(name).strip():
        return False, "กรุณากรอกชื่อของคุณ"

    if not any(ch.isalpha() for ch in str(name)):
        return False, "ชื่อต้องมีตัวอักษรอย่างน้อยหนึ่งตัว"

    if birth_month is None or str(birth_month).strip() == "":
        return False, "กรุณาเลือกเดือนเกิดของคุณ"

    try:
        month_int = int(birth_month)
    except (ValueError, TypeError):
        return False, "เดือนเกิดต้องเป็นตัวเลข"

    if month_int < 1 or month_int > 12:
        return False, "เดือนเกิดต้องอยู่ระหว่าง 1 ถึง 12"

    return True, "ข้อมูลถูกต้องครบถ้วน"