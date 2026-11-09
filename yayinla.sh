#!/usr/bin/env bash
# Kullanım:
#   ./yayinla.sh PAKET_ADI [--import-adi IMPORT_ADI] [--hedef test|pypi|yok]
#
# Örnekler:
#   ./yayinla.sh turkce-kelimeler                 # sadece pip adını değiştir, TestPyPI'ye yükle
#   ./yayinla.sh turkcekit --import-adi turkcekit # pip adı + import adı birlikte değişir
#   ./yayinla.sh turkce-kelimeler --hedef pypi    # gerçek PyPI'ye yükle
#   ./yayinla.sh turkce-kelimeler --hedef yok     # sadece değiştir ve derle
#
# Proje kök klasöründe (pyproject.toml'un olduğu yerde) çalıştır.

set -euo pipefail

RENK_K="\033[31m"; RENK_Y="\033[32m"; RENK_S="\033[33m"; RENK_0="\033[0m"
bilgi() { echo -e "${RENK_Y}==>${RENK_0} $*"; }
uyari() { echo -e "${RENK_S}!!${RENK_0}  $*"; }
hata()  { echo -e "${RENK_K}HATA:${RENK_0} $*" >&2; exit 1; }

# ---------- Argümanlar ----------
[[ $# -ge 1 ]] || hata "Paket adı gerekli. Örnek: ./yayinla.sh turkce-kelimeler"

YENI_AD="$1"; shift
IMPORT_ADI=""
HEDEF="test"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --import-adi) IMPORT_ADI="${2:-}"; shift 2 ;;
    --hedef)      HEDEF="${2:-}"; shift 2 ;;
    *) hata "Bilinmeyen seçenek: $1" ;;
  esac
done

RE_HEDEF='^(test|pypi|yok)$'
[[ "$HEDEF" =~ $RE_HEDEF ]] || hata "--hedef değeri test, pypi veya yok olmalı"
RE_AD='^[A-Za-z0-9]([A-Za-z0-9._-]*[A-Za-z0-9])?$'
[[ "$YENI_AD" =~ $RE_AD ]] || hata "Geçersiz paket adı: $YENI_AD"

[[ -f pyproject.toml ]] || hata "pyproject.toml bulunamadı. Scripti proje kök klasöründe çalıştır."
[[ -d src ]] || hata "src/ klasörü bulunamadı."

# Mevcut import (klasör) adı: src altındaki tek paket
PAKETLER=()
while IFS= read -r p; do PAKETLER+=("$p"); done < <(find src -mindepth 1 -maxdepth 1 -type d ! -name '*.egg-info' ! -name '__pycache__' -exec basename {} \;)
[[ ${#PAKETLER[@]} -eq 1 ]] || hata "src/ altında tek bir paket klasörü bekleniyordu, bulunan: ${PAKETLER[*]:-yok}"
ESKI_IMPORT="${PAKETLER[0]}"

if [[ -n "$IMPORT_ADI" ]]; then
  RE_IMPORT='^[a-z_][a-z0-9_]*$'
  [[ "$IMPORT_ADI" =~ $RE_IMPORT ]] || hata "Import adı küçük harf, rakam ve alt çizgiden oluşmalı: $IMPORT_ADI"
fi

# ---------- Gerekli araçlar ----------
command -v perl >/dev/null || hata "perl gerekli."
if [[ "$HEDEF" != "yok" ]]; then
  command -v twine >/dev/null || hata "twine yüklü değil. Kur: python3 -m pip install build twine (gerekirse bir venv içinde)"
fi
python3 -c "import build" 2>/dev/null || hata "build modülü yüklü değil. Kur: python3 -m pip install build twine (gerekirse bir venv içinde)"

# ---------- Ad uygunluk kontrolü ----------
ad_kontrol() {
  local site="$1" kod
  kod=$(curl -s -L -o /dev/null -w "%{http_code}" --max-time 10 "https://${site}/pypi/${YENI_AD}/json" || true)
  case "$kod" in
    404) bilgi "'${YENI_AD}' ${site} üzerinde BOŞ görünüyor." >&2 ;;
    200) uyari "'${YENI_AD}' ${site} üzerinde ZATEN ALINMIŞ olabilir. Yükleme 403 verebilir." >&2 ;;
    *)   uyari "${site} kontrol edilemedi (HTTP ${kod:-yok}). Elle bak: https://${site}/project/${YENI_AD}/" >&2 ;;
  esac
  echo "$kod"
}

bilgi "Ad kontrolü yapılıyor..."
KOD_TEST=$(ad_kontrol test.pypi.org | tail -n1)
KOD_PYPI=$(ad_kontrol pypi.org | tail -n1)

if [[ "$HEDEF" == "test" && "$KOD_TEST" == "200" ]] || [[ "$HEDEF" == "pypi" && "$KOD_PYPI" == "200" ]]; then
  read -r -p "Seçilen hedefte bu ad dolu görünüyor. Yine de devam edilsin mi? [e/H] " cevap
  [[ "$cevap" == "e" || "$cevap" == "E" ]] || hata "İptal edildi. Başka bir ad dene."
fi

# ---------- Dağıtım adını değiştir ----------
bilgi "pyproject.toml içinde paket adı -> ${YENI_AD}"
perl -pi -e 's/^name\s*=\s*".*"/name = "'"$YENI_AD"'"/' pyproject.toml

# ---------- Import adını değiştir (isteğe bağlı) ----------
if [[ -n "$IMPORT_ADI" && "$IMPORT_ADI" != "$ESKI_IMPORT" ]]; then
  bilgi "Import adı: ${ESKI_IMPORT} -> ${IMPORT_ADI}"
  [[ ! -e "src/${IMPORT_ADI}" ]] || hata "src/${IMPORT_ADI} zaten var."
  mv "src/${ESKI_IMPORT}" "src/${IMPORT_ADI}"

  # Kaynak, test ve README içindeki tam kelime eşleşmeleri
  while IFS= read -r -d '' dosya; do
    perl -pi -e 's/\b'"$ESKI_IMPORT"'\b/'"$IMPORT_ADI"'/g' "$dosya"
  done < <(find src tests -type f -name '*.py' -print0 2>/dev/null)
  [[ -f README.md ]] && perl -pi -e 's/\b'"$ESKI_IMPORT"'\b(?!-)/'"$IMPORT_ADI"'/g' README.md

  # pyproject: package-data anahtarı
  perl -pi -e 's/^'"$ESKI_IMPORT"'(\s*=\s*\[)/'"$IMPORT_ADI"'$1/' pyproject.toml
  ESKI_IMPORT="$IMPORT_ADI"
else
  bilgi "Import adı değişmiyor: ${ESKI_IMPORT}"
fi

# ---------- Temizle ve derle ----------
bilgi "Eski derleme çıktıları siliniyor..."
rm -rf dist build src/*.egg-info

bilgi "Derleniyor..."
python3 -m build

if command -v twine >/dev/null; then
  bilgi "twine check..."
  twine check dist/*
fi

# ---------- Yükle ----------
case "$HEDEF" in
  yok)
    bilgi "Hedef 'yok': yükleme yapılmadı. Çıktılar dist/ içinde." ;;
  test)
    bilgi "TestPyPI'ye yükleniyor (kullanıcı adı: __token__, parola: test.pypi.org token'ın)"
    twine upload --repository testpypi dist/*
    echo
    bilgi "Denemek için (temiz bir ortamda):"
    echo "  pip install --index-url https://test.pypi.org/simple/ ${YENI_AD}"
    echo "  python3 -c \"import ${ESKI_IMPORT}; print(${ESKI_IMPORT}.__version__)\"" ;;
  pypi)
    read -r -p "GERÇEK PyPI'ye yüklenecek ve geri alınamaz. Devam? [e/H] " cevap
    [[ "$cevap" == "e" || "$cevap" == "E" ]] || hata "İptal edildi."
    twine upload dist/*
    echo
    bilgi "Kurulum: pip install ${YENI_AD}" ;;
esac

bilgi "Bitti."
