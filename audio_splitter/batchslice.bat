@echo off
setlocal
echo Starting Batch Job ...

echo ================================================
echo === CiTR Audio Archive File Preparation Tool ===
echo ================================================

FOR /R C:\Users\techserv\TOPROCESS  %%f in (*.mp3) do python C:\Users\techserv\Documents\git\DJLand-Tools\audio_splitter\audioslicer.py %%f


echo ================================================
echo ================= JOB COMPLETE =================
echo ================================================
