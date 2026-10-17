/**
 * Modern SaaS Admin Dashboard - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Mobile Sidebar Toggle
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const sidebar = document.querySelector('.sidebar');
    const backdrop = document.querySelector('.sidebar-backdrop');

    if (sidebarToggleBtn && sidebar) {
        sidebarToggleBtn.addEventListener('click', function () {
            sidebar.classList.toggle('show');
            if (backdrop) {
                backdrop.classList.toggle('show');
            }
        });
    }

    if (backdrop) {
        backdrop.addEventListener('click', function () {
            sidebar.classList.remove('show');
            backdrop.classList.remove('show');
        });
    }

    // 2. Initialize Bootstrap Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // 3. Delete Confirmation Modal
    const deleteModal = document.getElementById('deleteConfirmModal');
    if (deleteModal) {
        deleteModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const productName = button.getAttribute('data-product-name');
            const productSku = button.getAttribute('data-product-sku');
            const deleteUrl = button.getAttribute('data-delete-url');

            const modalProductName = deleteModal.querySelector('#modalProductName');
            const modalProductSku = deleteModal.querySelector('#modalProductSku');
            const deleteForm = deleteModal.querySelector('#deleteForm');

            if (modalProductName) modalProductName.textContent = productName || 'Sản phẩm này';
            if (modalProductSku) modalProductSku.textContent = productSku || '';
            if (deleteForm) deleteForm.setAttribute('action', deleteUrl);
        });
    }

    // 4. Image Upload Live Preview
    const imageInput = document.getElementById('productImageInput');
    const imagePreviewBox = document.getElementById('imagePreviewBox');
    const imagePreview = document.getElementById('imagePreview');
    const currentImageBox = document.getElementById('currentImageBox');

    if (imageInput && imagePreviewBox && imagePreview) {
        imageInput.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file) {
                // Check file size (5MB max)
                if (file.size > 5 * 1024 * 1024) {
                    alert('Dung lượng hình ảnh vượt quá 5MB. Vui lòng chọn ảnh nhỏ hơn.');
                    imageInput.value = '';
                    return;
                }

                const reader = new FileReader();
                reader.onload = function (event) {
                    imagePreview.src = event.target.result;
                    imagePreviewBox.style.display = 'block';
                    if (currentImageBox) {
                        currentImageBox.style.display = 'none';
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // 5. Auto dismiss flash toasts after 5 seconds
    const toastElements = document.querySelectorAll('.toast');
    toastElements.forEach(function (toastEl) {
        const toast = new bootstrap.Toast(toastEl, { delay: 5000 });
        toast.show();
    });
});
