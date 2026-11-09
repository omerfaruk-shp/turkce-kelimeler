"""Türkçe harf işlemleri: büyük/küçük harf, ASCII dönüşümü, alfabetik sıralama."""

ALFABE = "abcçdefgğhıijklmnoöprsştuüvyz"

_ASCII = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")


def kucult(metin: str) -> str:
    """Türkçe kurallarına göre küçük harfe çevirir (I -> ı, İ -> i)."""
    return metin.replace("I", "ı").replace("İ", "i").lower()


def buyult(metin: str) -> str:
    """Türkçe kurallarına göre büyük harfe çevirir (i -> İ, ı -> I)."""
    return metin.replace("i", "İ").replace("ı", "I").upper()


def bas_harf_buyut(metin: str) -> str:
    """Her kelimenin ilk harfini Türkçe kurallarına göre büyütür."""
    return " ".join(
        buyult(k[0]) + kucult(k[1:]) if k else k for k in metin.split(" ")
    )


def ascii_cevir(metin: str) -> str:
    """Türkçe karakterleri ASCII karşılıklarına çevirir (şğüöçı -> sguoci)."""
    return metin.translate(_ASCII)


def sirala_anahtar(kelime: str):
    """Türkçe alfabe sırasına göre sıralama anahtarı üretir."""
    sira = {h: i for i, h in enumerate(ALFABE)}
    return [sira.get(h, len(ALFABE) + ord(h)) for h in kucult(kelime)]


def sirala(kelimeler, ters: bool = False):
    """Kelimeleri Türkçe alfabe sırasına göre sıralar (c < ç, ı < i, s < ş ...)."""
    return sorted(kelimeler, key=sirala_anahtar, reverse=ters)
