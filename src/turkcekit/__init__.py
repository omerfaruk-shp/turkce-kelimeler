"""turkcekit: Türkçe kelime listesi ve dil işleme yardımcıları."""

from .harf import kucult, buyult, bas_harf_buyut, ascii_cevir, sirala
from .ses import hecele, unlu_mu, unsuz_mu, son_unlu, kalin_mi
from .ek import ek_getir, EKLER
from .sozluk import kelimeler, var_mi, filtrele, ara, rastgele

__version__ = "0.1.0"

__all__ = [
    "kucult", "buyult", "bas_harf_buyut", "ascii_cevir", "sirala",
    "hecele", "unlu_mu", "unsuz_mu", "son_unlu", "kalin_mi",
    "ek_getir", "EKLER",
    "kelimeler", "var_mi", "filtrele", "ara", "rastgele",
]
