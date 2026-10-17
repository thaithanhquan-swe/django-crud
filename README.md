# Quản Lý Sản Phẩm - Django CRUD

Ứng dụng web quản lý kho và sản phẩm bằng Django & Bootstrap 5 (chế độ mở, không cần đăng nhập).

---

## 🚀 Cách Chạy Dự Án

### Cách 1: Nhanh nhất (Click đúp chuột)
Vào thư mục dự án và click đúp vào file **`run.bat`**.

---

### Cách 2: Chạy bằng lệnh (PowerShell)
Mở PowerShell tại thư mục dự án và chạy:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

*(Hoặc nếu đã kích hoạt môi trường ảo `.\.venv\Scripts\Activate.ps1`, bạn chỉ cần gõ: `python manage.py runserver`)*

---

## 🌐 Địa Chỉ Truy Cập

Sau khi chạy lệnh trên, mở trình duyệt vào các link sau:

- **Dashboard Tổng quan**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Danh sách sản phẩm**: [http://127.0.0.1:8000/products/](http://127.0.0.1:8000/products/)
- **Thêm sản phẩm mới**: [http://127.0.0.1:8000/products/create/](http://127.0.0.1:8000/products/create/)

---

## 🛠️ Một Số Lệnh Hữu Ích Khác

- **Nạp lại 14 sản phẩm mẫu**:
  ```powershell
  .\.venv\Scripts\python.exe manage.py seed_data --clear
  ```

- **Chạy kiểm thử tự động**:
  ```powershell
  .\.venv\Scripts\python.exe manage.py test
  ```
