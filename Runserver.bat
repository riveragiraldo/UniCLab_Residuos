@echo off
REM Comprobar si hay sesiones activas de ngrok y cerrarlas
C:\ngrok\ngrok.exe kill-all

REM Cambiar directorio al proyecto
cd C:\UniCLab_Residuos

REM Activar el entorno virtual
call env\Scripts\activate

REM Iniciar el servidor Django en segundo plano
start /b python manage.py runserver

REM Iniciar ngrok con el archivo de configuración
C:\ngrok\ngrok.exe start --all --config C:\ngrok\ngrok.yml

pause
