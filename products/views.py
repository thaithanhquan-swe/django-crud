import json
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Sum, F, ExpressionWrapper, DecimalField, Count
from .models import Product
from .forms import ProductForm


def dashboard_view(request):
    """
    Dashboard trang chủ hiển thị tổng quan KPI, biểu đồ thống kê và sản phẩm mới cập nhật.
    """
    products_qs = Product.objects.all()
    total_products = products_qs.count()
    
    # Tính tổng giá trị kho hàng
    inventory_agg = products_qs.aggregate(
        total_value=Sum(
            ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField(max_digits=15, decimal_places=2))
        )
    )
    total_inventory_value = inventory_agg['total_value'] or Decimal('0.00')

    # Thống kê tồn kho & trạng thái
    low_stock_count = products_qs.filter(quantity__gt=0, quantity__lte=10).count()
    out_of_stock_count = products_qs.filter(quantity=0).count()
    active_products_count = products_qs.filter(status='active').count()
    inactive_products_count = products_qs.filter(status='inactive').count()
    draft_products_count = products_qs.filter(status='draft').count()

    # Dữ liệu biểu đồ theo danh mục
    category_counts = (
        products_qs.values('category')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    # Lấy nhãn danh mục tiếng Việt
    category_display_map = dict(Product.CATEGORY_CHOICES)
    chart_category_labels = [category_display_map.get(item['category'], item['category']) for item in category_counts]
    chart_category_data = [item['count'] for item in category_counts]

    # Dữ liệu biểu đồ trạng thái
    chart_status_labels = ['Đang hoạt động', 'Tạm ngưng', 'Bản nháp']
    chart_status_data = [active_products_count, inactive_products_count, draft_products_count]

    # Sản phẩm gần đây
    recent_products = products_qs.order_by('-updated_at')[:6]

    context = {
        'total_products': total_products,
        'total_inventory_value': total_inventory_value,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'active_products_count': active_products_count,
        'recent_products': recent_products,
        # JSON cho Chart.js
        'chart_category_labels_json': json.dumps(chart_category_labels),
        'chart_category_data_json': json.dumps(chart_category_data),
        'chart_status_labels_json': json.dumps(chart_status_labels),
        'chart_status_data_json': json.dumps(chart_status_data),
    }
    return render(request, 'dashboard/index.html', context)


def product_list(request):
    """
    Trang danh sách sản phẩm có tìm kiếm, lọc theo danh mục, trạng thái, tồn kho, sắp xếp và phân trang.
    """
    qs = Product.objects.all()

    # Tìm kiếm theo tên hoặc mã SKU
    search_query = request.GET.get('q', '').strip()
    if search_query:
        qs = qs.filter(
            Q(name__icontains=search_query) | 
            Q(sku__icontains=search_query)
        )

    # Lọc danh mục
    category_filter = request.GET.get('category', '').strip()
    if category_filter:
        qs = qs.filter(category=category_filter)

    # Lọc trạng thái
    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        qs = qs.filter(status=status_filter)

    # Lọc tồn kho
    stock_filter = request.GET.get('stock', '').strip()
    if stock_filter == 'in_stock':
        qs = qs.filter(quantity__gt=10)
    elif stock_filter == 'low_stock':
        qs = qs.filter(quantity__gt=0, quantity__lte=10)
    elif stock_filter == 'out_of_stock':
        qs = qs.filter(quantity=0)

    # Sắp xếp
    sort = request.GET.get('sort', '-created_at')
    valid_sorts = {
        'name_asc': 'name',
        'name_desc': '-name',
        'price_asc': 'price',
        'price_desc': '-price',
        'qty_asc': 'quantity',
        'qty_desc': '-quantity',
        'newest': '-created_at',
        'oldest': 'created_at',
        '-created_at': '-created_at',
    }
    order_by_field = valid_sorts.get(sort, '-created_at')
    qs = qs.order_by(order_by_field)

    # Phân trang (8 sản phẩm / trang để grid hoặc table hiển thị cân đối)
    paginator = Paginator(qs, 8)
    page_number = request.GET.get('page', 1)
    try:
        products = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        products = paginator.get_page(1)

    # Xây dựng chuỗi query string bảo lưu bộ lọc khi chuyển trang
    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    querystring = query_params.urlencode()

    context = {
        'products': products,
        'total_count': paginator.count,
        'search_query': search_query,
        'category_filter': category_filter,
        'status_filter': status_filter,
        'stock_filter': stock_filter,
        'sort': sort,
        'querystring': querystring,
        'categories': Product.CATEGORY_CHOICES,
        'statuses': Product.STATUS_CHOICES,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, pk):
    """
    Trang chi tiết sản phẩm và gợi ý các sản phẩm cùng danh mục.
    """
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(pk=product.pk)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)


def product_create(request):
    """
    Thêm mới sản phẩm có validation và upload ảnh.
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Sản phẩm \"{product.name}\" ({product.sku}) đã được tạo thành công!")
            return redirect('product_detail', pk=product.pk)
        else:
            messages.error(request, "Đã có lỗi xảy ra. Vui lòng kiểm tra lại các trường thông tin bên dưới.")
    else:
        form = ProductForm()

    context = {
        'form': form,
        'action_title': 'Thêm sản phẩm mới',
        'is_edit': False,
    }
    return render(request, 'products/product_form.html', context)


def product_update(request, pk):
    """
    Cập nhật thông tin sản phẩm.
    """
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Thông tin sản phẩm \"{product.name}\" đã được cập nhật thành công!")
            return redirect('product_detail', pk=product.pk)
        else:
            messages.error(request, "Cập nhật không thành công. Vui lòng kiểm tra lại các lỗi bên dưới.")
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
        'action_title': f'Chỉnh sửa: {product.name}',
        'is_edit': True,
    }
    return render(request, 'products/product_form.html', context)


@require_POST
def product_delete(request, pk):
    """
    Xóa sản phẩm bằng phương thức POST an toàn (có CSRF protection).
    """
    product = get_object_or_404(Product, pk=pk)
    product_name = product.name
    sku = product.sku
    product.delete()
    messages.success(request, f"Đã xóa vĩnh viễn sản phẩm \"{product_name}\" ({sku}) khỏi hệ thống.")
    return redirect('product_list')


def handler404(request, exception):
    """Trang xử lý lỗi 404 tùy chỉnh."""
    return render(request, '404.html', status=404)


def handler500(request):
    """Trang xử lý lỗi 500 tùy chỉnh."""
    return render(request, '500.html', status=500)
