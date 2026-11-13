# Order Data Cleaner / Sipariş Verisi Temizleme Aracı

[English](#english) | [Türkçe](#türkçe)

---

## English

### Overview & Problem Solved
This modular Python tool automates the cleaning, validation, and reporting of messy customer and order datasets (Excel `.xlsx`, `.csv`, and `.json`). It eliminates hours of manual spreadsheet cleanup for e-commerce and business operations.

### Key Features
- **Multi-Format Support:** Reads `.xlsx`, `.csv`, and `.json` files seamlessly.
- **Currency & Text Normalization:** Converts messy currency formats (e.g., `"1.250,50 TL"`) into clean floating-point numbers.
- **Error Isolation:** Captures invalid emails, missing names, and negative prices without crashing, exporting them with clear rejection reasons.
- **Duplicate Removal:** Detects and filters out exact duplicate order records.
- **Excel-Ready Exports:** Generates clean and error reports in `.xlsx` and `utf-8-sig` `.csv` formats.

### Installation & Usage
```bash
pip install -r requirements.txt
python main.py
python main.py --giris musteriler.xlsx
```

---

## Türkçe

### Proje Amacı ve Çözdüğü İş Problemi
Bu modüler Python aracı; dağınık ve hatalı müşteri/sipariş tablolarını (Excel `.xlsx`, `.csv` ve `.json`) saniyeler içinde temizler, doğrular ve raporlar. Manuel Excel düzenleme iş yükünü ortadan kaldırır.

### Temel Özellikler
- **Çoklu Format Desteği:** `.xlsx`, `.csv` ve `.json` dosyalarını doğrudan okur.
- **Para Birimi ve Metin Düzenleme:** `"1.250,50 TL"` gibi metin formatındaki tutarları matematiksel sayılara çevirir.
- **Hata İzolasyonu:** Eksik isimleri, hatalı e-postaları ve negatif fiyatlar gibi geçersiz verileri programı çökertmeden yakalar ve eleme nedenleriyle ayrı raporlar.
- **Tekrar Kayıt Tespiti:** Birebir aynı olan mükerrer siparişleri otomatik ayıklar.
- **Türkçe Karakter Uyumlu Çıktı:** Sonuçları Microsoft Excel ile tam uyumlu (`utf-8-sig`) `.csv` ve `.xlsx` formatlarında dışa aktarır.

### Kurulum ve Kullanım
```bash
pip install -r requirements.txt
python main.py
python main.py --giris musteriler.xlsx
```
