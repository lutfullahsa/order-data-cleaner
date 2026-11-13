"""Sipariş kayıtlarını standart Python ile temizleyen bağımsız fonksiyonlar."""

import re


def isim_duzenle(isim):
    """İsim alanını kırpar, fazla boşlukları siler ve baş harfleri büyütür."""
    try:
        if isim is None:
            raise ValueError("İsim eksik (None)")
        duzenli = " ".join(str(isim).split())
        if not duzenli:
            raise ValueError("İsim boş")
        return duzenli.title()
    except ValueError:
        raise
    except Exception as hata:
        raise ValueError(f"İsim işlenirken beklenmeyen hata: {hata}") from hata


def eposta_dogrula(eposta):
    """E-posta metnini kırpar ve '@' işareti ile temel biçimi doğrular."""
    try:
        if eposta is None:
            raise ValueError("E-posta eksik (None)")
        temiz = str(eposta).strip()
        if not temiz:
            raise ValueError("E-posta boş")
        if "@" not in temiz:
            raise ValueError("E-posta '@' işareti içermiyor")
        # Basit biçim: yerel-kısım@alan
        if not re.match(r"^[^@\s]+@[^@\s]+$", temiz):
            raise ValueError("E-posta biçimi geçersiz")
        alan_adi = temiz.rsplit("@", 1)[1]
        if "." not in alan_adi:
            raise ValueError("Alan adı en az bir nokta içermelidir")
        return temiz.lower()
    except ValueError:
        raise
    except Exception as hata:
        raise ValueError(f"E-posta doğrulanırken beklenmeyen hata: {hata}") from hata


def fiyat_temizle(fiyat):
    """Metin veya sayısal fiyatı pozitif float değere çevirir (TR biçimini destekler)."""
    try:
        if fiyat is None:
            raise ValueError("Fiyat eksik (None)")

        if isinstance(fiyat, bool):
            raise ValueError("Fiyat boolean olamaz")

        if isinstance(fiyat, (int, float)):
            deger = float(fiyat)
        else:
            metin = str(fiyat).strip().lower()
            metin = re.sub(r"\s+", "", metin)
            metin = metin.replace("₺", "").replace("tl", "")
            if not metin:
                raise ValueError("Fiyat metni boş")

            # TR biçimi: 1.250,50 -> 1250.50 | 2.000 -> 2000 | 99,99 -> 99.99
            if "," in metin:
                metin = metin.replace(".", "").replace(",", ".")
            elif "." in metin:
                parcalar = metin.split(".")
                # 2.000 veya 1.250.000 gibi binlik grupları
                if len(parcalar) > 1 and all(len(p) == 3 for p in parcalar[1:]):
                    metin = "".join(parcalar)

            try:
                deger = float(metin)
            except ValueError:
                raise ValueError(f"Fiyat sayıya çevrilemedi: '{fiyat}'") from None

        if deger < 0:
            raise ValueError("Fiyat negatif olamaz")
        return round(deger, 2)
    except ValueError:
        raise
    except Exception as hata:
        raise ValueError(f"Fiyat dönüştürülemedi: {hata}") from hata


def tekrarlari_kaldir(kayitlar):
    """Aynı isim, e-posta, ürün ve fiyata sahip sonraki kayıtları ayıklar."""
    benzersiz = []
    hatali = []
    gorulen = set()

    try:
        for kayit in kayitlar:
            try:
                anahtar = (
                    kayit.get("isim"),
                    kayit.get("eposta"),
                    kayit.get("urun"),
                    kayit.get("fiyat"),
                )
                if anahtar in gorulen:
                    hatali.append({
                        **kayit,
                        "hata_sebebi": "Tamamen aynı olan tekrar eden kayıt",
                    })
                    continue
                gorulen.add(anahtar)
                benzersiz.append(kayit)
            except Exception as hata:
                hatali.append({
                    **kayit,
                    "hata_sebebi": f"Tekrar kontrolü başarısız: {hata}",
                })
    except Exception as hata:
        # Liste taraması beklenmedik şekilde bozulursa mevcut sonuçları koru.
        hatali.append({
            "satir_no": None,
            "hata_sebebi": f"Tekrarları kaldırma işlemi yarım kaldı: {hata}",
        })

    return benzersiz, hatali


def verileri_isle(ham_siparisler):
    """Tüm ham listeyi tarar; geçerli ve hatalı kayıtları ayırır."""
    gecici_temiz = []
    hatali_kayitlar = []

    for satir_no, kayit in enumerate(ham_siparisler, start=1):
        try:
            isim = isim_duzenle(kayit.get("isim") if isinstance(kayit, dict) else None)
            eposta = eposta_dogrula(kayit.get("eposta") if isinstance(kayit, dict) else None)
            fiyat = fiyat_temizle(kayit.get("fiyat") if isinstance(kayit, dict) else None)
            urun = ""
            if isinstance(kayit, dict) and kayit.get("urun"):
                urun = str(kayit.get("urun")).strip()

            gecici_temiz.append({
                "satir_no": satir_no,
                "isim": isim,
                "eposta": eposta,
                "urun": urun,
                "fiyat": fiyat,
            })
        except Exception as hata:
            hatali = dict(kayit) if isinstance(kayit, dict) else {"kayit": kayit}
            hatali["satir_no"] = satir_no
            hatali["hata_sebebi"] = str(hata)
            hatali_kayitlar.append(hatali)

    temiz_kayitlar, tekrar_hatalari = tekrarlari_kaldir(gecici_temiz)
    hatali_kayitlar.extend(tekrar_hatalari)
    hatali_kayitlar.sort(key=lambda k: k.get("satir_no") or 0)
    return temiz_kayitlar, hatali_kayitlar
