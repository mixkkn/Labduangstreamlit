"""
module_tarot.py
=================
โมดูลสำหรับจำลองการเปิดไพ่ยิปซี (Major Arcana บางส่วน) โดยใช้โมดูล random
ครอบคลุมการสร้างสำรับไพ่, การสับไพ่, การจั่วไพ่แบบ 1 ใบ และ 3 ใบ
รวมถึงการจัดฟอร์แมตผลลัพธ์ให้พร้อมแสดงผลบนหน้าเว็บ
"""

import random


def create_deck():
    """
    สร้างสำรับไพ่ยิปซี (Major Arcana บางส่วน) อย่างน้อย 10 ใบ
    แต่ละใบเก็บข้อมูลเป็น dictionary ที่มี "name" และ "meaning"

    Returns:
        list[dict]: ลิสต์ของไพ่ เช่น
            [{"name": "The Fool", "meaning": "..."}, ...]
    """
    deck = [
        {"name": "The Fool", "meaning": "การเริ่มต้นใหม่ ความกล้าที่จะก้าวออกจากพื้นที่ปลอดภัย"},
        {"name": "The Magician", "meaning": "พลังในการสร้างสรรค์ ความมั่นใจที่จะลงมือทำ"},
        {"name": "The High Priestess", "meaning": "สัญชาตญาณและความลึกลับ ควรฟังเสียงภายในใจ"},
        {"name": "The Empress", "meaning": "ความอุดมสมบูรณ์ ความรักและการเติบโต"},
        {"name": "The Emperor", "meaning": "ความมั่นคง อำนาจ และการควบคุมสถานการณ์"},
        {"name": "The Lovers", "meaning": "ความสัมพันธ์และการตัดสินใจครั้งสำคัญ"},
        {"name": "The Chariot", "meaning": "ความมุ่งมั่นและชัยชนะที่ได้จากความพยายาม"},
        {"name": "Strength", "meaning": "ความกล้าหาญภายในและการควบคุมอารมณ์"},
        {"name": "The Wheel of Fortune", "meaning": "การเปลี่ยนแปลงของโชคชะตาที่ไม่คาดคิด"},
        {"name": "Justice", "meaning": "ความยุติธรรมและผลลัพธ์ที่สมดุลกับสิ่งที่ทำมา"},
        {"name": "The Hanged Man", "meaning": "การหยุดพักเพื่อมองสิ่งต่างๆ ในมุมใหม่"},
        {"name": "Death", "meaning": "การสิ้นสุดของบางสิ่งเพื่อเปิดทางให้สิ่งใหม่"},
        {"name": "The Star", "meaning": "ความหวังและแรงบันดาลใจหลังผ่านช่วงเวลายากลำบาก"},
        {"name": "The Sun", "meaning": "ความสุข ความสำเร็จ และพลังงานเชิงบวก"},
        {"name": "The World", "meaning": "ความสำเร็จที่สมบูรณ์และการปิดฉากบทหนึ่งอย่างสวยงาม"},
    ]
    return deck


def shuffle_deck(deck):
    """
    สับสำรับไพ่ที่ได้รับมาโดยใช้ random.shuffle (สับแบบสุ่มลำดับในลิสต์เดิม)

    Args:
        deck (list[dict]): สำรับไพ่ที่ต้องการสับ

    Returns:
        list[dict]: สำรับไพ่ที่ถูกสับเรียบร้อยแล้ว
    """
    shuffled = deck.copy()
    random.shuffle(shuffled)
    return shuffled


def draw_one_card(deck):
    """
    จั่วไพ่ 1 ใบจากสำรับ เหมาะสำหรับคำถามแบบรวดเร็ว (Quick Question)

    Args:
        deck (list[dict]): สำรับไพ่ (ควรสับมาก่อนแล้ว)

    Returns:
        dict: ไพ่ 1 ใบที่จั่วได้ หรือ None ถ้าสำรับว่างเปล่า
    """
    if not deck:
        return None
    return random.choice(deck)


def draw_three_cards(deck):
    """
    จั่วไพ่ 3 ใบจากสำรับ สำหรับดูภาพรวม อดีต-ปัจจุบัน-อนาคต
    ไพ่ที่จั่วได้จะไม่ซ้ำกัน (ใช้ random.sample)

    Args:
        deck (list[dict]): สำรับไพ่ (ควรสับมาก่อนแล้ว)

    Returns:
        list[dict]: ลิสต์ไพ่ 3 ใบ เรียงตามลำดับ [อดีต, ปัจจุบัน, อนาคต]
                    หรือลิสต์ว่างถ้าสำรับมีไพ่ไม่ถึง 3 ใบ
    """
    if len(deck) < 3:
        return []
    return random.sample(deck, 3)


def format_tarot_reading(cards):
    """
    จัดฟอร์แมตไพ่ที่จั่วได้ให้เป็นข้อความ (string) ที่อ่านง่าย
    รองรับทั้งกรณีไพ่ใบเดียว (dict) และไพ่หลายใบ (list of dict)
    หากมีไพ่ 3 ใบ จะติดป้ายกำกับเป็น อดีต/ปัจจุบัน/อนาคต ให้อัตโนมัติ

    Args:
        cards (dict | list[dict]): ไพ่ 1 ใบ (dict) หรือไพ่หลายใบ (list of dict)

    Returns:
        str: ข้อความผลการเปิดไพ่ที่จัดรูปแบบพร้อมแสดงผล
    """
    if not cards:
        return "ไม่มีไพ่ให้แสดงผล"

    # กรณีไพ่ใบเดียว (dict)
    if isinstance(cards, dict):
        return f"🃏 ไพ่ที่จั่วได้: {cards['name']}\nความหมาย: {cards['meaning']}"

    # กรณีไพ่หลายใบ (list of dict)
    labels_3card = ["อดีต", "ปัจจุบัน", "อนาคต"]
    lines = []

    if len(cards) == 3:
        for label, card in zip(labels_3card, cards):
            lines.append(f"🃏 {label}: {card['name']}\n   ความหมาย: {card['meaning']}")
    else:
        for idx, card in enumerate(cards, start=1):
            lines.append(f"🃏 ใบที่ {idx}: {card['name']}\n   ความหมาย: {card['meaning']}")

    return "\n\n".join(lines)