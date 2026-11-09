from turkcekit import (kucult, buyult, ascii_cevir, sirala, hecele, ek_getir,
                    kelimeler, var_mi, filtrele, rastgele, ara)


def test_kucult_buyult():
    assert kucult("IŞIK") == "ışık"
    assert kucult("İSTANBUL") == "istanbul"
    assert buyult("ışık") == "IŞIK"
    assert buyult("istanbul") == "İSTANBUL"


def test_ascii():
    assert ascii_cevir("Çığ şöyle güzel") == "Cig soyle guzel"


def test_sirala():
    assert sirala(["zeytin", "çay", "cam", "şeker", "sut", "ılık", "iyi"]) == \
        ["cam", "çay", "ılık", "iyi", "sut", "şeker", "zeytin"]


def test_hecele():
    assert hecele("kitap") == ["ki", "tap"]
    assert hecele("kütüphane") == ["kü", "tüp", "ha", "ne"]
    assert hecele("altın") == ["al", "tın"]
    assert hecele("saat") == ["sa", "at"]
    assert hecele("Türkçe") == ["Türk", "çe"]
    assert hecele("ağ") == ["ağ"]


def test_ek_getir():
    assert ek_getir("kitap", "de") == "kitapta"
    assert ek_getir("ev", "de") == "evde"
    assert ek_getir("ev", "den") == "evden"
    assert ek_getir("kitap", "den") == "kitaptan"
    assert ek_getir("kitap", "ler") == "kitaplar"
    assert ek_getir("ev", "ler") == "evler"
    assert ek_getir("masa", "e") == "masaya"
    assert ek_getir("okul", "i") == "okulu"
    assert ek_getir("göz", "i") == "gözü"
    assert ek_getir("masa", "in") == "masanın"
    assert ek_getir("kitap", "i", yumusama=True) == "kitabı"
    assert ek_getir("çocuk", "a" if False else "e", yumusama=True) == "çocuğa"
    assert ek_getir("renk", "i", yumusama=True) == "rengi"


def test_sozluk():
    assert var_mi("KİTAP") and not var_mi("asdfgh")
    assert len(kelimeler()) > 50
    assert all(len(k) == 5 for k in filtrele(uzunluk=5))
    assert "kalem" in ara("kal")
    assert len(rastgele(uzunluk=5)) == 5
