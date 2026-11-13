"""CSV, Excel ve JSON dosyalarını okuyup sonuçları dışa aktaran işlemler."""

from pathlib import Path

import pandas as pd

from ornek_veri import ham_siparisler

DESTEKLENEN_UZANTILAR = {".json", ".csv", ".xlsx"}


def _hucreyi_standartlastir(deger):
    """pandas NaN / NA değerlerini None yapar, numpy skalerlerini Python'a çevirir."""
    try:
        if deger is None or pd.isna(deger):
            return None
    except Exception:
        pass
    if hasattr(deger, "item") and not isinstance(deger, (bytes, str)):
        try:
            return deger.item()
        except Exception:
            return deger
    if isinstance(deger, str):
        return deger
    return deger


def _tabloyu_sozluk_listesine_cevir(tablo):
    """DataFrame'i temizleyici.py'nin beklediği list[dict] biçimine çevirir."""
    try:
        ham_kayitlar = tablo.astype(object).where(pd.notna(tablo), None).to_dict(orient="records")
        kayitlar = []
        for kayit in ham_kayitlar:
            kayitlar.append({anahtar: _hucreyi_standartlastir(deger) for anahtar, deger in kayit.items()})
        return kayitlar
    except Exception as hata:
        raise ValueError(f"Tablo sözlük listesine çevrilemedi: {hata}") from hata


def dosyadan_veri_oku(dosya_yolu):
    """Dosya uzantısına göre JSON/CSV/Excel okur ve list[dict] döndürür."""
    yol = Path(dosya_yolu)
    if not yol.exists() or not yol.is_file():
        raise FileNotFoundError(
            f"Dosya bulunamadı: {yol}. Lütfen yolu kontrol edin."
        )

    uzanti = yol.suffix.lower()
    if uzanti not in DESTEKLENEN_UZANTILAR:
        raise ValueError(
            f"Desteklenmeyen dosya uzantısı: '{uzanti or '(yok)'}'. "
            "Kullanılabilir uzantılar: .json, .csv, .xlsx"
        )

    try:
        if uzanti == ".json":
            ham = pd.read_json(yol, dtype=object, convert_dates=False)
            if isinstance(ham, dict) or not hasattr(ham, "to_dict"):
                raise ValueError("JSON kökü bir kayıt listesi olmalıdır")
            tablo = ham
        elif uzanti == ".csv":
            tablo = pd.read_csv(yol, encoding="utf-8-sig", dtype=object, keep_default_na=True)
        else:
            tablo = pd.read_excel(yol, dtype=object, keep_default_na=True)

        if tablo.empty and len(tablo.columns) == 0:
            raise ValueError("Dosya boş görünüyor veya sütun başlığı yok")
        return _tabloyu_sozluk_listesine_cevir(tablo)
    except (FileNotFoundError, ValueError):
        raise
    except Exception as hata:
        raise ValueError(f"Dosya okunamadı ({yol}): {hata}") from hata


def sonuclari_disa_aktar(temiz_kayitlar, hatali_kayitlar, cikis_klasoru="cikti"):
    """Temiz ve hatalı kayıtları CSV (utf-8-sig) ve Excel olarak kaydeder."""
    klasor = Path(cikis_klasoru)
    try:
        klasor.mkdir(parents=True, exist_ok=True)
        temiz_tablo = pd.DataFrame(temiz_kayitlar)
        hatali_tablo = pd.DataFrame(hatali_kayitlar)
        temiz_sirasi = [s for s in ("satir_no", "isim", "eposta", "urun", "fiyat") if s in temiz_tablo.columns]
        hatali_sirasi = [s for s in ("satir_no", "isim", "eposta", "urun", "fiyat", "hata_sebebi") if s in hatali_tablo.columns]
        if temiz_sirasi:
            temiz_tablo = temiz_tablo[temiz_sirasi + [s for s in temiz_tablo.columns if s not in temiz_sirasi]]
        if hatali_sirasi:
            hatali_tablo = hatali_tablo[hatali_sirasi + [s for s in hatali_tablo.columns if s not in hatali_sirasi]]

        temiz_csv = klasor / "temiz_kayitlar.csv"
        hatali_csv = klasor / "hatali_kayitlar.csv"
        temiz_xlsx = klasor / "temiz_kayitlar.xlsx"
        hatali_xlsx = klasor / "hatali_kayitlar.xlsx"

        temiz_tablo.to_csv(temiz_csv, index=False, encoding="utf-8-sig")
        hatali_tablo.to_csv(hatali_csv, index=False, encoding="utf-8-sig")
        temiz_tablo.to_excel(temiz_xlsx, index=False)
        hatali_tablo.to_excel(hatali_xlsx, index=False)
    except Exception as hata:
        raise ValueError(f"Sonuçlar dışa aktarılamadı ({klasor}): {hata}") from hata


    return {
        "klasor": klasor,
        "temiz_csv": klasor / "temiz_kayitlar.csv",
        "temiz_xlsx": klasor / "temiz_kayitlar.xlsx",
        "hatali_csv": klasor / "hatali_kayitlar.csv",
        "hatali_xlsx": klasor / "hatali_kayitlar.xlsx",
    }


def ornek_bozuk_excel_olustur(dosya_yolu="ornek_musteri_verisi.xlsx"):
    """ornek_veri.py'deki bozuk kayıtlarla gerçek bir .xlsx test dosyası üretir."""
    yol = Path(dosya_yolu)
    try:
        tablo = pd.DataFrame(ham_siparisler)
        tablo.to_excel(yol, index=False)
    except Exception as hata:
        raise ValueError(f"Örnek Excel oluşturulamadı ({yol}): {hata}") from hata
    return yol
