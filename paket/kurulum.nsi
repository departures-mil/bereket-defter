; Bereket Defter — kurulum (NSIS, kullanıcı başına, tek tık; tr/en/ar). CI: makensis /DVERSION=X.Y.Z /DSRC=..\dist\BereketDefter paket\kurulum.nsi
; Kurulum yeri: %LOCALAPPDATA%\Programs\Bereket Defter\app (yönetici izni gerekmez). Uygulama içi güncelleme (win-app) yalnız app\
; klasörünü değiştirir (app.new → app); kaldırıcı ve kısayol bilgisi üst klasörde kalır, app\ içine program dışında dosya yazılmaz
; (yoksa istemcinin yeniden ürettiği zip CI'dakiyle aynı olmaz ve yama yerine tam paket iner).
; Kayıtlar BURADA DEĞİL: %APPDATA%\AlacakVerecek (ya da eski taşınabilir kurulumun Veriler klasörü — köprü veri-konumu.txt bırakır).
; Kaldırma kayıtlara dokunmaz.
Unicode true
SetCompressor /SOLID lzma
!include "MUI2.nsh"
!include "FileFunc.nsh"

!ifndef VERSION
  !define VERSION "0.0.0"
!endif
!ifndef SRC
  !define SRC "..\dist\BereketDefter"
!endif
!ifndef OUT
  !define OUT "..\dist\BereketDefter-Setup-${VERSION}.exe"
!endif
!define APPNAME "Bereket Defter"
!define EXE "BereketDefter.exe"
!define APPDIR "$INSTDIR\app"
!define UNKEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\BereketDefter"

Name "${APPNAME}"
OutFile "${OUT}"
InstallDir "$LOCALAPPDATA\Programs\${APPNAME}"
InstallDirRegKey HKCU "Software\BereketDefter" "InstallDir"
RequestExecutionLevel user
ShowInstDetails nevershow
AutoCloseWindow true
BrandingText "${APPNAME} ${VERSION}"
VIProductVersion "${VERSION}.0"
VIAddVersionKey "ProductName" "${APPNAME}"
VIAddVersionKey "FileVersion" "${VERSION}"
VIAddVersionKey "ProductVersion" "${VERSION}"
VIAddVersionKey "FileDescription" "${APPNAME} kurulumu"
VIAddVersionKey "LegalCopyright" "departures-mil"

!define MUI_ICON "${__FILEDIR__}\..\masaustu\assets\logo.ico"
!define MUI_UNICON "${__FILEDIR__}\..\masaustu\assets\logo.ico"
!define MUI_INSTFILESPAGE_COLORS "FFFFFF 0F172A"
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "Turkish"
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "Arabic"

LangString KAPAT ${LANG_TURKISH} "Bereket Defter açık. Lütfen kapatıp Tamam'a basın."
LangString KAPAT ${LANG_ENGLISH} "Bereket Defter is running. Please close it and press OK."
LangString KAPAT ${LANG_ARABIC} "برنامج Bereket Defter مفتوح. يرجى إغلاقه ثم الضغط على موافق."

Function .onInit
  ; kurulum penceresi Windows diline göre (yoksa Türkçe)
  System::Call 'kernel32::GetUserDefaultUILanguage() i .r0'
  IntOp $1 $0 & 0x3FF
  StrCpy $LANGUAGE ${LANG_TURKISH}
  IntCmp $1 0x09 0 +2 +2
    StrCpy $LANGUAGE ${LANG_ENGLISH}
  IntCmp $1 0x01 0 +2 +2
    StrCpy $LANGUAGE ${LANG_ARABIC}
FunctionEnd

Section "Kur"
  SetShellVarContext current
  SetOutPath "$INSTDIR"
  ; program güncellemeden sonra kapanıyor olabilir: exe serbest kalana kadar bekle (en çok ~20 sn), sonra kullanıcıya sor
  StrCpy $2 0
  bekle:
    IfFileExists "${APPDIR}\${EXE}" 0 hazir
    ClearErrors
    FileOpen $3 "${APPDIR}\${EXE}" a
    IfErrors 0 acik
    IntOp $2 $2 + 1
    IntCmp $2 40 sor
    Sleep 500
    Goto bekle
  sor:
    MessageBox MB_OKCANCEL|MB_ICONEXCLAMATION "$(KAPAT)" IDOK bekle
    Abort
  acik:
    FileClose $3
  hazir:
  ; eski program dosyaları yeni sürümle karışmasın (kayıtlar burada değil)
  RMDir /r "${APPDIR}"
  RMDir /r "${APPDIR}.new"
  SetOutPath "${APPDIR}"
  File /r "${SRC}\*.*"
  SetOutPath "$INSTDIR"
  WriteUninstaller "$INSTDIR\Kaldir.exe"
  CreateShortCut "$DESKTOP\${APPNAME}.lnk" "${APPDIR}\${EXE}"
  CreateDirectory "$SMPROGRAMS\${APPNAME}"
  CreateShortCut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "${APPDIR}\${EXE}"
  WriteRegStr HKCU "Software\BereketDefter" "InstallDir" "$INSTDIR"
  WriteRegStr HKCU "${UNKEY}" "DisplayName" "${APPNAME}"
  WriteRegStr HKCU "${UNKEY}" "DisplayVersion" "${VERSION}"
  WriteRegStr HKCU "${UNKEY}" "Publisher" "departures-mil"
  WriteRegStr HKCU "${UNKEY}" "DisplayIcon" "${APPDIR}\${EXE}"
  WriteRegStr HKCU "${UNKEY}" "InstallLocation" "$INSTDIR"
  WriteRegStr HKCU "${UNKEY}" "UninstallString" '"$INSTDIR\Kaldir.exe"'
  WriteRegStr HKCU "${UNKEY}" "QuietUninstallString" '"$INSTDIR\Kaldir.exe" /S'
  WriteRegDWORD HKCU "${UNKEY}" "NoModify" 1
  WriteRegDWORD HKCU "${UNKEY}" "NoRepair" 1
  ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
  WriteRegDWORD HKCU "${UNKEY}" "EstimatedSize" "$0"
  ; kurulumdan sonra program açılır (sessiz kurulumda /S da)
  Exec '"${APPDIR}\${EXE}"'
SectionEnd

Section "Uninstall"
  SetShellVarContext current
  Delete "$DESKTOP\${APPNAME}.lnk"
  RMDir /r "$SMPROGRAMS\${APPNAME}"
  RMDir /r "${APPDIR}"
  RMDir /r "${APPDIR}.new"
  RMDir /r "${APPDIR}.bak"
  Delete "$INSTDIR\Kaldir.exe"
  RMDir "$INSTDIR"
  DeleteRegKey HKCU "${UNKEY}"
  DeleteRegKey HKCU "Software\BereketDefter"
SectionEnd
