
from pathlib import Path

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousFileOperation
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ProductForm
from .models import Product


@login_required
def product_list(request):
    products = Product.objects.filter(
        customer=request.user
    ).order_by("-created_at")

    product_items = list(products)

    active_count = sum(
        1 for product in product_items
        if product.is_under_warranty
    )

    context = {
        "products": product_items,
        "total_products": len(product_items),
        "active_count": active_count,
        "expired_count": len(product_items) - active_count,
    }

    return render(
        request,
        "products/product_list.html",
        context
    )


@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            product = form.save(commit=False)
            product.customer = request.user
            product.save()

            messages.success(
                request,
                "Your product has been registered successfully!"
            )

            return redirect(
                "product_detail",
                pk=product.pk
            )
    else:
        form = ProductForm()

    return render(
        request,
        "products/product_form.html",
        {"form": form}
    )


@login_required
def product_detail(request, pk):
    product = get_object_or_404(
        Product,
        pk=pk,
        customer=request.user
    )

    context = {
        "product": product,
        "today": timezone.localdate(),
    }

    return render(
        request,
        "products/product_detail.html",
        context
    )


@login_required
def download_purchase_bill(request, pk):
    product = get_object_or_404(
        Product,
        pk=pk,
        customer=request.user
    )

    if not product.purchase_bill:
        raise Http404("No purchase bill available.")

    try:
        file_handle = product.purchase_bill.open("rb")
    except (FileNotFoundError, OSError, ValueError):
        raise Http404("Purchase bill not found.")

    filename = Path(product.purchase_bill.name).name

    return FileResponse(
        file_handle,
        as_attachment=True,
        filename=filename
    )
