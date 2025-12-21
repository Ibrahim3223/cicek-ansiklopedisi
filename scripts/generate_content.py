"""
Groq API ile Bitki İçeriği Üretimi
Çiçek Ansiklopedisi için otomatik içerik oluşturma scripti
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
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from tqdm import tqdm

# Load environment variables
load_dotenv()

# Groq API settings
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"  # Hızlı ve ücretsiz model

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
CONTENT_DIR = PROJECT_DIR / "hugo-site" / "content"
PROGRESS_FILE = SCRIPT_DIR / "generation_progress.json"

# Rate limiting
REQUESTS_PER_MINUTE = 30
REQUEST_DELAY = 60 / REQUESTS_PER_MINUTE  # 2 seconds between requests

# Import plant database
sys.path.insert(0, str(SCRIPT_DIR))
from plants_database import PLANTS, get_plants_by_category

# System prompt for content generation
SYSTEM_PROMPT = """Sen Türkiye'nin en deneyimli botanik uzmanısın ve bitki bakımı konusunda 20 yıllık tecrübeye sahipsin.
Bitki ve çiçekler hakkında detaylı, doğru ve ilgi çekici içerikler yazıyorsun.

Yazım kuralları:
- Türkçe yaz, akıcı ve anlaşılır bir dil kullan
- Pratik bilgiler ve ipuçları ver
- Başlangıç seviyesinden uzmana kadar herkesin anlayabileceği şekilde yaz
- Markdown formatı kullan (## başlıklar, - listeler, **kalın**)
- Emoji kullanma
- Minimum 800 kelime yaz
- Her bölümü detaylı açıkla"""


def get_user_prompt(plant_name, latin_name, category, care_level, info):
    """Bitki için kullanıcı promptu oluştur"""

    category_names = {
        "ev-bitkileri": "ev bitkisi",
        "bahce-bitkileri": "bahçe bitkisi",
        "sukulent": "sukulent",
        "kaktus": "kaktüs",
        "sifali-bitkiler": "şifalı bitki",
        "sebzeler": "sebze",
        "meyveler": "meyve ağacı",
        "cicek": "çiçek"
    }

    category_tr = category_names.get(category, "bitki")

    return f"""'{plant_name}' ({latin_name}) hakkında kapsamlı bir rehber yaz.

Bu bir {category_tr}, bakım seviyesi: {care_level}

Bitki bilgileri:
- Familya: {info.get('familya', 'Bilinmiyor')}
- Ana Vatan: {info.get('anaVatan', 'Bilinmiyor')}
- Işık ihtiyacı: {info.get('isik', 'Orta')}
- Sulama: {info.get('sulama', 'Orta')}
- Nem: {info.get('nem', 'Orta')}
- Sıcaklık: {info.get('sicaklik', '18-24°C')}
- Zehirlilik: {info.get('zehirlilik', 'Bilinmiyor')}

İçerikte şu bölümler olsun:

## {plant_name} Nedir?
Bitkinin genel tanımı, görünümü ve özellikleri (en az 150 kelime)

## Bakım Rehberi
### Sulama
Detaylı sulama bilgileri, sıklık, mevsimsel değişiklikler (en az 100 kelime)

### Işık İhtiyacı
Işık gereksinimleri, ideal konum önerileri (en az 80 kelime)

### Toprak ve Saksı
Uygun toprak karışımı, saksı seçimi, drenaj (en az 100 kelime)

### Gübreleme
Gübre türleri, uygulama sıklığı, mevsimsel bakım (en az 80 kelime)

## Çoğaltma Yöntemleri
Çoğaltma teknikleri detaylı açıklama (en az 150 kelime)

## Hastalıklar ve Zararlılar
Yaygın sorunlar ve çözümleri (en az 150 kelime)

## Sık Yapılan Hatalar
Yeni başlayanların yaptığı hatalar ve nasıl önlenir (en az 100 kelime)

Sadece içeriği yaz, başlık veya meta bilgi ekleme."""


def generate_faq(plant_name, category):
    """Bitki için SSS oluştur"""
    category_names = {
        "ev-bitkileri": "ev bitkisi",
        "bahce-bitkileri": "bahçe bitkisi",
        "sukulent": "sukulent",
        "kaktus": "kaktüs",
        "sifali-bitkiler": "şifalı bitki",
        "sebzeler": "sebze",
        "meyveler": "meyve",
        "cicek": "çiçek"
    }
    cat_tr = category_names.get(category, "bitki")

    return [
        {
            "soru": f"{plant_name} ne sıklıkla sulanmalı?",
            "cevap": f"{plant_name} sulaması toprağın kuruluğuna göre yapılmalıdır. Parmağınızı toprağa batırarak kontrol edin."
        },
        {
            "soru": f"{plant_name} için ideal ışık koşulları nelerdir?",
            "cevap": f"Bu {cat_tr} için uygun ışık koşulları detaylı bakım rehberinde açıklanmıştır."
        },
        {
            "soru": f"{plant_name} zehirli mi?",
            "cevap": f"Zehirlilik bilgisi bitki bilgi kartında belirtilmiştir. Evcil hayvan ve çocuklardan uzak tutun."
        },
        {
            "soru": f"{plant_name} nasıl çoğaltılır?",
            "cevap": f"Çoğaltma yöntemleri sayfada detaylı olarak açıklanmıştır."
        }
    ]


def create_frontmatter(plant_name, latin_name, category, care_level, info):
    """Hugo frontmatter oluştur"""

    # Slug oluştur (Türkçe karakterleri dönüştür)
    slug = plant_name.lower()
    tr_chars = {'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c',
                'İ': 'i', 'Ğ': 'g', 'Ü': 'u', 'Ş': 's', 'Ö': 'o', 'Ç': 'c', ' ': '-'}
    for tr, en in tr_chars.items():
        slug = slug.replace(tr, en)

    # Kategori belirleme
    if category == "cicek":
        content_type = "cicek"
        categories = ["cicek", "bahce-bitkileri"]
    else:
        content_type = "bitki"
        categories = [category]

    frontmatter = {
        "title": plant_name,
        "slug": slug,
        "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+03:00"),
        "lastmod": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+03:00"),
        "description": f"{plant_name} ({latin_name}) bakım rehberi. Sulama, ışık, toprak gereksinimleri ve çoğaltma yöntemleri.",
        "keywords": [plant_name, latin_name, f"{plant_name} bakımı", f"{plant_name} sulama", f"{plant_name} çoğaltma"],
        "categories": categories,
        "tags": [plant_name.lower(), category, care_level.lower()],
        "latince": latin_name,
        "tur": category.replace("-", " ").title(),
        "familya": info.get("familya", ""),
        "anaVatan": info.get("anaVatan", ""),
        "bakim_kolayligi": care_level,
        "isik": info.get("isik", ""),
        "sulama": info.get("sulama", ""),
        "nem": info.get("nem", ""),
        "sicaklik": info.get("sicaklik", ""),
        "toprak": "Humuslu, iyi drene",
        "gubre": "Büyüme döneminde aylık",
        "zehirlilik": info.get("zehirlilik", ""),
        "hava_temizleyici": info.get("hava_temizleyici", False),
        "cicek_acar": info.get("cicek_acar", False),
        "image": f"/images/bitkiler/{slug}.jpg",
        "image_attribution": "",
        "populer": True if care_level == "Kolay" else False,
        "draft": False,
        "sss": generate_faq(plant_name, category)
    }

    return frontmatter, slug, content_type


async def generate_content_async(session, plant_data, semaphore):
    """Asenkron içerik üretimi"""
    plant_name, latin_name, category, care_level, info = plant_data

    async with semaphore:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": get_user_prompt(plant_name, latin_name, category, care_level, info)}
            ],
            "temperature": 0.7,
            "max_tokens": 4000
        }

        try:
            async with session.post(GROQ_API_URL, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    content = data["choices"][0]["message"]["content"]
                    return plant_data, content, None
                else:
                    error = await response.text()
                    return plant_data, None, f"API Error {response.status}: {error}"
        except Exception as e:
            return plant_data, None, str(e)


def save_content(plant_data, content):
    """İçeriği dosyaya kaydet"""
    plant_name, latin_name, category, care_level, info = plant_data

    # Frontmatter oluştur
    frontmatter, slug, content_type = create_frontmatter(plant_name, latin_name, category, care_level, info)

    # Hedef dizin
    target_dir = CONTENT_DIR / content_type
    target_dir.mkdir(parents=True, exist_ok=True)

    # Markdown dosyası oluştur
    file_path = target_dir / f"{slug}.md"

    # YAML frontmatter formatla
    yaml_lines = ["---"]
    for key, value in frontmatter.items():
        if isinstance(value, bool):
            yaml_lines.append(f'{key}: {str(value).lower()}')
        elif isinstance(value, list):
            if key == "sss":
                yaml_lines.append(f'{key}:')
                for item in value:
                    yaml_lines.append(f'  - soru: "{item["soru"]}"')
                    yaml_lines.append(f'    cevap: "{item["cevap"]}"')
            else:
                yaml_lines.append(f'{key}: {json.dumps(value, ensure_ascii=False)}')
        elif isinstance(value, str) and ('"' in value or ':' in value or '\n' in value):
            yaml_lines.append(f'{key}: "{value}"')
        else:
            yaml_lines.append(f'{key}: {value}')
    yaml_lines.append("---\n")

    # Dosyayı yaz
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(yaml_lines))
        f.write(content)

    return file_path


def load_progress():
    """İlerleme dosyasını yükle"""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"completed": [], "failed": []}


def save_progress(progress):
    """İlerlemeyi kaydet"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


async def main():
    """Ana fonksiyon"""
    print("=" * 60)
    print("Çiçek Ansiklopedisi - İçerik Üretimi")
    print("=" * 60)

    if not GROQ_API_KEY:
        print("HATA: GROQ_API_KEY bulunamadı! .env dosyasını kontrol edin.")
        return

    # İlerlemeyi yükle
    progress = load_progress()
    completed = set(progress["completed"])

    # İşlenecek bitkileri filtrele
    plants_to_process = [p for p in PLANTS if p[0] not in completed]

    print(f"\nToplam bitki: {len(PLANTS)}")
    print(f"Tamamlanan: {len(completed)}")
    print(f"İşlenecek: {len(plants_to_process)}")

    if not plants_to_process:
        print("\nTüm bitkiler zaten işlenmiş!")
        return

    # Onay al
    response = input(f"\n{len(plants_to_process)} bitki için içerik üretilecek. Devam? (e/h): ")
    if response.lower() != 'e':
        print("İptal edildi.")
        return

    # Semaphore ile eşzamanlı istek limiti
    semaphore = asyncio.Semaphore(1)  # Aynı anda 1 istek (rate limit için)

    async with aiohttp.ClientSession() as session:
        for i, plant_data in enumerate(tqdm(plants_to_process, desc="İçerik üretiliyor")):
            plant_name = plant_data[0]

            # İçerik üret
            _, content, error = await generate_content_async(session, plant_data, semaphore)

            if error:
                print(f"\n❌ {plant_name}: {error}")
                progress["failed"].append({"name": plant_name, "error": error})
            else:
                # Kaydet
                file_path = save_content(plant_data, content)
                print(f"\n✓ {plant_name} -> {file_path.name}")
                progress["completed"].append(plant_name)

            # İlerlemeyi kaydet
            save_progress(progress)

            # Rate limiting
            if i < len(plants_to_process) - 1:
                await asyncio.sleep(REQUEST_DELAY)

    # Özet
    print("\n" + "=" * 60)
    print("ÖZET")
    print("=" * 60)
    print(f"Başarılı: {len(progress['completed'])}")
    print(f"Başarısız: {len(progress['failed'])}")

    if progress["failed"]:
        print("\nBaşarısız olanlar:")
        for item in progress["failed"]:
            print(f"  - {item['name']}: {item['error']}")


def generate_single(plant_name):
    """Tek bir bitki için içerik üret"""
    from plants_database import get_plant_by_name

    plant_data = get_plant_by_name(plant_name)
    if not plant_data:
        print(f"Bitki bulunamadı: {plant_name}")
        return

    print(f"İçerik üretiliyor: {plant_name}...")

    import requests

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    plant_name, latin_name, category, care_level, info = plant_data

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": get_user_prompt(plant_name, latin_name, category, care_level, info)}
        ],
        "temperature": 0.7,
        "max_tokens": 4000
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        content = response.json()["choices"][0]["message"]["content"]
        file_path = save_content(plant_data, content)
        print(f"✓ Kaydedildi: {file_path}")
    else:
        print(f"Hata: {response.status_code} - {response.text}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Tek bitki için üret
        plant_name = " ".join(sys.argv[1:])
        generate_single(plant_name)
    else:
        # Tüm bitkiler için üret
        asyncio.run(main())
