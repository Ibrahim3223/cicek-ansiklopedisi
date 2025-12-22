#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Wikimedia Commons'tan eksik bitki gorsellerini indiren script
"""

import os
import sys
import glob
import requests
import time
import re
import urllib.parse
from pathlib import Path

# Windows console icin UTF-8
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Ayarlar
HUGO_CONTENT_DIR = "hugo-site/content"
HUGO_IMAGES_DIR = "hugo-site/static/images/bitkiler"

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

def search_wikimedia_image(search_term):
    """Wikimedia Commons'ta gorsel ara"""
    api_url = "https://commons.wikimedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrnamespace": "6",
        "gsrsearch": f"filetype:bitmap {search_term}",
        "gsrlimit": "5",
        "prop": "imageinfo",
        "iiprop": "url|extmetadata",
        "iiurlwidth": "800"
    }

    headers = {
        "User-Agent": "PlantEncyclopedia/1.0 (https://cicekansiklopedisi.com)"
    }

    try:
        response = requests.get(api_url, params=params, headers=headers, timeout=15)
        if response.status_code != 200:
            return None

        data = response.json()

        if "query" in data and "pages" in data["query"]:
            pages = data["query"]["pages"]
            for page_id, page in pages.items():
                if "imageinfo" in page:
                    info = page["imageinfo"][0]
                    if "thumburl" in info:
                        return info["thumburl"]
                    elif "url" in info:
                        return info["url"]
    except Exception as e:
        pass

    return None

def search_wikipedia_image(search_term):
    """Wikipedia'dan gorsel ara"""
    # Ingilizce Wikipedia (daha cok icerik)
    api_url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "titles": search_term,
        "prop": "pageimages",
        "pithumbsize": "800",
        "redirects": "1"
    }

    headers = {
        "User-Agent": "PlantEncyclopedia/1.0 (https://cicekansiklopedisi.com)"
    }

    try:
        response = requests.get(api_url, params=params, headers=headers, timeout=15)
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
            "User-Agent": "PlantEncyclopedia/1.0 (https://cicekansiklopedisi.com)"
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

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
    print("Wikimedia Commons Gorsel Indirici")
    print("=" * 60)

    plants = get_plants_without_images()
    total = len(plants)
    print(f"\nToplam {total} bitki icin gorsel eksik.\n")

    found = 0
    not_found = 0
    not_found_list = []

    for i, plant in enumerate(plants):
        print(f"[{i+1}/{total}] {plant['title']} ({plant['latince']})")

        # Latince isimle Wikipedia'da ara (en iyi sonuc)
        image_url = search_wikipedia_image(plant['latince'])

        # Bulunamazsa Wikimedia Commons'ta ara
        if not image_url:
            image_url = search_wikimedia_image(plant['latince'])

        # Hala bulunamazsa sadece genus (ilk kelime) ile dene
        if not image_url and ' ' in plant['latince']:
            genus = plant['latince'].split()[0]
            image_url = search_wikipedia_image(genus)

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
                print(f"  [OK] Indirildi: {filename}")
                found += 1
            else:
                print(f"  [HATA] Indirilemedi")
                not_found += 1
                not_found_list.append(plant['title'])
        else:
            print(f"  [YOK] Gorsel bulunamadi")
            not_found += 1
            not_found_list.append(plant['title'])

        # Rate limiting
        time.sleep(0.3)

    print("\n" + "=" * 60)
    print("SONUC")
    print("=" * 60)
    print(f"[OK] Bulunan ve indirilen: {found}")
    print(f"[YOK] Bulunamayan: {not_found}")
    print(f"Basari orani: {found}/{total} ({100*found/total:.1f}%)")

    if not_found_list and len(not_found_list) <= 50:
        print("\nBulunamayan bitkiler:")
        for name in not_found_list:
            print(f"  - {name}")

if __name__ == "__main__":
    main()
