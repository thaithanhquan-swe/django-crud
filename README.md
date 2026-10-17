# NexusAdmin - Hệ Thống Quản Lý Kho Hàng & Sản Phẩm (Django CRUD)

> **LƯU Ý:** Dự án hoạt động theo chế độ **Mở hoàn toàn (Zero Authentication)**. Người dùng không cần tài khoản, không cần đăng nhập — chỉ cần mở server là có thể thêm, xem, sửa, xóa sản phẩm trực tiếp.
> **Cách chạy nhanh nhất trên Windows:** Click đúp vào file **`run.bat`** để chạy ngay!

Hệ thống quản lý sản phẩm hoàn chỉnh theo chuẩn **Modern SaaS Admin Dashboard**, được xây dựng trên nền tảng **Django Framework (Python)** kết hợp **Bootstrap 5**, **Chart.js** và **Bootstrap Icons**.

Dự án sở hữu kiến trúc chuẩn production-ready, phân tầng trách nhiệm rõ ràng, giao diện responsive mượt mà và hỗ trợ đầy đủ các thao tác CRUD cùng các tính năng nghiệp vụ mở rộng.

---

## 🚀 Tính Năng Chính

### 1. Dashboard Quản Trị (Tổng Quan)
- **Thẻ KPI thời gian thực**: Tổng số sản phẩm, Tổng giá trị vốn kho hàng hóa (VNĐ), Cảnh báo sắp hết hàng ($\le 10$ sản phẩm), Số sản phẩm đang kinh doanh (Active).
- **Biểu đồ trực quan hóa (Chart.js)**:
  - *Biểu đồ cột*: Phân bổ cơ cấu hàng hóa theo từng danh mục.
  - *Biểu đồ Donut*: Tỷ lệ phân loại trạng thái sản phẩm (Đang hoạt động, Tạm ngưng, Bản nháp).
- **Bảng cập nhật nhanh**: Hiển thị danh sách các sản phẩm có biến động gần nhất kèm thao tác truy cập nhanh.

### 2. Quản Lý Sản Phẩm (CRUD Đầy Đủ)
- **Create (Thêm mới)**:
  - Form chia nhóm trực quan (Thông tin cơ bản, Giá cả & Tồn kho, Phân loại & Trạng thái, Upload ảnh).
  - Tự động chuẩn hóa mã SKU (viết hoa, cắt khoảng trắng dư).
  - Kiểm tra tính duy nhất của mã SKU (báo lỗi ngay tại form).
  - Validation chặt chẽ: Giá và số lượng không được âm, kiểm tra kích thước ảnh ($\le 5\text{MB}$) và định dạng hợp lệ (JPG, PNG, WEBP).
  - **Live Image Preview**: Xem trước ảnh tức thì bằng JavaScript trước khi submit form.
- **Read (Xem danh sách & Chi tiết)**:
  - **Danh sách sản phẩm**: Hiển thị dạng bảng hiện đại, phân loại badge màu sắc thông minh cho mức tồn kho (*Còn hàng*, *Sắp hết hàng*, *Hết hàng*) và trạng thái kinh doanh.
  - **Chi tiết sản phẩm**: Hiển thị ảnh kích thước lớn, thông số chi tiết, tổng giá trị tồn kho của mã hàng, tiến trình tồn kho và gợi ý các sản phẩm liên quan trong cùng danh mục.
- **Update (Chỉnh sửa)**:
  - Tự động nạp dữ liệu hiện tại của sản phẩm vào form.
  - Cho phép giữ nguyên SKU hoặc đổi SKU mới (kiểm tra trùng lặp ngoại trừ chính sản phẩm đang sửa).
  - Hiển thị ảnh hiện tại kèm tùy chọn cập nhật ảnh mới.
- **Delete (Xóa an toàn)**:
  - Modal xác nhận xóa hiển thị rõ tên và mã SKU cần xóa.
  - Bắt buộc thực hiện thông qua giao thức **POST** kèm mã bảo mật **CSRF Token** (tuyệt đối không sử dụng GET để xóa dữ liệu).

### 3. Bộ Lọc & Tìm Kiếm Nâng Cao
- Tìm kiếm từ khóa theo cả **Tên sản phẩm** hoặc **Mã định danh SKU**.
- Lọc theo **Danh mục ngành hàng** (Điện tử, Thời trang, Nhà cửa, Làm đẹp, Sách, Thể thao, Thực phẩm...).
- Lọc theo **Trạng thái kinh doanh** (Đang hoạt động, Tạm ngưng, Bản nháp).
- Lọc theo **Tình trạng tồn kho** (Còn hàng, Sắp hết hàng $\le 10$, Hết hàng).
- Sắp xếp linh hoạt (Mới nhất, Cũ nhất, Tên A-Z, Tên Z-A, Giá tăng/giảm, Tồn kho cao/thấp).
- **Phân trang bảo lưu bộ lọc**: Giữ nguyên toàn bộ tham số truy vấn (query string) khi chuyển qua lại giữa các trang.

### 4. UI/UX & Trải Nghiệm Người Dùng
- Bảng màu hiện đại phong cách SaaS: Navy chủ đạo (`#0f172a`), điểm nhấn Indigo (`#4f46e5` / `#6366f1`) và nền sáng tối giản (`#f8fafc`).
- Hoàn toàn responsive trên Mobile, Tablet và Desktop (Sidebar có thể thu gọn / offcanvas trên mobile).
- Hệ thống thông báo **Toast Notifications** tự động hiển thị và biến mất sau 5 giây.
- Xử lý mượt mà các trạng thái: Danh sách trống (Empty state), thiếu ảnh đại diện (SVG Placeholder) và trang lỗi tùy chỉnh (404, 500).

---

## 📁 Cấu Trúc Dự Án

```
django-crud/
├── .venv/                          # Virtual environment
├── .gitignore                      # Git ignore chuẩn Django/Python
├── manage.py                       # Django CLI entrypoint
├── requirements.txt                # Danh sách thư viện phụ thuộc
├── README.md                       # Tài liệu hướng dẫn dự án
├── core/                           # Cấu hình project Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                 # Thiết lập apps, media, static, database, messages
│   ├── urls.py                     # Định tuyến URL chính và media static
│   └── wsgi.py
├── products/                       # App quản lý sản phẩm
│   ├── __init__.py
│   ├── admin.py                    # Cấu hình giao diện Django Admin
│   ├── apps.py
│   ├── forms.py                    # ModelForm & validation logic
│   ├── models.py                   # Product Model với các thuộc tính & validation
│   ├── urls.py                     # Định tuyến các view CRUD
│   ├── views.py                    # Xử lý logic Dashboard, List, Detail, Create, Update, Delete
│   ├── management/
│   │   └── commands/
│   │       ├── seed_data.py        # Command nạp 14 sản phẩm thực tế mẫu
│   │       └── create_admin.py     # Command khởi tạo superuser an toàn
│   ├── migrations/                 # Lịch sử migration cơ sở dữ liệu
│   └── tests/                      # Bộ kiểm thử tự động toàn diện
│       ├── __init__.py
│       ├── test_models.py          # Kiểm thử logic model & properties
│       ├── test_forms.py           # Kiểm thử form validation (SKU trùng, số âm...)
│       └── test_views.py           # Kiểm thử luồng HTTP, CRUD, search, filter
├── static/                         # Tài nguyên tĩnh
│   ├── css/
│   │   └── style.css               # Tùy biến phong cách Modern SaaS Admin
│   ├── js/
│   │   └── main.js                 # Xử lý Sidebar, Delete Modal, Image Preview, Toasts
│   └── img/
│       └── placeholder.svg         # Ảnh mặc định khi sản phẩm chưa có ảnh
├── media/                          # Thư mục lưu trữ ảnh người dùng tải lên
│   └── products/
└── templates/                      # Hệ thống giao diện Django Templates
    ├── base.html                   # Khung giao diện chính (Sidebar, Header, Main, Toasts)
    ├── 404.html                    # Trang báo lỗi 404
    ├── 500.html                    # Trang báo lỗi 500
    ├── includes/
    │   ├── header.html             # Topbar, breadcrumb, user profile, notifications
    │   ├── sidebar.html            # Sidebar điều hướng
    │   ├── messages.html           # Toast notifications
    │   └── delete_modal.html       # Reusable confirm delete modal
    ├── dashboard/
    │   └── index.html              # Màn hình Dashboard KPI & Biểu đồ
    └── products/
        ├── product_list.html       # Danh sách, tìm kiếm, lọc, phân trang
        ├── product_detail.html     # Xem chi tiết sản phẩm
        └── product_form.html       # Form thêm mới & chỉnh sửa sản phẩm
```

---

## 🛠️ Yêu Cầu Môi Trường

- **Python**: Phiên bản 3.10 trở lên (khuyến nghị Python 3.12).
- **Hệ điều hành**: Windows, macOS hoặc Linux.

---

## ⚡ Hướng Dẫn Cài Đặt & Chạy Dự Án

### Bước 1: Tạo và kích hoạt môi trường ảo (Virtual Environment)

**Trên Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
*(Nếu gặp lỗi script execution policy trên PowerShell, hãy chạy: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`)*

**Trên macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### Bước 2: Cài đặt các thư viện cần thiết

```bash
pip install -r requirements.txt
```

---

### Bước 3: Áp dụng Migration cơ sở dữ liệu

Khởi tạo các bảng cơ sở dữ liệu SQLite:
```bash
python manage.py migrate
```

---

### Bước 4: Nạp dữ liệu mẫu thực tế (Seeding)

Dự án có sẵn lệnh quản lý để nạp 14 sản phẩm thuộc nhiều ngành hàng với đầy đủ các mức giá, số lượng tồn kho (bao gồm cả sản phẩm sắp hết hàng và đã hết hàng):
```bash
python manage.py seed_data
```

*(Tùy chọn: Thêm cờ `--clear` nếu muốn xóa sạch dữ liệu cũ trước khi nạp lại: `python manage.py seed_data --clear`)*

---

### Bước 5: Khởi tạo tài khoản Quản trị viên (Superuser)

Bạn có thể tạo nhanh bằng lệnh an toàn được tích hợp sẵn:
```bash
python manage.py create_admin --username admin --email admin@local.dev --password AdminPassword123
```
*Hoặc sử dụng lệnh tương tác truyền thống của Django:*
```bash
python manage.py createsuperuser
```

---

### Bước 6: Khởi chạy Development Server

```bash
python manage.py runserver
```

Sau khi server khởi động thành công, hãy mở trình duyệt và truy cập:
- **Trang Dashboard & Quản lý Kho**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Trang Danh sách Sản phẩm**: [http://127.0.0.1:8000/products/](http://127.0.0.1:8000/products/)
- **Trang Quản trị Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) (Đăng nhập với user `admin` / `AdminPassword123`)

---

## 🧪 Kiểm Thử Tự Động (Automated Testing)

Dự án đi kèm bộ kiểm thử toàn diện với **21 test cases** kiểm tra toàn bộ luồng hoạt động:
- Kiểm tra tính đúng đắn của Model, thuộc tính tính toán giá trị tồn kho, cờ cảnh báo `is_low_stock` và `is_out_of_stock`.
- Kiểm tra ràng buộc duy nhất của SKU, validation giá âm, tồn kho âm, kích thước file ảnh.
- Kiểm tra giao diện Dashboard, danh sách, tìm kiếm, lọc danh mục, sắp xếp, phân trang.
- Kiểm tra tính an toàn: Từ chối phương thức `GET` khi xóa dữ liệu (bắt buộc dùng `POST`).

Chạy toàn bộ test suite bằng lệnh:
```bash
python manage.py test
```

Xem kết quả chi tiết từng test:
```bash
python manage.py test -v 2
```

---

## 🔧 Một Số Vấn Đề Thường Gặp & Cách Khắc Phục

1. **Lỗi `Execution of scripts is disabled on this system` khi kích hoạt `.venv` trên Windows:**
   - *Cách khắc phục*: Chạy lệnh PowerShell:
     ```powershell
     Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
     ```
2. **Lỗi `Pillow` khi upload ảnh:**
   - *Cách khắc phục*: Đảm bảo gói `pillow` đã được cài đặt trong môi trường ảo:
     ```bash
     pip install pillow
     ```
3. **Ảnh upload không hiển thị trên giao diện:**
   - Trong môi trường phát triển (`DEBUG = True`), `core/urls.py` đã cấu hình phục vụ media thông qua `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`. Hãy đảm bảo thư mục `media/` tồn tại trong thư mục gốc của dự án.

