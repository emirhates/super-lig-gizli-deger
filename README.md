# ⚽ Süper Lig Gizli Değerli Oyuncular

Piyasa değeri düşük ama performansı yüksek oyuncuları veriyle bulan analiz projesi.

## Proje Hakkında
Bu proje FBref ve Transfermarkt verilerini birleştirerek Süper Lig'deki "gizli değerli" oyuncuları tespit ediyor. Scoutların manuel yaptığı işi veri bilimi ile otomatikleştiriyor.

## Kullanılan Yöntemler
- Web scraping (BeautifulSoup, requests)
- Veri temizleme ve birleştirme (pandas)
- Bulanık eşleştirme (fuzzy matching)
- Performans skoru hesaplama (pozisyon bazlı)
- Yaş faktörü analizi
- Görselleştirme (matplotlib)
- Web uygulaması (Streamlit)

## Veri Kaynakları
- [FBref](https://fbref.com) — oyuncu istatistikleri
- [Transfermarkt](https://transfermarkt.com.tr) — piyasa değerleri

## Kurulum
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Sonuçlar
![Gizli Değer Grafiği](gizli_deger_grafik.png)
