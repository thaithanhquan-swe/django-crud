from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from products.models import Product


class ProductModelTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Laptop Gaming ASUS ROG",
            sku="LAP-ASUS-001",
            category="Electronics",
            description="Laptop hiệu năng cao",
            price=Decimal("25000000.00"),
            quantity=15,
            status="active"
        )

    def test_product_str(self):
        """Kiểm tra chuỗi biểu diễn __str__ của Product"""
        self.assertEqual(str(self.product), "Laptop Gaming ASUS ROG (LAP-ASUS-001)")

    def test_total_value(self):
        """Kiểm tra tính tổng giá trị tồn kho"""
        expected_value = Decimal("25000000.00") * 15
        self.assertEqual(self.product.total_value, expected_value)

    def test_is_low_stock(self):
        """Kiểm tra cờ cảnh báo sắp hết hàng (1 <= quantity <= 10)"""
        self.assertFalse(self.product.is_low_stock)
        self.product.quantity = 5
        self.assertTrue(self.product.is_low_stock)
        self.product.quantity = 0
        self.assertFalse(self.product.is_low_stock)

    def test_is_out_of_stock(self):
        """Kiểm tra cờ hết hàng (quantity == 0)"""
        self.assertFalse(self.product.is_out_of_stock)
        self.product.quantity = 0
        self.assertTrue(self.product.is_out_of_stock)

    def test_sku_uniqueness(self):
        """Kiểm tra tính duy nhất của mã SKU trên tầng database"""
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                name="Sản phẩm trùng SKU",
                sku="LAP-ASUS-001",
                category="Electronics",
                price=Decimal("1000000.00"),
                quantity=2
            )

    def test_clean_formats_sku_and_name(self):
        """Kiểm tra clean() chuẩn hóa SKU thành chữ hoa và bỏ khoảng trắng"""
        p = Product(
            name="  Tai nghe Bluetooth  ",
            sku="  ear-bt-99  ",
            category="Electronics",
            price=Decimal("500000.00"),
            quantity=10
        )
        p.clean()
        self.assertEqual(p.name, "Tai nghe Bluetooth")
        self.assertEqual(p.sku, "EAR-BT-99")
