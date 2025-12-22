#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bitki gorsel indirici - iNaturalist > Trefle.io > Wikimedia siralamasi
Latince isimle nokta atisi arama
"""

import os
import sys
import glob
import requests
import time
import re
from pathlib import Path

# Windows console icin UTF-8
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Ayarlar
HUGO_CONTENT_DIR = "hugo-site/content"
HUGO_IMAGES_DIR = "hugo-site/static/images/bitkiler"
TREFLE_API_KEY = "usr-0LuXWX3-id0PoJRas8sdjy8Hy4Sy2IUJ0ReEjLjG9Cs"

# Klasor yoksa olustur
os.makedirs(HUGO_IMAGES_DIR, exist_ok=True)

def get_plants_without_images():
    """Gorsel eksik olan bitkilerin listesini dondur"""
    plants = []

    for md_file in glob.glob(f"{HUGO_CONTENT_DIR}/**/*.md", recursive=True):
        if "_index.md" in md_file:
            continue
        if md_file.endswith(("hakkimizda.md", "iletisim.md", "gizlilik-politikasi.md", "kullanim-sartlari.md")):
            continue

        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Frontmatter'i parse et
        title = ""
        latince = ""
        image = ""
        slug = ""

        in_frontmatter = False
        for line in content.split("\n"):
            if line.strip() == "---":
                if in_frontmatter:
                    break
                in_frontmatter = True
                continue

            if in_frontmatter:
                if line.startswith("title:"):
                    title = line.replace("title:", "").strip().strip('"\'')
                elif line.startswith("latince:"):
                    latince = line.replace("latince:", "").strip().strip('"\'')
                elif line.startswith("image:"):
                    image = line.replace("image:", "").strip().strip('"\'')
                elif line.startswith("slug:"):
                    slug = line.replace("slug:", "").strip().strip('"\'')

        # Gorsel bossa listeye ekle
        if not image and latince:
            plants.append({
                "file": md_file,
                "title": title,
                "latince": latince,
                "slug": slug
            })

    return plants


def clean_latin_name(name):
    """Latince ismi temizle - sadece genus species kalsin"""
    # Parantez icindeki seyleri kaldir
    name = re.sub(r'\([^)]*\)', '', name)
    # Ekstra kelimeleri kaldir (var., subsp., cultivar isimleri vs.)
    parts = name.strip().split()
    if len(parts) >= 2:
        # Sadece ilk iki kelimeyi al (genus + species)
        return f"{parts[0]} {parts[1]}"
    return name.strip()


def search_inaturalist(latin_name):
    """iNaturalist'te gorsel ara - gercek doga fotograflari"""
    clean_name = clean_latin_name(latin_name)

    url = "https://api.inaturalist.org/v1/taxa"
    params = {
        "q": clean_name,
        "rank": "species,genus",
        "per_page": 5
    }

    headers = {
        "User-Agent": "PlantEncyclopedia/1.0 (cicekansiklopedisi.com)"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        if response.status_code != 200:
            return None

        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            for result in data["results"]:
                # Isim eslesmesini kontrol et
                result_name = result.get("name", "").lower()
                search_name = clean_name.lower()

                # Genus veya tam isim eslesmesi
                if search_name.split()[0] in result_name or result_name in search_name:
                    if "default_photo" in result and result["default_photo"]:
                        photo = result["default_photo"]
                        # medium veya original URL'i al
                        if "medium_url" in photo and photo["medium_url"]:
                            return photo["medium_url"]
                        elif "url" in photo and photo["url"]:
                            return photo["url"]
    except Exception as e:
        pass

    return None


def search_trefle(latin_name):
    """Trefle.io'da gorsel ara - botanik veritabani"""
    clean_name = clean_latin_name(latin_name)

    url = "https://trefle.io/api/v1/plants/search"
    params = {
        "token": TREFLE_API_KEY,
        "q": clean_name
    }

    headers = {
        "User-Agent": "PlantEncyclopedia/1.0 (cicekansiklopedisi.com)"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        if response.status_code != 200:
            return None

        data = response.json()

        if "data" in data and len(data["data"]) > 0:
            for plant in data["data"]:
                # Isim eslesmesini kontrol et
                plant_name = plant.get("scientific_name", "").lower()
                search_name = clean_name.lower()

                if search_name.split()[0] in plant_name or plant_name.startswith(search_name.split()[0]):
                    if "image_url" in plant and plant["image_url"]:
                        return plant["image_url"]
    except Exception as e:
        pass

    return None


def search_wikimedia(latin_name):
    """Wikimedia Commons'ta gorsel ara - son care"""
    clean_name = clean_latin_name(latin_name)

    # Wikipedia API ile dene
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": clean_name,
        "prop": "pageimages",
        "pithumbsize": "800",
        "redirects": "1"
    }

    headers = {
        "User-Agent": "PlantEncyclopedia/1.0 (cicekansiklopedisi.com)"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        if response.status_code != 200:
            return None

        data = response.json()

        if "query" in data and "pages" in data["query"]:
            pages = data["query"]["pages"]
            for page_id, page in pages.items():
                if "thumbnail" in page:
                    return page["thumbnail"]["source"]
    except Exception as e:
        pass

    return None


def download_image(url, save_path):
    """Gorseli indir"""
    try:
        headers = {
            "User-Agent": "PlantEncyclopedia/1.0 (cicekansiklopedisi.com)"
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        # Dosya boyutunu kontrol et (en az 5KB olmali)
        if len(response.content) < 5000:
            return False

        with open(save_path, "wb") as f:
            f.write(response.content)

        return True
    except Exception as e:
        return False


def update_frontmatter(file_path, image_path):
    """Frontmatter'daki image alanini guncelle"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    new_lines = []
    updated = False

    for line in lines:
        if line.startswith("image:") and not updated:
            new_lines.append(f"image: {image_path}")
            updated = True
        else:
            new_lines.append(line)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))


def main():
    print("=" * 60)
    print("Bitki Gorsel Indirici")
    print("Siralama: iNaturalist > Trefle.io > Wikimedia")
    print("=" * 60)

    plants = get_plants_without_images()
    total = len(plants)
    print(f"\nToplam {total} bitki icin gorsel eksik.\n")

    stats = {
        "inaturalist": 0,
        "trefle": 0,
        "wikimedia": 0,
        "not_found": 0
    }
    not_found_list = []

    for i, plant in enumerate(plants):
        print(f"[{i+1}/{total}] {plant['title']} ({plant['latince']})")

        image_url = None
        source = None

        # 1. iNaturalist
        image_url = search_inaturalist(plant['latince'])
        if image_url:
            source = "iNaturalist"

        # 2. Trefle.io
        if not image_url:
            image_url = search_trefle(plant['latince'])
            if image_url:
                source = "Trefle"

        # 3. Wikimedia
        if not image_url:
            image_url = search_wikimedia(plant['latince'])
            if image_url:
                source = "Wikimedia"

        if image_url:
            # Dosya uzantisi
            ext = ".jpg"
            url_lower = image_url.lower()
            if ".png" in url_lower:
                ext = ".png"
            elif ".gif" in url_lower:
                ext = ".gif"

            filename = f"{plant['slug']}{ext}"
            save_path = os.path.join(HUGO_IMAGES_DIR, filename)

            if download_image(image_url, save_path):
                image_hugo_path = f"/images/bitkiler/{filename}"
                update_frontmatter(plant['file'], image_hugo_path)
                print(f"  [OK] {source}: {filename}")
                stats[source.lower()] = stats.get(source.lower(), 0) + 1
            else:
                print(f"  [HATA] Indirilemedi")
                stats["not_found"] += 1
                not_found_list.append(plant['title'])
        else:
            print(f"  [YOK] Hicbir kaynakta bulunamadi")
            stats["not_found"] += 1
            not_found_list.append(plant['title'])

        # Rate limiting
        time.sleep(0.5)

    print("\n" + "=" * 60)
    print("SONUC")
    print("=" * 60)
    print(f"iNaturalist: {stats['inaturalist']}")
    print(f"Trefle.io: {stats['trefle']}")
    print(f"Wikimedia: {stats['wikimedia']}")
    print(f"Bulunamayan: {stats['not_found']}")

    found = stats['inaturalist'] + stats['trefle'] + stats['wikimedia']
    print(f"\nToplam basari: {found}/{total} ({100*found/total:.1f}%)")

    if not_found_list and len(not_found_list) <= 30:
        print("\nBulunamayan bitkiler:")
        for name in not_found_list:
            print(f"  - {name}")


if __name__ == "__main__":
    main()
