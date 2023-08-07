Name "{appName}{ver}"
OutFile "{Name} installer.exe"
RequestExecutionLevel admin
Unicode True
AllowRootDirInstall true
{optional}
!include "MUI2.nsh"
!include "x64.nsh"
;Interface Settings
;--------------------------------
  !define MUI_ABORTWARNING
  !define MUI_HEADERIMAGE
;  !define MUI_HEADERIMAGE_BITMAP       "C:\Users\RG\Desktop\AmirAli's Files\Namava Downloader\build\{appName}\nsis3\nsis3-metro-right.bmp"
;  !define MUI_WELCOMEFINISHPAGE_BITMAP "C:\Users\RG\Desktop\AmirAli's Files\Namava Downloader\build\{appName}\nsis3\nsis3-metro.bmp"
;--------------------------------
;Pages
;--------------------------------
  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES
  ;------------------------------
  ; Finish Page
  ;------------------------------
  ; 1 Checkbox to launch the app.
  {launch}
  !insertmacro MUI_PAGE_FINISH
  !insertmacro MUI_UNPAGE_WELCOME
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  !insertmacro MUI_UNPAGE_FINISH
;--------------------------------
;Languages
  !insertmacro MUI_LANGUAGE "English"
;--------------------------------
InstallDirRegKey HKLM "Software\{appName}" ""
UninstPage uninstConfirm
UninstPage instfiles
InstallDir "$PROGRAMFILES\{appName}"
Section 
  ${If} ${RunningX64}
    SetRegView 64
  ${Else}
    SetRegView 32
  ${EndIf}
  SetOutPath $INSTDIR
  File /r "{thisPath}\dist\{Name}\*"
  WriteRegStr HKLM "SOFTWARE\Namava_Downloader_X" "Install_Dir" "$INSTDIR"
  CreateShortcut "$DESKTOP\{appName}.lnk" "$INSTDIR\{appName}.exe"
  CreateShortcut "$SMPROGRAMS\{appName}.lnk" "$INSTDIR\{appName}.exe"
SectionEnd