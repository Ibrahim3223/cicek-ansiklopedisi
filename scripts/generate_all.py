#!/usr/bin/env python3
"""
Toplu Bitki Üretim Sistemi
CSV dosyasından okuyarak toplu bitki içeriği oluşturur
Kullanım: python generate_all.py --input bitki_listesi.csv --start 1 --end 100
"""

import os
import sys
import csv
import json
import time
import argparse
from pathlib import Path
from datetime import datetime

# UTF-8 encoding fix for Windows
if sys.platform == "win32":
    import io
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding='utf-8')
    if isinstance(sys.stderr, io.TextIOWrapper):
        sys.stderr.reconfigure(encoding='utf-8')

# Import generate_plant functions
sys.path.insert(0, str(Path(__file__).parent))
from generate_plant import (
    generate_content_with_groq,
    generate_faq,
    create_markdown_file,
    normalize_filename,
    IMAGES_DIR
)
from fetch_images import (
    search_wikimedia_commons,
    search_inaturalist,
    download_and_optimize_image,
    save_attribution
)

# Configuration
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
PROGRESS_FILE = DATA_DIR / "generation_progress.json"
ERROR_LOG_FILE = DATA_DIR / "generation_errors.log"

# Rate limiting
BATCH_SIZE = 10
DELAY_BETWEEN_BATCHES = 5  # seconds
DELAY_BETWEEN_REQUESTS = 2  # seconds


def load_progress():
    """Mevcut ilerlemeyi yükle"""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"completed": [], "failed": [], "last_index": 0}


def save_progress(progress):
    """İlerlemeyi kaydet"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def log_error(plant_name, error_message):
    """Hatayı logla"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(ERROR_LOG_FILE, 'a', encoding='utf-8') as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {plant_name}: {error_message}\n")


def read_plant_csv(csv_file):
    """CSV dosyasından bitki listesini oku"""
    plants = []

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            plants.append({
                'turkce_ad': row.get('turkce_ad', '').strip(),
                'latince_ad': row.get('latince_ad', '').strip(),
                'kategori': row.get('kategori', 'ev-bitkileri').strip(),
            })

    return plants


def process_plant(plant, skip_existing=True):
    """Tek bir bitki işle"""
    turkce_ad = plant['turkce_ad']
    latince_ad = plant['latince_ad']
    kategori = plant['kategori']

    slug = normalize_filename(turkce_ad)

    # Check if already exists
    if skip_existing:
        bitki_path = BASE_DIR / "hugo-site" / "content" / "bitki" / f"{slug}.md"
        cicek_path = BASE_DIR / "hugo-site" / "content" / "cicek" / f"{slug}.md"

        if bitki_path.exists() or cicek_path.exists():
            print(f"  ⏭️  {turkce_ad} zaten mevcut")
            return True

    print(f"\n{'='*60}")
    print(f"🌿 {turkce_ad} ({latince_ad})")
    print(f"{'='*60}")

    # Step 1: Download image
    print("📸 Görsel indiriliyor...")
    image_path = IMAGES_DIR / f"{slug}.jpg"
    image_downloaded = False

    if not image_path.exists():
        # Try Wikimedia
        results = search_wikimedia_commons(latince_ad)
        time.sleep(1)

        # Try iNaturalist if no results
        if not results:
            results = search_inaturalist(latin_name=latince_ad, turkish_name=turkce_ad)
            time.sleep(1)

        if results:
            result = results[0]
            if download_and_optimize_image(result['url'], image_path):
                save_attribution(slug, {
                    'source': result['source'],
                    'author': result['author'],
                    'license': result['license'],
                    'url': result['page_url'],
                })
                print(f"   ✅ Görsel indirildi")
                image_downloaded = True
            else:
                print(f"   ⚠️  Görsel indirilemedi")
        else:
            print(f"   ⚠️  Görsel bulunamadı")
    else:
        print(f"   ✓ Görsel zaten mevcut")
        image_downloaded = True

    # Step 2: Generate content
    print("📝 İçerik üretiliyor (Groq API)...")
    content = generate_content_with_groq(turkce_ad, latince_ad, kategori)

    if not content:
        raise Exception("İçerik üretilemedi")

    print(f"   ✅ İçerik oluşturuldu ({len(content.split())} kelime)")
    time.sleep(DELAY_BETWEEN_REQUESTS)

    # Step 3: Generate FAQ
    print("❓ FAQ üretiliyor...")
    faq = generate_faq(turkce_ad, latince_ad)

    if faq:
        print(f"   ✅ {len(faq)} FAQ oluşturuldu")
    else:
        print(f"   ⚠️  FAQ oluşturulamadı")

    time.sleep(DELAY_BETWEEN_REQUESTS)

    # Step 4: Create markdown
    print("💾 Markdown dosyası oluşturuluyor...")
    file_path = create_markdown_file(
        turkce_ad,
        latince_ad,
        kategori,
        content,
        faq,
        image_slug=slug if image_downloaded else None
    )

    print(f"   ✅ Oluşturuldu: {file_path.name}")

    return True


def main():
    parser = argparse.ArgumentParser(description='CSV\'den toplu bitki üret')
    parser.add_argument('--input', required=True, help='CSV dosyası (turkce_ad,latince_ad,kategori)')
    parser.add_argument('--start', type=int, default=1, help='Başlangıç index (1-based)')
    parser.add_argument('--end', type=int, help='Bitiş index (dahil)')
    parser.add_argument('--resume', action='store_true', help='Kaldığı yerden devam et')
    parser.add_argument('--force', action='store_true', help='Mevcut dosyaları da yeniden oluştur')

    args = parser.parse_args()

    print("=" * 60)
    print("🌿 Toplu Bitki İçerik Üretim Sistemi")
    print("=" * 60)

    # Read CSV
    print(f"\n📄 CSV okunuyor: {args.input}")
    plants = read_plant_csv(args.input)
    print(f"   ✓ {len(plants)} bitki bulundu")

    # Load progress
    progress = load_progress()

    if args.resume:
        start_index = progress['last_index']
        print(f"   🔄 Kaldığı yerden devam ediliyor (index: {start_index})")
    else:
        start_index = args.start - 1  # Convert to 0-based

    end_index = (args.end - 1) if args.end else len(plants) - 1

    # Filter plants
    plants_to_process = plants[start_index:end_index + 1]

    print(f"\n📊 İşlenecek bitki: {len(plants_to_process)}")
    print(f"   Başlangıç: {start_index + 1}")
    print(f"   Bitiş: {end_index + 1}")

    # Process in batches
    total = len(plants_to_process)
    success_count = 0
    fail_count = 0

    for i, plant in enumerate(plants_to_process, start=1):
        current_index = start_index + i - 1

        try:
            if process_plant(plant, skip_existing=not args.force):
                success_count += 1
                progress['completed'].append(plant['turkce_ad'])
            else:
                # Skipped (already exists)
                success_count += 1

            progress['last_index'] = current_index + 1
            save_progress(progress)

        except Exception as e:
            fail_count += 1
            error_msg = str(e)
            progress['failed'].append({
                'name': plant['turkce_ad'],
                'error': error_msg
            })
            log_error(plant['turkce_ad'], error_msg)
            print(f"   ❌ HATA: {error_msg}")
            save_progress(progress)

        # Batch delay
        if i % BATCH_SIZE == 0 and i < total:
            print(f"\n⏸️  Batch tamamlandı ({i}/{total}). {DELAY_BETWEEN_BATCHES} saniye bekleniyor...")
            time.sleep(DELAY_BETWEEN_BATCHES)

        # Progress indicator
        print(f"\n📊 İlerleme: {i}/{total} ({success_count} başarılı, {fail_count} başarısız)")

    # Final summary
    print("\n" + "=" * 60)
    print("✅ TAMAMLANDI")
    print("=" * 60)
    print(f"✅ Başarılı: {success_count}")
    print(f"❌ Başarısız: {fail_count}")
    print(f"📁 İlerleme: {PROGRESS_FILE}")

    if fail_count > 0:
        print(f"📄 Hata logu: {ERROR_LOG_FILE}")


if __name__ == "__main__":
    main()
