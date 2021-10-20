@echo off
del .\test\*.j.gold
for /f %%f in ('dir /b .\test\*.j') do (
    "python" .\gen.py .\test\%%f  > .\test\%%f.gold 2>&1
    echo Wrote to .\test\%%f.gold
)