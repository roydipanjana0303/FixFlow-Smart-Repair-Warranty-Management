
from django.contrib import admin
from .models import RepairTicket, RepairUpdate


class RepairUpdateInline(admin.TabularInline):
    model = RepairUpdate
    extra = 0


@admin.register(RepairTicket)
class RepairTicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "product",
        "priority",
        "status",
        "warranty_status",
        "assigned_technician",
        "created_at",
    )

    list_filter = (
        "status",
        "priority",
        "warranty_status",
    )

    search_fields = (
        "customer__username",
        "product__product_name",
    )

    inlines = [RepairUpdateInline]


@admin.register(RepairUpdate)
class RepairUpdateAdmin(admin.ModelAdmin):
    list_display = ("ticket", "updated_by", "created_at")
