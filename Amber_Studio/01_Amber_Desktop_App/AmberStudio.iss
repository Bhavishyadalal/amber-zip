; AmberStudio installer script for Inno Setup 6 (free: https://jrsoftware.org/isdl.php)
; Run build_exe.bat first (it creates build\app\AmberStudio), then compile this file.
; build_exe.bat does both steps for you when Inno Setup is installed.

#define MyAppName "Amber Studio"
#define MyAppVersion "1.0"
#define MyAppExe "AmberStudio.exe"

[Setup]
AppId={{D3B15F7A-47B6-4D6B-9B0E-7539A4E20C68}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher=Amber
; Per-user install: no admin prompt, and the app can write its settings and
; data in its own LocalAppData folder.
PrivilegesRequired=lowest
DefaultDirName={localappdata}\Programs\AmberStudio
DisableProgramGroupPage=yes
DisableDirPage=no
DirExistsWarning=no
AlwaysShowDirOnReadyPage=yes
UninstallDisplayName={#MyAppName}
ArchitecturesInstallIn64BitMode=x64
SetupIconFile=amber.ico
UninstallDisplayIcon={app}\{#MyAppExe}
OutputDir=dist
OutputBaseFilename=AmberStudioSetup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
CloseApplications=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &Desktop shortcut"; GroupDescription: "Shortcuts:"
Name: "startmenu"; Description: "Add Amber Studio to the &Start menu"; GroupDescription: "Shortcuts:"

[Files]
Source: "build\app\AmberStudio\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExe}"; WorkingDir: "{app}"; Tasks: startmenu
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExe}"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExe}"; Description: "Launch Amber Studio"; WorkingDir: "{app}"; Flags: nowait postinstall skipifsilent

[InstallDelete]
; A yt-dlp that was updated inside an older install would override the newer one packed in this build.
; Clear it on install; the in-app Update button fetches a newer one again whenever there is one.
Type: filesandordirs; Name: "{localappdata}\AmberStudio\updated_site_packages"

[UninstallDelete]
; Only app-made cache is removed. Your songs, videos, settings and queue
; (downloads, video_downloads, soundboard, soundboard.json, amber_config.json, amber_data.json) are kept.
Type: filesandordirs; Name: "{localappdata}\AmberStudio\updated_site_packages"

[Code]
{ Amber Studio owns its separate data folder; the per-user installation stays writable. }

function IsUnder(Dir, Base: String): Boolean;
begin
  Result := (Base <> '') and (Pos(Lowercase(AddBackslash(Base)), Lowercase(AddBackslash(Dir))) = 1);
end;

function DirHasFiles(Dir: String): Boolean;
var
  FindRec: TFindRec;
begin
  Result := False;
  if FindFirst(AddBackslash(Dir) + '*', FindRec) then
  begin
    try
      repeat
        if (FindRec.Name <> '.') and (FindRec.Name <> '..') then
        begin
          Result := True;
          Break;
        end;
      until not FindNext(FindRec);
    finally
      FindClose(FindRec);
    end;
  end;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
var
  Dir: String;
begin
  Result := True;
  if CurPageID = wpSelectDir then
  begin
    Dir := RemoveBackslash(WizardDirValue);
    if IsUnder(Dir, ExpandConstant('{commonpf}')) or IsUnder(Dir, ExpandConstant('{commonpf32}')) or
       IsUnder(Dir, ExpandConstant('{win}')) then
    begin
      MsgBox('Amber Studio uses a per-user installation. Please choose a writable folder outside Program Files and the Windows folder.' + #13#10 + #13#10 +
             'Please choose another folder, for example D:\AmberStudio or a folder in your user profile.', mbError, MB_OK);
      Result := False;
      Exit;
    end;
    { Existing AmberStudio install (has AmberStudio.exe) is fine. Any other non-empty folder gets its own subfolder. }
    if DirExists(Dir) and DirHasFiles(Dir) and (not FileExists(AddBackslash(Dir) + '{#MyAppExe}')) then
    begin
      if MsgBox('The folder you chose is not empty.' + #13#10 + #13#10 +
                'AmberStudio will be installed into a new "AmberStudio" folder inside it:' + #13#10 +
                AddBackslash(Dir) + 'AmberStudio' + #13#10 + #13#10 + 'Continue?', mbConfirmation, MB_YESNO) = IDYES then
        WizardForm.DirEdit.Text := AddBackslash(Dir) + 'AmberStudio'
      else
        Result := False;
    end;
  end;
end;
