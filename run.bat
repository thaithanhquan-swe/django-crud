@echo off
title NexusAdmin - Product CRUD
chcp 65001 >nul
echo ====================================================
echo        NexusAdmin - Django Product Management
echo        Khong can dang nhap (Zero Authentication)
echo ====================================================
echo.

if exist ".venv\Scripts\python.exe" (
    echo [*] Su dung moi truong ao .venv...
    set "PYTHON_EXE=.venv\Scripts\python.exe"
) else (
    echo [*] Dang tao moi truong ao .venv...
    py -m venv .venv
    set "PYTHON_EXE=.venv\Scripts\python.exe"
    echo [*] Cai dat cac thu vien can thiet...
    %PYTHON_EXE% -m pip install -r requirements.txt
)

echo [*] Kiem tra va cap nhat Database...
%PYTHON_EXE% manage.py migrate --noinput

echo [*] Nap du lieu mau (neu chua co)...
%PYTHON_EXE% manage.py seed_data

echo.
echo ====================================================
echo  Server dang khoi dong tai: http://127.0.0.1:8000/
echo  - Danh sach san pham:      http://127.0.0.1:8000/products/
echo  - Them san pham moi:       http://127.0.0.1:8000/products/create/
echo  (Nhan Ctrl + C de dung server)
echo ====================================================
echo.

%PYTHON_EXE% manage.py runserver

pause

