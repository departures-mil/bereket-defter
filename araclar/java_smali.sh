#!/usr/bin/env bash
# Android Java eki (android/java: FcGuncelle + ortak FcDelta) → dex → smali → android/smali/ (apktool ağacına katılır).
# Java kaynağı değişince çalıştırın; üretilen smali depoya eklenir (CI test adımı güncel mi diye denetler: --kontrol).
# Gerekenler: JDK 17+, android.jar (ANDROID_JAR ya da ~/.cache/og-apk/android.jar), d8 (R8_JAR ya da Android SDK build-tools),
# apktool.jar (baksmali; APKTOOL_JAR ya da ~/.cache/og-apk/apktool.jar).
set -euo pipefail
KOK="$(cd "$(dirname "$0")/.." && pwd)"
C="${HOME}/.cache/og-apk"
AJAR="${ANDROID_JAR:-$C/android.jar}"
APKTOOL="${APKTOOL_JAR:-$C/apktool.jar}"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
mkdir -p "$T/cls" "$T/dex" "$T/smali"
find "$KOK/android/java" "$KOK/android/java-stub" -name '*.java' > "$T/src.txt"
javac -nowarn --release 8 -encoding UTF-8 -cp "$AJAR" -d "$T/cls" @"$T/src.txt" 2>&1 | grep -v "^warning\|^Note\|JAVA_TOOL\|_JAVA_OPT" || true
# taslaklar (smali'de zaten var olan sınıflar) dex'e girmez
rm -f "$T/cls/com/bereket/alacakverecek/FilesProvider.class" "$T/cls/com/bereket/alacakverecek/Reminders.class"
CLASSES=$(cd "$T/cls" && find . -name '*.class' | sort)
if [ -n "${R8_JAR:-}" ] || [ -f "$C/r8.jar" ]; then
  (cd "$T/cls" && java -cp "${R8_JAR:-$C/r8.jar}" com.android.tools.r8.D8 --release --min-api 23 --lib "$AJAR" --output "$T/dex" $CLASSES)
else
  (cd "$T/cls" && d8 --release --min-api 23 --lib "$AJAR" --output "$T/dex" $CLASSES)
fi
mkdir -p "$T/bk"
javac -nowarn -cp "$APKTOOL" -d "$T/bk" "$KOK/araclar/apk/Baksmali.java" 2>&1 | grep -v "JAVA_TOOL\|_JAVA_OPT" || true
java -cp "$APKTOOL:$T/bk" Baksmali "$T/dex/classes.dex" "$T/smali" 2>&1 | grep -v "JAVA_TOOL\|_JAVA_OPT" || true
if [ "${1:-}" = "--kontrol" ]; then
  for f in $(cd "$T/smali" && find . -name '*.smali'); do
    cmp -s "$T/smali/$f" "$KOK/android/smali/$f" || { echo "GÜNCEL DEĞİL: android/smali/$f → bash araclar/java_smali.sh"; exit 1; }
  done
  echo "Java eki smali güncel"; exit 0
fi
cp -r "$T/smali/." "$KOK/android/smali/"
(cd "$T/smali" && find . -name '*.smali' | sort)
