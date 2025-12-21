#!/usr/bin/env python3
"""
Bitki markdown dosyalarına image path ekle
"""

import os
import sys
from pathlib import Path

# UTF-8 encoding fix for Windows
if sys.platform == "win32":
    import io
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).parent.parent
IMAGES_DIR = BASE_DIR / "hugo-site" / "static" / "images" / "bitkiler"


def update_markdown_file(md_file):
    """Markdown dosyasına image path ekle veya güncelle"""
    slug = md_file.stem
    image_path = IMAGES_DIR / f"{slug}.jpg"

    if not image_path.exists():
        return False

    # Read file
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    image_value = f'/images/bitkiler/{slug}.jpg'
    updated = False

    # Find and update image line
    for i, line in enumerate(lines):
        # Check if line is "image:" with empty or wrong value
        if line.startswith('image:'):
            current_value = line.split(':', 1)[1].strip()
            if not current_value or current_value != image_value:
                lines[i] = f'image: {image_value}\n'
                updated = True
            else:
                # Already has correct value
                return False
            break

    if not updated:
        return False

    # Write back
    with open(md_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    return True


def main():
    print("=" * 60)
    print("🖼️  Bitki Görsel Path Güncelleme")
    print("=" * 60)

    content_dirs = [
        BASE_DIR / "hugo-site" / "content" / "bitki",
        BASE_DIR / "hugo-site" / "content" / "cicek",
    ]

    updated = 0
    skipped = 0

    for content_dir in content_dirs:
        if not content_dir.exists():
            continue

        for md_file in content_dir.glob("*.md"):
            slug = md_file.stem
            if update_markdown_file(md_file):
                print(f"✅ {slug}.md - image path eklendi")
                updated += 1
            else:
                print(f"⏭️  {slug}.md - atlandı (görsel yok veya zaten var)")
                skipped += 1

    print("\n" + "=" * 60)
    print(f"✅ Güncellenen: {updated}")
    print(f"⏭️  Atlanan: {skipped}")


if __name__ == "__main__":
    main()
