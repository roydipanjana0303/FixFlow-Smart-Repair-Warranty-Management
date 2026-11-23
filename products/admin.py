
from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "product_name",
        "brand",
        "customer",
        "category",
        "purchase_date",
        "warranty_expiry",
        "is_under_warranty",
    )

    list_filter = ("category", "brand")
    search_fields = ("product_name", "serial_number")
