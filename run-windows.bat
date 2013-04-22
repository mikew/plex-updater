@echo off

set strProgramFiles=%ProgramFiles%
if exist "%ProgramFiles(x86)%" set strProgramFiles=%ProgramFiles(x86)%

set PYTHONPATH=%strProgramFiles%\Plex\Plex Media Server\DLLs;%strProgramFiles%\Plex\Plex Media Server\Exts;%LOCALAPPDATA%\Plex Media Server\Plug-ins/Framework.bundle/Contents/Resources/Platforms/Shared/Libraries/
set PLEXBUNDLEDEXTS=1
set PLEXLOCALAPPDATA=%LOCALAPPDATA%
set PLEX_FRAMEWORK_PATH=%LOCALAPPDATA%\Plex Media Server\Plug-ins\Framework.bundle\Contents\Resources\Versions\2\Python

"%strProgramFiles%\Plex\Plex Media Server\PlexScriptHost.exe" "Contents\Tests\nose_runner.py" "%cd%\%1"
