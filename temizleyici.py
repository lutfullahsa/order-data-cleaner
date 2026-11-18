from datetime import datetime
import logging
from pathlib import Path
import re

class VeriTemizleyici:
    """Sipariş kayıtlarını doğrular ve temizler."""

    def __init__(self, ham_kayitlar, log_dosyasi=None):
        """Kayıtları ve temizleme günlükleyicisini başlatır."""
        self.ham_kayitlar = ham_kayitlar if ham_kayitlar is not None else []
        self.temiz_kayitlar = []
        self.hatali_kayitlar = []
        
        self.logger = logging.getLogger("VeriTemizleyici")
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            
            if log_dosyasi:
                log_path = Path(log_dosyasi)
                log_path.parent.mkdir(parents=True, exist_ok=True)
                file_handler = logging.FileHandler(log_dosyasi, encoding='utf-8')
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

    def isim_duzenle(self, isim):
        """İsim metnini boşluklardan arındırıp baş harflerini büyütür."""
        if not isim: raise ValueError("İsim eksik")
        return " ".join(str(isim).split()).title()

    def eposta_dogrula(self, eposta):
        """E-posta adresini temel biçimde doğrular ve küçük harfe çevirir."""
        if not eposta or "@" not in str(eposta): raise ValueError("Geçersiz e-posta")
        return str(eposta).strip().lower()

    def fiyat_temizle(self, fiyat):
        """Fiyatı ondalık sayıya çevirir ve negatif değerleri reddeder."""
        if isinstance(fiyat, str):
            if "-" in fiyat:
                raise ValueError("Negatif fiyat olamaz")
        else:
            try:
                if fiyat < 0:
                    raise ValueError("Negatif fiyat olamaz")
            except TypeError:
                pass

        fiyat_str = re.sub(r'[^\d,.]', '', str(fiyat))
        if ',' in fiyat_str and '.' in fiyat_str:
            if fiyat_str.find(',') > fiyat_str.find('.'): fiyat_str = fiyat_str.replace('.', '').replace(',', '.')
            else: fiyat_str = fiyat_str.replace(',', '')
        elif ',' in fiyat_str:
            fiyat_str = fiyat_str.replace(',', '.')
        elif re.fullmatch(r'\d{1,3}(?:\.\d{3})+', fiyat_str):
            fiyat_str = fiyat_str.replace('.', '')

        try:
            val = float(fiyat_str)
        except (TypeError, ValueError) as hata:
            raise ValueError("Geçersiz fiyat") from hata
        if val < 0:
            raise ValueError("Negatif fiyat olamaz")
        return val

    def telefon_temizle(self, telefon):
        """Telefon numarasını Türkiye biçiminde standartlaştırır."""
        temiz = re.sub(r'\D', '', str(telefon))
        if len(temiz) == 14 and temiz.startswith('0090'): temiz = temiz[2:]
        if len(temiz) == 10: temiz = "90" + temiz
        elif len(temiz) == 11 and temiz.startswith('0'): temiz = "90" + temiz[1:]
        elif len(temiz) == 12 and temiz.startswith('90'): pass
        else: raise ValueError("Geçersiz telefon")
        return f"+{temiz[:2]} {temiz[2:5]} {temiz[5:8]} {temiz[8:10]} {temiz[10:12]}"

    def tarih_temizle(self, tarih):
        """Desteklenen tarih biçimlerini YYYY-AA-GG biçimine dönüştürür."""
        if isinstance(tarih, datetime):
            return tarih.strftime("%Y-%m-%d")
        tarih = str(tarih).strip()
        for fmt in ("%d.%m.%Y", "%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
            try: return datetime.strptime(tarih, fmt).strftime("%Y-%m-%d")
            except: continue
        raise ValueError("Geçersiz tarih formatı")

    def tekrarlari_kaldir(self, veriler):
        """Aynı siparişe ait yinelenen kayıtları hatalı listesine ayırır."""
        yeni, hatali = [], []
        gorulen = set()
        for v in veriler:
            kimlik = (
                v.get("isim"),
                v.get("eposta"),
                v.get("urun"),
                v.get("fiyat"),
                v.get("telefon"),
                v.get("tarih"),
            )
            if kimlik not in gorulen:
                yeni.append(v)
                gorulen.add(kimlik)
            else:
                v["hata_sebebi"] = "Tekrar eden kayıt"
                hatali.append(v)
        return yeni, hatali

    def verileri_temizle(self):
        """Ham kayıtları temizleyip geçerli ve hatalı listeleri döndürür."""
        self.logger.info("Veri temizleme işlemi başladı.")
        gecici_temiz, self.hatali_kayitlar = [], []
        for i, kayit in enumerate(self.ham_kayitlar, 1):
            try:
                temiz = {
                    "satir_no": i,
                    "isim": self.isim_duzenle(kayit.get("isim")),
                    "eposta": self.eposta_dogrula(kayit.get("eposta")),
                    "fiyat": self.fiyat_temizle(kayit.get("fiyat")),
                    "urun": str(kayit.get("urun", "")).strip()
                }
                if kayit.get("telefon"): temiz["telefon"] = self.telefon_temizle(kayit["telefon"])
                if kayit.get("tarih"): temiz["tarih"] = self.tarih_temizle(kayit["tarih"])
                gecici_temiz.append(temiz)
            except Exception as e:
                self.logger.warning(f"Satır {i} hatalı: {e}")
                h = dict(kayit)
                h["satir_no"] = i
                h["hata_sebebi"] = str(e)
                self.hatali_kayitlar.append(h)
        self.temiz_kayitlar, tekrarlar = self.tekrarlari_kaldir(gecici_temiz)
        self.hatali_kayitlar.extend(tekrarlar)
        self.logger.info("Veri temizleme işlemi tamamlandı.")
        return self.temiz_kayitlar, self.hatali_kayitlar

    def ozet_rapor_al(self):
        """Toplam, geçerli ve hatalı kayıt sayılarını döndürür."""
        return {"toplam": len(self.ham_kayitlar), "gecerli": len(self.temiz_kayitlar), "hatali": len(self.hatali_kayitlar)}

def verileri_isle(ham_siparisler):
    t = VeriTemizleyici(ham_siparisler)
    return t.verileri_temizle()
