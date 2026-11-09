"""Türkçe ek getirme (ünlü uyumu ve ünsüz benzeşmesine göre)."""

from .harf import kucult
from .ses import UNLULER, SERT_UNSUZLER, son_unlu

_DORT = {"a": "ı", "ı": "ı", "e": "i", "i": "i", "o": "u", "u": "u", "ö": "ü", "ü": "ü"}
_YUMUSAMA = {"p": "b", "ç": "c", "t": "d", "k": "ğ"}

EKLER = {
    "ler": "çoğul (kitaplar, evler)",
    "de": "bulunma (kitapta, evde)",
    "den": "ayrılma (kitaptan, evden)",
    "e": "yönelme (kitaba, eve)",
    "i": "belirtme (kitabı, evi)",
    "in": "tamlayan (kitabın, evin)",
}


def _iki(unlu: str) -> str:
    return "a" if unlu in "aıou" else "e"


def _yumusat(kelime: str) -> str:
    son = kucult(kelime[-1])
    if son not in _YUMUSAMA:
        return kelime
    if son == "k" and len(kelime) > 1 and kucult(kelime[-2]) == "n":
        return kelime[:-1] + "g"  # renk -> rengi
    return kelime[:-1] + _YUMUSAMA[son]


def ek_getir(kelime: str, ek: str, yumusama: bool = False) -> str:
    """Kelimeye uyuma uygun eki getirir.

    ek: 'ler', 'de', 'den', 'e', 'i', 'in' (bkz. EKLER).
    yumusama: True ise ünlüyle başlayan eklerde p/ç/t/k -> b/c/d/ğ yumuşaması
    uygulanır (kitap -> kitabı). Bu kural istisnalıdır (devlet -> devleti,
    saat -> saati), bu yüzden varsayılan olarak kapalıdır.
    """
    if ek not in EKLER:
        raise ValueError(f"Desteklenmeyen ek: {ek!r}. Seçenekler: {', '.join(EKLER)}")
    if not kelime:
        raise ValueError("Boş kelime")

    son = kucult(kelime[-1])
    unlu_ile_biter = son in UNLULER
    u = son_unlu(kelime)

    if ek == "ler":
        return kelime + "l" + _iki(u) + "r"

    if ek in ("de", "den"):
        d = "t" if son in SERT_UNSUZLER else "d"
        return kelime + d + _iki(u) + ("n" if ek == "den" else "")

    govde = kelime
    if yumusama and not unlu_ile_biter:
        govde = _yumusat(kelime)

    if ek == "e":
        return govde + ("y" if unlu_ile_biter else "") + _iki(u)
    if ek == "i":
        return govde + ("y" if unlu_ile_biter else "") + _DORT[u]
    # ek == "in"
    return govde + ("n" if unlu_ile_biter else "") + _DORT[u] + "n"
