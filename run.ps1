# ====================================================
# Script khoi chay du an Django CRUD (PowerShell)
# Khong can authen / login - chay truc tiep
# ====================================================

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "     NexusAdmin - Django Product Management" -ForegroundColor Green
Write-Host "     Hoan toan truc tiep, khong can login / authen" -ForegroundColor Yellow
Write-Host "====================================================" -ForegroundColor Cyan

$pythonExe = ".\.venv\Scripts\python.exe"

if (-Not (Test-Path $pythonExe)) {
    Write-Host "[*] Dang tao virtual environment..." -ForegroundColor Yellow
    py -m venv .venv
    & $pythonExe -m pip install -r requirements.txt
}

Write-Host "[*] Cap nhat Database SQLite..." -ForegroundColor Gray
& $pythonExe manage.py migrate --noinput

Write-Host "[*] Nap du lieu mau..." -ForegroundColor Gray
& $pythonExe manage.py seed_data

Write-Host "`nServer dang chay tai: http://127.0.0.1:8000/" -ForegroundColor Green
Write-Host "Danh sach san pham:  http://127.0.0.1:8000/products/" -ForegroundColor Green
Write-Host "Them san pham moi:   http://127.0.0.1:8000/products/create/" -ForegroundColor Green
Write-Host "Nhan Ctrl + C de dung server`n" -ForegroundColor DarkGray

& $pythonExe manage.py runserver

