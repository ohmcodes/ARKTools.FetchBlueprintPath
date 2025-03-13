@echo off
REM Set the path to UE4Editor-Cmd.exe
set UE4EditorPath="C:\Program Files\Epic Games\ARKDevkit\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"

REM Set the path to your project file
set ProjectPath="C:\Program Files\Epic Games\ARKDevkit\Projects\ShooterGame\ShooterGame.uproject"

REM Set the path to your Python script
set ScriptPath="D:\REPO\ARKTools.FetchBlueprintPath\export_weapon_attachments.py"

REM Run the Python script using UE4Editor-Cmd
%UE4EditorPath% %ProjectPath% -run=pythonscript -script=%ScriptPath%

REM Pause the command prompt to see the output
pause