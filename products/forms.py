from django import forms
from django.core.exceptions import ValidationError
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'sku',
            'category',
            'price',
            'quantity',
            'status',
            'image',
            'description',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tên sản phẩm (vd: Bàn phím cơ không dây)',
                'autocomplete': 'off',
            }),
            'sku': forms.TextInput(attrs={
                'class': 'form-control text-uppercase font-monospace',
                'placeholder': 'VD: PRD-KEY-001',
                'autocomplete': 'off',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '1000',
                'min': '0',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'min': '0',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'productImageInput',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Mô tả chi tiết tính năng, thông số kỹ thuật, hướng dẫn sử dụng...',
            }),
        }

    def clean_sku(self):
        sku = self.cleaned_data.get('sku', '').strip().upper()
        if not sku:
            raise ValidationError("Mã SKU không được để trống.")
        
        # Check duplicate SKU, excluding current instance if updating
        qs = Product.objects.filter(sku__iexact=sku)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
            
        if qs.exists():
            raise ValidationError(f"Mã SKU '{sku}' đã tồn tại trong hệ thống. Vui lòng chọn mã khác.")
            
        return sku

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            raise ValidationError("Vui lòng nhập giá sản phẩm.")
        if price < 0:
            raise ValidationError("Giá sản phẩm không được là số âm.")
        return price

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is None:
            raise ValidationError("Vui lòng nhập số lượng tồn kho.")
        if quantity < 0:
            raise ValidationError("Số lượng tồn kho không được là số âm.")
        return quantity

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and hasattr(image, 'size'):
            # Max file size 5MB
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Dung lượng hình ảnh không được vượt quá 5MB.")
            # Check extension
            valid_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
            ext = '.' + image.name.split('.')[-1].lower() if '.' in image.name else ''
            if ext not in valid_extensions:
                raise ValidationError("Định dạng file không hỗ trợ. Vui lòng tải lên file JPG, PNG, WEBP.")
        return image

