from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Electronics', 'Điện tử & Công nghệ'),
        ('Fashion', 'Thời trang & May mặc'),
        ('Home', 'Nhà cửa & Đời sống'),
        ('Beauty', 'Sức khỏe & Làm đẹp'),
        ('Books', 'Sách & Văn phòng phẩm'),
        ('Sports', 'Thể thao & Dã ngoại'),
        ('Food', 'Thực phẩm & Đồ uống'),
        ('Other', 'Danh mục khác'),
    ]

    STATUS_CHOICES = [
        ('active', 'Đang hoạt động'),
        ('inactive', 'Tạm ngưng'),
        ('draft', 'Bản nháp'),
    ]

    name = models.CharField(
        max_length=255, 
        verbose_name="Tên sản phẩm",
        help_text="Nhập tên đầy đủ của sản phẩm"
    )
    sku = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Mã SKU",
        help_text="Mã định danh duy nhất (ví dụ: PRD-001)"
    )
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        default='Electronics', 
        verbose_name="Danh mục"
    )
    description = models.TextField(
        blank=True, 
        verbose_name="Mô tả",
        help_text="Mô tả chi tiết về thông số, tính năng sản phẩm"
    )
    price = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Giá bán (VNĐ)",
        help_text="Đơn giá bán hiện tại"
    )
    quantity = models.PositiveIntegerField(
        default=0, 
        verbose_name="Số lượng tồn kho",
        help_text="Số lượng sản phẩm còn lại trong kho"
    )
    image = models.ImageField(
        upload_to='products/', 
        blank=True, 
        null=True, 
        verbose_name="Hình ảnh sản phẩm",
        help_text="Định dạng JPG, PNG, WEBP. Dung lượng tối đa 5MB"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='active', 
        verbose_name="Trạng thái"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Ngày tạo"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Ngày cập nhật"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Danh sách sản phẩm"

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def clean(self):
        super().clean()
        if self.sku:
            self.sku = self.sku.strip().upper()
        if self.name:
            self.name = self.name.strip()

    @property
    def is_low_stock(self):
        """Cảnh báo khi tồn kho từ 1 đến 10 sản phẩm."""
        return 0 < self.quantity <= 10

    @property
    def is_out_of_stock(self):
        """Kiểm tra sản phẩm đã hết hàng."""
        return self.quantity == 0

    @property
    def total_value(self):
        """Tổng giá trị tồn kho của sản phẩm này."""
        return self.price * self.quantity

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})
