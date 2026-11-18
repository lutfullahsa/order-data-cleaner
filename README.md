# Order Data Cleaner / Sipariş Verisi Temizleme Aracı (v2.2)

[English](#english) | [Türkçe](#türkçe)

---

## English / Türkçe

### Overview / Proje Amacı (v2.2)
The Order Data Cleaner is a modular Python ETL tool for cleaning, validating, and storing messy datasets (`.xlsx`, `.csv`, `.json`) into **SQLite** with duplicate protection. / Dağınık müşteri ve sipariş tablolarını temizleyen, doğrulayan ve **SQLite** veritabanına aktaran modüler bir Python ETL aracıdır.

### Key Features / Öne Çıkan Özellikler
- **OOP Architecture:** Clean `VeriTemizleyici` and `VeritabaniYoneticisi` classes. / Modüler sınıf yapısı.
- **SQLite Persistence:** Automatically stores records into `siparisler.db` with duplicate-file protection. / Verileri `siparisler.db` veritabanına kaydeder ve mükerrer yüklemeleri önler.
- **Normalization & Support:** Standardizes Turkish phone numbers, dates, and uses `openpyxl` for Excel. / Telefon numaralarını ve tarihleri standardize eder, `openpyxl` desteği sunar.

### Usage / Kullanım
```bash
python -m pip install openpyxl
python main.py --giris data.xlsx
```
