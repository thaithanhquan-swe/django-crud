from decimal import Decimal
from django.core.management.base import BaseCommand
from products.models import Product


SAMPLE_PRODUCTS = [
    {
        'name': 'Bàn phím cơ không dây Keychron K2 Pro QMK/VIA',
        'sku': 'TECH-KEY-001',
        'category': 'Electronics',
        'price': Decimal('2190000.00'),
        'quantity': 35,
        'status': 'active',
        'description': 'Bàn phím cơ layout 75%, kết nối Bluetooth 5.1 và Type-C, switch Gateron G Pro Brown, keycap PBT double-shot cao cấp, tương thích Mac và Windows.',
    },
    {
        'name': 'Chuột công thái học Logitech MX Master 3S',
        'sku': 'TECH-MOU-002',
        'category': 'Electronics',
        'price': Decimal('2450000.00'),
        'quantity': 8,  # Low stock
        'status': 'active',
        'description': 'Cảm biến Darkfield 8000 DPI hoạt động trên mọi bề mặt, con lăn MagSpeed siêu nhanh và êm ái, kết nối đa thiết bị Easy-Switch.',
    },
    {
        'name': 'Tai nghe chống ồn Sony WH-1000XM5 Silver',
        'sku': 'TECH-HEA-003',
        'category': 'Electronics',
        'price': Decimal('6990000.00'),
        'quantity': 14,
        'status': 'active',
        'description': 'Khử tiếng ồn đỉnh cao với bộ xử lý Integrated Processor V1, thời lượng pin 30 giờ, micro đa hướng đàm thoại siêu nét.',
    },
    {
        'name': 'Áo sơ mi Oxford Slimfit Nam Trắng Cổ Điển',
        'sku': 'FASH-SHT-010',
        'category': 'Fashion',
        'price': Decimal('450000.00'),
        'quantity': 50,
        'status': 'active',
        'description': 'Chất liệu 100% Cotton Oxford dệt sợi đôi cao cấp, chống nhăn tự nhiên, thấm hút mồ hôi tối ưu, form dáng ôm thanh lịch.',
    },
    {
        'name': 'Áo khoác gió thể thao chống nước Ultra-Light',
        'sku': 'FASH-JKT-011',
        'category': 'Fashion',
        'price': Decimal('680000.00'),
        'quantity': 5,  # Low stock
        'status': 'active',
        'description': 'Công nghệ trượt nước DWR, trọng lượng chỉ 180g, có túi gấp gọn tiện lợi, phản quang an toàn khi chạy ban đêm.',
    },
    {
        'name': 'Đèn bàn làm việc thông minh Yeelight LED Pro',
        'sku': 'HOME-LGT-020',
        'category': 'Home',
        'price': Decimal('1290000.00'),
        'quantity': 22,
        'status': 'active',
        'description': 'Chỉ số hoàn màu Ra95 bảo vệ thị lực chuẩn y khoa, điều chỉnh nhiệt độ màu 2700K - 6500K qua ứng dụng điện thoại và HomeKit.',
    },
    {
        'name': 'Nồi chiên không dầu Philips XXL 7.2L Smart Sense',
        'sku': 'HOME-FRY-021',
        'category': 'Home',
        'price': Decimal('4890000.00'),
        'quantity': 0,  # Out of stock
        'status': 'active',
        'description': 'Công nghệ Rapid Air giảm đến 90% lượng chất béo, công suất 2200W nấu chín nhanh đều, tự động căn chỉnh thời gian nhiệt độ.',
    },
    {
        'name': 'Serum phục hồi & dưỡng ẩm da Skin1004 Madagascar Centella',
        'sku': 'BEAU-SRM-030',
        'category': 'Beauty',
        'price': Decimal('340000.00'),
        'quantity': 80,
        'status': 'active',
        'description': 'Chiết xuất 100% rau má hữu cơ vùng Madagascar, làm dịu da tức thì, củng cố hàng rào bảo vệ da, phù hợp cho da nhạy cảm.',
    },
    {
        'name': 'Kem chống nắng quang phổ rộng La Roche-Posay Anthelios 50ml',
        'sku': 'BEAU-SUN-031',
        'category': 'Beauty',
        'price': Decimal('465000.00'),
        'quantity': 4,  # Low stock
        'status': 'active',
        'description': 'Màng lọc độc quyền Mexoryl 400 bảo vệ khỏi tia UVA dài, kiềm dầu đến 12 giờ, không nhờn rít không để lại vệt trắng.',
    },
    {
        'name': 'Sách Thiết Kế Kiến Trúc Phần Mềm Thực Chiến (Clean Architecture)',
        'sku': 'BOOK-ARC-040',
        'category': 'Books',
        'price': Decimal('220000.00'),
        'quantity': 65,
        'status': 'active',
        'description': 'Tác phẩm kinh điển của Robert C. Martin (Uncle Bob) hướng dẫn xây dựng các hệ thống phần mềm có cấu trúc module độc lập và dễ kiểm thử.',
    },
    {
        'name': 'Thảm tập Yoga định tuyến Liforme Travel Edition',
        'sku': 'SPRT-YOG-050',
        'category': 'Sports',
        'price': Decimal('2850000.00'),
        'quantity': 0,  # Out of stock
        'status': 'inactive',
        'description': 'Chất liệu cao su tự nhiên thân thiện với môi trường, hệ thống định tuyến thông minh hỗ trợ căn chỉnh động tác chính xác.',
    },
    {
        'name': 'Cà phê hạt Specialty Arabica Cầu Đất Hộp 500g',
        'sku': 'FOOD-COF-060',
        'category': 'Food',
        'price': Decimal('280000.00'),
        'quantity': 45,
        'status': 'active',
        'description': 'Thu hoạch thủ công tại độ cao 1.600m Cầu Đất - Đà Lạt, sơ chế ướt, rang mộc độ vừa (Medium Roast) tỏa hương cam chanh và caramel ngọt hậu.',
    },
    {
        'name': 'Màn hình chuyên đồ họa Dell UltraSharp 27 inch 4K (U2723QE)',
        'sku': 'TECH-MON-004',
        'category': 'Electronics',
        'price': Decimal('13500000.00'),
        'quantity': 3,  # Low stock
        'status': 'active',
        'description': 'Tấm nền IPS Black độ tương phản 2000:1, chuẩn màu 98% DCI-P3, cổng kết nối Type-C cấp nguồn sạc 90W cho laptop.',
    },
    {
        'name': 'Bình giữ nhiệt Stanley Classic Legendary Bottle 1.4L',
        'sku': 'HOME-BTL-022',
        'category': 'Home',
        'price': Decimal('1150000.00'),
        'quantity': 18,
        'status': 'draft',
        'description': 'Thép không gỉ 18/8 không chứa BPA, cách nhiệt chân không 2 lớp giữ nóng và lạnh lên đến 40 giờ liên tục.',
    },
]


class Command(BaseCommand):
    help = 'Seed realistic sample products'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing products before seeding'
        )

    def handle(self, *args, **options):
        if options['clear']:
            deleted_count, _ = Product.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Cleared {deleted_count} existing products."))

        created_count = 0
        updated_count = 0

        for item in SAMPLE_PRODUCTS:
            product, created = Product.objects.update_or_create(
                sku=item['sku'],
                defaults=item
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded sample data: Created {created_count} products, Updated {updated_count} products."
            )
        )

