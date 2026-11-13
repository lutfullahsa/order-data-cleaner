# Test amaçlı bozuk müşteri ve sipariş kayıtları.

ham_siparisler = [
    {"isim": "Ali Yılmaz", "eposta": "ali@example.com", "urun": "Kulaklık", "fiyat": 150},
    {"isim": "Ayşe Demir", "eposta": "ayse@example.com", "urun": "Monitör", "fiyat": "1.250,50 TL"},
    {"isim": None, "eposta": "mehmet@test.com", "urun": "Klavye", "fiyat": 200},
    {"isim": "", "eposta": "fatma@test.com", "urun": "Mouse", "fiyat": 300},
    {"isim": "Can Kaya", "eposta": "cankaya.com", "urun": "USB Bellek", "fiyat": 400},
    {"isim": "Deniz Arslan", "eposta": "denizars", "urun": "Webcam", "fiyat": 100},
    {"isim": "Elif Şahin", "eposta": "elif@test.com", "urun": "Hoparlör", "fiyat": "450tl"},
    {"isim": "Fatih Koç", "eposta": "fatih@test.com", "urun": "Çanta", "fiyat": "hatalı"},
    {"isim": "Gizem Ak", "eposta": "gizem@test.com", "urun": "Stand", "fiyat": -100},
    {"isim": "Hasan Çelik", "eposta": "hasan@test.com", "urun": "Hub", "fiyat": None},
    # 1. kaydın birebir tekrarı
    {"isim": "Ali Yılmaz", "eposta": "ali@example.com", "urun": "Kulaklık", "fiyat": 150},
    {"isim": "İrem Yıldız", "eposta": "irem@mail.com", "urun": "SSD", "fiyat": "99,99 TL"},
    {"isim": "Burak Öz", "eposta": "burak@firma.com", "urun": "RAM", "fiyat": 750},
    # 13. kaydın birebir tekrarı
    {"isim": "Burak Öz", "eposta": "burak@firma.com", "urun": "RAM", "fiyat": 750},
    {"isim": "  merve  yılmaz  ", "eposta": "merve@test.com", "urun": "Pad", "fiyat": 80},
    {"isim": "Okan Demirtaş", "eposta": "okan@ok.com", "urun": "Kasa", "fiyat": "2.000 TL"},
    {"isim": "Pınar Acar", "eposta": "", "urun": "Fan", "fiyat": 500},
    {"isim": "Selin Korkmaz", "eposta": "selin@example.org", "urun": "Kablo", "fiyat": 45.5},
    {"isim": None, "eposta": "yanlis-adres", "urun": "Adaptör", "fiyat": "hatalı"},
    {"isim": "Tarık Uçar", "eposta": "tarik@ucar.com", "urun": "Router", "fiyat": "1.000,00"},
    {"isim": "Umut Eren", "eposta": "umut@eren.com", "urun": "Mikrofon", "fiyat": "abc"},
    {"isim": "Veli Can", "eposta": "veli.can@site.com", "urun": "Mousepad", "fiyat": 10},
    # 22. kaydın birebir tekrarı
    {"isim": "Veli Can", "eposta": "veli.can@site.com", "urun": "Mousepad", "fiyat": 10},
    {"isim": "Yasemin Nur", "eposta": " yasemin@nur.com ", "urun": "Lamba", "fiyat": 220},
    {"isim": "Zeynep Aydın", "eposta": "zeynep@aydin.co", "urun": "Yazıcı", "fiyat": "3.450,75 TL"},
]
