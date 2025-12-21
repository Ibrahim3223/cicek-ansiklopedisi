# 🌿 Bitki İçerik Üretim Sistemi - Kullanım Kılavuzu

## 📋 İçindekiler
1. [Hızlı Başlangıç](#hızlı-başlangıç)
2. [Toplu Üretim (1000+ Bitki)](#toplu-üretim)
3. [Tek Bitki Üretimi](#tek-bitki-üretimi)
4. [Görsel İndirme](#görsel-indirme)
5. [İlerleme Takibi](#ilerleme-takibi)
6. [Sorun Giderme](#sorun-giderme)

---

## 🚀 Hızlı Başlangıç

### Gereksinimler
- Python 3.x kurulu olmalı
- GROQ_API_KEY `.env` dosyasında tanımlı olmalı
- İnternet bağlantısı (API ve görsel indirme için)

### Kurulum Kontrolü
```bash
# Python versiyonunu kontrol et
python --version

# Gerekli paketleri kontrol et
pip list | grep -E "requests|Pillow|groq"

# Eğer eksikse kur
pip install requests Pillow groq python-dotenv
```

---

## 📦 Toplu Üretim (1000+ Bitki)

### Adım 1: CSV Dosyasını Kontrol Et
CSV dosyası hazır: `data/bitki_listesi_1000.csv`
- **1052 bitki** tanımlı
- Türkçe ad, Latin ad ve kategori bilgileri mevcut

### Adım 2: Toplu Üretimi Başlat

#### Tüm 1052 bitkiyi üretmek için:
```bash
cd "c:\Users\Dante\Desktop\Yeniden\WebSite\bitki-sitesi"
python scripts/generate_all.py --input data/bitki_listesi_1000.csv --start 1 --end 1052
```

#### Küçük gruplar halinde üretmek için (ÖNER İLEN):
```bash
# İlk 100 bitki
python scripts/generate_all.py --input data/bitki_listesi_1000.csv --start 1 --end 100

# İkinci 100 bitki
python scripts/generate_all.py --input data/bitki_listesi_1000.csv --start 101 --end 200

# Üçüncü 100 bitki
python scripts/generate_all.py --input data/bitki_listesi_1000.csv --start 201 --end 300

# ...ve böyle devam
```

**Neden küçük gruplar halinde?**
- Her 10 bitkide 5 saniye bekleme var (API rate limit)
- Hata olursa sadece o grubu tekrar çalıştırırsın
- İlerlemeyi daha kolay takip edersin

### Adım 3: Parametreler

#### Temel Parametreler:
```bash
--input     # CSV dosya yolu (zorunlu)
--start     # Başlangıç satırı (varsayılan: 1)
--end       # Bitiş satırı (varsayılan: CSV'deki toplam satır)
```

#### Opsiyonel Parametreler:
```bash
--resume    # Kaldığı yerden devam et (progress.json'dan)
--force     # Varolan dosyaların üzerine yaz
```

#### Kullanım Örnekleri:
```bash
# Kaldığı yerden devam et
python scripts/generate_all.py --input data/bitki_listesi_1000.csv --resume

# Varolan dosyaları atla
python scripts/generate_all.py --input data/bitki_listesi_1000.csv --start 1 --end 100

# Varolan dosyaların üzerine yaz
python scripts/generate_all.py --input data/bitki_listesi_1000.csv --start 1 --end 100 --force
```

---

## 🎯 Tek Bitki Üretimi

Manuel test veya özel bitkiler için:

```bash
python scripts/generate_plant.py --name "Lavanta" --latin "Lavandula" --category "bahce-bitkileri"
```

### Parametreler:
```bash
--name          # Türkçe bitki adı (zorunlu)
--latin         # Latin (bilimsel) adı (zorunlu)
--category      # Kategori (zorunlu)
--skip-image    # Görsel indirmeyi atla
--skip-content  # İçerik üretimini atla (sadece görsel indir)
```

### Örnekler:
```bash
# Tam üretim (içerik + görsel)
python scripts/generate_plant.py --name "Gül" --latin "Rosa" --category "cicek"

# Sadece içerik (görsel zaten varsa)
python scripts/generate_plant.py --name "Gül" --latin "Rosa" --category "cicek" --skip-image

# Sadece görsel (içerik zaten varsa)
python scripts/generate_plant.py --name "Gül" --latin "Rosa" --category "cicek" --skip-content
```

---

## 🖼️ Görsel İndirme

İçerik üretildikten sonra görselleri ayrıca güncellemek için:

### Tüm Bitkiler İçin Görsel İndir:
```bash
python scripts/fetch_images.py --all
```

### Sadece Görseli Olmayan Bitkiler:
```bash
python scripts/fetch_images.py --missing
```

### Tek Bitki İçin:
```bash
python scripts/fetch_images.py --plant monstera
```

### Test Modu (indirmeden önce kontrol et):
```bash
python scripts/fetch_images.py --all --dry-run
```

---

## 📊 İlerleme Takibi

### 1. Progress Dosyası
Üretim sırasında `data/generation_progress.json` dosyası oluşturulur:

```json
{
  "completed": ["gul", "papatya", "lale"],
  "failed": ["orkide"],
  "last_index": 3
}
```

### 2. Log Dosyası
Hatalar `data/generation_errors.log` dosyasına kaydedilir:

```
2025-12-21 18:00:00 - ERROR - orkide: API hatası
```

### 3. Canlı Çıktı
Script çalışırken şunları göreceksin:

```
============================================================
🌿 Gül (Rosa)
============================================================
📸 Görsel indiriliyor...
   ✅ Görsel indirildi
📝 İçerik üretiliyor (Groq API)...
   ✅ İçerik oluşturuldu (632 kelime)
❓ FAQ üretiliyor...
   ✅ 4 FAQ oluşturuldu
💾 Markdown dosyası oluşturuluyor...
   ✅ Oluşturuldu: gul.md

📊 İlerleme: 1/100 (1 başarılı, 0 başarısız)
```

### 4. Hugo Server
Hugo otomatik olarak yeni sayfaları algılar ve rebuild eder.

---

## ⏱️ Süre Tahmini

### Tek Bitki Başına:
- **Görsel indirme:** 3-5 saniye
- **İçerik üretimi (Groq):** 5-10 saniye
- **FAQ üretimi (Groq):** 3-5 saniye
- **Toplam:** ~15-20 saniye

### 100 Bitki:
- **Süre:** ~25-35 dakika
- **Rate limit beklemesi:** +45 saniye (her 10 bitkide 5 saniye)
- **Toplam:** ~30-40 dakika

### 1000 Bitki:
- **Süre:** ~4-6 saat
- **Rate limit beklemesi:** +8 dakika
- **Toplam:** ~5-7 saat

**ÖNERİ:** Bilgisayarı çalışır durumda bırak, geceleri çalıştır.

---

## 🛠️ Sorun Giderme

### Sorun 1: API Rate Limit Hatası
**Çözüm:** Script zaten her 10 bitkide 5 saniye bekliyor. Eğer yine hata alırsan:
```bash
# Daha uzun bekleme süresi ekle (generate_all.py içinde)
time.sleep(10)  # 5 yerine 10 saniye yap
```

### Sorun 2: Görsel Bulunamadı
**Sebep:** Latin adı çok genel veya yanlış
**Çözüm:** CSV'de Latin adını düzelt ve tekrar çalıştır:
```bash
python scripts/fetch_images.py --plant bitki-adi
```

### Sorun 3: API Anahtarı Hatası
**Kontrol:**
```bash
# .env dosyasını kontrol et
cat .env | grep GROQ_API_KEY
```

### Sorun 4: Script Durdu
**Kaldığı yerden devam et:**
```bash
python scripts/generate_all.py --input data/bitki_listesi_1000.csv --resume
```

### Sorun 5: Disk Doldu
**Kontrol:**
```bash
# Görsel klasörü boyutu
du -sh hugo-site/static/images/bitkiler

# Beklenen boyut: ~500MB-1GB (1000 bitki için)
```

---

## 📈 Önerilen İş Akışı

### Senaryo 1: Tüm 1000+ Bitkiyi Üret (Gece Boyunca)
```bash
# Akşam başlat
python scripts/generate_all.py --input data/bitki_listesi_1000.csv --start 1 --end 1052

# Sabah kontrol et
cat data/generation_errors.log

# Başarısızları tekrar üret
python scripts/generate_all.py --input data/bitki_listesi_1000.csv --resume --force
```

### Senaryo 2: 100'er 100'er Üret (Kontrollü)
```bash
# Her gün 100 bitki
python scripts/generate_all.py --input data/bitki_listesi_1000.csv --start 1 --end 100
# İzle, kontrol et, sorunları çöz

# Ertesi gün
python scripts/generate_all.py --input data/bitki_listesi_1000.csv --start 101 --end 200
# 10 gün içinde tamamla
```

### Senaryo 3: Test Et Sonra Üret
```bash
# İlk 10 bitkiyi test et
python scripts/generate_all.py --input data/bitki_listesi_1000.csv --start 1 --end 10

# Sonuçları kontrol et
ls hugo-site/content/cicek/
ls hugo-site/static/images/bitkiler/

# Sorun yoksa devam et
python scripts/generate_all.py --input data/bitki_listesi_1000.csv --start 11 --end 1052
```

---

## ✅ Kontrol Listesi

Üretim Öncesi:
- [ ] Python 3.x kurulu
- [ ] Gerekli paketler kurulu (requests, Pillow, groq)
- [ ] .env dosyasında GROQ_API_KEY var
- [ ] CSV dosyası hazır (bitki_listesi_1000.csv)
- [ ] Yeterli disk alanı var (~2GB)
- [ ] İnternet bağlantısı stabil

Üretim Sırasında:
- [ ] İlerlemeyi takip et (her 10-20 dakikada kontrol)
- [ ] Hata loglarını kontrol et
- [ ] Hugo server çalışıyor mu kontrol et
- [ ] Disk alanını izle

Üretim Sonrası:
- [ ] Başarısız bitkileri kontrol et (generation_errors.log)
- [ ] Görsel olmayan bitkileri kontrol et (--missing ile)
- [ ] Hugo build yap (hugo --buildDrafts)
- [ ] Örnek sayfaları tarayıcıda test et

---

## 🎯 Hızlı Komutlar

```bash
# Test - İlk 5 bitki
python scripts/generate_all.py --input data/bitki_listesi_1000.csv --start 1 --end 5

# Küçük batch - 50 bitki
python scripts/generate_all.py --input data/bitki_listesi_1000.csv --start 1 --end 50

# Orta batch - 100 bitki
python scripts/generate_all.py --input data/bitki_listesi_1000.csv --start 1 --end 100

# Büyük batch - 500 bitki
python scripts/generate_all.py --input data/bitki_listesi_1000.csv --start 1 --end 500

# TAM LİSTE - 1052 bitki (5-7 saat)
python scripts/generate_all.py --input data/bitki_listesi_1000.csv --start 1 --end 1052

# Kaldığı yerden devam
python scripts/generate_all.py --input data/bitki_listesi_1000.csv --resume

# Görselleri güncelle
python scripts/fetch_images.py --missing
```

---

## 💡 İpuçları

1. **İlk kez çalıştırıyorsan:** 10 bitkiyle test et
2. **Gece çalıştır:** Bilgisayarı sabaha bırak
3. **Gruplar halinde:** 100'er 100'er daha güvenli
4. **Hataları kaydet:** Log dosyalarını sakla
5. **Yedekle:** Her 200 bitkide bir backup al
6. **Hugo server:** Açık bırak, otomatik rebuild için
7. **İzle:** İlk 1-2 saatte yakından takip et
8. **Sabırlı ol:** 1000 bitki 5-7 saat sürer

---

## 📞 Destek

Sorun yaşarsan:
1. Log dosyalarını kontrol et (`data/generation_errors.log`)
2. Progress dosyasını kontrol et (`data/generation_progress.json`)
3. Script çıktısını oku (hangi adımda hata verdi?)
4. Tek bitki ile test et (`generate_plant.py`)
5. API anahtarını kontrol et (`.env`)

---

**Başarılar! 🌿**

1052 bitki başarıyla üretildiğinde siteniz Türkiye'nin en kapsamlı çiçek ansiklopedisi olacak!
