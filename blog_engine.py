#!/usr/bin/env python3
"""
ARSEN BEKIROV — CONTENT ENGINE
Генерирует SEO-статьи для блога на arsenbekirov.com
Каждая статья = трафик = заказы выступлений + стримы
"""

import json
from pathlib import Path
from datetime import datetime

ARTICLES = [
    {
        "slug": "crimean-tatar-music-modern-sound",
        "title_en": "How Crimean Tatar Folk Music Is Finding a Modern Sound — Meet Arsen Bekirov",
        "title_ru": "Как крымскотатарская народная музыка обретает современное звучание — Арсен Бекиров",
        "tags": "crimean tatar music, ethno pop, world music, qirim ep, traditional folk modern",
        "desc": "Discover how Arsen Bekirov blends 500-year-old Crimean Tatar folk traditions with contemporary pop and electronic production in his debut EP 'Qirim EP'."
    },
    {
        "slug": "singing-in-six-languages",
        "title_en": "Singing in 6 Languages: The Story of Crimean Tatar Tenor Arsen Bekirov",
        "title_ru": "Пение на 6 языках: История крымскотатарского тенора Арсена Бекирова",
        "tags": "multilingual singer, crimean tatar tenor, vocalist, languages, polyglot musician",
        "desc": "From Crimean Tatar to Turkish, Russian to English, Arabic to French — Arsen Bekirov performs in six languages, bridging cultures through music."
    },
    {
        "slug": "qirim-ep-behind-the-scenes",
        "title_en": "Behind the Scenes of 'Qirim EP' — Recording Ethno-Pop in Crimea",
        "title_ru": "За кулисами 'Qirim EP' — запись этно-попа в Крыму",
        "tags": "qirim ep, music production, recording studio, crimean music, album making",
        "desc": "How Arsen Bekirov recorded his debut EP blending Crimean Tatar folk instruments with modern production. A behind-the-scenes look at the QARADENIZ award-winning album."
    },
    {
        "slug": "qaradeniz-award-2025",
        "title_en": "QARADENIZ Production 2025 Winner — Arsen Bekirov's Journey to Recognition",
        "title_ru": "Лауреат QARADENIZ Production 2025 — путь Арсена Бекирова к признанию",
        "tags": "qaradeniz award, music award, crimean artist, honored artist, music competition",
        "desc": "Arsen Bekirov's music video 'Seni Seven' won the prestigious QARADENIZ Production 2025 award. Read about his journey from Crimea to international recognition."
    },
    {
        "slug": "cover-songs-reimagined",
        "title_en": "World Hits Reimagined: Teddy Swims to Scorpions — Covers by Arsen Bekirov",
        "title_ru": "Мировые хиты в новом звучании: от Teddy Swims до Scorpions — каверы Арсена Бекирова",
        "tags": "cover songs, teddy swims cover, scorpions cover, bocelli cover, vocal covers",
        "desc": "Listen to Arsen Bekirov's unique covers of Lose Control, Wind of Change, Portofino, and Blinding Lights — each reimagined with Crimean Tatar musical sensibility."
    },
    {
        "slug": "hire-vocalist-crimea",
        "title_en": "Hire a Professional Vocalist in Crimea — Arsen Bekirov for Your Event",
        "title_ru": "Заказать профессионального вокалиста в Крыму — Арсен Бекиров для вашего мероприятия",
        "tags": "hire vocalist crimea, wedding singer, corporate event, live performance, booking",
        "desc": "Honored Artist of Crimea and Tatarstan, Arsen Bekirov, is available for weddings, corporate events, private parties, and concerts. 6 languages, professional sound."
    },
]

def generate_blog():
    output_dir = Path.home() / "Desktop" / "blog_articles"
    output_dir.mkdir(exist_ok=True)
    
    for article in ARTICLES:
        slug = article["slug"]
        filepath = output_dir / f"{slug}.md"
        
        content = f"""---
title: "{article['title_en']}"
title_ru: "{article['title_ru']}"
description: "{article['desc']}"
tags: [{article['tags']}]
date: {datetime.now().strftime('%Y-%m-%d')}
slug: {slug}
---

# {article['title_en']}

{article['desc']}

---

*Article content ready for publication. Add 500-800 words of engaging content here.*

## About Arsen Bekirov

Arsen Bekirov is a Crimean Tatar tenor and ethno-pop artist, Honored Artist of the Republic of Crimea and the Republic of Tatarstan. Winner of QARADENIZ Production 2025. Debut EP "Qirim EP" out now.

**Listen:** [Spotify](https://open.spotify.com/artist/09qk3MsxjyxpWXhpCm7CXB) | [Website](https://arsenbekirov.com) | [Instagram](https://instagram.com/mr.arsenbekirov)

**Book:** [WhatsApp](https://wa.me/79780525045) | [Telegram](https://t.me/NikosKworkAssistantBot)

---
*© {datetime.now().year} Arsen Bekirov. All rights reserved.*
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {slug}")
    
    # Создаём index.html для блога
    index_path = output_dir / "index.html"
    
    articles_html = ""
    for a in ARTICLES:
        articles_html += f"""
    <article class="blog-card">
      <h2><a href="/blog/{a['slug']}.html">{a['title_en']}</a></h2>
      <p class="blog-desc">{a['desc']}</p>
      <div class="blog-meta">
        <span class="blog-tags">{', '.join(a['tags'].split(', ')[:3])}</span>
        <span class="blog-date">{datetime.now().strftime('%B %d, %Y')}</span>
      </div>
    </article>"""
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Blog — Arsen Bekirov | Crimean Tatar Tenor & Ethno-Pop Artist</title>
  <meta name="description" content="Official blog of Arsen Bekirov — articles about Crimean Tatar music, vocal performance, world music, and behind-the-scenes stories.">
  <link rel="canonical" href="https://arsenbekirov.com/blog/">
  <style>
    * {{ margin:0; padding:0; box-sizing:border-box }}
    body {{ background:#0a0a0f; color:#e0e0e0; font-family:'Segoe UI',sans-serif; line-height:1.7 }}
    .container {{ max-width:800px; margin:0 auto; padding:60px 24px }}
    h1 {{ color:#c9a959; font-size:36px; margin-bottom:8px }}
    .subtitle {{ color:rgba(255,255,255,0.5); margin-bottom:40px }}
    .blog-card {{ background:rgba(255,255,255,0.03); border:1px solid rgba(201,169,89,0.15); border-radius:12px; padding:28px; margin-bottom:24px; transition:.3s }}
    .blog-card:hover {{ border-color:rgba(201,169,89,0.4); background:rgba(255,255,255,0.05) }}
    .blog-card h2 {{ margin-bottom:8px; font-size:22px }}
    .blog-card h2 a {{ color:#c9a959; text-decoration:none }}
    .blog-card h2 a:hover {{ text-decoration:underline }}
    .blog-desc {{ color:rgba(255,255,255,0.7); font-size:15px; margin-bottom:12px }}
    .blog-meta {{ font-size:13px; color:rgba(255,255,255,0.4); display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px }}
    .blog-tags {{ color:rgba(201,169,89,0.6) }}
    .footer {{ text-align:center; padding:40px 24px; color:rgba(255,255,255,0.3); font-size:13px }}
    .footer a {{ color:rgba(201,169,89,0.7); text-decoration:none }}
  </style>
</head>
<body>
  <div class="container">
    <h1>Blog</h1>
    <p class="subtitle">Stories about music, culture, and the creative journey</p>
    {articles_html}
  </div>
  <footer class="footer">
    <p><a href="https://arsenbekirov.com">arsenbekirov.com</a> &copy; {datetime.now().year}</p>
  </footer>
</body>
</html>"""
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n📁 {len(ARTICLES)} статей + индекс блога → {output_dir}")
    print("Залей папку blog_articles на сайт в /blog/")
    print("И отправь sitemap в Google Search Console заново")

if __name__ == "__main__":
    generate_blog()
