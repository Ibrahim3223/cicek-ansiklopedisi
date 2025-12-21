#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hugo Alias Ekleme - Backlink URL'lerini Yeni Sayfalara Yönlendir
"""

import csv
from pathlib import Path
import re

# Klasörler
CONTENT_DIR = Path(__file__).parent.parent / 'hugo-site' / 'content'
CSV_FILE = Path(__file__).parent.parent / 'data' / 'backlink_bitkiler.csv'

def normalize_filename(text):
    """Türkçe karakterleri normalize et"""
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

    text = text.lower().replace(' ', '-')
    safe_chars = 'abcdefghijklmnopqrstuvwxyz0-9-'
    text = ''.join(c for c in text if c in safe_chars)
    return text

def add_alias_to_frontmatter(md_file, old_url):
    """Markdown dosyasına alias ekle"""
    if not md_file.exists():
        print(f"X Dosya bulunamadi: {md_file}")
        return False

    # Dosyayı oku
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Frontmatter'ı bul
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not frontmatter_match:
        print(f"! Frontmatter bulunamadi: {md_file}")
        return False

    frontmatter = frontmatter_match.group(1)
    body = frontmatter_match.group(2)

    # Zaten alias var mı kontrol et
    if 'aliases:' in frontmatter:
        # Varolan aliases'a ekle
        if old_url in frontmatter:
            print(f"- Zaten var: {md_file.name}")
            return False

        # aliases: satırını bul ve altına ekle
        lines = frontmatter.split('\n')
        new_lines = []
        found_aliases = False

        for line in lines:
            new_lines.append(line)
            if line.startswith('aliases:'):
                found_aliases = True
                new_lines.append(f'  - {old_url}')

        if not found_aliases:
            # aliases: yoksa draft: satırından önce ekle
            new_lines = []
            for line in lines:
                if line.startswith('draft:'):
                    new_lines.append('aliases:')
                    new_lines.append(f'  - {old_url}')
                new_lines.append(line)

        frontmatter = '\n'.join(new_lines)
    else:
        # Hiç aliases yok, draft: satırından önce ekle
        lines = frontmatter.split('\n')
        new_lines = []

        for line in lines:
            if line.startswith('draft:'):
                new_lines.append('aliases:')
                new_lines.append(f'  - {old_url}')
            new_lines.append(line)

        frontmatter = '\n'.join(new_lines)

    # Dosyayı yaz
    new_content = f"---\n{frontmatter}\n---\n{body}"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"+ Alias eklendi: {md_file.name} -> {old_url}")
    return True

def main():
    print("=" * 60)
    print("Hugo Alias Ekleme - Backlink Yonlendirme")
    print("=" * 60)
    print()

    if not CSV_FILE.exists():
        print(f"X CSV dosyasi bulunamadi: {CSV_FILE}")
        return

    # CSV'yi oku
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        plants = list(reader)

    print(f"{len(plants)} bitki bulundu\n")

    updated = 0
    skipped = 0

    for plant in plants:
        turkce_ad = plant['turkce_ad']
        kategori = plant['kategori']
        old_url = plant['old_url']

        # Dosya adını oluştur
        slug = normalize_filename(turkce_ad)

        # Dosyayı bul (hangi klasörde olursa olsun)
        md_file = None
        for folder in ['cicek', 'bitki', 'bahce-bitkileri', 'meyveler', 'sifali-bitkiler', 'ev-bitkileri']:
            potential_path = CONTENT_DIR / folder / f"{slug}.md"
            if potential_path.exists():
                md_file = potential_path
                break

        if not md_file:
            print(f"X Dosya bulunamadi: {slug}.md")
            skipped += 1
            continue

        # Alias ekle
        if add_alias_to_frontmatter(md_file, old_url):
            updated += 1
        else:
            skipped += 1

    print()
    print("=" * 60)
    print(f"+ Guncellenen: {updated}")
    print(f"- Atlanan: {skipped}")
    print("=" * 60)

if __name__ == "__main__":
    main()
