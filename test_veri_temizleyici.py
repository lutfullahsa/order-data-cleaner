import unittest
from temizleyici import VeriTemizleyici

class TestVeriTemizleyici(unittest.TestCase):
    def test_telefon_temizleme(self):
        t = VeriTemizleyici([])
        self.assertEqual(t.telefon_temizle("0532 123 45 67"), "+90 532 123 45 67")
        self.assertEqual(t.telefon_temizle("+90 (532) 123-45-67"), "+90 532 123 45 67")
        self.assertEqual(t.telefon_temizle("5321234567"), "+90 532 123 45 67")
        self.assertEqual(t.telefon_temizle("00905321234567"), "+90 532 123 45 67")
        with self.assertRaises(ValueError):
            t.telefon_temizle("123")

    def test_tarih_temizleme(self):
        t = VeriTemizleyici([])
        self.assertEqual(t.tarih_temizle("18.11.2026"), "2026-11-18")
        self.assertEqual(t.tarih_temizle("18/11/2026"), "2026-11-18")
        self.assertEqual(t.tarih_temizle("2026-11-18"), "2026-11-18")
        with self.assertRaises(ValueError):
            t.tarih_temizle("32.13.2026")

    def test_verileri_temizle(self):
        ham = [{
            "isim": "Ali Yılmaz", 
            "eposta": "ali@example.com", 
            "fiyat": 150, 
            "telefon": "05321234567", 
            "tarih": "18.11.2026"
        }]
        t = VeriTemizleyici(ham)
        temiz, hatali = t.verileri_temizle()
        self.assertEqual(len(temiz), 1)
        self.assertEqual(temiz[0]["telefon"], "+90 532 123 45 67")
        self.assertEqual(temiz[0]["tarih"], "2026-11-18")

if __name__ == "__main__":
    unittest.main()
