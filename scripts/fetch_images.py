#!/usr/bin/env python3
"""
Bitki Görsel İndirme Sistemi
Wikimedia Commons ve iNaturalist'ten bitki görselleri çeker
"""

import os
import sys
import json
import time
import argparse
import requests
from pathlib import Path
from urllib.parse import quote, unquote
from io import BytesIO
from PIL import Image
import unicodedata

# UTF-8 encoding fix for Windows
if sys.platform == "win32":
    import io
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding='utf-8')
    if isinstance(sys.stderr, io.TextIOWrapper):
        sys.stderr.reconfigure(encoding='utf-8')

# Configuration
BASE_DIR = Path(__file__).parent.parent
IMAGES_DIR = BASE_DIR / "hugo-site" / "static" / "images" / "bitkiler"
DATA_DIR = BASE_DIR / "data"
ATTRIBUTION_FILE = DATA_DIR / "image_attributions.json"
MAX_IMAGE_WIDTH = 800
IMAGE_QUALITY = 85
RETRY_COUNT = 3
RATE_LIMIT_DELAY = 1.0  # seconds between requests

# User agent for API requests
USER_AGENT = "CicekAnsiklopedisi/1.0 (https://cicekansiklopedisi.com; contact@example.com)"


def normalize_filename(text):
    """Türkçe karakterleri normalize et, dosya adı için güvenli hale getir"""
    # Türkçe karakterleri değiştir
    replacements = {
        'ç': 'c', 'Ç': 'C',
        'ğ': 'g', 'Ğ': 'G',
        'ı': 'i', 'İ': 'I',
        'ö': 'o', 'Ö': 'O',
        'ş': 's', 'Ş': 'S',
        'ü': 'u', 'Ü': 'U',
    }

    for turkish, latin in replacements.items():
        text = text.replace(turkish, latin)

    # Boşlukları tire ile değiştir
    text = text.lower().replace(' ', '-')

    # Sadece güvenli karakterleri tut
    safe_chars = 'abcdefghijklmnopqrstuvwxyz0-9-'
    text = ''.join(c for c in text if c in safe_chars)

    return text


def load_attributions():
    """Mevcut attribution bilgilerini yükle"""
    if ATTRIBUTION_FILE.exists():
        with open(ATTRIBUTION_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_attribution(slug, attribution_data):
    """Attribution bilgisini kaydet"""
    attributions = load_attributions()
    attributions[slug] = attribution_data

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(ATTRIBUTION_FILE, 'w', encoding='utf-8') as f:
        json.dump(attributions, f, ensure_ascii=False, indent=2)


def search_wikimedia_commons(latin_name, max_results=10):
    """Wikimedia Commons'ta bitki ara"""
    try:
        # Search for images
        url = "https://commons.wikimedia.org/w/api.php"
        params = {
            'action': 'query',
            'format': 'json',
            'generator': 'search',
            'gsrsearch': latin_name,
            'gsrlimit': max_results,
            'prop': 'imageinfo',
            'iiprop': 'url|extmetadata|size',
            'iiurlwidth': MAX_IMAGE_WIDTH,
        }

        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        if 'query' not in data or 'pages' not in data['query']:
            return []

        results = []
        for page_id, page in data['query']['pages'].items():
            if 'imageinfo' not in page:
                continue

            imageinfo = page['imageinfo'][0]

            # Check if it's a photo (not illustration/diagram)
            extmeta = imageinfo.get('extmetadata', {})
            categories = extmeta.get('Categories', {}).get('value', '').lower()

            # Skip illustrations, diagrams, maps, etc.
            skip_keywords = ['illustration', 'diagram', 'map', 'drawing', 'svg']
            if any(keyword in categories for keyword in skip_keywords):
                continue

            # Check minimum size
            width = imageinfo.get('width', 0)
            height = imageinfo.get('height', 0)
            if width < 400 or height < 400:
                continue

            # Extract metadata
            author = extmeta.get('Artist', {}).get('value', 'Unknown')
            license_short = extmeta.get('LicenseShortName', {}).get('value', 'Unknown')

            results.append({
                'url': imageinfo.get('thumburl') or imageinfo.get('url'),
                'source': 'Wikimedia Commons',
                'author': author,
                'license': license_short,
                'page_url': imageinfo.get('descriptionurl', ''),
                'width': width,
                'height': height,
            })

        return results

    except Exception as e:
        print(f"  ⚠️  Wikimedia arama hatası: {str(e)}")
        return []


def search_inaturalist(latin_name=None, turkish_name=None):
    """iNaturalist API'den bitki ara"""
    try:
        # First, find the taxon
        search_term = latin_name or turkish_name
        url = "https://api.inaturalist.org/v1/taxa"
        params = {
            'q': search_term,
            'rank': 'species,genus',
            'per_page': 5,
        }

        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data.get('results'):
            return []

        # Get the first matching taxon
        taxon = data['results'][0]
        default_photo = taxon.get('default_photo')

        if not default_photo:
            return []

        # Get medium size photo
        photo_url = default_photo.get('medium_url')

        if not photo_url:
            return []

        results = [{
            'url': photo_url,
            'source': 'iNaturalist',
            'author': default_photo.get('attribution', 'iNaturalist User'),
            'license': default_photo.get('license_code', 'CC BY'),
            'page_url': f"https://www.inaturalist.org/taxa/{taxon['id']}",
            'width': 500,  # iNaturalist medium size
            'height': 500,
        }]

        return results

    except Exception as e:
        print(f"  ⚠️  iNaturalist arama hatası: {str(e)}")
        return []


def download_and_optimize_image(url, output_path):
    """Görseli indir ve optimize et"""
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, headers=headers, timeout=15, stream=True)
        response.raise_for_status()

        # Open image
        img = Image.open(BytesIO(response.content))

        # Convert to RGB if needed (for PNG with transparency)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background

        # Resize if larger than max width
        if img.width > MAX_IMAGE_WIDTH:
            ratio = MAX_IMAGE_WIDTH / img.width
            new_height = int(img.height * ratio)
            img = img.resize((MAX_IMAGE_WIDTH, new_height), Image.Resampling.LANCZOS)

        # Save as optimized JPEG
        img.save(output_path, 'JPEG', quality=IMAGE_QUALITY, optimize=True)

        return True

    except Exception as e:
        print(f"  ❌ İndirme hatası: {str(e)}")
        return False


def fetch_image_for_plant(turkish_name, latin_name, slug, dry_run=False):
    """Bir bitki için görsel bul ve indir"""
    print(f"\n🔍 {turkish_name} ({latin_name})")

    # Check if image already exists
    image_path = IMAGES_DIR / f"{slug}.jpg"
    if image_path.exists():
        print(f"  ✓ Görsel zaten mevcut: {image_path.name}")
        return True

    if dry_run:
        print(f"  [DRY RUN] Görsel aranacak")
        return False

    # Try sources in order
    results = []

    # 1. Try Wikimedia Commons with Latin name
    print(f"  → Wikimedia Commons araması...")
    time.sleep(RATE_LIMIT_DELAY)
    results = search_wikimedia_commons(latin_name)

    # 2. If no results, try iNaturalist
    if not results:
        print(f"  → iNaturalist araması...")
        time.sleep(RATE_LIMIT_DELAY)
        results = search_inaturalist(latin_name=latin_name, turkish_name=turkish_name)

    # 3. If still no results, skip
    if not results:
        print(f"  ❌ Görsel bulunamadı")
        return False

    # Try to download the first result
    for attempt in range(RETRY_COUNT):
        result = results[0]
        print(f"  📥 İndiriliyor: {result['source']} (deneme {attempt + 1}/{RETRY_COUNT})")

        if download_and_optimize_image(result['url'], image_path):
            # Save attribution
            save_attribution(slug, {
                'source': result['source'],
                'author': result['author'],
                'license': result['license'],
                'url': result['page_url'],
            })

            print(f"  ✅ Başarıyla indirildi: {image_path.name}")
            return True

        time.sleep(1)  # Wait before retry

    print(f"  ❌ İndirme başarısız")
    return False


def get_plants_from_content():
    """Content dizinindeki bitkileri listele"""
    plants = []

    content_dirs = [
        BASE_DIR / "hugo-site" / "content" / "bitki",
        BASE_DIR / "hugo-site" / "content" / "cicek",
    ]

    for content_dir in content_dirs:
        if not content_dir.exists():
            continue

        for md_file in content_dir.glob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract frontmatter
                if not content.startswith('---'):
                    continue

                parts = content.split('---', 2)
                if len(parts) < 3:
                    continue

                frontmatter = parts[1]

                # Extract fields
                title = None
                latin = None

                for line in frontmatter.split('\n'):
                    line = line.strip()
                    if line.startswith('title:'):
                        title = line.split(':', 1)[1].strip().strip('"\'')
                    elif line.startswith('latince:'):
                        latin = line.split(':', 1)[1].strip().strip('"\'')

                if title and latin:
                    slug = md_file.stem
                    plants.append({
                        'turkish_name': title,
                        'latin_name': latin,
                        'slug': slug,
                    })

            except Exception as e:
                print(f"⚠️  {md_file.name} okunamadı: {str(e)}")

    return plants


def main():
    parser = argparse.ArgumentParser(description='Bitki görsellerini indir')
    parser.add_argument('--all', action='store_true', help='Tüm bitkiler için görsel indir')
    parser.add_argument('--missing', action='store_true', help='Sadece görseli olmayan bitkiler')
    parser.add_argument('--plant', type=str, help='Belirli bir bitki için görsel indir (slug)')
    parser.add_argument('--dry-run', action='store_true', help='Gerçek indirme yapmadan test et')

    args = parser.parse_args()

    print("=" * 60)
    print("🌿 Bitki Görsel İndirme Sistemi")
    print("=" * 60)

    # Create directories
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Get plants
    plants = get_plants_from_content()

    if not plants:
        print("\n❌ Bitki bulunamadı!")
        return

    print(f"\n📊 Toplam {len(plants)} bitki bulundu")

    # Filter plants based on arguments
    if args.plant:
        plants = [p for p in plants if p['slug'] == args.plant]
        if not plants:
            print(f"\n❌ '{args.plant}' adlı bitki bulunamadı!")
            return

    elif args.missing:
        plants = [p for p in plants if not (IMAGES_DIR / f"{p['slug']}.jpg").exists()]
        print(f"📊 Görseli olmayan {len(plants)} bitki")

    if not plants:
        print("\n✅ Tüm bitkilerin görseli mevcut!")
        return

    # Download images
    success_count = 0
    fail_count = 0

    for i, plant in enumerate(plants, 1):
        print(f"\n[{i}/{len(plants)}]", end=" ")

        if fetch_image_for_plant(
            plant['turkish_name'],
            plant['latin_name'],
            plant['slug'],
            dry_run=args.dry_run
        ):
            success_count += 1
        else:
            fail_count += 1

        # Rate limiting
        if i < len(plants):
            time.sleep(RATE_LIMIT_DELAY)

    # Summary
    print("\n" + "=" * 60)
    print("📊 ÖZET")
    print("=" * 60)
    print(f"✅ Başarılı: {success_count}")
    print(f"❌ Başarısız: {fail_count}")
    print(f"📁 Görsel klasörü: {IMAGES_DIR}")

    if not args.dry_run:
        print(f"📄 Attribution dosyası: {ATTRIBUTION_FILE}")


if __name__ == "__main__":
    main()
