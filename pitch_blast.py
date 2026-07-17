#!/usr/bin/env python3
"""
🎤 ARSEN BEKIROV — PITCH BLASTER
Автоматическая рассылка питчей по всем контактам:
лейблы, блоги, радио, плейлист-кураторы
"""

import csv, io, os, json
from pathlib import Path
from datetime import datetime

CONTACTS = """
Putumayo World Music,submissions@putumayo.com,Legendary world music label
Real World Records,info@realworldrecords.com,Peter Gabriel's world music label
Six Degrees Records,info@sixdegreesrecords.com,World/electronic fusion label
Cumbancha,info@cumbancha.com,Boutique world music label
ARC Music,anr@arcmusic.co.uk,World music label
Compass Records,submissions@compassrecords.com,Folk/world/Celtic
World Circuit Records,help@worldcircuit.co.uk,Buena Vista Social Club label
Riverboat Records,eden.bedeau@worldmusic.net,World music label
Smithsonian Folkways,folkwrights@si.edu,US folk/world institutional
Songlines Magazine,russ@songlines.co.uk,Leading world music magazine UK
Songlines Deputy,charis@songlines.co.uk,World music magazine
Songlines Asst,spencer@songlines.co.uk,World music magazine
Afropop Worldwide,info@afropop.org,US world music radio/podcast
Global Sounds,info@globalsounds.org,World music blog
World Music Report,editor@worldmusicreport.com,World music news
Altofonic,info@altofonic.com,World/electronic curator
Awesome Tapes from Africa,info@awesometapes.com,African music curator
PAM Magazine,contact@pan-african-music.com,Pan-African music
Native Magazine,info@thenativemag.com,Nigerian music
AfroPunk,info@afropunk.com,Afro-diaspora music
OkayAfrica,editorial@okayafrica.com,African music/diaspora
BBC World Service,worldservice.music@bbc.co.uk,Global audience
Radiooooo,hello@radiooooo.com,Time-travel world radio
Funkhaus Europa,info@funkhauseuropa.de,German world radio
BalconyTV,submissions@balconytv.com,Acoustic live sessions
KEXP World Music,worldmusic@kexp.org,World music radio
Aquarium Drunkard,info@aquariumdrunkard.com,Eclectic curator
WOMEX,info@womex.com,World music expo
GlobalFest,info@globalfest.org,World music festival
The Quietus,luke@thequietus.com,UK music publication
Resident Advisor,editorial@residentadvisor.net,Electronic music
Mixmag,features@mixmag.net,Dance music magazine
DJ Mag,editorial@djmag.com,Global electronic magazine
XLR8R,info@xlr8r.com,Underground electronic
Pitchfork,feedback@pitchfork.com,Music criticism
Stereogum,tips@stereogum.com,Indie/electronic
FACT Magazine,news@factmag.com,UK electronic
Crack Magazine,info@crackmagazine.com,UK independent
The Fader,info@thefader.com,US music/culture
Clash Music,info@clashmusic.com,UK music magazine
BBC Radio 6 Music,6music@bbc.co.uk,Gilles Peterson
BBC Radio 3 Late Junction,latejunction@bbc.co.uk,Experimental
KCRW,music@kcrw.org,LA eclectic radio
WFMU,info@wfmu.org,Freeform radio NYC
NPR Music,worldmusic@npr.org,Massive US reach
Radio Nova Paris,contact@nova.fr,French eclectic
FIP France,fip@radiofrance.com,French world radio
NTS Radio,info@nts.live,London underground
Worldwide FM,info@worldwidefm.net,Gilles Peterson station
Rinse FM,info@rinse.fm,London electronic
The Lot Radio,info@thelotradio.com,Brooklyn indie
Indie Shuffle,submit@indieshuffle.com,Indie playlist curator
Stereofox,demos@stereofox.com,Electronic beats curator
Electronic Gems,submit@electronicgems.com,Synthwave curator
Deep House Bible,contact@deephousebible.com,Deep house playlist
Madorasindahouse,info@madorasindahouse.com,Afro house curator
David Dean Burkhart,daviddeanburkhart@gmail.com,YouTube indie curator
La Belle Musique,submit@labellemusique.co,Chill electronic
MrRevillz,submit@mrrevillz.com,Deep house/vocal
"""

# =========== ШАБЛОНЫ ПИТЧЕЙ ===========

PITCH_WORLD_LABEL = """Subject: Submission: Arsen Bekirov — Crimean Tatar ethno-pop from Crimea (Honored Artist, QARADENIZ winner)

Hi {name},

I'm Arsen Bekirov — a Crimean Tatar tenor and ethno-pop artist from Crimea. I'm an Honored Artist of the Republic of Crimea and the Republic of Tatarstan, and a winner of the QARADENIZ Production 2025 award.

I sing in six languages (Crimean Tatar, Turkish, Russian, English, Arabic, French), blending traditional Crimean Tatar folk music with contemporary pop and electronic production.

My debut EP "Qirim EP" (2025, 11 tracks) reimagines Crimean Tatar music for a global audience. I believe it aligns with {organization}'s commitment to authentic world music.

Listen here:
• Spotify: https://open.spotify.com/artist/0TUkZ5dvqD50Kzg7IsvgCk
• Website: https://arsenbekirov.com
• Instagram: @mr.arsenbekirov

I'd love to discuss potential collaboration, licensing, or distribution opportunities.

Thank you for your time,
Arsen Bekirov
arsen@arsenbekirov.com
WhatsApp: +7 978 052 5045"""

PITCH_MEDIA = """Subject: Feature pitch: Arsen Bekirov — Crimean Tatar artist blending folk with ethno-pop (QARADENIZ 2025 winner)

Hi {name},

I'm pitching a story about my music and journey as a Crimean Tatar artist from Crimea.

I'm a multilingual tenor and ethno-pop artist, an Honored Artist of Crimea and Tatarstan. I blend traditional Crimean Tatar folk forms with contemporary pop and electronic production.

My debut EP "Qirim EP" (2025) won the QARADENIZ Production award. I perform in 6 languages and have built a following across Russia, Turkey, and Europe.

I think {organization} readers would appreciate a story about an artist preserving and evolving his musical heritage while navigating between tradition and modernity, East and West.

Links:
• Website: https://arsenbekirov.com
• Spotify: https://open.spotify.com/artist/0TUkZ5dvqD50Kzg7IsvgCk
• Instagram: @mr.arsenbekirov
• YouTube: @mr.arsenbekirov

Happy to provide photos, interview, or more details.

Best,
Arsen Bekirov
arsen@arsenbekirov.com"""

PITCH_RADIO = """Subject: Track submission: Arsen Bekirov — "Qirim EP" ethno-pop from Crimea (6 languages)

Hi {name},

I'm Arsen Bekirov, a Crimean Tatar ethno-pop artist and Honored Artist of Crimea and Tatarstan. I'm submitting my debut EP "Qirim EP" for potential airplay on {organization}.

The EP blends Crimean Tatar folk music with contemporary pop/electronic — sung in multiple languages. Tracks range from upbeat dance numbers to soulful ballads.

Key tracks:
• "Maneler" — uptempo ethno-pop
• "Seni Seven" — award-winning ballad (QARADENIZ 2025)
• "INAN" — Turkish language crossover

Listen: https://open.spotify.com/artist/0TUkZ5dvqD50Kzg7IsvgCk

Full EP and individual tracks available. Happy to provide WAV files or any format you need.

Thank you for considering,
Arsen Bekirov
arsen@arsenbekirov.com"""

PITCH_PLAYLIST = """Subject: Playlist submission: Arsen Bekirov — Ethno-pop from Crimea (6 languages, QARADENIZ winner)

Hi {name},

I'd like to submit my music for consideration in {organization}'s playlist.

I'm Arsen Bekirov — a Crimean Tatar tenor and ethno-pop artist, Honored Artist of Crimea and Tatarstan. My sound blends traditional Crimean Tatar folk with modern pop production. I sing in 6 languages.

Debut EP "Qirim EP" (2025) won the QARADENIZ Production award.

Suggested tracks for your playlist:
• "Seni Seven" — atmospheric ballad, perfect for chill/world playlists
• "Maneler" — upbeat ethno-pop, for world/dance playlists

Spotify: https://open.spotify.com/artist/0TUkZ5dvqD50Kzg7IsvgCk
Website: https://arsenbekirov.com

Thank you!
Arsen Bekirov"""

def classify_contact(org, info):
    """Определяет тип контакта по описанию"""
    info_lower = info.lower()
    if 'label' in info_lower:
        return 'label'
    if any(w in info_lower for w in ['magazine', 'blog', 'mag', 'publication', 'criticism', 'pitchfork']):
        return 'media'
    if any(w in info_lower for w in ['radio', 'fm', 'bbc']):
        return 'radio'
    if any(w in info_lower for w in ['playlist', 'curator', 'curated']):
        return 'playlist'
    return 'media'

TEMPLATES = {
    'label': PITCH_WORLD_LABEL,
    'media': PITCH_MEDIA,
    'radio': PITCH_RADIO,
    'playlist': PITCH_PLAYLIST,
}

def generate_pitches():
    """Генерирует все питч-имейлы"""
    reader = csv.reader(io.StringIO(CONTACTS.strip()))
    contacts = [row for row in reader if len(row) >= 3 and '@' in row[1]]
    
    output_dir = Path.home() / 'Desktop' / 'pitch_emails'
    output_dir.mkdir(exist_ok=True)
    
    for org, email, info in contacts:
        contact_type = classify_contact(org, info)
        template = TEMPLATES.get(contact_type, PITCH_MEDIA)
        
        body = template.format(
            name=org.split(' - ')[0].strip(),
            organization=org
        )
        
        filename = f"{org.replace(' ', '_').replace('/', '-')[:60]}.txt"
        filepath = output_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(f"TO: {email}\n")
            f.write(f"TYPE: {contact_type}\n")
            f.write(f"ORGANIZATION: {org}\n")
            f.write(f"INFO: {info}\n")
            f.write("=" * 60 + "\n\n")
            f.write(body)
        
        print(f"✅ {org} → {email} ({contact_type})")
    
    print(f"\n📊 Всего: {len(contacts)} питчей")
    print(f"📁 Сохранено в: {output_dir}")
    print()
    print("Чтобы отправить, открой папку и скопируй текст в email.")
    print("Или используй: openclaw отправь питчи")

if __name__ == '__main__':
    generate_pitches()
