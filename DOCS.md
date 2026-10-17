# Hướng Dẫn Chạy Dự Án

### Cách 1: Nhanh nhất (Click đúp chuột)
Vào thư mục dự án và click đúp vào file **`run.bat`**.

---

### Cách 2: Chạy bằng lệnh (PowerShell / Terminal)
Mở terminal tại thư mục dự án và chạy:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

*(Hoặc kích hoạt môi trường ảo rồi chạy:*
```powershell
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```
*)*

---

### Các link truy cập sau khi bật server:
- **Trang chủ / Dashboard**: http://127.0.0.1:8000/
- **Danh sách sản phẩm**: http://127.0.0.1:8000/products/
- **Thêm sản phẩm mới**: http://127.0.0.1:8000/products/create/

---

*(Tùy chọn) Nạp lại dữ liệu mẫu nếu cần:*
```powershell
.\.venv\Scripts\python.exe manage.py seed_data --clear
```
