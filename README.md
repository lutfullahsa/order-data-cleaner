# Order Data Cleaner / Siparis Verisi Temizleme Araci

[English](#english) | [Turkce](#turkce)

---

## English

### Overview & Problem Solved
This modular Python tool automates the cleaning, validation, and reporting of messy customer and order datasets (Excel .xlsx, .csv, and .json). It eliminates hours of manual spreadsheet cleanup for e-commerce and business operations.

### Key Features
- **Multi-Format Support:** Reads .xlsx, .csv, and .json files seamlessly.
- **Currency & Text Normalization:** Converts messy currency formats (e.g., "1.250,50 TL") into clean floating-point numbers.
- **Error Isolation:** Captures invalid emails, missing names, and negative prices without crashing, exporting them with clear rejection reasons.
- **Duplicate Removal:** Detects and filters out exact duplicate order records.
- **Excel-Ready Exports:** Generates clean and error reports in .xlsx and utf-8-sig .csv formats.

### Installation & Usage
``bash
pip install -r requirements.txt
python main.py
python main.py --giris musteriler.xlsx
``

---

## Turkce

### Proje Amaci ve Cozdugu Is Problemi
Bu moduler Python araci; daginik ve hatali musteri/siparis tablolarini (Excel .xlsx, .csv ve .json) saniyeler icinde temizler, dogrular ve raporlar. Manuel Excel duzenleme is yukunu ortadan kaldirir.

### Temel Ozellikler
- **Coklu Format Destegi:** .xlsx, .csv ve .json dosyalarini dogrudan okur.
- **Para Birimi ve Metin Duzenleme:** "1.250,50 TL" gibi metin formatindaki tutarlari matematiksel sayilara cevirir.
- **Hata Izolasyonu:** Eksik isimleri, hatali e-postalari ve negatif fiyatlari programi cokertmeden yakalar ve eleme nedenleriyle ayri raporlar.
- **Tekrar Kayit Tespiti:** Birebir ayni olan mukerrer siparisleri otomatik ayiklar.
- **Turkce Karakter Uyumlu Cikti:** Sonuclari Microsoft Excel ile tam uyumlu (utf-8-sig) .csv ve .xlsx formatlarinda disa aktarir.

### Kurulum ve Kullanim
``bash
pip install -r requirements.txt
python main.py
python main.py --giris musteriler.xlsx
``
