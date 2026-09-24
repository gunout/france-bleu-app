@echo off
echo ============================================================
echo   Gunout Player - Edition France Bleu / ICI
echo   Installation automatique (Windows)
echo ============================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe.
    echo Telechargez Python 3.10+ : https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [INFO] Creation de l'environnement virtuel...
python -m venv .venv
call .venv\Scripts\activate.bat

echo [INFO] Mise a jour de pip...
python -m pip install --upgrade pip

echo [INFO] Installation des dependances Python...
pip install -r requirements.txt

echo.
echo [INFO] Verification de yt-dlp...
yt-dlp --version >nul 2>&1
if errorlevel 1 (
    echo [!] yt-dlp n'est pas dans le PATH.
    echo Telechargez-le : https://github.com/yt-dlp/yt-dlp/releases
    echo Placez yt-dlp.exe dans le dossier du projet ou dans C:\Windows\System32
)

echo.
echo ============================================================
echo   INSTALLATION TERMINEE
echo ============================================================
echo.
echo Pour lancer le player :
echo   .venv\Scripts\activate.bat
echo   python fr.py
echo.
pause
