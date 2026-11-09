"""Türkçe ses bilgisi: ünlü/ünsüz, hece ayırma, ünlü uyumu."""

from .harf import kucult

UNLULER = "aeıioöuü"
KALIN_UNLULER = "aıou"
INCE_UNLULER = "eiöü"
DUZ_UNLULER = "aeıi"
YUVARLAK_UNLULER = "oöuü"
SERT_UNSUZLER = "fstkçşhp"


def unlu_mu(harf: str) -> bool:
    return len(harf) == 1 and kucult(harf) in UNLULER


def unsuz_mu(harf: str) -> bool:
    return len(harf) == 1 and harf.isalpha() and kucult(harf) not in UNLULER


def unlu_sayisi(kelime: str) -> int:
    return sum(1 for h in kelime if unlu_mu(h))


def son_unlu(kelime: str) -> str:
    """Kelimedeki son ünlüyü (küçük harfle) döndürür."""
    for h in reversed(kucult(kelime)):
        if h in UNLULER:
            return h
    raise ValueError(f"'{kelime}' kelimesinde ünlü yok")


def hecele(kelime: str) -> list:
    """Kelimeyi hecelerine ayırır.

    Kural: her hecede tek ünlü vardır. İki ünlü arasındaki ünsüz sayısı
    0 ise ünlüler ayrılır (sa-at), 1 ise ünsüz sonraki heceye geçer (ka-pı),
    2 ise ilk ünsüz öncekinde kalır (al-tın), 3 veya daha fazlaysa ilk ikisi
    öncekinde kalır (Türk-çe, kont-rol).
    """
    k = kucult(kelime)
    unlu_idx = [i for i, h in enumerate(k) if h in UNLULER]
    if not unlu_idx:
        return [kelime] if kelime else []

    sinirlar = [0]
    for a, b in zip(unlu_idx, unlu_idx[1:]):
        aradaki = b - a - 1
        if aradaki == 0:
            sinirlar.append(b)
        elif aradaki == 1:
            sinirlar.append(a + 1)
        elif aradaki == 2:
            sinirlar.append(a + 2)
        else:
            sinirlar.append(a + 3)
    sinirlar.append(len(kelime))
    return [kelime[s:e] for s, e in zip(sinirlar, sinirlar[1:])]


def kalin_mi(kelime: str) -> bool:
    """Kelimenin son ünlüsü kalın mı? (a, ı, o, u)"""
    return son_unlu(kelime) in KALIN_UNLULER


def buyuk_unlu_uyumuna_uyar_mi(kelime: str) -> bool:
    """Kelimedeki tüm ünlüler ya kalın ya ince mi? (Bileşik/yabancı kelimeler uymayabilir.)"""
    unluler = [h for h in kucult(kelime) if h in UNLULER]
    return all(u in KALIN_UNLULER for u in unluler) or all(
        u in INCE_UNLULER for u in unluler
    )
