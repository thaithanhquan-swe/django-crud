from decimal import Decimal
from django.test import TestCase
from products.models import Product
from products.forms import ProductForm


class ProductFormTests(TestCase):
    def setUp(self):
        self.existing_product = Product.objects.create(
            name="Áo thun thể thao",
            sku="FASH-TSH-001",
            category="Fashion",
            price=Decimal("150000.00"),
            quantity=20,
            status="active"
        )

    def test_valid_form(self):
        """Form hợp lệ khi cung cấp đầy đủ thông tin chuẩn"""
        form_data = {
            'name': 'Quần jean slimfit',
            'sku': 'FASH-JEA-002',
            'category': 'Fashion',
            'price': '350000.00',
            'quantity': 30,
            'status': 'active',
            'description': 'Quần jean chất liệu co giãn nhẹ',
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_duplicate_sku_invalid(self):
        """Form phải báo lỗi khi SKU bị trùng lặp"""
        form_data = {
            'name': 'Áo thun trùng mã',
            'sku': 'fash-tsh-001',  # case-insensitive check
            'category': 'Fashion',
            'price': '190000.00',
            'quantity': 10,
            'status': 'active',
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('sku', form.errors)
        self.assertIn("đã tồn tại", form.errors['sku'][0])

    def test_update_same_sku_valid(self):
        """Khi cập nhật chính sản phẩm đó, giữ nguyên SKU vẫn hợp lệ"""
        form_data = {
            'name': 'Áo thun thể thao cao cấp',
            'sku': 'FASH-TSH-001',
            'category': 'Fashion',
            'price': '180000.00',
            'quantity': 25,
            'status': 'active',
            'description': 'Đã cập nhật tên và giá',
        }
        form = ProductForm(data=form_data, instance=self.existing_product)
        self.assertTrue(form.is_valid())

    def test_negative_price_invalid(self):
        """Giá sản phẩm không được là số âm"""
        form_data = {
            'name': 'Sản phẩm giá âm',
            'sku': 'NEG-PRC-001',
            'category': 'Electronics',
            'price': '-50000',
            'quantity': 5,
            'status': 'active',
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_negative_quantity_invalid(self):
        """Tồn kho không được là số âm"""
        form_data = {
            'name': 'Sản phẩm tồn kho âm',
            'sku': 'NEG-QTY-001',
            'category': 'Electronics',
            'price': '100000',
            'quantity': '-5',
            'status': 'active',
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)

