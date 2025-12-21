"""
Bitki Veritabanı - Çiçek Ansiklopedisi
Türkçe ve Latince bitki isimleri, kategoriler ve temel bilgiler
"""

# Bitki yapısı: (Türkçe Ad, Latince Ad, Kategori, Bakım Kolaylığı, Bilgiler)
# Kategoriler: ev-bitkileri, bahce-bitkileri, sukulent, kaktus, sifali-bitkiler, sebzeler, meyveler, cicek

PLANTS = [
    # ==================== EV BİTKİLERİ ====================
    ("Monstera", "Monstera deliciosa", "ev-bitkileri", "Kolay", {
        "familya": "Araceae",
        "anaVatan": "Orta Amerika",
        "isik": "Parlak dolaylı",
        "sulama": "Haftada 1-2",
        "nem": "Yüksek",
        "sicaklik": "18-27°C",
        "zehirlilik": "Evcil hayvanlara zararlı",
        "hava_temizleyici": True,
        "cicek_acar": False
    }),
    ("Pothos", "Epipremnum aureum", "ev-bitkileri", "Kolay", {
        "familya": "Araceae",
        "anaVatan": "Güneydoğu Asya",
        "isik": "Az-orta ışık",
        "sulama": "Toprak kuruduğunda",
        "nem": "Orta",
        "sicaklik": "15-30°C",
        "zehirlilik": "Evcil hayvanlara zararlı",
        "hava_temizleyici": True,
        "cicek_acar": False
    }),
    ("Kauçuk Bitkisi", "Ficus elastica", "ev-bitkileri", "Kolay", {
        "familya": "Moraceae",
        "anaVatan": "Güneydoğu Asya",
        "isik": "Parlak dolaylı",
        "sulama": "Haftada 1",
        "nem": "Orta-yüksek",
        "sicaklik": "16-24°C",
        "zehirlilik": "Hafif toksik",
        "hava_temizleyici": True,
        "cicek_acar": False
    }),
    ("Barış Zambağı", "Spathiphyllum", "ev-bitkileri", "Kolay", {
        "familya": "Araceae",
        "anaVatan": "Tropik Amerika",
        "isik": "Az-orta ışık",
        "sulama": "Haftada 1",
        "nem": "Yüksek",
        "sicaklik": "18-26°C",
        "zehirlilik": "Evcil hayvanlara zararlı",
        "hava_temizleyici": True,
        "cicek_acar": True
    }),
    ("Yılan Bitkisi", "Sansevieria trifasciata", "ev-bitkileri", "Kolay", {
        "familya": "Asparagaceae",
        "anaVatan": "Batı Afrika",
        "isik": "Az-parlak ışık",
        "sulama": "2-3 haftada 1",
        "nem": "Düşük-orta",
        "sicaklik": "15-27°C",
        "zehirlilik": "Hafif toksik",
        "hava_temizleyici": True,
        "cicek_acar": False
    }),
    ("Fil Kulağı", "Alocasia", "ev-bitkileri", "Orta", {
        "familya": "Araceae",
        "anaVatan": "Güneydoğu Asya",
        "isik": "Parlak dolaylı",
        "sulama": "Toprak nemli kalmalı",
        "nem": "Yüksek",
        "sicaklik": "18-26°C",
        "zehirlilik": "Toksik",
        "hava_temizleyici": False,
        "cicek_acar": False
    }),
    ("Calathea", "Calathea", "ev-bitkileri", "Zor", {
        "familya": "Marantaceae",
        "anaVatan": "Tropik Amerika",
        "isik": "Orta dolaylı",
        "sulama": "Toprak nemli kalmalı",
        "nem": "Yüksek",
        "sicaklik": "18-24°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": False
    }),
    ("Palmiye", "Chamaedorea elegans", "ev-bitkileri", "Kolay", {
        "familya": "Arecaceae",
        "anaVatan": "Meksika",
        "isik": "Orta dolaylı",
        "sulama": "Haftada 1",
        "nem": "Orta",
        "sicaklik": "18-27°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": True,
        "cicek_acar": False
    }),
    ("Zamioculcas", "Zamioculcas zamiifolia", "ev-bitkileri", "Kolay", {
        "familya": "Araceae",
        "anaVatan": "Doğu Afrika",
        "isik": "Az-orta ışık",
        "sulama": "2-3 haftada 1",
        "nem": "Düşük",
        "sicaklik": "15-24°C",
        "zehirlilik": "Toksik",
        "hava_temizleyici": True,
        "cicek_acar": False
    }),
    ("Filodendron", "Philodendron", "ev-bitkileri", "Kolay", {
        "familya": "Araceae",
        "anaVatan": "Tropik Amerika",
        "isik": "Orta dolaylı",
        "sulama": "Toprak kuruduğunda",
        "nem": "Orta-yüksek",
        "sicaklik": "18-27°C",
        "zehirlilik": "Toksik",
        "hava_temizleyici": True,
        "cicek_acar": False
    }),
    ("Dracaena", "Dracaena marginata", "ev-bitkileri", "Kolay", {
        "familya": "Asparagaceae",
        "anaVatan": "Madagaskar",
        "isik": "Orta-parlak dolaylı",
        "sulama": "Haftada 1",
        "nem": "Orta",
        "sicaklik": "18-27°C",
        "zehirlilik": "Evcil hayvanlara zararlı",
        "hava_temizleyici": True,
        "cicek_acar": False
    }),
    ("Fikus Benjamin", "Ficus benjamina", "ev-bitkileri", "Orta", {
        "familya": "Moraceae",
        "anaVatan": "Güneydoğu Asya",
        "isik": "Parlak dolaylı",
        "sulama": "Toprak kuruduğunda",
        "nem": "Orta",
        "sicaklik": "16-24°C",
        "zehirlilik": "Hafif toksik",
        "hava_temizleyici": True,
        "cicek_acar": False
    }),
    ("Şeflera", "Schefflera arboricola", "ev-bitkileri", "Kolay", {
        "familya": "Araliaceae",
        "anaVatan": "Tayvan",
        "isik": "Parlak dolaylı",
        "sulama": "Toprak kuruduğunda",
        "nem": "Orta",
        "sicaklik": "15-24°C",
        "zehirlilik": "Hafif toksik",
        "hava_temizleyici": True,
        "cicek_acar": False
    }),
    ("Aloe Vera", "Aloe barbadensis", "ev-bitkileri", "Kolay", {
        "familya": "Asphodelaceae",
        "anaVatan": "Arap Yarımadası",
        "isik": "Parlak ışık",
        "sulama": "2-3 haftada 1",
        "nem": "Düşük",
        "sicaklik": "13-27°C",
        "zehirlilik": "Kedilere zararlı",
        "hava_temizleyici": True,
        "cicek_acar": True
    }),
    ("Begonia", "Begonia", "ev-bitkileri", "Orta", {
        "familya": "Begoniaceae",
        "anaVatan": "Tropik bölgeler",
        "isik": "Parlak dolaylı",
        "sulama": "Toprak kuruduğunda",
        "nem": "Yüksek",
        "sicaklik": "18-24°C",
        "zehirlilik": "Evcil hayvanlara zararlı",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Eğrelti Otu", "Nephrolepis exaltata", "ev-bitkileri", "Orta", {
        "familya": "Nephrolepidaceae",
        "anaVatan": "Tropik bölgeler",
        "isik": "Orta dolaylı",
        "sulama": "Toprak nemli kalmalı",
        "nem": "Yüksek",
        "sicaklik": "16-24°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": True,
        "cicek_acar": False
    }),
    ("Kaktüs Orman", "Schlumbergera", "ev-bitkileri", "Kolay", {
        "familya": "Cactaceae",
        "anaVatan": "Brezilya",
        "isik": "Parlak dolaylı",
        "sulama": "Toprak kuruduğunda",
        "nem": "Orta",
        "sicaklik": "15-21°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Antoryum", "Anthurium", "ev-bitkileri", "Orta", {
        "familya": "Araceae",
        "anaVatan": "Kolombiya",
        "isik": "Parlak dolaylı",
        "sulama": "Haftada 1-2",
        "nem": "Yüksek",
        "sicaklik": "18-27°C",
        "zehirlilik": "Toksik",
        "hava_temizleyici": True,
        "cicek_acar": True
    }),
    ("Croton", "Codiaeum variegatum", "ev-bitkileri", "Orta", {
        "familya": "Euphorbiaceae",
        "anaVatan": "Malezya",
        "isik": "Parlak ışık",
        "sulama": "Toprak nemli kalmalı",
        "nem": "Yüksek",
        "sicaklik": "18-27°C",
        "zehirlilik": "Toksik",
        "hava_temizleyici": False,
        "cicek_acar": False
    }),
    ("Dieffenbachia", "Dieffenbachia", "ev-bitkileri", "Kolay", {
        "familya": "Araceae",
        "anaVatan": "Tropik Amerika",
        "isik": "Orta dolaylı",
        "sulama": "Toprak kuruduğunda",
        "nem": "Orta-yüksek",
        "sicaklik": "18-27°C",
        "zehirlilik": "Çok toksik",
        "hava_temizleyici": True,
        "cicek_acar": False
    }),

    # ==================== SUKULENTLER ====================
    ("Echeveria", "Echeveria", "sukulent", "Kolay", {
        "familya": "Crassulaceae",
        "anaVatan": "Meksika",
        "isik": "Parlak ışık",
        "sulama": "2 haftada 1",
        "nem": "Düşük",
        "sicaklik": "10-27°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Haworthia", "Haworthia", "sukulent", "Kolay", {
        "familya": "Asphodelaceae",
        "anaVatan": "Güney Afrika",
        "isik": "Parlak dolaylı",
        "sulama": "2-3 haftada 1",
        "nem": "Düşük",
        "sicaklik": "10-27°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Sedum", "Sedum", "sukulent", "Kolay", {
        "familya": "Crassulaceae",
        "anaVatan": "Kuzey Yarımküre",
        "isik": "Parlak ışık",
        "sulama": "2 haftada 1",
        "nem": "Düşük",
        "sicaklik": "5-27°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Crassula", "Crassula ovata", "sukulent", "Kolay", {
        "familya": "Crassulaceae",
        "anaVatan": "Güney Afrika",
        "isik": "Parlak ışık",
        "sulama": "2-3 haftada 1",
        "nem": "Düşük",
        "sicaklik": "10-24°C",
        "zehirlilik": "Kedilere zararlı",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Senecio", "Senecio rowleyanus", "sukulent", "Orta", {
        "familya": "Asteraceae",
        "anaVatan": "Güney Afrika",
        "isik": "Parlak dolaylı",
        "sulama": "2 haftada 1",
        "nem": "Düşük",
        "sicaklik": "13-24°C",
        "zehirlilik": "Toksik",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Graptopetalum", "Graptopetalum paraguayense", "sukulent", "Kolay", {
        "familya": "Crassulaceae",
        "anaVatan": "Meksika",
        "isik": "Parlak ışık",
        "sulama": "2 haftada 1",
        "nem": "Düşük",
        "sicaklik": "10-27°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Kalanchoe", "Kalanchoe", "sukulent", "Kolay", {
        "familya": "Crassulaceae",
        "anaVatan": "Madagaskar",
        "isik": "Parlak ışık",
        "sulama": "2 haftada 1",
        "nem": "Düşük",
        "sicaklik": "15-27°C",
        "zehirlilik": "Evcil hayvanlara zararlı",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Lithops", "Lithops", "sukulent", "Orta", {
        "familya": "Aizoaceae",
        "anaVatan": "Güney Afrika",
        "isik": "Parlak ışık",
        "sulama": "Ayda 1",
        "nem": "Çok düşük",
        "sicaklik": "15-27°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Aeonium", "Aeonium", "sukulent", "Kolay", {
        "familya": "Crassulaceae",
        "anaVatan": "Kanarya Adaları",
        "isik": "Parlak ışık",
        "sulama": "Haftada 1",
        "nem": "Düşük",
        "sicaklik": "10-27°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Sempervivum", "Sempervivum", "sukulent", "Kolay", {
        "familya": "Crassulaceae",
        "anaVatan": "Avrupa",
        "isik": "Parlak ışık",
        "sulama": "2 haftada 1",
        "nem": "Düşük",
        "sicaklik": "-10-27°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),

    # ==================== KAKTÜSLER ====================
    ("Echinopsis", "Echinopsis", "kaktus", "Kolay", {
        "familya": "Cactaceae",
        "anaVatan": "Güney Amerika",
        "isik": "Parlak ışık",
        "sulama": "2-3 haftada 1",
        "nem": "Düşük",
        "sicaklik": "10-35°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Mammillaria", "Mammillaria", "kaktus", "Kolay", {
        "familya": "Cactaceae",
        "anaVatan": "Meksika",
        "isik": "Parlak ışık",
        "sulama": "2-3 haftada 1",
        "nem": "Düşük",
        "sicaklik": "10-35°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Opuntia", "Opuntia", "kaktus", "Kolay", {
        "familya": "Cactaceae",
        "anaVatan": "Amerika",
        "isik": "Parlak ışık",
        "sulama": "3-4 haftada 1",
        "nem": "Düşük",
        "sicaklik": "5-35°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Gymnocalycium", "Gymnocalycium", "kaktus", "Kolay", {
        "familya": "Cactaceae",
        "anaVatan": "Güney Amerika",
        "isik": "Parlak dolaylı",
        "sulama": "2-3 haftada 1",
        "nem": "Düşük",
        "sicaklik": "10-30°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Ferocactus", "Ferocactus", "kaktus", "Kolay", {
        "familya": "Cactaceae",
        "anaVatan": "Meksika",
        "isik": "Parlak ışık",
        "sulama": "3-4 haftada 1",
        "nem": "Düşük",
        "sicaklik": "10-40°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Rebutia", "Rebutia", "kaktus", "Kolay", {
        "familya": "Cactaceae",
        "anaVatan": "Bolivya",
        "isik": "Parlak ışık",
        "sulama": "2 haftada 1",
        "nem": "Düşük",
        "sicaklik": "5-30°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Cereus", "Cereus", "kaktus", "Kolay", {
        "familya": "Cactaceae",
        "anaVatan": "Güney Amerika",
        "isik": "Parlak ışık",
        "sulama": "2-3 haftada 1",
        "nem": "Düşük",
        "sicaklik": "10-35°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Echinocactus", "Echinocactus grusonii", "kaktus", "Kolay", {
        "familya": "Cactaceae",
        "anaVatan": "Meksika",
        "isik": "Parlak ışık",
        "sulama": "3-4 haftada 1",
        "nem": "Düşük",
        "sicaklik": "10-40°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),

    # ==================== ŞİFALI BİTKİLER ====================
    ("Nane", "Mentha", "sifali-bitkiler", "Kolay", {
        "familya": "Lamiaceae",
        "anaVatan": "Avrupa, Asya",
        "isik": "Orta-parlak",
        "sulama": "Toprak nemli kalmalı",
        "nem": "Orta",
        "sicaklik": "15-25°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Biberiye", "Rosmarinus officinalis", "sifali-bitkiler", "Kolay", {
        "familya": "Lamiaceae",
        "anaVatan": "Akdeniz",
        "isik": "Parlak ışık",
        "sulama": "Toprak kuruduğunda",
        "nem": "Düşük-orta",
        "sicaklik": "10-25°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Lavanta", "Lavandula", "sifali-bitkiler", "Kolay", {
        "familya": "Lamiaceae",
        "anaVatan": "Akdeniz",
        "isik": "Parlak ışık",
        "sulama": "Toprak kuruduğunda",
        "nem": "Düşük",
        "sicaklik": "10-25°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Kekik", "Thymus vulgaris", "sifali-bitkiler", "Kolay", {
        "familya": "Lamiaceae",
        "anaVatan": "Akdeniz",
        "isik": "Parlak ışık",
        "sulama": "Toprak kuruduğunda",
        "nem": "Düşük",
        "sicaklik": "10-25°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Adaçayı", "Salvia officinalis", "sifali-bitkiler", "Kolay", {
        "familya": "Lamiaceae",
        "anaVatan": "Akdeniz",
        "isik": "Parlak ışık",
        "sulama": "Toprak kuruduğunda",
        "nem": "Düşük-orta",
        "sicaklik": "10-25°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Papatya", "Matricaria chamomilla", "sifali-bitkiler", "Kolay", {
        "familya": "Asteraceae",
        "anaVatan": "Avrupa",
        "isik": "Parlak ışık",
        "sulama": "Düzenli",
        "nem": "Orta",
        "sicaklik": "10-20°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Ekinezya", "Echinacea", "sifali-bitkiler", "Kolay", {
        "familya": "Asteraceae",
        "anaVatan": "Kuzey Amerika",
        "isik": "Parlak ışık",
        "sulama": "Toprak kuruduğunda",
        "nem": "Orta",
        "sicaklik": "15-25°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Melisa", "Melissa officinalis", "sifali-bitkiler", "Kolay", {
        "familya": "Lamiaceae",
        "anaVatan": "Güney Avrupa",
        "isik": "Orta-parlak",
        "sulama": "Toprak nemli kalmalı",
        "nem": "Orta",
        "sicaklik": "15-25°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Rezene", "Foeniculum vulgare", "sifali-bitkiler", "Kolay", {
        "familya": "Apiaceae",
        "anaVatan": "Akdeniz",
        "isik": "Parlak ışık",
        "sulama": "Düzenli",
        "nem": "Orta",
        "sicaklik": "15-25°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Zencefil", "Zingiber officinale", "sifali-bitkiler", "Orta", {
        "familya": "Zingiberaceae",
        "anaVatan": "Güneydoğu Asya",
        "isik": "Parlak dolaylı",
        "sulama": "Toprak nemli kalmalı",
        "nem": "Yüksek",
        "sicaklik": "20-30°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),

    # ==================== SEBZELER ====================
    ("Domates", "Solanum lycopersicum", "sebzeler", "Orta", {
        "familya": "Solanaceae",
        "anaVatan": "Güney Amerika",
        "isik": "Tam güneş",
        "sulama": "Düzenli",
        "nem": "Orta",
        "sicaklik": "20-30°C",
        "zehirlilik": "Yapraklar toksik",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Biber", "Capsicum annuum", "sebzeler", "Orta", {
        "familya": "Solanaceae",
        "anaVatan": "Amerika",
        "isik": "Tam güneş",
        "sulama": "Düzenli",
        "nem": "Orta",
        "sicaklik": "20-30°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Patlıcan", "Solanum melongena", "sebzeler", "Orta", {
        "familya": "Solanaceae",
        "anaVatan": "Güney Asya",
        "isik": "Tam güneş",
        "sulama": "Düzenli",
        "nem": "Orta",
        "sicaklik": "22-30°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Salatalık", "Cucumis sativus", "sebzeler", "Kolay", {
        "familya": "Cucurbitaceae",
        "anaVatan": "Güney Asya",
        "isik": "Tam güneş",
        "sulama": "Bol su",
        "nem": "Orta-yüksek",
        "sicaklik": "20-30°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Kabak", "Cucurbita pepo", "sebzeler", "Kolay", {
        "familya": "Cucurbitaceae",
        "anaVatan": "Amerika",
        "isik": "Tam güneş",
        "sulama": "Düzenli",
        "nem": "Orta",
        "sicaklik": "18-30°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Marul", "Lactuca sativa", "sebzeler", "Kolay", {
        "familya": "Asteraceae",
        "anaVatan": "Akdeniz",
        "isik": "Yarı gölge-güneş",
        "sulama": "Düzenli",
        "nem": "Orta",
        "sicaklik": "15-20°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Ispanak", "Spinacia oleracea", "sebzeler", "Kolay", {
        "familya": "Amaranthaceae",
        "anaVatan": "İran",
        "isik": "Yarı gölge-güneş",
        "sulama": "Düzenli",
        "nem": "Orta",
        "sicaklik": "10-20°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Havuç", "Daucus carota", "sebzeler", "Kolay", {
        "familya": "Apiaceae",
        "anaVatan": "Avrupa, Asya",
        "isik": "Tam güneş",
        "sulama": "Düzenli",
        "nem": "Orta",
        "sicaklik": "15-25°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Soğan", "Allium cepa", "sebzeler", "Kolay", {
        "familya": "Amaryllidaceae",
        "anaVatan": "Orta Asya",
        "isik": "Tam güneş",
        "sulama": "Orta",
        "nem": "Düşük-orta",
        "sicaklik": "13-25°C",
        "zehirlilik": "Evcil hayvanlara zararlı",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Sarımsak", "Allium sativum", "sebzeler", "Kolay", {
        "familya": "Amaryllidaceae",
        "anaVatan": "Orta Asya",
        "isik": "Tam güneş",
        "sulama": "Orta",
        "nem": "Düşük-orta",
        "sicaklik": "13-25°C",
        "zehirlilik": "Evcil hayvanlara zararlı",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),

    # ==================== MEYVELER ====================
    ("Limon", "Citrus limon", "meyveler", "Orta", {
        "familya": "Rutaceae",
        "anaVatan": "Güney Asya",
        "isik": "Tam güneş",
        "sulama": "Düzenli",
        "nem": "Orta",
        "sicaklik": "15-30°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Portakal", "Citrus sinensis", "meyveler", "Orta", {
        "familya": "Rutaceae",
        "anaVatan": "Güneydoğu Asya",
        "isik": "Tam güneş",
        "sulama": "Düzenli",
        "nem": "Orta",
        "sicaklik": "15-30°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Elma", "Malus domestica", "meyveler", "Orta", {
        "familya": "Rosaceae",
        "anaVatan": "Orta Asya",
        "isik": "Tam güneş",
        "sulama": "Düzenli",
        "nem": "Orta",
        "sicaklik": "10-25°C",
        "zehirlilik": "Çekirdekler toksik",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Çilek", "Fragaria × ananassa", "meyveler", "Kolay", {
        "familya": "Rosaceae",
        "anaVatan": "Avrupa",
        "isik": "Tam güneş",
        "sulama": "Düzenli",
        "nem": "Orta",
        "sicaklik": "15-25°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Ahududu", "Rubus idaeus", "meyveler", "Kolay", {
        "familya": "Rosaceae",
        "anaVatan": "Avrupa, Asya",
        "isik": "Tam güneş",
        "sulama": "Düzenli",
        "nem": "Orta",
        "sicaklik": "15-25°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Üzüm", "Vitis vinifera", "meyveler", "Orta", {
        "familya": "Vitaceae",
        "anaVatan": "Akdeniz",
        "isik": "Tam güneş",
        "sulama": "Orta",
        "nem": "Orta",
        "sicaklik": "15-30°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("İncir", "Ficus carica", "meyveler", "Kolay", {
        "familya": "Moraceae",
        "anaVatan": "Batı Asya",
        "isik": "Tam güneş",
        "sulama": "Orta",
        "nem": "Orta",
        "sicaklik": "15-30°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Zeytin", "Olea europaea", "meyveler", "Kolay", {
        "familya": "Oleaceae",
        "anaVatan": "Akdeniz",
        "isik": "Tam güneş",
        "sulama": "Az",
        "nem": "Düşük",
        "sicaklik": "10-30°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),

    # ==================== ÇİÇEKLER (BAHÇE) ====================
    ("Gül", "Rosa", "cicek", "Orta", {
        "familya": "Rosaceae",
        "anaVatan": "Asya",
        "isik": "Tam güneş",
        "sulama": "Düzenli",
        "nem": "Orta",
        "sicaklik": "15-25°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Orkide", "Orchidaceae", "cicek", "Zor", {
        "familya": "Orchidaceae",
        "anaVatan": "Tropik bölgeler",
        "isik": "Parlak dolaylı",
        "sulama": "Haftada 1",
        "nem": "Yüksek",
        "sicaklik": "18-27°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Lale", "Tulipa", "cicek", "Kolay", {
        "familya": "Liliaceae",
        "anaVatan": "Orta Asya",
        "isik": "Tam güneş",
        "sulama": "Orta",
        "nem": "Orta",
        "sicaklik": "10-20°C",
        "zehirlilik": "Kedilere zararlı",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Sümbül", "Hyacinthus", "cicek", "Kolay", {
        "familya": "Asparagaceae",
        "anaVatan": "Doğu Akdeniz",
        "isik": "Parlak ışık",
        "sulama": "Orta",
        "nem": "Orta",
        "sicaklik": "10-18°C",
        "zehirlilik": "Toksik",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Nergis", "Narcissus", "cicek", "Kolay", {
        "familya": "Amaryllidaceae",
        "anaVatan": "Akdeniz",
        "isik": "Tam güneş",
        "sulama": "Orta",
        "nem": "Orta",
        "sicaklik": "10-18°C",
        "zehirlilik": "Toksik",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Sardunya", "Pelargonium", "cicek", "Kolay", {
        "familya": "Geraniaceae",
        "anaVatan": "Güney Afrika",
        "isik": "Tam güneş",
        "sulama": "Toprak kuruduğunda",
        "nem": "Orta",
        "sicaklik": "15-25°C",
        "zehirlilik": "Hafif toksik",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Petunya", "Petunia", "cicek", "Kolay", {
        "familya": "Solanaceae",
        "anaVatan": "Güney Amerika",
        "isik": "Tam güneş",
        "sulama": "Düzenli",
        "nem": "Orta",
        "sicaklik": "15-27°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Menekşe", "Viola", "cicek", "Kolay", {
        "familya": "Violaceae",
        "anaVatan": "Avrupa",
        "isik": "Yarı gölge",
        "sulama": "Düzenli",
        "nem": "Orta",
        "sicaklik": "10-20°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Karanfil", "Dianthus", "cicek", "Kolay", {
        "familya": "Caryophyllaceae",
        "anaVatan": "Akdeniz",
        "isik": "Tam güneş",
        "sulama": "Orta",
        "nem": "Orta",
        "sicaklik": "15-20°C",
        "zehirlilik": "Hafif toksik",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Kasımpatı", "Chrysanthemum", "cicek", "Kolay", {
        "familya": "Asteraceae",
        "anaVatan": "Doğu Asya",
        "isik": "Tam güneş",
        "sulama": "Düzenli",
        "nem": "Orta",
        "sicaklik": "10-20°C",
        "zehirlilik": "Hafif toksik",
        "hava_temizleyici": True,
        "cicek_acar": True
    }),
    ("Yasemin", "Jasminum", "cicek", "Orta", {
        "familya": "Oleaceae",
        "anaVatan": "Asya",
        "isik": "Parlak ışık",
        "sulama": "Düzenli",
        "nem": "Orta-yüksek",
        "sicaklik": "15-25°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Zambak", "Lilium", "cicek", "Orta", {
        "familya": "Liliaceae",
        "anaVatan": "Kuzey Yarımküre",
        "isik": "Parlak ışık",
        "sulama": "Düzenli",
        "nem": "Orta",
        "sicaklik": "15-25°C",
        "zehirlilik": "Kedilere çok toksik",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Kadife Çiçeği", "Tagetes", "cicek", "Kolay", {
        "familya": "Asteraceae",
        "anaVatan": "Amerika",
        "isik": "Tam güneş",
        "sulama": "Orta",
        "nem": "Orta",
        "sicaklik": "18-27°C",
        "zehirlilik": "Zararsız",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Ortanca", "Hydrangea", "cicek", "Orta", {
        "familya": "Hydrangeaceae",
        "anaVatan": "Asya",
        "isik": "Yarı gölge",
        "sulama": "Bol su",
        "nem": "Yüksek",
        "sicaklik": "15-25°C",
        "zehirlilik": "Toksik",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
    ("Açelya", "Rhododendron", "cicek", "Orta", {
        "familya": "Ericaceae",
        "anaVatan": "Asya",
        "isik": "Yarı gölge",
        "sulama": "Düzenli",
        "nem": "Yüksek",
        "sicaklik": "15-22°C",
        "zehirlilik": "Çok toksik",
        "hava_temizleyici": False,
        "cicek_acar": True
    }),
]

# Kategorileri ayrı ayrı almak için yardımcı fonksiyonlar
def get_plants_by_category(category):
    """Belirli bir kategorideki bitkileri döndürür"""
    return [p for p in PLANTS if p[2] == category]

def get_all_categories():
    """Tüm kategorileri döndürür"""
    return list(set([p[2] for p in PLANTS]))

def get_plant_by_name(name):
    """İsme göre bitki bilgisini döndürür"""
    for plant in PLANTS:
        if plant[0].lower() == name.lower():
            return plant
    return None

def get_plant_count():
    """Toplam bitki sayısını döndürür"""
    return len(PLANTS)

if __name__ == "__main__":
    print(f"Toplam bitki sayısı: {get_plant_count()}")
    print(f"\nKategoriler:")
    for cat in get_all_categories():
        count = len(get_plants_by_category(cat))
        print(f"  - {cat}: {count} bitki")
