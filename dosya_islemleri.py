import csv
import json
from pathlib import Path
import openpyxl

# Gerekli kütüphaneyi içe aktardık
# import pandas kaldırıldı.

DESTEKLENEN_UZANTILAR = {".json", ".csv", ".xlsx"}

def dosyadan_veri_oku(dosya_yolu):
    yol = Path(dosya_yolu)
    if not yol.exists(): raise FileNotFoundError("Dosya bulunamadı")
    
    uzanti = yol.suffix.lower()
    if uzanti == ".json":
        with open(yol, 'r', encoding='utf-8') as f: return json.load(f)
    elif uzanti == ".csv":
        with open(yol, 'r', encoding='utf-8-sig') as f:
            return list(csv.DictReader(f))
    elif uzanti == ".xlsx":
        wb = openpyxl.load_workbook(yol, data_only=True)
        ws = wb.active
        data = list(ws.iter_rows(values_only=True))
        keys = data[0]
        return [dict(zip(keys, row)) for row in data[1:]]
    raise ValueError("Desteklenmeyen format")

def sonuclari_disa_aktar(temiz_kayitlar, hatali_kayitlar, cikis_klasoru="cikti"):
    klasor = Path(cikis_klasoru)
    klasor.mkdir(parents=True, exist_ok=True)
    
    # CSV Yazma
    for isim, veri in [("temiz_kayitlar.csv", temiz_kayitlar), ("hatali_kayitlar.csv", hatali_kayitlar)]:
        if veri:
            with open(klasor / isim, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=veri[0].keys())
                writer.writeheader()
                writer.writerows(veri)
    
    # Excel Yazma (openpyxl)
    for isim, veri in [("temiz_kayitlar.xlsx", temiz_kayitlar), ("hatali_kayitlar.xlsx", hatali_kayitlar)]:
        if veri:
            wb = openpyxl.Workbook()
            ws = wb.active
            headers = list(veri[0].keys())
            ws.append(headers)
            for row in veri: ws.append(list(row.values()))
            wb.save(klasor / isim)
            
    return {
        "klasor": klasor,
        "temiz_csv": klasor / "temiz_kayitlar.csv",
        "temiz_xlsx": klasor / "temiz_kayitlar.xlsx",
        "hatali_csv": klasor / "hatali_kayitlar.csv",
        "hatali_xlsx": klasor / "hatali_kayitlar.xlsx",
    }

def ornek_bozuk_excel_olustur(dosya_yolu="ornek_musteri_verisi.xlsx"):
    from ornek_veri import ham_siparisler
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(list(ham_siparisler[0].keys()))
    for row in ham_siparisler: ws.append(list(row.values()))
    wb.save(dosya_yolu)
    return Path(dosya_yolu)


