#!/usr/bin/env python3
"""
Tek Bitki Oluşturma Sistemi
Groq API + Görsel İndirme + Markdown Oluşturma
Kullanım: python generate_plant.py --name "Orkide" --latin "Phalaenopsis"
"""

import os
import sys
import json
import time
import argparse
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# UTF-8 encoding fix for Windows
if sys.platform == "win32":
    import io
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding='utf-8')
    if isinstance(sys.stderr, io.TextIOWrapper):
        sys.stderr.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

# Import image fetching functions
sys.path.insert(0, str(Path(__file__).parent))
from fetch_images import (
    search_wikimedia_commons,
    search_inaturalist,
    download_and_optimize_image,
    save_attribution,
    normalize_filename,
    IMAGES_DIR
)

# Configuration
BASE_DIR = Path(__file__).parent.parent
CONTENT_DIR = BASE_DIR / "hugo-site" / "content"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"

# System prompt for Groq
SYSTEM_PROMPT = """Sen Türkiye'nin en deneyimli botanik uzmanısın.
Bitki ve çiçekler hakkında detaylı, doğru ve ilgi çekici içerikler yazıyorsun.

Yazım kuralları:
- Türkçe yaz, akıcı ve anlaşılır bir dil kullan
- Pratik bilgiler ve ipuçları ver
- Markdown formatı kullan (## başlıklar, - listeler, **kalın**)
- Emoji kullanma
- Minimum 600 kelime yaz
- Her bölümü detaylı açıkla"""


def generate_content_with_groq(plant_name, latin_name, category="ev-bitkileri"):
    """Groq API ile bitki içeriği üret"""
    if not GROQ_API_KEY:
        print("  ⚠️  GROQ_API_KEY bulunamadı!")
        return None

    user_prompt = f"""'{plant_name}' ({latin_name}) hakkında kapsamlı bir bakım rehberi yaz.

İçerikte şu bölümler olsun:

## {plant_name} Nedir?
Bitkinin genel tanımı, görünümü ve özellikleri (en az 150 kelime)

## Bakım Rehberi
### Sulama
Detaylı sulama bilgileri, sıklık, mevsimsel değişiklikler (en az 80 kelime)

### Işık İhtiyacı
Işık gereksinimleri, doğrudan/dolaylı güneş, ideal pencere yönü (en az 80 kelime)

### Toprak ve Saksı
Toprak karışımı, drenaj, saksı seçimi (en az 60 kelime)

### Sıcaklık ve Nem
İdeal sıcaklık aralığı, nem gereksinimleri (en az 60 kelime)

### Gübreleme
Gübre tipi, sıklık, mevsimsel değişiklikler (en az 60 kelime)

## Sık Karşılaşılan Sorunlar
En az 5 yaygın sorun ve çözümleri (en az 100 kelime)

## Çoğaltma Yöntemleri
Çelik, tohum, bölme gibi yöntemler (en az 80 kelime)

ÖNEMLI: Markdown formatında yaz, emoji kullanma."""

    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2500
        }

        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()

        data = response.json()
        content = data['choices'][0]['message']['content']

        return content.strip()

    except Exception as e:
        print(f"  ❌ Groq API hatası: {str(e)}")
        return None


def generate_faq(plant_name, latin_name):
    """FAQ oluştur"""
    if not GROQ_API_KEY:
        return []

    prompt = f"""{plant_name} ({latin_name}) için 4 adet sık sorulan soru ve cevap yaz.

Her cevap 3-4 cümle olsun, pratik ve spesifik bilgiler içersin.

Format (JSON):
[
  {{"soru": "soru metni", "cevap": "detaylı cevap"}},
  ...
]

SADECE JSON çıktısı ver, başka metin yazma."""

    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "Sen bir bitki uzmanısın. JSON formatında cevap veriyorsun."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 800
        }

        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        data = response.json()
        content = data['choices'][0]['message']['content'].strip()

        # Extract JSON from response
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0].strip()
        elif '```' in content:
            content = content.split('```')[1].split('```')[0].strip()

        faq_list = json.loads(content)
        return faq_list[:4]  # Max 4 FAQ

    except Exception as e:
        print(f"  ⚠️  FAQ üretilemedi: {str(e)}")
        return []


def create_markdown_file(plant_name, latin_name, category, content, faq, image_slug=None):
    """Markdown dosyası oluştur"""
    slug = normalize_filename(plant_name)

    # Determine folder
    if category == "cicek" or "çiçek" in plant_name.lower():
        folder = CONTENT_DIR / "cicek"
    else:
        folder = CONTENT_DIR / "bitki"

    folder.mkdir(parents=True, exist_ok=True)

    # Create frontmatter
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+03:00")

    frontmatter = f"""---
title: {plant_name}
slug: {slug}
date: {now}
lastmod: {now}
description: {plant_name} ({latin_name}) bakım rehberi. Sulama, ışık, toprak gereksinimleri ve çoğaltma yöntemleri.
keywords:
  - {plant_name}
  - {latin_name}
  - {plant_name} bakımı
  - {plant_name} sulama
  - {plant_name} çoğaltma
categories:
  - {category}
tags:
  - {slug}
  - {category}
latince: {latin_name}
image: {f"/images/bitkiler/{slug}.jpg" if image_slug else ""}
populer: false
draft: false"""

    # Add FAQ if available
    if faq:
        frontmatter += "\nsss:"
        for item in faq:
            soru = item.get('soru', '').replace('"', '\\"')
            cevap = item.get('cevap', '').replace('"', '\\"')
            frontmatter += f'\n  - soru: "{soru}"\n    cevap: "{cevap}"'

    frontmatter += "\n---\n"

    # Full content
    full_content = frontmatter + "\n" + content

    # Write file
    file_path = folder / f"{slug}.md"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(full_content)

    return file_path


def main():
    parser = argparse.ArgumentParser(description='Tek bitki için tam içerik oluştur')
    parser.add_argument('--name', required=True, help='Bitki Türkçe adı (örn: Monstera)')
    parser.add_argument('--latin', required=True, help='Bitki Latince adı (örn: Monstera deliciosa)')
    parser.add_argument('--category', default='ev-bitkileri', help='Kategori (ev-bitkileri, cicek, vb.)')
    parser.add_argument('--skip-image', action='store_true', help='Görsel indirmeyi atla')
    parser.add_argument('--skip-content', action='store_true', help='İçerik üretimini atla')

    args = parser.parse_args()

    print("=" * 60)
    print(f"🌿 {args.name} İçerik Oluşturma")
    print("=" * 60)

    slug = normalize_filename(args.name)
    image_downloaded = False

    # Step 1: Download image
    if not args.skip_image:
        print("\n📸 ADIM 1: Görsel İndirme")
        print(f"   Aranıyor: {args.latin}")

        image_path = IMAGES_DIR / f"{slug}.jpg"

        if image_path.exists():
            print(f"   ✓ Görsel zaten mevcut")
            image_downloaded = True
        else:
            # Try Wikimedia
            results = search_wikimedia_commons(args.latin)
            time.sleep(1)

            # Try iNaturalist if no results
            if not results:
                results = search_inaturalist(latin_name=args.latin, turkish_name=args.name)
                time.sleep(1)

            if results:
                result = results[0]
                print(f"   → {result['source']} üzerinden indiriliyor...")

                if download_and_optimize_image(result['url'], image_path):
                    save_attribution(slug, {
                        'source': result['source'],
                        'author': result['author'],
                        'license': result['license'],
                        'url': result['page_url'],
                    })
                    print(f"   ✅ Görsel indirildi: {slug}.jpg")
                    image_downloaded = True
                else:
                    print(f"   ❌ İndirme başarısız")
            else:
                print(f"   ⚠️  Görsel bulunamadı")

    # Step 2: Generate content
    content = ""
    if not args.skip_content:
        print("\n📝 ADIM 2: İçerik Üretimi (Groq API)")
        content = generate_content_with_groq(args.name, args.latin, args.category)

        if content:
            word_count = len(content.split())
            print(f"   ✅ İçerik oluşturuldu ({word_count} kelime)")
        else:
            print(f"   ❌ İçerik oluşturulamadı")
            return

    # Step 3: Generate FAQ
    print("\n❓ ADIM 3: FAQ Üretimi")
    faq = generate_faq(args.name, args.latin)

    if faq:
        print(f"   ✅ {len(faq)} FAQ oluşturuldu")
    else:
        print(f"   ⚠️  FAQ oluşturulamadı")

    # Step 4: Create markdown file
    print("\n💾 ADIM 4: Markdown Dosyası Oluşturma")
    file_path = create_markdown_file(
        args.name,
        args.latin,
        args.category,
        content,
        faq,
        image_slug=slug if image_downloaded else None
    )

    print(f"   ✅ Dosya oluşturuldu: {file_path}")

    # Summary
    print("\n" + "=" * 60)
    print("✅ TAMAMLANDI")
    print("=" * 60)
    print(f"📄 Dosya: {file_path}")
    print(f"📸 Görsel: {'Evet' if image_downloaded else 'Hayır'}")
    print(f"📝 İçerik: {'Evet' if content else 'Hayır'}")
    print(f"❓ FAQ: {len(faq)} adet")


if __name__ == "__main__":
    main()
