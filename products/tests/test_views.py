from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product


class ProductViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.p1 = Product.objects.create(
            name="Chuột Logitech G102",
            sku="MOU-LOG-102",
            category="Electronics",
            price=Decimal("400000.00"),
            quantity=5,  # low stock
            status="active"
        )
        self.p2 = Product.objects.create(
            name="Áo Polo Thể Thao Nam",
            sku="FASH-POL-01",
            category="Fashion",
            price=Decimal("250000.00"),
            quantity=50,
            status="active"
        )
        self.p3 = Product.objects.create(
            name="Sách Thiết Kế Giao Diện UI/UX",
            sku="BOOK-UIX-01",
            category="Books",
            price=Decimal("180000.00"),
            quantity=0,  # out of stock
            status="draft"
        )

    def test_dashboard_view(self):
        """Dashboard trả về mã HTTP 200 và chứa các thống kê KPI chính xác"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')
        self.assertEqual(response.context['total_products'], 3)
        self.assertEqual(response.context['low_stock_count'], 1)
        self.assertEqual(response.context['out_of_stock_count'], 1)
        self.assertEqual(response.context['active_products_count'], 2)

    def test_product_list_view(self):
        """Trang danh sách sản phẩm hiển thị đầy đủ và đúng template"""
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_list.html')
        self.assertEqual(len(response.context['products']), 3)

    def test_product_list_search(self):
        """Tìm kiếm theo tên sản phẩm hoặc mã SKU"""
        # Tìm theo tên
        response = self.client.get(reverse('product_list'), {'q': 'Logitech'})
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['products'][0].sku, 'MOU-LOG-102')

        # Tìm theo SKU
        response_sku = self.client.get(reverse('product_list'), {'q': 'BOOK'})
        self.assertEqual(len(response_sku.context['products']), 1)
        self.assertEqual(response_sku.context['products'][0].name, 'Sách Thiết Kế Giao Diện UI/UX')

    def test_product_list_filter_category_and_status(self):
        """Lọc danh sách theo danh mục và trạng thái"""
        # Lọc danh mục Fashion
        response = self.client.get(reverse('product_list'), {'category': 'Fashion'})
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['products'][0].category, 'Fashion')

        # Lọc trạng thái draft
        response_draft = self.client.get(reverse('product_list'), {'status': 'draft'})
        self.assertEqual(len(response_draft.context['products']), 1)
        self.assertEqual(response_draft.context['products'][0].status, 'draft')

    def test_product_list_filter_stock(self):
        """Lọc danh sách theo mức tồn kho"""
        response_low = self.client.get(reverse('product_list'), {'stock': 'low_stock'})
        self.assertEqual(len(response_low.context['products']), 1)
        self.assertEqual(response_low.context['products'][0].sku, 'MOU-LOG-102')

        response_out = self.client.get(reverse('product_list'), {'stock': 'out_of_stock'})
        self.assertEqual(len(response_out.context['products']), 1)
        self.assertEqual(response_out.context['products'][0].sku, 'BOOK-UIX-01')

    def test_product_list_sort(self):
        """Sắp xếp theo giá tăng dần"""
        response = self.client.get(reverse('product_list'), {'sort': 'price_asc'})
        products = list(response.context['products'])
        self.assertEqual(products[0].sku, 'BOOK-UIX-01')  # 180.000
        self.assertEqual(products[-1].sku, 'MOU-LOG-102')  # 400.000

    def test_product_detail_view(self):
        """Xem chi tiết sản phẩm hợp lệ và sản phẩm không tồn tại (404)"""
        response = self.client.get(reverse('product_detail', kwargs={'pk': self.p1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], self.p1)

        # 404 cho id không tồn tại
        response_404 = self.client.get(reverse('product_detail', kwargs={'pk': 9999}))
        self.assertEqual(response_404.status_code, 404)

    def test_product_create_get_and_post(self):
        """Tạo sản phẩm qua form POST và chuyển hướng thành công"""
        # GET form
        response_get = self.client.get(reverse('product_create'))
        self.assertEqual(response_get.status_code, 200)

        # POST valid
        new_data = {
            'name': 'Tai nghe chụp tai Sony',
            'sku': 'TECH-SNY-01',
            'category': 'Electronics',
            'price': '1200000.00',
            'quantity': 12,
            'status': 'active',
            'description': 'Tai nghe chất lượng cao',
        }
        response_post = self.client.post(reverse('product_create'), data=new_data)
        self.assertEqual(response_post.status_code, 302)
        created_product = Product.objects.get(sku='TECH-SNY-01')
        self.assertRedirects(response_post, reverse('product_detail', kwargs={'pk': created_product.pk}))

    def test_product_update_view(self):
        """Chỉnh sửa thông tin sản phẩm và lưu thành công"""
        update_data = {
            'name': 'Chuột Logitech G102 Lightsync Gen 2',
            'sku': 'MOU-LOG-102',
            'category': 'Electronics',
            'price': '420000.00',
            'quantity': 18,
            'status': 'active',
            'description': 'Đã nâng cấp phiên bản Gen 2',
        }
        response = self.client.post(reverse('product_update', kwargs={'pk': self.p1.pk}), data=update_data)
        self.assertEqual(response.status_code, 302)
        self.p1.refresh_from_db()
        self.assertEqual(self.p1.name, 'Chuột Logitech G102 Lightsync Gen 2')
        self.assertEqual(self.p1.quantity, 18)

    def test_product_delete_post_only(self):
        """Xóa sản phẩm bằng POST thành công, từ chối phương thức GET"""
        product_to_delete = Product.objects.create(
            name="Sản phẩm thử nghiệm xóa",
            sku="DEL-TEST-001",
            category="Other",
            price=Decimal("10000.00"),
            quantity=1
        )
        pk = product_to_delete.pk

        # GET bị từ chối 405 Method Not Allowed
        response_get = self.client.get(reverse('product_delete', kwargs={'pk': pk}))
        self.assertEqual(response_get.status_code, 405)
        self.assertTrue(Product.objects.filter(pk=pk).exists())

        # POST xóa thành công
        response_post = self.client.post(reverse('product_delete', kwargs={'pk': pk}))
        self.assertEqual(response_post.status_code, 302)
        self.assertFalse(Product.objects.filter(pk=pk).exists())
