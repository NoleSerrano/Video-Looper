@echo off
cd "path\to\your\folder"

for %%i in (*.mp4) do (
    if /I not "%%i"=="input.mp4" (
        del /Q "%%i"
    )
)