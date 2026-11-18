import sqlite3
from pathlib import Path
from datetime import datetime
import json

class VeritabaniYoneticisi:
    def __init__(self, db_yolu="cikti/siparisler.db"):
        self.db_yolu = Path(db_yolu)
        self.db_yolu.parent.mkdir(parents=True, exist_ok=True)
        self.baglanti = sqlite3.connect(self.db_yolu)
        self._tablolari_olustur()

    def _tablolari_olustur(self):
        with self.baglanti:
            self.baglanti.execute("""
                CREATE TABLE IF NOT EXISTS temiz_siparisler (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kaynak_dosya TEXT,
                    satir_no INTEGER,
                    isim TEXT,
                    eposta TEXT,
                    urun TEXT,
                    fiyat REAL,
                    telefon TEXT,
                    tarih TEXT,
                    eklenme_tarihi TEXT
                )
            """)
            self.baglanti.execute("""
                CREATE TABLE IF NOT EXISTS hatali_siparisler (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kaynak_dosya TEXT,
                    satir_no INTEGER,
                    ham_veri TEXT,
                    hata_sebebi TEXT,
                    eklenme_tarihi TEXT
                )
            """)

    def kayitlari_ekle(self, kaynak_dosya, temiz_kayitlar, hatali_kayitlar):
        tarih = datetime.now().isoformat()
        with self.baglanti:
             # Aynı kaynak dosyaya ait eski kayıtları temizle (mükerrer koruması)
            self.baglanti.execute("DELETE FROM temiz_siparisler WHERE kaynak_dosya = ?", (kaynak_dosya,))
            self.baglanti.execute("DELETE FROM hatali_siparisler WHERE kaynak_dosya = ?", (kaynak_dosya,))
            for k in temiz_kayitlar:
                self.baglanti.execute("""
                    INSERT INTO temiz_siparisler 
                    (kaynak_dosya, satir_no, isim, eposta, urun, fiyat, telefon, tarih, eklenme_tarihi)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (kaynak_dosya, k.get("satir_no"), k.get("isim"), k.get("eposta"), k.get("urun"), 
                      k.get("fiyat"), k.get("telefon"), k.get("tarih"), tarih))
            
            for h in hatali_kayitlar:
                self.baglanti.execute("""
                    INSERT INTO hatali_siparisler 
                    (kaynak_dosya, satir_no, ham_veri, hata_sebebi, eklenme_tarihi)
                    VALUES (?, ?, ?, ?, ?)
                """, (kaynak_dosya, h.get("satir_no"), json.dumps(h, default=str, ensure_ascii=False), h.get("hata_sebebi"), tarih))

    def kapat(self):
        """Veritabanı bağlantısını güvenli şekilde kapatır."""
        if self.baglanti:
            self.baglanti.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.kapat()

