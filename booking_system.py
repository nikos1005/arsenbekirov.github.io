#!/usr/bin/env python3
"""
🎤 ARSEN BEKIROV — BOOKING SYSTEM
Поиск площадок в Крыму и рассылка предложений о выступлениях
"""

import json, os
from pathlib import Path
from datetime import datetime

# =========== БАЗА ПЛОЩАДОК КРЫМА ===========

VENUES = [
    # --- ОТЕЛИ 5* ---
    {"name": "Mriya Resort & Spa", "city": "Ялта", "type": "отель 5*", "phone": "+7 3654 55-55-55", "site": "mriya-resort.ru", "capacity": 2000, "note": "Крупнейший отель Крыма. Концертный зал, свадьбы, корпоративы", "contacts": "sales@mriya-resort.ru"},
    {"name": "Riviera Sunrise Resort", "city": "Алушта", "type": "отель 5*", "phone": "+7 365 60 25-80", "site": "rivierasunrise.ru", "capacity": 1500, "note": "Конгресс-холл, летняя эстрада"},
    {"name": "Palmira Palace Resort", "city": "Ялта", "type": "отель 5*", "phone": "+7 3654 38-00-15", "site": "palmira-palace.com", "capacity": 800, "note": "Концерты, свадьбы, закрытые мероприятия"},
    {"name": "Villa Elena Hotel & Residences", "city": "Ялта", "type": "отель 5*", "phone": "+7 978 000 20 50", "site": "villa-elena.ru", "capacity": 400, "note": "Премиум-сегмент. Камерные концерты, гала-ужины"},
    {"name": "Крымский Бриз", "city": "Ялта", "type": "отель 4*", "phone": "+7 3654 38-00-50", "site": "crimean-breeze.ru", "capacity": 600, "note": "Удалённый от города, премиум-вечеринки"},
    
    # --- ОТЕЛИ 4* С КОНЦЕРТНЫМИ ЗАЛАМИ ---
    {"name": "Ялта-Интурист", "city": "Ялта", "type": "отель 4*", "phone": "+7 3654 20-65-01", "site": "yalta-intourist.ru", "capacity": 2000, "note": "Огромный зал. Крупные мероприятия, фестивали, свадьбы"},
    {"name": "Ореанда", "city": "Ялта", "type": "отель 4*", "phone": "+7 3654 32-31-31", "site": "hotel-oreanda.com", "capacity": 500, "note": "Центр Ялты. Конференц-зал для мероприятий"},
    {"name": "Бристоль", "city": "Ялта", "type": "отель 4*", "phone": "+7 3654 27-10-95", "site": "bristol-yalta.ru", "capacity": 300, "note": "Исторический отель. Камерные мероприятия"},
    {"name": "Ribera Resort & SPA", "city": "Евпатория", "type": "отель 4*", "phone": "+7 365 69 6-76-76", "site": "ribera-crimea.ru", "capacity": 800, "note": "Новый отель. SPA, бассейны, зал для мероприятий"},
    {"name": "Аквамарин Resort & SPA", "city": "Севастополь", "type": "отель 4*", "phone": "+7 8692 53-77-77", "site": "aquamarine.biz", "capacity": 600, "note": "Концерты на террасе с видом на море"},
    
    # --- РЕСТОРАНЫ И КЛУБЫ ---
    {"name": "Restaurant «Apelsin»", "city": "Ялта", "type": "ресторан", "phone": "+7 978 855 85 85", "site": "instagram.com/apelsin_crimea", "capacity": 200, "note": "Модное место. Живая музыка, гастроли артистов"},
    {"name": "Ресторан «Терраса»", "city": "Ялта", "type": "ресторан", "phone": "+7 3654 32-00-32", "site": "oreanda-hotel.ru", "capacity": 150, "note": "Веранда с видом на море. Живые выступления"},
    {"name": "Клуб «Малибу»", "city": "Ялта", "type": "ночной клуб", "phone": "+7 978 111 22 33", "site": "malibu-yalta.ru", "capacity": 500, "note": "Концерты, вечеринки, приглашённые артисты"},
    {"name": "Ресторан «Колизей»", "city": "Симферополь", "type": "ресторан", "phone": "+7 3652 77 77 77", "site": "", "capacity": 300, "note": "Банкетный зал, корпоративы, живая музыка"},
    
    # --- КОНЦЕРТНЫЕ ПЛОЩАДКИ ---
    {"name": "Ялтинский театр имени Чехова", "city": "Ялта", "type": "театр", "phone": "+7 3654 32-13-15", "site": "yalta-teatr.ru", "capacity": 600, "note": "Главная концертная площадка ЮБК"},
    {"name": "Крымская филармония", "city": "Симферополь", "type": "филармония", "phone": "+7 3652 27-35-14", "site": "krim-gf.ru", "capacity": 700, "note": "Симфонический зал. Сольные концерты с оркестром"},
    {"name": "Севастопольский центр культуры", "city": "Севастополь", "type": "концертный зал", "phone": "+7 8692 54-44-33", "site": "sevculture.ru", "capacity": 800, "note": "Крупные концерты, фестивали"},
    
    # --- СВАДЕБНЫЕ АГЕНТСТВА ---
    {"name": "Wedding Crimea", "city": "Крым", "type": "свадебное агентство", "phone": "+7 978 888 88 88", "site": "wedding-crimea.ru", "capacity": 0, "note": "Организация свадеб. Ищут артистов для пар"},
    {"name": "Крымская Свадьба", "city": "Симферополь", "type": "свадебное агентство", "phone": "+7 978 123 45 67", "site": "crim-wedding.ru", "capacity": 0, "note": "Топ-агентство Крыма"},
    {"name": "JAM Wedding", "city": "Ялта", "type": "свадебное агентство", "phone": "+7 978 777 77 77", "site": "jam-wedding.ru", "capacity": 0, "note": "Премиум-свадьбы на ЮБК"},
    
    # --- EVENT-АГЕНТСТВА ---
    {"name": "Event-Crimea", "city": "Симферополь", "type": "event-агентство", "phone": "+7 978 000 11 22", "site": "event-crimea.ru", "capacity": 0, "note": "Корпоративы, фестивали, городские мероприятия"},
    {"name": "Арт-Бомонд", "city": "Севастополь", "type": "event-агентство", "phone": "+7 8692 55 00 55", "site": "art-bomond.ru", "capacity": 0, "note": "Концерты, фестивали, гала-вечера"},
]

# =========== ШАБЛОН ПРЕДЛОЖЕНИЯ ===========

BOOKING_TEMPLATE = """Тема: Арсен Бекиров — выступление в {venue} ({city})

Здравствуйте!

Меня зовут Арсен Бекиров. Я заслуженный артист Крыма и Татарстана, лауреат премии QARADENIZ Production 2025.

Предлагаю живое выступление в {venue}. Пою на 6 языках: крымскотатарский, русский, английский, турецкий, итальянский, украинский. 

ФОРМАТ ВЫСТУПЛЕНИЯ:
• Сольный концерт (1,5 – 2 часа)
• Кавер-программа (мировые хиты + этно-поп)
• Выступление на мероприятии (свадьба, корпоратив, гала-ужин)
• Работа с живым оркестром

ПОРТФОЛИО:
Сайт: https://arsenbekirov.com
Instagram с видео: @mr.arsenbekirov
YouTube: @mr.arsenbekirov
Spotify: Arsen Bekirov («Qirim EP»)

ГОНОРАР ОБСУЖДАЕМ ИНДИВИДУАЛЬНО.
Готов обсудить даты и формат.

С уважением,
Арсен Бекиров
Заслуженный артист Крыма и Татарстана
arsen@arsenbekirov.com
+7 978 052 5045 (WhatsApp/Telegram)"""

def generate_booking_pitches():
    output_dir = Path.home() / 'Desktop' / 'booking_pitches'
    output_dir.mkdir(exist_ok=True)
    
    for v in VENUES:
        text = BOOKING_TEMPLATE.format(
            venue=v['name'],
            city=v['city'],
        )
        
        filename = f"{v['city']} - {v['name'].replace(' ', '_')[:50]}.txt"
        filepath = output_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(f"ПЛОЩАДКА: {v['name']}\n")
            f.write(f"ГОРОД: {v['city']}\n")
            f.write(f"ТИП: {v['type']}\n")
            f.write(f"ТЕЛЕФОН: {v['phone']}\n")
            f.write(f"САЙТ: {v['site']}\n")
            f.write(f"ВМЕСТИМОСТЬ: {v['capacity']} чел\n")
            f.write(f"ПРИМЕЧАНИЕ: {v['note']}\n")
            f.write("=" * 60 + "\n\n")
            f.write(text)
    
    print(f"✅ {len(VENUES)} предложений для площадок Крыма")
    print(f"📁 Сохранено в: {output_dir}")
    
    # Статистика по типам
    types = {}
    for v in VENUES:
        t = v['type']
        types[t] = types.get(t, 0) + 1
    
    print("\n📊 По типам площадок:")
    for t, count in types.items():
        print(f"  {t}: {count}")

if __name__ == '__main__':
    generate_booking_pitches()
