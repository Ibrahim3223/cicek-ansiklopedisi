"""
Wikimedia Commons ve iNaturalist'ten Bitki Görselleri İndirme
Çiçek Ansiklopedisi için otomatik görsel çekme sistemi
"""

import os
import sys

# Windows console encoding fix
if sys.platform == "win32":
    import io
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding='utf-8')
    if isinstance(sys.stderr, io.TextIOWrapper):
        sys.stderr.reconfigure(encoding='utf-8')

import json
import time
import asyncio
import aiohttp
from pathlib import Path
from dotenv import load_dotenv
from tqdm import tqdm
from PIL import Image
from io import BytesIO

# Load environment variables
load_dotenv()

# API Settings
WIKIMEDIA_API = "https://commons.wikimedia.org/w/api.php"
INATURALIST_API = "https://api.inaturalist.org/v1/taxa/autocomplete"
USER_AGENT = os.getenv("WIKIMEDIA_USER_AGENT", "CicekAnsiklopedisi/1.0")

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
IMAGES_DIR = PROJECT_DIR / "hugo-site" / "static" / "images" / "bitkiler"
PROGRESS_FILE = SCRIPT_DIR / "image_download_progress.json"

# Settings
IMAGE_SIZE_LIMIT = 2048  # Max width/height
REQUEST_DELAY = 1  # Seconds between requests
MAX_RETRIES = 3

# Import plant database
sys.path.insert(0, str(SCRIPT_DIR))
from plants_database import PLANTS


def create_slug(plant_name):
    """Bitki adından slug oluştur"""
    slug = plant_name.lower()
    tr_chars = {'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c',
                'İ': 'i', 'Ğ': 'g', 'Ü': 'u', 'Ş': 's', 'Ö': 'o', 'Ç': 'c', ' ': '-'}
    for tr, en in tr_chars.items():
        slug = slug.replace(tr, en)
    return slug


async def search_wikimedia(session, latin_name, semaphore):
    """Wikimedia Commons'tan görsel ara"""
    async with semaphore:
        headers = {"User-Agent": USER_AGENT}

        params = {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrsearch": f"{latin_name}",
            "gsrlimit": 5,
            "prop": "imageinfo",
            "iiprop": "url|extmetadata|size",
            "iiurlwidth": IMAGE_SIZE_LIMIT
        }

        try:
            async with session.get(WIKIMEDIA_API, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()

                    if "query" in data and "pages" in data["query"]:
                        pages = data["query"]["pages"]

                        # En iyi görseli seç
                        for page_id, page in pages.items():
                            if "imageinfo" in page:
                                image_info = page["imageinfo"][0]
                                url = image_info.get("thumburl") or image_info.get("url")

                                if url and url.lower().endswith(('.jpg', '.jpeg', '.png')):
                                    # Attribution bilgisi
                                    metadata = image_info.get("extmetadata", {})
                                    artist = metadata.get("Artist", {}).get("value", "Unknown")
                                    license = metadata.get("LicenseShortName", {}).get("value", "")

                                    attribution = f"Photo by {artist} via Wikimedia Commons ({license})"

                                    return {
                                        "url": url,
                                        "source": "wikimedia",
                                        "attribution": attribution
                                    }
                    return None
                else:
                    return None
        except Exception as e:
            print(f"\n⚠️ Wikimedia error: {e}")
            return None


async def search_inaturalist(session, latin_name, semaphore):
    """iNaturalist'ten görsel ara"""
    async with semaphore:
        headers = {"User-Agent": USER_AGENT}

        params = {
            "q": latin_name,
            "rank": "species"
        }

        try:
            async with session.get(INATURALIST_API, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()

                    if data.get("results"):
                        taxon = data["results"][0]

                        # Fotoğraf var mı?
                        if "default_photo" in taxon and taxon["default_photo"]:
                            photo = taxon["default_photo"]
                            url = photo.get("medium_url") or photo.get("square_url")

                            if url:
                                attribution = f"Photo via iNaturalist (CC BY)"

                                return {
                                    "url": url,
                                    "source": "inaturalist",
                                    "attribution": attribution
                                }
                    return None
                else:
                    return None
        except Exception as e:
            print(f"\n⚠️ iNaturalist error: {e}")
            return None


async def download_image(session, url, save_path, semaphore):
    """Görseli indir ve kaydet"""
    async with semaphore:
        headers = {"User-Agent": USER_AGENT}

        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    image_data = await response.read()

                    # Resmi aç ve optimize et
                    img = Image.open(BytesIO(image_data))

                    # RGB'ye çevir (PNG alpha channel vs.)
                    if img.mode in ('RGBA', 'LA', 'P'):
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = background

                    # Boyutlandır
                    img.thumbnail((IMAGE_SIZE_LIMIT, IMAGE_SIZE_LIMIT), Image.Resampling.LANCZOS)

                    # Kaydet
                    img.save(save_path, "JPEG", quality=85, optimize=True)

                    return True
                else:
                    return False
        except Exception as e:
            print(f"\n⚠️ Download error: {e}")
            return False


async def process_plant(session, plant_data, semaphore, progress):
    """Bir bitki için görsel bul ve indir"""
    plant_name, latin_name, category, care_level, info = plant_data

    slug = create_slug(plant_name)
    image_path = IMAGES_DIR / f"{slug}.jpg"

    # Zaten indirilmiş mi?
    if slug in progress["downloaded"]:
        return None

    # Görsel zaten var mı?
    if image_path.exists():
        progress["downloaded"].append(slug)
        save_progress(progress)
        return None

    # 1. Wikimedia'da ara
    result = await search_wikimedia(session, latin_name, semaphore)
    await asyncio.sleep(REQUEST_DELAY)

    # 2. Bulunamazsa iNaturalist'te ara
    if not result:
        result = await search_inaturalist(session, latin_name, semaphore)
        await asyncio.sleep(REQUEST_DELAY)

    # 3. Görsel bulduysa indir
    if result:
        success = await download_image(session, result["url"], image_path, semaphore)

        if success:
            progress["downloaded"].append(slug)
            progress["attributions"][slug] = result["attribution"]
            save_progress(progress)

            return {
                "plant": plant_name,
                "source": result["source"],
                "attribution": result["attribution"],
                "path": str(image_path)
            }
        else:
            progress["failed"].append({"plant": plant_name, "reason": "Download failed"})
            save_progress(progress)
            return None
    else:
        # Placeholder kullan
        progress["no_image"].append(plant_name)
        save_progress(progress)
        return None


def load_progress():
    """İlerleme dosyasını yükle"""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "downloaded": [],
        "no_image": [],
        "failed": [],
        "attributions": {}
    }


def save_progress(progress):
    """İlerlemeyi kaydet"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def update_markdown_files(progress):
    """Markdown dosyalarına attribution bilgisi ekle"""
    content_dirs = [
        PROJECT_DIR / "hugo-site" / "content" / "bitki",
        PROJECT_DIR / "hugo-site" / "content" / "cicek"
    ]

    updated = 0

    for content_dir in content_dirs:
        if not content_dir.exists():
            continue

        for md_file in content_dir.glob("*.md"):
            slug = md_file.stem

            if slug in progress["attributions"]:
                attribution = progress["attributions"][slug]

                # Dosyayı oku
                content = md_file.read_text(encoding='utf-8')

                # Attribution güncelle
                if 'image_attribution: ""' in content:
                    content = content.replace(
                        'image_attribution: ""',
                        f'image_attribution: "{attribution}"'
                    )
                    md_file.write_text(content, encoding='utf-8')
                    updated += 1

    print(f"\n✓ {updated} dosyada attribution bilgisi güncellendi")


async def main():
    """Ana fonksiyon"""
    print("=" * 60)
    print("Çiçek Ansiklopedisi - Görsel İndirme")
    print("=" * 60)

    # Görsel klasörünü oluştur
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # İlerlemeyi yükle
    progress = load_progress()

    # İşlenecek bitkileri filtrele
    plants_to_process = [p for p in PLANTS if create_slug(p[0]) not in progress["downloaded"]]

    print(f"\nToplam bitki: {len(PLANTS)}")
    print(f"İndirilmiş: {len(progress['downloaded'])}")
    print(f"Görsel yok: {len(progress['no_image'])}")
    print(f"Başarısız: {len(progress['failed'])}")
    print(f"İşlenecek: {len(plants_to_process)}")

    if not plants_to_process:
        print("\nTüm bitkiler için görsel kontrol edilmiş!")

        # Attribution güncelle
        if progress["attributions"]:
            update_markdown_files(progress)
        return

    # Otomatik onay
    response = "e"
    print(f"\n{len(plants_to_process)} bitki için görsel aranacak. Otomatik devam ediliyor...")

    # Semaphore ile eşzamanlı istek limiti
    semaphore = asyncio.Semaphore(2)  # Aynı anda 2 istek

    results = []

    async with aiohttp.ClientSession() as session:
        for plant_data in tqdm(plants_to_process, desc="Görseller indiriliyor"):
            result = await process_plant(session, plant_data, semaphore, progress)

            if result:
                results.append(result)
                print(f"\n✓ {result['plant']} [{result['source']}]")

    # Attribution güncelle
    if progress["attributions"]:
        update_markdown_files(progress)

    # Özet
    print("\n" + "=" * 60)
    print("ÖZET")
    print("=" * 60)
    print(f"İndirilen: {len(results)}")
    print(f"Görsel bulunamayan: {len(progress['no_image'])}")
    print(f"Başarısız: {len(progress['failed'])}")

    if progress["no_image"]:
        print("\nGörsel bulunamayanlar (placeholder kullanılacak):")
        for plant in progress["no_image"][:10]:
            print(f"  - {plant}")
        if len(progress["no_image"]) > 10:
            print(f"  ... ve {len(progress['no_image']) - 10} tane daha")


def download_single(plant_name):
    """Tek bir bitki için görsel indir"""
    from plants_database import get_plant_by_name

    plant_data = get_plant_by_name(plant_name)
    if not plant_data:
        print(f"Bitki bulunamadı: {plant_name}")
        return

    print(f"Görsel aranıyor: {plant_name}...")

    progress = load_progress()

    async def run():
        semaphore = asyncio.Semaphore(1)
        async with aiohttp.ClientSession() as session:
            result = await process_plant(session, plant_data, semaphore, progress)

            if result:
                print(f"✓ İndirildi: {result['path']}")
                print(f"Kaynak: {result['source']}")
                print(f"Attribution: {result['attribution']}")

                # Attribution güncelle
                update_markdown_files(progress)
            else:
                print("❌ Görsel bulunamadı")

    asyncio.run(run())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Tek bitki için indir
        plant_name = " ".join(sys.argv[1:])
        download_single(plant_name)
    else:
        # Tüm bitkiler için indir
        asyncio.run(main())
