; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "JCP+ PULP"
#define MyAppVersion GetEnv('AW_VERSION')
#define MyAppPublisher "JCP+"
#define MyAppURL "https://www.jcp.plus/"
#define MyAppExeName "jcp-plus-pulp-qt.exe"
#define RootDir "..\.."
#define DistDir "..\..\dist"

#pragma verboselevel 9

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
; NOTE: the double {{ are used to escape the { character (needed for the AppId)
AppId={{F226B8F4-3244-46E6-901D-0CE8035423E4}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL="https://github.com/jcp-blr/jcp-plus-pulp/issues"
AppUpdatesURL="https://github.com/jcp-blr/jcp-plus-pulp/releases"
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
; Uncomment the following line to run in non administrative install mode (install for current user only.)
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir={#DistDir}
OutputBaseFilename=jcp-plus-pulp-setup
SetupIconFile="{#RootDir}\jcp-plus-pulp-qt\media\logo\logo.ico"
UninstallDisplayName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "StartMenuEntry" ; Description: "Start JCP+ PULP when Windows starts"; GroupDescription: "Windows Startup"; MinVersion: 4,4;

[Files]
Source: "{#DistDir}\jcp-plus-pulp\jcp-plus-pulp-qt.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#DistDir}\jcp-plus-pulp\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: StartMenuEntry;

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

; Removes the previously installed version before installing the new one
; NOTE: Doesn't work? And also discouraged by the docs
;[InstallDelete]
;Type: filesandordirs; Name: "{app}\"