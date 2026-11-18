"""Veri temizleme uygulamasını başlatır, raporu basar ve dosyalara aktarır."""

import argparse
import json
from pathlib import Path

from dosya_islemleri import (
    dosyadan_veri_oku,
    ornek_bozuk_excel_olustur,
    sonuclari_disa_aktar,
)
from temizleyici import VeriTemizleyici
from veritabani import VeritabaniYoneticisi



def tl_metni(tutar):
    """Sayıyı 1.250,50 TL biçiminde yazar."""
    return f"{tutar:,.2f} TL".replace(",", "X").replace(".", ",").replace("X", ".")


def ham_veriyi_yukle(giris_yolu):
    """--giris yoksa örnek Excel üretir; varsa JSON/CSV/Excel dosyasını okur."""
    if giris_yolu is None:
        yol = ornek_bozuk_excel_olustur("ornek_musteri_verisi.xlsx")
        kaynak = str(yol)
    else:
        yol = Path(giris_yolu)
        kaynak = str(yol)

    try:
        return dosyadan_veri_oku(yol), kaynak
    except Exception as hata:
        raise SystemExit(f"Girdi okunamadı: {hata}") from hata


def json_disa_aktar(cikis_yolu, kaynak, temiz_kayitlar, hatali_kayitlar, ciro):
    """Özet, geçerli ve hatalı kayıtları UTF-8 JSON dosyasına yazar."""
    paket = {
        "ozet": {
            "kaynak": kaynak,
            "toplam_incelenen": len(temiz_kayitlar) + len(hatali_kayitlar),
            "gecerli_kayit": len(temiz_kayitlar),
            "hatali_kayit": len(hatali_kayitlar),
            "toplam_ciro": ciro,
            "toplam_ciro_metin": tl_metni(ciro),
        },
        "temiz_kayitlar": temiz_kayitlar,
        "hatali_kayitlar": hatali_kayitlar,
    }
    yol = Path(cikis_yolu)
    try:
        yol.parent.mkdir(parents=True, exist_ok=True)
        with yol.open("w", encoding="utf-8") as dosya:
            json.dump(paket, dosya, ensure_ascii=False, indent=2)
    except Exception as hata:
        raise SystemExit(f"JSON yazılamadı ({yol}): {hata}") from hata
    return yol


def _sutun_genisligi(kayitlar, anahtar, baslik, en_az=4):
    """Başlık ve değerlerin en uzun metin genişliğini bulur."""
    uzunluklar = [len(baslik)]
    for kayit in kayitlar:
        uzunluklar.append(len(str(kayit.get(anahtar, ""))))
    return max(en_az, max(uzunluklar))


def raporu_yazdir(ham_liste, temiz_kayitlar, hatali_kayitlar, kaynak):
    """İnceleme özetini hizalı sütunlarla basar."""
    toplam = len(ham_liste)
    gecerli_sayisi = len(temiz_kayitlar)
    hatali_sayisi = len(hatali_kayitlar)
    ciro = sum(kayit.get("fiyat", 0) or 0 for kayit in temiz_kayitlar)

    etiket_w = 28
    deger_w = 22
    cizgi = "=" * 78

    print(cizgi)
    print(f"{'SİPARİŞ VERİSİ TEMİZLEME RAPORU':^{len(cizgi)}}")
    print(cizgi)
    print(f"{'Kaynak':<{etiket_w}} {kaynak:>{deger_w}}")
    print(f"{'Toplam incelenen kayıt':<{etiket_w}} {toplam:>{deger_w}d}")
    print(f"{'Temizlenen geçerli kayıt':<{etiket_w}} {gecerli_sayisi:>{deger_w}d}")
    print(f"{'Hatalı / elenen kayıt':<{etiket_w}} {hatali_sayisi:>{deger_w}d}")
    print(f"{'Toplam geçerli sipariş cirosu':<{etiket_w}} {tl_metni(ciro):>{deger_w}}")
    print("-" * 78)

    print("Geçerli kayıtlar:")
    if not temiz_kayitlar:
        print("  (yok)")
    else:
        no_w = max(4, max(len("No"), max(len(str(k["satir_no"])) for k in temiz_kayitlar)))
        isim_w = _sutun_genisligi(temiz_kayitlar, "isim", "İsim")
        posta_w = _sutun_genisligi(temiz_kayitlar, "eposta", "E-posta")
        urun_w = _sutun_genisligi(temiz_kayitlar, "urun", "Ürün")
        fiyat_basliklari = [tl_metni(k["fiyat"]) for k in temiz_kayitlar]
        fiyat_w = max(len("Fiyat"), max(len(m) for m in fiyat_basliklari))

        print(
            f"{'No':>{no_w}}  "
            f"{'İsim':<{isim_w}}  "
            f"{'E-posta':<{posta_w}}  "
            f"{'Ürün':<{urun_w}}  "
            f"{'Fiyat':>{fiyat_w}}"
        )
        print("-" * 78)
        for kayit in temiz_kayitlar:
            print(
                f"{kayit['satir_no']:>{no_w}d}  "
                f"{kayit['isim']:<{isim_w}}  "
                f"{kayit['eposta']:<{posta_w}}  "
                f"{kayit['urun']:<{urun_w}}  "
                f"{tl_metni(kayit['fiyat']):>{fiyat_w}}"
            )

    print("-" * 78)
    print("Hatalı kayıtlar:")
    if not hatali_kayitlar:
        print("  (yok)")
    else:
        no_w = max(8, max(len(str(k.get("satir_no", "?"))) for k in hatali_kayitlar))
        sebep_w = max(
            len("Neden"),
            max(len(str(k.get("hata_sebebi", "Belirtilmedi"))) for k in hatali_kayitlar),
        )
        print(f"{'Satır':>{no_w}}  {'Neden':<{sebep_w}}")
        print("-" * 78)
        for kayit in hatali_kayitlar:
            satir = kayit.get("satir_no", "?")
            sebep = kayit.get("hata_sebebi", "Belirtilmedi")
            print(f"{satir:>{no_w}}  {sebep:<{sebep_w}}")

    print(cizgi)
    return ciro


def argumanlari_ayir():
    """Komut satırı seçeneklerini tanımlar."""
    parser = argparse.ArgumentParser(
        description="Müşteri/sipariş kayıtlarını temizler; CSV, Excel ve JSON üretir.",
    )
    parser.add_argument(
        "--giris",
        "-g",
        metavar="DOSYA",
        help="Ham sipariş dosyası (.json, .csv, .xlsx). Verilmezse örnek Excel üretilir.",
    )
    parser.add_argument(
        "--cikis",
        "-c",
        metavar="KLASOR",
        default="cikti",
        help="Çıktı klasörü (varsayılan: cikti).",
    )
    return parser.parse_args()


def main():
    """CLI'yi çalıştırır, veriyi işler, raporu basar ve CSV/Excel/JSON yazar."""
    args = argumanlari_ayir()
    ham_liste, kaynak = ham_veriyi_yukle(args.giris)
    temizleyici = VeriTemizleyici(ham_liste, log_dosyasi=Path(args.cikis) / "islem_gecmisi.log")
    temiz_kayitlar, hatali_kayitlar = temizleyici.verileri_temizle()

    # SQLite'a kaydet ve bağlantıyı güvenli şekilde kapat
    with VeritabaniYoneticisi(Path(args.cikis) / "siparisler.db") as db:
        db.kayitlari_ekle(kaynak, temiz_kayitlar, hatali_kayitlar)

    ciro = raporu_yazdir(ham_liste, temiz_kayitlar, hatali_kayitlar, kaynak)

    try:
        dosyalar = sonuclari_disa_aktar(temiz_kayitlar, hatali_kayitlar, args.cikis)
    except Exception as hata:
        raise SystemExit(str(hata)) from hata

    json_yol = json_disa_aktar(
        Path(args.cikis) / "rapor.json",
        kaynak,
        temiz_kayitlar,
        hatali_kayitlar,
        ciro,
    )

    print(f"{'Çıktı klasörü':<28} {str(dosyalar['klasor']):>22}")
    print(f"{'Temiz CSV':<28} {str(dosyalar['temiz_csv'].name):>22}")
    print(f"{'Temiz Excel':<28} {str(dosyalar['temiz_xlsx'].name):>22}")
    print(f"{'Hatalı CSV':<28} {str(dosyalar['hatali_csv'].name):>22}")
    print(f"{'Hatalı Excel':<28} {str(dosyalar['hatali_xlsx'].name):>22}")
    print(f"{'JSON çıktı':<28} {json_yol.name:>22}")
    print(f"{'SQLite DB':<28} {'siparisler.db':>22}")


if __name__ == "__main__":
    main()
