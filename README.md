# Order Data Cleaner / Sipariş Verisi Temizleme Aracı (v2.0)

[English](#english) | [Türkçe](#türkçe)

---

## English

### Overview (v2.0)
The Order Data Cleaner is a robust, modular Python tool for cleaning, validating, and reporting customer and order datasets. **v2.0** introduces a professional Object-Oriented Architecture (`VeriTemizleyici`), advanced data normalization, and native Excel processing.

### What's New in v2.0
- **OOP Architecture:** Refactored into a clean `VeriTemizleyici` class for better scalability.
- **Advanced Normalization:** Intelligent cleaning of phone numbers (+90 format) and multi-format date parsing (e.g., `DD.MM.YYYY`, `YYYY-MM-DD`).
- **Excel Processing:** Shifted to `openpyxl` for high-performance, dependency-free Excel handling.
- **Enhanced Logging:** Integrated `logging` module with real-time stream and file outputs.
- **Detailed Error Reporting:** Now tracks duplicate entries with explicit rejection reasons.

### Usage
```bash
python -m pip install openpyxl
python main.py --giris data.xlsx
```

---

## Türkçe

### Proje Amacı (v2.0)
Dağınık ve hatalı müşteri/sipariş tablolarını (`.xlsx`, `.csv`, `.json`) temizleyen, doğrulayan ve raporlayan modüler bir Python aracıdır. **v2.0** sürümüyle birlikte OOP mimarisine geçilmiş, veri normalizasyonu güçlendirilmiş ve Excel bağımlılığı (`pandas` kaldırıldı) tamamen optimize edilmiştir.

### v2.0 ile Gelen Yenilikler
- **OOP Mimari:** `VeriTemizleyici` sınıf yapısı ile daha modüler ve sürdürülebilir kod.
- **Gelişmiş Normalizasyon:** Telefon numaraları için `+90` standardizasyonu ve esnek tarih (DD.MM.YYYY, YYYY-MM-DD vb.) işleme.
- **Saf Excel Desteği:** `pandas` kaldırıldı, `openpyxl` ile hafif ve performanslı Excel işlemleri sağlandı.
- **Loglama:** İşlem adımlarının, hataların ve rapor özetlerinin `logging` modülü ile takibi.
- **Hata Raporlama:** Tekrar eden kayıtlar artık "Tekrar eden kayıt" sebebiyle hatalı kayıtlar listesine aktarılıyor.

### Kurulum ve Kullanım
```bash
python -m pip install openpyxl
python main.py --giris data.xlsx
```

