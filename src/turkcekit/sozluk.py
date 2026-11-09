"""Paketle birlikte gelen kelime listesi ve arama/filtreleme işlevleri."""

import random as _random
from functools import lru_cache
from importlib import resources

from .harf import kucult, sirala


@lru_cache(maxsize=1)
def kelimeler() -> tuple:
    """Kelime listesini Türkçe alfabe sırasıyla (tuple olarak) döndürür."""
    metin = resources.files("turkcekit").joinpath("data/kelimeler.txt").read_text(encoding="utf-8")
    liste = {kucult(s.strip()) for s in metin.splitlines() if s.strip() and not s.startswith("#")}
    return tuple(sirala(liste))


def var_mi(kelime: str) -> bool:
    return kucult(kelime) in set(kelimeler())


def filtrele(uzunluk=None, baslangic=None, bitis=None, iceren=None) -> list:
    """Kelimeleri uzunluğa, başlangıca, bitişe veya içerdiği harflere göre süzer."""
    sonuc = []
    for k in kelimeler():
        if uzunluk is not None and len(k) != uzunluk:
            continue
        if baslangic is not None and not k.startswith(kucult(baslangic)):
            continue
        if bitis is not None and not k.endswith(kucult(bitis)):
            continue
        if iceren is not None and any(h not in k for h in kucult(iceren)):
            continue
        sonuc.append(k)
    return sonuc


def ara(onek: str) -> list:
    """Verilen önekle başlayan kelimeler."""
    return filtrele(baslangic=onek)


def rastgele(uzunluk=None, **kwargs) -> str:
    """Rastgele bir kelime seçer (filtrelerle birlikte kullanılabilir)."""
    adaylar = filtrele(uzunluk=uzunluk, **kwargs)
    if not adaylar:
        raise ValueError("Bu ölçütlere uyan kelime yok")
    return _random.choice(adaylar)
