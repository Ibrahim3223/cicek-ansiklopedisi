# Çiçek Ansiklopedisi

Türkiye'nin en kapsamlı bitki ve çiçek ansiklopedisi. Hugo static site generator ve Groq API ile otomatik içerik üretimi.

## 🌱 Özellikler

- **85+ Bitki Türü** - Ev bitkileri, bahçe bitkileri, sukulentler, kaktüsler, şifalı bitkiler, sebzeler, meyveler
- **Otomatik İçerik Üretimi** - Groq API (Llama 3.1) ile detaylı bakım rehberleri
- **Otomatik Görsel Sistemi** - Wikimedia Commons ve iNaturalist API entegrasyonu
- **SEO Optimizasyonu** - JSON-LD şema, meta tags, breadcrumb
- **Responsive Tasarım** - Mobil ve desktop için optimize edilmiş
- **Arama Sistemi** - Gerçek zamanlı Türkçe arama (karakter normalizasyonu)

## 📁 Proje Yapısı

```
bitki-sitesi/
├── .env                    # API anahtarları (git'e gitmez)
├── .gitignore
├── requirements.txt        # Python bağımlılıkları
├── README.md
├── hugo-site/
│   ├── config.toml        # Hugo yapılandırması
│   ├── content/           # Markdown içerikler
│   │   ├── bitki/         # Bitki sayfaları
│   │   ├── cicek/         # Çiçek sayfaları
│   │   ├── ev-bitkileri/
│   │   ├── bahce-bitkileri/
│   │   ├── sukulent/
│   │   ├── kaktus/
│   │   ├── sifali-bitkiler/
│   │   ├── sebzeler/
│   │   └── meyveler/
│   ├── layouts/           # Hugo şablonları
│   │   ├── _default/
│   │   ├── bitki/
│   │   ├── cicek/
│   │   ├── partials/
│   │   ├── index.html
│   │   └── index.json
│   └── static/            # Statik dosyalar
│       ├── css/style.css
│       ├── js/main.js
│       ├── images/bitkiler/
│       └── favicons/
└── scripts/               # Python scriptleri
    ├── plants_database.py      # Bitki veritabanı (85+ bitki)
    ├── generate_content.py     # Groq ile içerik üretimi
    ├── download_images.py      # Görsel indirme
    └── instant_indexing.py     # Google Indexing API (opsiyonel)
```

## 🚀 Kurulum

### 1. Gereksinimleri Yükle

```bash
# Python bağımlılıkları
pip install -r requirements.txt

# Hugo'yu yükle (Windows için)
# https://gohugo.io/installation/windows/
choco install hugo-extended

# veya elle indir:
# https://github.com/gohugoio/hugo/releases
```

### 2. API Key'i Ayarla

`.env` dosyasındaki `GROQ_API_KEY` değerini kendi API key'iniz ile değiştirin.

Groq API key almak için: https://console.groq.com/

### 3. İçerik Üret

```bash
# Tüm bitkiler için içerik üret (85+ bitki)
cd scripts
python generate_content.py

# Tek bir bitki için içerik üret
python generate_content.py Monstera
```

### 4. Görselleri İndir

```bash
# Tüm bitkiler için görsel indir
python download_images.py

# Tek bir bitki için görsel indir
python download_images.py Monstera
```

### 5. Hugo Sitesini Çalıştır

```bash
cd hugo-site

# Development server (localhost:1313)
hugo server -D

# Production build
hugo
```

## 📝 İçerik Üretimi

### Groq API

`scripts/generate_content.py` scripti her bitki için şu bölümleri üretir:

- Bitki hakkında genel bilgi
- Detaylı bakım rehberi (sulama, ışık, toprak, gübre)
- Çoğaltma yöntemleri
- Hastalıklar ve zararlılar
- Sık yapılan hatalar
- SSS (Sık Sorulan Sorular)

### Markdown Format

```yaml
---
title: "Monstera"
slug: "monstera"
latince: "Monstera deliciosa"
categories: ["ev-bitkileri"]
bakim_kolayligi: "Kolay"
isik: "Parlak dolaylı"
sulama: "Haftada 1-2"
...
---

## İçerik markdown formatında...
```

## 🖼️ Görsel Sistemi

### Kaynak Önceliği

1. **Wikimedia Commons** - Açık lisanslı görseller (CC BY-SA)
2. **iNaturalist** - Topluluk fotoğrafları (CC BY)
3. **Placeholder** - Görsel bulunamazsa 🌱 emoji

### Attribution

Tüm görseller için kaynak bilgisi otomatik olarak frontmatter'a eklenir:

```yaml
image: "/images/bitkiler/monstera.jpg"
image_attribution: "Photo by User via Wikimedia Commons (CC BY-SA 4.0)"
```

## 🎨 Tasarım

### Renk Paleti

- **Primary**: `#16a34a` (Yeşil)
- **Secondary**: `#059669` (Koyu yeşil)
- **Accent**: `#f59e0b` (Turuncu)

### Kategori Renkleri

- Ev Bitkileri: Yeşil (`#10b981`)
- Bahçe Bitkileri: Mavi (`#3b82f6`)
- Sukulentler: Mor (`#8b5cf6`)
- Kaktüsler: Turuncu (`#f97316`)
- Şifalı Bitkiler: Pembe (`#ec4899`)
- Sebzeler: Lime (`#84cc16`)
- Meyveler: Kırmızı (`#ef4444`)

## 🔍 Arama Sistemi

JavaScript ile gerçek zamanlı arama:

- Türkçe karakter normalizasyonu (ı→i, ğ→g, ü→u, ş→s, ö→o, ç→c)
- Bitki adı, Latince adı ve açıklamada arama
- Debounce (200ms)
- İlk 8 sonucu göster

## 📊 SEO

### JSON-LD Şemalar

- **WebSite** - Ana sayfa
- **Organization** - Kuruluş bilgisi
- **Article** - Bitki sayfaları
- **BreadcrumbList** - Breadcrumb navigasyon
- **FAQPage** - SSS bölümü

### Meta Tags

- Title, description, keywords
- Open Graph (Facebook, WhatsApp)
- Twitter Card
- Canonical URL

## 🛠️ Geliştirme

### Yeni Bitki Eklemek

1. `scripts/plants_database.py` dosyasına bitki ekle:

```python
("Bitki Adı", "Latince Ad", "kategori", "Kolay", {
    "familya": "...",
    "anaVatan": "...",
    # ... diğer bilgiler
})
```

2. İçerik üret:

```bash
python scripts/generate_content.py "Bitki Adı"
```

3. Görsel indir:

```bash
python scripts/download_images.py "Bitki Adı"
```

### Hugo Komutları

```bash
# Development server
hugo server -D

# Production build
hugo

# Temizle
hugo --gc

# Taslakları dahil et
hugo server -D --buildDrafts
```

## 📦 Deployment

### Netlify

1. GitHub'a push et
2. Netlify'da yeni site oluştur
3. Build ayarları:
   - Build command: `hugo`
   - Publish directory: `hugo-site/public`

### Vercel

1. Vercel'e import et
2. Framework preset: Hugo
3. Build settings:
   - Build command: `cd hugo-site && hugo`
   - Output directory: `hugo-site/public`

### GitHub Pages

```bash
cd hugo-site
hugo
cd public
git init
git add .
git commit -m "Deploy"
git remote add origin https://github.com/username/repo.git
git push -u origin main
```

## 🔐 Güvenlik

- `.env` dosyası `.gitignore`'da - asla commit etmeyin
- API anahtarları environment variable olarak saklayın
- Rate limiting uygulayın (Groq: 30/dakika)

## 📈 İstatistikler

- **85+ Bitki** - Ev bitkileri, bahçe, sukulent, kaktüs, şifalı, sebze, meyve
- **8 Kategori** - Organize edilmiş içerik
- **1900+ satır CSS** - Responsive tasarım
- **Otomatik içerik** - Groq API ile üretim
- **Otomatik görseller** - API entegrasyonu

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

Görseller için:
- Wikimedia Commons: CC BY-SA 4.0
- iNaturalist: CC BY 4.0

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Commit edin (`git commit -m 'Yeni özellik ekle'`)
4. Push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request açın

## 📧 İletişim

Sorularınız için: [cicekansiklopedisi@example.com](mailto:cicekansiklopedisi@example.com)

---

**Notlar:**

- İçerik üretimi için Groq API anahtarı gereklidir (ücretsiz)
- Görseller Creative Commons lisansı altındadır
- Hugo extended versiyonu kullanın (SCSS desteği için)
- Python 3.8+ gereklidir
