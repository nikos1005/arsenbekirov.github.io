#!/usr/bin/env python3
"""
🎬 ARSEN BEKIROV — YOUTUBE CONTENT FACTORY
Генерация видео-описаний, тамбнейлов, тайтлов и расписания
"""

import json, os, io
from pathlib import Path
from datetime import datetime, timedelta

# =========== КАТАЛОГ ВИДЕО ===========

COVERS = [
    {"title": "Lose Control", "artist": "Teddy Swims", "lang": "English", "file": "Lose control.mp3", "hook": "голос, который тебя удивит", "best_part": "припев, мощный вокал"},
    {"title": "Wind of Change", "artist": "Scorpions", "lang": "Crimean Tatar + English", "file": "wind of change.mp3", "hook": "легендарная песня по-крымскотатарски", "best_part": "первый куплет"},
    {"title": "Blinding Lights", "artist": "The Weeknd", "lang": "English", "file": "The Weeknd-Blinding Light.mp3", "hook": "кавер, который взорвал Instagram", "best_part": "припев"},
    {"title": "Portofino", "artist": "Andrea Bocelli", "lang": "Italian", "file": "Portofino Arsen.mp3", "hook": "итальянская классика в новом звучании", "best_part": "верхние ноты"},
    {"title": "Wave", "artist": "Fast Boy / Raf", "lang": "English", "file": "wave+.mp3", "hook": "танцевальный кавер", "best_part": "дроп"},
]

ORIGINALS = [
    {"title": "Maneler", "lang": "Crimean Tatar", "mood": "uptempo ethno-pop", "file": "02_Maneler.mp3"},
    {"title": "Seni Seven", "lang": "Crimean Tatar", "mood": "award-winning ballad", "file": "08_Seni_Seven.mp3"},
    {"title": "INAN", "lang": "Turkish", "mood": "emotional crossover", "file": "11_INAN.mp3"},
    {"title": "Sensin", "lang": "Turkish", "mood": "romantic", "file": "03_Sensin.mp3"},
]

SPECIALS = [
    {"title": "6 Languages in 60 Seconds", "type": "challenge", "hook": "полиглот-вокалист"},
    {"title": "My Voice Journey — 5 to 25 Years", "type": "story", "hook": "путь артиста"},
    {"title": "QIRIM EP — Behind the Scenes", "type": "behind", "hook": "как записывался альбом"},
    {"title": "Live with Orchestra — Best Moments", "type": "live", "hook": "симфонический оркестр"},
]

# =========== ГЕНЕРАЦИЯ ===========

def generate_title(video, vtype):
    if vtype == "cover":
        return f"{video['title']} — {video['artist']} (Cover by Arsen Bekirov)"
    elif vtype == "original":
        return f"Арсен Бекиров — {video['title']} (Official Audio)"
    elif vtype == "short":
        hook = video.get('hook', video.get('title', ''))
        return f"#Shorts {hook} 🎤"
    return video.get('title', '')

def generate_description(video, vtype):
    base = f"""🎤 Arsen Bekirov — {video.get('title', '')}

"""
    if vtype == "cover":
        base += f"""Оригинал: {video['artist']} — {video['title']}

🔔 Подпишись: https://youtube.com/@mr.arsenbekirov
📸 Instagram: @mr.arsenbekirov
🎵 Spotify: Arsen Bekirov

#кавер #вокал #cover #arsenbekirov #этнопоп"""
    elif vtype == "original":
        base += f"""Из EP «Qirim EP» (2025)

🔔 Подпишись: https://youtube.com/@mr.arsenbekirov
🎵 Слушать на Spotify: https://open.spotify.com/artist/0TUkZ5dvqD50Kzg7IsvgCk
📸 Instagram: @mr.arsenbekirov

#arsenbekirov #qirimep #этнопоп #крымскотатарскаямузыка"""
    elif vtype == "short":
        base += f"""🎤 Полная версия на канале!

Подпишись: @mr.arsenbekirov

#shorts #вокал #кавер"""

    return base

def generate_hashtags(video, vtype):
    if vtype == "cover":
        return "#кавер #вокал #cover #arsenbekirov #этнопоп"
    elif vtype == "original":
        return "#arsenbekirov #qirimep #этнопоп #worldmusic #крымскотатарскаямузыка"
    return "#shorts #вокал #music"

def generate_schedule(start_date=None):
    """Генерирует контент-план на 4 недели"""
    if not start_date:
        start_date = datetime.now() + timedelta(days=1)
    
    schedule = []
    day = start_date
    
    # Неделя 1: Каверы (запуск)
    week1 = [
        ("cover", COVERS[0], "short", "Lose Control — самый мощный момент"),
        ("cover", COVERS[0], "long", "Lose Control — полный кавер"),
        ("cover", COVERS[1], "short", "Wind of Change — легендарная песня"),
        ("cover", COVERS[2], "short", "Blinding Lights — припев"),
    ]
    
    # Неделя 2: Оригиналы + бэкстейдж
    week2 = [
        ("cover", COVERS[1], "long", "Wind of Change — полный кавер"),
        ("original", ORIGINALS[1], "long", "Seni Seven — трек, получивший премию"),
        ("special", SPECIALS[0], "short", "6 языков за 60 секунд"),
        ("cover", COVERS[3], "short", "Portofino — итальянская классика"),
    ]
    
    # Неделя 3: Авторская музыка
    week3 = [
        ("original", ORIGINALS[0], "long", "Maneler — главный трек EP"),
        ("cover", COVERS[4], "short", "Wave — танцевальный кавер"),
        ("special", SPECIALS[2], "short", "Как записывался Qirim EP"),
        ("original", ORIGINALS[2], "short", "INAN — эмоциональный трек"),
    ]
    
    # Неделя 4: Разное + Live
    week4 = [
        ("cover", COVERS[3], "long", "Portofino — полный кавер"),
        ("special", SPECIALS[3], "short", "Лучшие моменты с оркестром"),
        ("original", ORIGINALS[3], "long", "Sensin — новый трек"),
        ("special", SPECIALS[1], "short", "Мой путь в музыке"),
    ]
    
    all_weeks = week1 + week2 + week3 + week4
    
    for i, (vtype_name, video, format_type, comment) in enumerate(all_weeks):
        # Распределяем по дням: 3 видео в неделю
        video_day = day + timedelta(days=i * 2 + (0 if i % 2 == 0 else 1))
        
        if format_type == "long":
            pub_hour = "12:00"
            pub_day_name = video_day.strftime("%A")
        else:
            pub_hour = "18:00"
            pub_day_name = video_day.strftime("%A")
        
        entry = {
            "date": video_day.strftime("%Y-%m-%d"),
            "day": pub_day_name,
            "time": pub_hour,
            "type": format_type,
            "category": vtype_name,
            "title": generate_title(video, format_type if format_type == "short" else vtype_name),
            "description": generate_description(video, vtype_name),
            "hashtags": generate_hashtags(video, vtype_name),
            "hook": comment,
            "file": video.get("file", ""),
            "best_part": video.get("best_part", video.get("hook", "")),
        }
        schedule.append(entry)
    
    return schedule

def main():
    schedule = generate_schedule()
    
    print("🎬 YOUTUBE КОНТЕНТ-ПЛАН НА 4 НЕДЕЛИ")
    print("=" * 60)
    
    for i, v in enumerate(schedule, 1):
        print(f"\n--- Видео {i} ---")
        print(f"📅 {v['date']} ({v['day']}) в {v['time']}")
        print(f"🎬 {v['type'].upper()} | {v['category']}")
        print(f"📝 {v['title']}")
        print(f"💡 Hook: {v['hook']}")
        if v['file']:
            print(f"🎵 Файл: {v['file']}")
    
    # Сохраняем
    output = Path.home() / 'Desktop' / 'youtube_schedule.json'
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(schedule, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Сохранено: {output}")
    print(f"📊 Всего: {len(schedule)} видео на 4 недели")
    print(f"   Shorts: {sum(1 for v in schedule if v['type']=='short')}")
    print(f"   Long-form: {sum(1 for v in schedule if v['type']=='long')}")

if __name__ == '__main__':
    main()
