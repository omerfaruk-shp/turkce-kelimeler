	# turkce-kelimeler

[![PyPI version](https://img.shields.io/pypi/v/turkce-kelimeler.svg)](https://pypi.org/project/turkce-kelimeler/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

Türkçe kelime listesi ve dil işleme yardımcıları (`hecele`, `ek getirme`, `İ/ı dönüşümü` vb.).

## Kurulum

Paketi PyPI üzerinden doğrudan kurabilirsiniz:

```bash
pip install turkce-kelimeler
```

## Kullanım

Paket içerisinde gelen temel fonksiyonların kullanımı:

```python
from turkcekit import kucult, hecele, ek_getir, rastgele, sirala

# Türkçe karakterlere duyarlı küçük harf dönüşümü
kucult("IŞIK")            # 'ışık'

# Kelimeleri hecelerine ayırma
hecele("kütüphane")       # ['kü', 'tüp', 'ha', 'ne']

# Kural tabanlı ek getirme ve ünsüz yumuşaması
ek_getir("kitap", "de")   # 'kitapta'
ek_getir("kitap", "i", yumusama=True)  # 'kitabı'

# Belirli uzunlukta rastgele kelime üretme
rastgele(uzunluk=5)       # rastgele 5 harfli kelime

# Türkçe alfabeye göre sıralama
sirala(["çay", "cam", "ılık", "iyi"])  # Türkçe alfabe sırası
```

## Sınırlamalar

- Ek getirme mekanizması kural tabanlıdır; yabancı kökenli kelimelerde (`saat`, `harf`, `kalp`) ve bazı ünsüz yumuşaması istisnalarında hatalar görülebilir.
- Kelime listesi henüz başlangıç aşamasındadır ve geliştirilmeye devam etmektedir.

## Geliştirme ve Katkı

Projeyi yerel ortamınızda geliştirmek veya test etmek için:

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/omerfaruk-shp/turkce-kelimeler.git
   cd turkce-kelimeler
   ```

2. Geliştirme modunda kurun:
   ```bash
   pip install -e .
   ```

3. Testleri çalıştırın:
   ```bash
   pytest
   ```

## Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.
