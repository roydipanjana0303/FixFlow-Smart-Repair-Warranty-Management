
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import CustomerProfile
from products.models import Product

from .forms import RepairTicketForm
from .models import RepairTicket, RepairUpdate
from .services.tickets import create_repair_ticket


def require_customer(request):
    user = request.user

    if not user.is_authenticated:
        raise PermissionDenied(
            "Please log in to access customer services."
        )

    if user.is_staff or user.is_superuser:
        raise PermissionDenied(
            "Administrators cannot access customer repair pages."
        )

    profile = CustomerProfile.objects.filter(
        user=user
    ).first()

    if profile is None:
        raise PermissionDenied(
            "Your account does not have a customer profile."
        )

    if profile.role != "customer":
        raise PermissionDenied(
            "Only customers can access this page."
        )

    return profile


@login_required
def ticket_list(request):
    require_customer(request)

    tickets = (
        RepairTicket.objects.filter(
            customer=request.user
        )
        .select_related(
            "product",
            "assigned_technician",
            "assigned_technician__user",
        )
        .order_by("-created_at")
    )

    context = {
        "tickets": tickets,
        "total_tickets": tickets.count(),
        "pending_count": tickets.filter(
            status="pending"
        ).count(),
        "active_count": tickets.filter(
            status__in=["assigned", "in_progress"]
        ).count(),
        "completed_count": tickets.filter(
            status="completed"
        ).count(),
    }

    return render(
        request,
        "repairs/ticket_list.html",
        context,
    )


@login_required
def create_ticket(request):
    require_customer(request)

    has_products = Product.objects.filter(
        customer=request.user
    ).exists()

    if request.method == "POST":
        form = RepairTicketForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            ticket = create_repair_ticket(
                customer=request.user,
                product=form.cleaned_data["product"],
                issue_description=form.cleaned_data[
                    "issue_description"
                ],
                priority=form.cleaned_data["priority"],
            )

            messages.success(
                request,
                "Repair request submitted successfully!",
            )

            return redirect(
                "ticket_detail",
                pk=ticket.pk,
            )
    else:
        form = RepairTicketForm(
            user=request.user
        )

    return render(
        request,
        "repairs/ticket_form.html",
        {
            "form": form,
            "has_products": has_products,
        },
    )


@login_required
def ticket_detail(request, pk):
    require_customer(request)

    ticket = get_object_or_404(
        RepairTicket.objects.select_related(
            "product",
            "assigned_technician",
            "assigned_technician__user",
        ),
        pk=pk,
        customer=request.user,
    )

    # Fetch repair updates using the actual foreign key
    # rather than assuming a reverse relationship name.
    updates = (
        RepairUpdate.objects.filter(
            ticket=ticket
        )
        .select_related("updated_by")
        .order_by("created_at", "pk")
    )

    context = {
        "ticket": ticket,
        "updates": updates,
    }

    return render(
        request,
        "repairs/ticket_detail.html",
        context,
    )
