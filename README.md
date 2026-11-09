# turkcekit

Türkçe kelime listesi ve dil işleme yardımcıları.

```python
from turkcekit import kucult, hecele, ek_getir, rastgele, sirala

kucult("IŞIK")            # 'ışık'
hecele("kütüphane")       # ['kü', 'tüp', 'ha', 'ne']
ek_getir("kitap", "de")   # 'kitapta'
ek_getir("kitap", "i", yumusama=True)  # 'kitabı'
rastgele(uzunluk=5)       # rastgele 5 harfli kelime
sirala(["çay", "cam", "ılık", "iyi"])  # Türkçe alfabe sırası
```

## Sınırlamalar
- Ek getirme kural tabanlıdır; yabancı kökenli kelimelerde (saat, harf, kalp) ve
  ünsüz yumuşaması istisnalarında hata yapabilir.
- Kelime listesi başlangıç aşamasındadır.

## Kurulum (geliştirme)
```
pip install -e .
pytest
```
