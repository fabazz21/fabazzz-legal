@echo off
echo ================================
echo Projector Fusion - Installation
echo ================================
echo.

echo [1/5] Mise a jour de pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 goto :error

echo.
echo [2/5] Installation de pygame (pre-compile)...
pip install pygame==2.5.2 --only-binary :all:
if %errorlevel% neq 0 goto :error

echo.
echo [3/5] Installation de moderngl et numpy...
pip install moderngl==5.10.0 numpy==1.26.4
if %errorlevel% neq 0 goto :error

echo.
echo [4/5] Installation de pyrr et Pillow...
pip install pyrr==0.10.3 Pillow==10.2.0
if %errorlevel% neq 0 goto :error

echo.
echo [5/5] Installation de imgui...
pip install imgui[pygame]==2.0.0
if %errorlevel% neq 0 (
    echo Tentative sans extras...
    pip install imgui==2.0.0
    if %errorlevel% neq 0 goto :error
)

echo.
echo ================================
echo Installation terminee avec succes !
echo ================================
echo.
echo Pour lancer l'application :
echo python main.py
echo.
pause
exit /b 0

:error
echo.
echo ================================
echo ERREUR lors de l'installation !
echo ================================
echo.
echo Consultez INSTALL.md pour plus d'aide
echo.
pause
exit /b 1
