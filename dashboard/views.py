
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render

from products.models import Product
from repairs.models import RepairTicket


def landing_view(request):
    return render(request, "landing.html")


@login_required
def dashboard_view(request):
    user = request.user

    products = Product.objects.filter(
        customer=user
    ).order_by("-created_at")

    tickets = RepairTicket.objects.filter(
        customer=user
    ).select_related(
        "product", "assigned_technician"
    ).order_by("-created_at")

    active_tickets = tickets.exclude(
        status__in=["completed", "cancelled"]
    ).count()

    completed_tickets = tickets.filter(
        status="completed"
    ).count()

    product_list = list(products)

    warranty_active = sum(
        1 for product in product_list
        if product.is_under_warranty
    )

    context = {
        "total_products": len(product_list),
        "total_tickets": tickets.count(),
        "active_tickets": active_tickets,
        "completed_tickets": completed_tickets,
        "warranty_active": warranty_active,
        "recent_tickets": tickets[:5],
        "recent_products": product_list[:4],
    }

    return render(
        request,
        "dashboard/home.html",
        context
    )
